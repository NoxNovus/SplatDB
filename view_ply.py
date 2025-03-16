from pathlib import Path
import open3d as o3d

SPLAT_DIR = "splats"
FILE = "test.ply"

ply_file = Path.cwd() / SPLAT_DIR / FILE

if not ply_file.exists():
    raise FileNotFoundError(f"File not found: {ply_file}")

mesh = o3d.io.read_point_cloud(str(ply_file))
o3d.visualization.draw_geometries([mesh])
