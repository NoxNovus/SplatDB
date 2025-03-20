from pathlib import Path
import open3d as o3d

from render_utils import generate_axes, generate_chunk_wireframe, generate_connecting_wireframe
from utils import compute_min_max_bound, convert_gps_data_to_chunk

SPLAT_DIR = "splats"
FILE = "test.ply"

ply_file = Path.cwd() / SPLAT_DIR / FILE

if not ply_file.exists():
    raise FileNotFoundError(f"File not found: {ply_file}")

mesh = o3d.io.read_point_cloud(str(ply_file))

chunk_pos = [0, 0, 0]
chunk_size = 10

wire_frame = generate_chunk_wireframe(chunk_pos, chunk_size)
wire_frame2 = generate_chunk_wireframe([10, 0, 0], 10)
axes = generate_axes(100)

min_bound, max_bound = compute_min_max_bound(mesh)
min_bound = convert_gps_data_to_chunk(min_bound, 10)
max_bound = convert_gps_data_to_chunk(max_bound, 10)
print(f"Min bound: {min_bound}, Max bound: {max_bound}")
min_wireframe = generate_chunk_wireframe(convert_gps_data_to_chunk(min_bound, 10), 10)
max_wireframe = generate_chunk_wireframe(convert_gps_data_to_chunk(max_bound, 10), 10)

all_wireframes = generate_connecting_wireframe(min_bound, max_bound, 10)

o3d.visualization.draw_geometries([mesh, all_wireframes, axes])
