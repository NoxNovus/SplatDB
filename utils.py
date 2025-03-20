import json
from typing import List
import numpy as np
import open3d as o3d

from engine.type import ChunkMetadata

def convert_gps_data_to_chunk(gps_data: List[float], chunk_size: int) -> List[int]:
    """
    Convert GPS data to chunk position
    """
    return [int(coord / chunk_size)*chunk_size for coord in gps_data]

def load_point_cloud_from_file(file_path: str) -> o3d.geometry.PointCloud:
    """
    Load point cloud from file
    """
    pcd = o3d.io.read_point_cloud(file_path)
    return pcd

def compute_min_max_bound(pcd: o3d.geometry.PointCloud) -> List[float]:
    """
    Compute min and max bound of point cloud
    """
    points = np.asarray(pcd.points)
    if len(points) == 0:
        return [0, 0, 0], [0, 0, 0]
    min_bound = points.min(axis=0)
    max_bound = points.max(axis=0)
    return min_bound, max_bound

def parse_chunk_mapping_from_file(file_path: str) -> ChunkMetadata:
    """
    Parse chunk mapping from file
    """
    with open(file_path, 'r') as f:
        raw_dict = json.load(f)

    return ChunkMetadata.from_raw_json(raw_dict)