from pydantic import BaseModel
from typing import Dict, List
import open3d as o3d

class CameraPos(BaseModel):
    file_name: str
    position: List[float]
    rotation: List[float]

    @classmethod
    def from_list(cls, data: List):
        return cls(
            file_name=data[0],
            position=data[1],
            rotation=data[2]
        )

class ChunkData(BaseModel):
    pcd: o3d.geometry.PointCloud
    camera_pos: List[CameraPos]
    chunk_pos: List[float]
    chunk_size: int

class ChunkMetadata(BaseModel):
    chunks: Dict[str, List[CameraPos]]

    @classmethod
    def from_raw_json(cls, raw_dict: Dict):
        parsed_chunks = {}
        for k, v in raw_dict.items():
            parsed_chunks[k] = [CameraPos.from_list(entry) for entry in v]
        return cls(chunks=parsed_chunks)