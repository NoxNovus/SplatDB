from pathlib import Path
import open3d as o3d

SPLAT_DIR = "chunks/test"

ply_dir = Path.cwd() / SPLAT_DIR

if not ply_dir.exists():
    raise FileNotFoundError(f"Directory not found: {ply_dir}")

ply_files = list(ply_dir.glob("*.ply"))

if not ply_files:
    raise FileNotFoundError(f"No .ply files found in directory: {ply_dir}")

point_clouds = []
for ply_file in ply_files:
    print(f"Loading: {ply_file}")
    point_cloud = o3d.io.read_point_cloud(str(ply_file))
    point_clouds.append(point_cloud)

o3d.visualization.draw_geometries(point_clouds)
