from typing import Dict, List

import numpy as np
from engine.type import ChunkData, ChunkMetadata
from engine.interface import EngineDBInterface
import open3d as o3d

from utils import compute_min_max_bound, convert_gps_data_to_chunk


class MemDB(EngineDBInterface):
    """
    In-memory database for storing chunk data
    """

    def __init__(self, chunk_size, **kwargs):
        super().__init__(chunk_size, **kwargs)
        self.chunk_size = chunk_size
        self.db: Dict[ChunkData] = {}

    def connect(self):
        pass

    def disconnect(self):
        pass

    def insert(self, gps_data: List[float], point_cloud: o3d.geometry.PointCloud) -> int:
        chunk_pos = convert_gps_data_to_chunk(gps_data, self.chunk_size)

        chunk_splited = self._split_point_cloud(point_cloud)

        ok_flag = 1

        for chunk in chunk_splited:
            actual_chunk_pos = (np.asarray(chunk['chunk_pos']) + np.asarray(chunk_pos)).tolist()
            actual_chunk_pcd = chunk['point_cloud']

            actual_chunk_pcd.translate(-np.asarray(chunk['chunk_pos']))

            chunk_id = str(actual_chunk_pos)

            if chunk_id in self.db:
                self.db[chunk_id]['pcd'] += actual_chunk_pcd
                # dedup pcd
                self.db[chunk_id]['pcd'].remove_duplicated_points()

            else:
                self.db[chunk_id] = {
                    'pcd': actual_chunk_pcd,
                    'camera_pos': [],
                    'chunk_pos': actual_chunk_pos,
                    'chunk_size': self.chunk_size
                }
        


        return ok_flag

    def query(self, gps_data: List[float], chunk_radius: int) -> List[ChunkData]:
        chunk_pos = convert_gps_data_to_chunk(gps_data, self.chunk_size)
        actual_metric_radius = chunk_radius * self.chunk_size

        ret = []

        for chunk in self.db.values():
            if np.linalg.norm(np.array(chunk['chunk_pos']) - np.array(chunk_pos)) <= actual_metric_radius:
                chunk_data = ChunkData(**chunk)
                pcd = chunk_data.pcd
                pcd.translate(np.asarray(chunk['chunk_pos']))

                ret.append(chunk_data)

        return ret

    def add_metadata(self, metadata: ChunkMetadata) -> int:
        pass

    def _split_point_cloud(self, point_cloud: o3d.geometry.PointCloud) -> List[Dict]:
        
        min_bound, max_bound = compute_min_max_bound(point_cloud)
        start = convert_gps_data_to_chunk(min_bound, self.chunk_size)
        end = convert_gps_data_to_chunk(max_bound, self.chunk_size)

        n = self.chunk_size

        points = np.asarray(point_cloud.points)
        colors = np.asarray(point_cloud.colors)

        ret = []

        for x in range(int(start[0] - n), int(end[0] + n), n):
            for y in range(int(start[1] - n), int(end[1] + n), n):
                for z in range(int(start[2] - n), int(end[2] + n), n):
                    chunk_start = [x, y, z]
                    chunk_end = [x + n, y + n, z + n]

                    mask = np.all((points >= chunk_start) & (points < chunk_end), axis=1)
                    chunk_points = points[mask]
                    chunk_colors = colors[mask]

                    if(len(chunk_points) == 0):
                        continue

                    pcd = o3d.geometry.PointCloud()
                    pcd.points = o3d.utility.Vector3dVector(chunk_points)
                    pcd.colors = o3d.utility.Vector3dVector(chunk_colors)

        
                    ret.append({
                        'chunk_pos': chunk_start,
                        'point_cloud': pcd
                    })

        return ret

        
