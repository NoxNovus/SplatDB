from pathlib import Path
import open3d as o3d

from engine.memdb import MemDB
from render_utils import generate_axes, generate_connecting_wireframe
from utils import compute_min_max_bound, load_point_cloud_from_file


CHUNK_SIZE = 10
FILE = "test.ply"
DIR = "splats"

ply_file = Path.cwd() / DIR / FILE

pcd = load_point_cloud_from_file(str(ply_file))

db = MemDB(CHUNK_SIZE)

err = db.insert([0, 0, 0], pcd)
print(bool(err))

print(db.db)
result = db.query([0, 10, 0], 0)

print(result)

mesh = o3d.geometry.PointCloud()
for chunk in result:
    mesh += chunk.pcd

min_bound, max_bound = compute_min_max_bound(mesh)
wire_frame = generate_connecting_wireframe(min_bound, max_bound, CHUNK_SIZE)
axes = generate_axes(100)

o3d.visualization.draw_geometries([mesh, wire_frame, axes])
