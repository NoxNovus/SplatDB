from typing import List
import open3d as o3d
from utils import convert_gps_data_to_chunk

def generate_chunk_wireframe(chunk_pos: List[float], chunk_size: float) -> o3d.geometry.LineSet:
    """
    Generate wireframe for chunk
    """

    vertices = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                vertices.append([i, j, k])

    edges = [
        [0, 1], [0, 2], [0, 4],
        [1, 3], [1, 5],
        [2, 3], [2, 6],
        [3, 7],
        [4, 5], [4, 6],
        [5, 7],
        [6, 7]
    ]

    vertices = [[v[i] * chunk_size + chunk_pos[i] for i in range(3)] for v in vertices]

    line_set = o3d.geometry.LineSet()
    line_set.points = o3d.utility.Vector3dVector(vertices)
    line_set.lines = o3d.utility.Vector2iVector(edges)

    return line_set

def generate_axes(size: float) -> o3d.geometry.LineSet:
    """
    Generate axes
    """

    vertices = [[0, 0, 0], [size, 0, 0], [0, size, 0], [0, 0, size]]
    edges = [[0, 1], [0, 2], [0, 3]]
    colors = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]

    line_set = o3d.geometry.LineSet()
    line_set.points = o3d.utility.Vector3dVector(vertices)
    line_set.lines = o3d.utility.Vector2iVector(edges)
    line_set.colors = o3d.utility.Vector3dVector(colors)

    return line_set


def generate_connecting_wireframe(min_bound: List[float], max_bound: List[float], chunk_size: int = 10) -> o3d.geometry.LineSet:
    """
    Generate a combined wireframe connecting all chunks between min_bound and max_bound.
    """
    start = convert_gps_data_to_chunk(min_bound, chunk_size)
    end = convert_gps_data_to_chunk(max_bound, chunk_size)

    all_points = []
    all_lines = []
    point_offset = 0

    for x in range(int(start[0] - chunk_size), int(end[0] + chunk_size), chunk_size):
        for y in range(int(start[1] - chunk_size), int(end[1] + chunk_size), chunk_size):
            for z in range(int(start[2] - chunk_size), int(end[2] + chunk_size), chunk_size):
                print(f"Generating wireframe for chunk {x}, {y}, {z}")
                pos = [x, y, z]
                wireframe = generate_chunk_wireframe(pos, chunk_size)
                
                points = list(wireframe.points)
                lines = list(wireframe.lines)

                all_points.extend(points)
                all_lines.extend([[l[0] + point_offset, l[1] + point_offset] for l in lines])
                point_offset += len(points)

    line_set = o3d.geometry.LineSet()
    line_set.points = o3d.utility.Vector3dVector(all_points)
    line_set.lines = o3d.utility.Vector2iVector(all_lines)

    return line_set