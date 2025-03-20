from typing import List
from engine.type import ChunkData, ChunkMetadata
from interface import EngineDBInterface
from open3d import o3d

class MemDB(EngineDBInterface):

    def __init__(self, chunk_size, **kwargs):
        super().__init__(chunk_size, **kwargs)

    def connect(self):
        pass

    def disconnect(self):
        pass

    def insert(self, gps_data: List[float], point_cloud: o3d.geometry.PointCloud) -> int:
        pass

    def query(self, gps_data: List[float], chunk_radius: int) -> ChunkData:
        pass

    def add_metadata(self, metadata: ChunkMetadata) -> int:
        pass