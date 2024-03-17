import os
from pose_format import Pose
from pose_format.pose_visualizer import PoseVisualizer
from tqdm import tqdm

poses_folder = "poses"
gifs_folder = "gifs"

if not os.path.exists(gifs_folder):
    os.makedirs(gifs_folder)


def visualize(pose_file: str):
    with open(f"{poses_folder}/{pose_file}", "rb") as f:
        pose = Pose.read(f.read())

    vis = PoseVisualizer(pose, thickness=1)
    gif_path = f'{gifs_folder}/{pose_file.replace(".pose", ".gif")}'
    try:
        vis.save_gif(gif_path, vis.draw())
    except KeyboardInterrupt:
        os.remove(gif_path)
        raise  # Re-raise the exception to terminate the script


def visualize_files():
    files = [f for f in os.listdir(poses_folder) if os.path.isfile(
        os.path.join(poses_folder, f)) and (not os.path.exists(f'{gifs_folder}/{file.replace(".pose", ".gif")}'))]
    for file in tqdm(files):
        try:
            visualize(file)
        except KeyboardInterrupt:
            print(f"Processing interrupted. Cleaning up {file}...")
            if os.path.exists(f'{gifs_folder}/{file.replace(".pose", ".gif")}'):
                os.remove(f'{gifs_folder}/{file.replace(".pose", ".gif")}')
            raise  # Re-raise the exception to terminate the script


try:
    visualize_files()
except KeyboardInterrupt:
    print("Script terminated.")
