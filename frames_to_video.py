# import cv2
# import os
# from natsort import natsorted
# from concurrent.futures import ThreadPoolExecutor
# from tqdm import tqdm

# def choose_codec():
#     """Try NVENC first; fallback to mp4v if unavailable."""
#     try:
#         test = cv2.VideoWriter_fourcc(*'H264')  # NVENC-accelerated H.264
#         return test
#     except:
#         return cv2.VideoWriter_fourcc(*'mp4v')


# def frames_to_video(frames_folder, output_path, fps=15, corrupt_threshold=0.1):
#     # Get all image filenames
#     frames = [f for f in os.listdir(frames_folder)
#               if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

#     if not frames:
#         print(f"⚠️ No frames in {frames_folder}, skipping.")
#         return

#     frames = natsorted(frames)

#     # Read first frame
#     first_frame_path = os.path.join(frames_folder, frames[0])
#     frame = cv2.imread(first_frame_path)

#     if frame is None:
#         print(f"❌ First frame corrupt in {frames_folder}, skipping video.")
#         return

#     height, width, _ = frame.shape

#     # Choose GPU codec if available
#     fourcc = choose_codec()

#     if not output_path.lower().endswith(".mp4"):
#         output_path += ".mp4"

#     video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

#     corrupt_count = 0

#     for f in tqdm(frames, desc=f"Writing {os.path.basename(output_path)}"):
#         frame_path = os.path.join(frames_folder, f)
#         frame = cv2.imread(frame_path)

#         if frame is None:
#             corrupt_count += 1
#             continue

#         video.write(frame)

#     video.release()

#     corrupt_rate = corrupt_count / len(frames)

#     if corrupt_rate > corrupt_threshold:
#         print(f"❌ Too many corrupt frames ({corrupt_rate:.1%}). Skipping {output_path}.")
#         try:
#             os.remove(output_path)
#         except:
#             pass
#         return

#     print(f"✅ Saved: {output_path} (Skipped {corrupt_count} corrupt frames)")


# def process_pair(left_path, right_path, out_left, out_right):
#     # Convert left + right in parallel (GPU can handle both)
#     with ThreadPoolExecutor(max_workers=2) as executor:
#         executor.submit(frames_to_video, left_path, out_left, 15)
#         executor.submit(frames_to_video, right_path, out_right, 15)


# if __name__ == "__main__":
#     directory_path = os.path.join(os.getcwd(), "SANPO_DATA", "sanpo-real")

#     output_dir_left = "sanpo_videos/left/"
#     output_dir_right = "sanpo_videos/right/"
#     os.makedirs(output_dir_left, exist_ok=True)
#     os.makedirs(output_dir_right, exist_ok=True)

#     entries = natsorted(os.listdir(directory_path))
#     count = 0

#     for entry in entries:
#         full_path_l = os.path.join(directory_path, entry, "camera_chest", "left", "video_frames")
#         full_path_r = os.path.join(directory_path, entry, "camera_chest", "right", "video_frames")

#         if os.path.isdir(full_path_l) and os.path.isdir(full_path_r):

#             output_path_l = os.path.join(output_dir_left, f"video_{count}.mp4")
#             output_path_r = os.path.join(output_dir_right, f"video_{count}.mp4")

#             print(f"\n Processing {entry} (index {count})")
#             process_pair(full_path_l, full_path_r, output_path_l, output_path_r)
#             count += 1

#     print("\n🎉 All videos processed!")


import cv2
import os
from natsort import natsorted
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def choose_codec():
    """Force AVI-compatible codec."""
    return cv2.VideoWriter_fourcc(*'MJPG')


def frames_to_video(frames_folder, output_path, fps=15, corrupt_threshold=0.1):
    # Get all image filenames
    frames = [f for f in os.listdir(frames_folder)
              if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not frames:
        print(f"⚠️ No frames in {frames_folder}, skipping.")
        return

    frames = natsorted(frames)

    # Read first frame
    first_frame_path = os.path.join(frames_folder, frames[0])
    frame = cv2.imread(first_frame_path)

    if frame is None:
        print(f"❌ First frame corrupt in {frames_folder}, skipping video.")
        return

    height, width, _ = frame.shape

    # Choose AVI codec
    fourcc = choose_codec()

    # Force .avi extension
    if not output_path.lower().endswith(".avi"):
        output_path += ".avi"

    video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    corrupt_count = 0

    for f in tqdm(frames, desc=f"Writing {os.path.basename(output_path)}"):
        frame_path = os.path.join(frames_folder, f)
        frame = cv2.imread(frame_path)

        if frame is None:
            corrupt_count += 1
            continue

        video.write(frame)

    video.release()

    corrupt_rate = corrupt_count / len(frames)

    if corrupt_rate > corrupt_threshold:
        print(f"❌ Too many corrupt frames ({corrupt_rate:.1%}). Skipping {output_path}.")
        try:
            os.remove(output_path)
        except:
            pass
        return

    print(f"✅ Saved: {output_path} (Skipped {corrupt_count} corrupt frames)")


def process_pair(left_path, right_path, out_left, out_right):
    # Convert left + right in parallel
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(frames_to_video, left_path, out_left, 15)
        executor.submit(frames_to_video, right_path, out_right, 15)


if __name__ == "__main__":
    directory_path = os.path.join(os.getcwd(), "SANPO_DATA", "sanpo-real")

    output_dir_left = "sanpo_videos/left/"
    output_dir_right = "sanpo_videos/right/"
    os.makedirs(output_dir_left, exist_ok=True)
    os.makedirs(output_dir_right, exist_ok=True)

    entries = natsorted(os.listdir(directory_path))
    count = 0

    for entry in entries:
        full_path_l = os.path.join(directory_path, entry, "camera_chest", "left", "video_frames")
        full_path_r = os.path.join(directory_path, entry, "camera_chest", "right", "video_frames")

        if os.path.isdir(full_path_l) and os.path.isdir(full_path_r):

            output_path_l = os.path.join(output_dir_left, f"video_{count}.avi")
            output_path_r = os.path.join(output_dir_right, f"video_{count}.avi")

            print(f"\n Processing {entry} (index {count})")
            process_pair(full_path_l, full_path_r, output_path_l, output_path_r)
            count += 1

    print("\n🎉 All videos processed!")
