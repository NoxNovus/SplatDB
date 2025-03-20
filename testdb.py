from pathlib import Path
import open3d as o3d

from engine.memdb import MemDB
from render_utils import generate_axes, generate_connecting_wireframe
from utils import compute_min_max_bound, load_point_cloud_from_file
from utils import parse_chunk_mapping_from_file

CHUNK_SIZE = 10
FILE = "transformed.ply"
DIR = "splats"

ply_file = Path.cwd() / DIR / FILE

pcd = load_point_cloud_from_file(str(ply_file))

db = MemDB(CHUNK_SIZE)

db.connect()

refer = [10, 10, 10]

err = db.insert(refer, pcd)
print(bool(err))

data = parse_chunk_mapping_from_file("splats/chunk_map.json")
db.add_metadata(refer, data)

db.load_images("C:/Users/nguye/Downloads/images")

result = db.query([20, 0, 0], 1)

print(result)

mesh = o3d.geometry.PointCloud()
camera_list = []
for chunk in result:
    mesh += chunk.pcd
    camera_list.extend(chunk.camera_pos)

set_camera = set(camera_list)
camera_list = list(set_camera)

print(f"Loaded: {len(camera_list)} cameras")

sphere_list = []

for camera in camera_list:
    sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.1)
    sphere.translate(camera.position)
    sphere.paint_uniform_color([1, 0, 0])  # Red color for the spheres
    sphere_list.append(sphere)

min_bound, max_bound = compute_min_max_bound(mesh)
wire_frame = generate_connecting_wireframe(min_bound, max_bound, CHUNK_SIZE)
axes = generate_axes(50)


o3d.visualization.draw_geometries([mesh, axes, *sphere_list])

db.disconnect()
