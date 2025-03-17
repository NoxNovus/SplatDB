import os
import numpy as np
import open3d as o3d
from typing import List, Tuple

NAME = "test"

def main():
    folder_path = "chunks/test"
    origin = (20, 16, 28)  
    length = 5 
    output_path = "result.ply"

    point_clouds = load_point_clouds_within_cube(folder_path, origin, length)
    merged_pcd = merge_point_clouds(point_clouds)
    save_merged_point_cloud(merged_pcd, output_path)
    print(f"Merged point cloud saved to {output_path}")


def create_blank_chunk() -> o3d.geometry.PointCloud:
    return o3d.geometry.PointCloud() 


def load_point_clouds_within_cube(folder_path: str, origin: Tuple[int, int, int], length: int) -> List[o3d.geometry.PointCloud]:
    point_clouds = []
    x_min, y_min, z_min = origin
    x_max, y_max, z_max = x_min + length, y_min + length, z_min + length

    for x in range(x_min, x_max):
        for y in range(y_min, y_max):
            for z in range(z_min, z_max):
                file_name = f"{NAME}_chunk_{x}_{y}_{z}.ply"
                file_path = os.path.join(folder_path, file_name)
                if os.path.exists(file_path):
                    pcd = o3d.io.read_point_cloud(file_path)
                else:
                    pcd = create_blank_chunk()
                point_clouds.append(pcd)
    return point_clouds


def merge_point_clouds(point_clouds: List[o3d.geometry.PointCloud]) -> o3d.geometry.PointCloud:
    if not point_clouds:
        return o3d.geometry.PointCloud()

    merged_pcd = point_clouds[0]
    for pcd in point_clouds[1:]:
        merged_pcd += pcd
    return merged_pcd


def save_merged_point_cloud(merged_pcd: o3d.geometry.PointCloud, output_path: str):
    o3d.io.write_point_cloud(output_path, merged_pcd)


if __name__ == "__main__":
    main()