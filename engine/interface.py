from abc import ABC, abstractmethod
from typing import List
import open3d as o3d

from engine.type import ChunkData, ChunkMetadata

class EngineDBInterface(ABC):
    """
    A db engine to interact with
    """

    @abstractmethod
    def __init__(self, chunk_size: int, **kwargs):
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def insert(self, gps_data: List[float], point_cloud: o3d.geometry.PointCloud) -> int:
        pass

    @abstractmethod
    def query(self, gps_data: List[float], chunk_radius: int) -> ChunkData:
        pass

    @abstractmethod
    def add_metadata(self, metadata: ChunkMetadata) -> int:
        pass