import cv2
import os
import pandas as pd
import numpy as np

VIDEO_DIR =  "Data/left_videos"

CSV_OUT = "Data/annotations.csv"

NUM_FRAMES_SAMPLED = 32


# Configuration: Define questions, required inputs, and specific options

QUESTION_CONFIGS = [
    {
        "label": "Navigation Turn", # control f to be Navigation Turn
        "template": "Is there an immediate turn between frame {start} and {end}?",
        "options": {"A": "yes turn left", "B": "yes turn right","C": "yes turn left or right" ,"D": "no"},
        "requires_frame_range": True
    },
    {
        "label": "Pedestrians (Specific Range)",
        "template": "Are there pedestrians visible between frame {start} and {end}?",
        "options": {"A": "yes", "B": "no"},
        "requires_frame_range": True
    },
    {
        "label": "Obstructions (Specific Range)",
        "template": "Are there obstructions visible to my left or right between frame {start} and {end}?",
        "options": {"A": "left", "B": "right", "C": "none", "D": "both"},
        "requires_frame_range": True
    },
    {
        "label": "Intersections Ahead (Specific Range)",
        "template": "I am jogging, are there any Intersections visible between frame {start} and {end}?", # change to intersections or crosswalks
        "options": {"A": "yes", "B": "no"},
        "requires_frame_range": True
    },
    {
        "label": "Navigation Veer",
        "template": "I am jogging. Should I veer left or right to avoid obstructions between frame {start} and {end}?",
        "options": {"A": "left", "B": "right", "C": "stay straight"},
        "requires_frame_range": True
    },
    {
        "label": "Navigation Lane ",
        "template": "Where am I currently running between frame {start} and {end}?",
        "options": {"A": "designated running lane", "B": "sidewalk", "C": "street", "D": "off trail or hiking path"},
        "requires_frame_range": True
    }
] 

def load_existing_annotations(csv_path):
    # Columns match VSTIBench format
    cols = ["id", "video_file", "question", "options", "answer", "ground_truth", "question_type"]
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        return pd.DataFrame(columns=cols)

def extract_uniform_frames(video_path, num_frames=32):
    """
    Simulates VLM-3R data loading:
    Opens video, calculates 32 equidistant indices, and returns those frames.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Handle short videos
    if total_frames < num_frames:
        indices = np.arange(total_frames)
    else:
        # Linspace generates evenly spaced numbers over the interval
        indices = np.linspace(0, total_frames - 1, num_frames).astype(int)

    frames = []
    current_idx = 0
    
    # Optimization: Iterate through video once, picking only needed frames
    for target_idx in indices:
        # set/grab is faster than read() if skipping many frames
        cap.set(cv2.CAP_PROP_POS_FRAMES, target_idx)
        ret, frame = cap.read()
        if ret:
            # Resize for consistent viewing if needed, or keep original
            # frame = cv2.resize(frame, (640, 480)) 
            frames.append(frame)
    
    cap.release()
    return frames

def play_sampled_frames(frames):
    print("\nDisplaying 32 uniformly sampled frames. Press 'q' to stop and annotate.")
    
    idx = 0
    while True:
        frame_display = frames[idx].copy()
        
        # Overlay the frame index (0-31) so user can pick ranges
        text = f"Frame: {idx}/{len(frames)-1}"
        cv2.putText(frame_display, text, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow("VLM-3R Sampled View", frame_display)

        key = cv2.waitKey(100)  # Play speed (100ms = 10fps)
        
        if key & 0xFF == ord('q'):
            break
        
        # Loop playback
        idx = (idx + 1) % len(frames)

    cv2.destroyAllWindows()

def get_user_annotation(frames):
    # 1. Select Question Type
    print("\n--- Select Question Template ---")
    for i, cfg in enumerate(QUESTION_CONFIGS):
        print(f"{i+1}. {cfg['label']} | \"{cfg['template']}\"")
    
    while True:
        try:
            sel = int(input("Selection (number): ")) - 1
            if 0 <= sel < len(QUESTION_CONFIGS):
                config = QUESTION_CONFIGS[sel]
                break
        except ValueError:
            pass
        print("Invalid selection.")

    # 2. Handle Dynamic Frame Ranges (if required)
    question_text = config['template']
    if config['requires_frame_range']:
        print("\nThis question requires a frame range (0-31).")
        while True:
            try:
                s = int(input("Start Frame (0-31): "))
                e = int(input("End Frame (0-31): "))
                if 0 <= s <= 31 and 0 <= e <= 31 and s <= e:
                    question_text = question_text.format(start=s, end=e)
                    break
                else:
                    print("Invalid range. Start must be <= End, and within 0-31.")
            except ValueError:
                print("Please enter integers.")

    # 3. Select Answer from Options
    print(f"\nQuestion: {question_text}")
    print("--- Options ---")
    
    # Create the list format string usually found in VLM datasets: ["A. yes", "B. no"]
    options_list = []
    valid_keys = []
    
    for key, val in config['options'].items():
        print(f"{key}. {val}")
        options_list.append(f"{key}. {val}")
        valid_keys.append(key)

    while True:
        ans_key = input("Choose Answer (A/B/C...): ").strip().upper()
        if ans_key in valid_keys:
            ground_truth_text = config['options'][ans_key]
            break
        print(f"Invalid option. Choose from {valid_keys}")

    return {
        "question": question_text,
        "options": str(options_list), # Store as string representation of list
        "answer": ans_key,
        "ground_truth": ground_truth_text,
        "question_type": config['label']
    }

def main():
    if not os.path.exists(VIDEO_DIR):
        print(f"Error: Directory '{VIDEO_DIR}' not found.")
        return

    df = load_existing_annotations(CSV_OUT)
    
    # Filter only supported video extensions
    video_files = sorted([f for f in os.listdir(VIDEO_DIR) 
                         if f.lower().endswith(('.avi', '.mp4', '.mov', '.mkv'))])
    
    # Calculate next ID
    if not df.empty and "id" in df.columns:
        next_id = pd.to_numeric(df["id"], errors='coerce').max()
        if pd.isna(next_id): next_id = 0
        else: next_id = int(next_id) + 1
    else:
        next_id = 0

    already_done = set(df["video_file"].astype(str).tolist())

    print(f"Found {len(video_files)} videos. Starting annotation...")

    for video in video_files:
        video_path = os.path.join(VIDEO_DIR, video)

        if video_path in already_done:
            print(f"Skipping {video} (already annotated).")
            continue

        print(f"\n=================================")
        print(f"Processing: {video}")
        print(f"=================================")

        # 1. Extract exactly 32 frames (VLM-3R logic)
        frames = extract_uniform_frames(video_path, NUM_FRAMES_SAMPLED)
        if frames is None or len(frames) == 0:
            print("Could not read frames.")
            continue

        # 2. Play the sampled frames with index overlay
        play_sampled_frames(frames)

        # 3. Get Annotation
        skip = input("Annotate this video? (y/n): ").lower().strip()
        if skip != 'y':
            print("Skipping...")
            continue

        data = get_user_annotation(frames)

        # 4. Save
        new_row = {
            "id": next_id,
            "video_file": video_path,
            "question": data['question'],
            "options": data['options'],
            "answer": data['answer'],
            "ground_truth": data['ground_truth'],
            "question_type": data['question_type']
        }
        
        df.loc[len(df)] = new_row
        df.to_csv(CSV_OUT, index=False)
        
        print(f"Saved ID {next_id} successfully.")
        next_id += 1

    print("\nAll videos reviewed.")

if __name__ == "__main__":
    main()