import os
import numpy as np
import open3d as o3d
from pathlib import Path

SPLAT_DIR = "splats"
FILE = "test.ply"


def main():
    input_ply = Path.cwd() / SPLAT_DIR / FILE
    n = 4  
    split_point_cloud(input_ply, n)


def split_point_cloud(input_ply: str, n: int):
    pcd = o3d.io.read_point_cloud(input_ply)
    points = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors) if pcd.has_colors() else None

    ply_name = Path(input_ply).stem
    output_dir = Path(f'chunks/{ply_name}')
    output_dir.mkdir(parents=True, exist_ok=True)

    min_bound = points.min(axis=0)
    max_bound = points.max(axis=0)
    voxel_size = (max_bound - min_bound) / n

    chunks = {}

    for i, point in enumerate(points):
        index = tuple(((point - min_bound) / voxel_size).astype(int))
        if index not in chunks:
            chunks[index] = {'points': [], 'colors': []}

        chunks[index]['points'].append(point)
        if colors is not None:
            chunks[index]['colors'].append(colors[i])

    for index, chunk_data in chunks.items():
        if len(chunk_data['points']) == 0:
            continue
        chunk_pcd = o3d.geometry.PointCloud()
        chunk_pcd.points = o3d.utility.Vector3dVector(np.array(chunk_data['points']))
        if colors is not None:
            chunk_pcd.colors = o3d.utility.Vector3dVector(np.array(chunk_data['colors']))

        output_path = output_dir / f'chunk_{index[0]}_{index[1]}_{index[2]}.ply'
        o3d.io.write_point_cloud(str(output_path), chunk_pcd)

    print(f"Successfully split {input_ply} into {len(chunks)} chunks and saved to {output_dir}")


if __name__ == "__main__":
    main()
