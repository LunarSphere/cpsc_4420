#!/bin/bash
# avi to mp4 conversion script using ffmpeg
## reduced file size with HEVC encoding 1/5 of original size
# Usage: ./convert_videos.sh /path/to/videos
# If no path is provided, it defaults to the current directory (.)

TARGET_DIR="${1:-.}"

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "Error: ffmpeg is not installed."
    exit 1
fi

# Check if directory exists
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Directory '$TARGET_DIR' does not exist."
    exit 1
fi

# Enable nullglob so the loop simply does nothing if no *.avi files exist
shopt -s nullglob nocaseglob

echo "Scanning '$TARGET_DIR' for .avi files..."

found_files=0

for video in "$TARGET_DIR"/*.avi; do
    # Verify file exists to handle edge cases
    [ -e "$video" ] || continue
    
    found_files=1
    
    # Get filename without path and extension
    filename=$(basename "$video")
    # Get directory path
    dirname=$(dirname "$video")
    # Remove extension
    name_no_ext="${filename%.*}"
    # Create new file path
    mp4_file="$dirname/$name_no_ext.mp4"

    if [ -f "$mp4_file" ]; then
        echo "Skipping '$filename' - '$name_no_ext.mp4' already exists."
        continue
    fi

    echo "Converting: $filename..."

    # Run ffmpeg
    # < /dev/null is CRITICAL in bash loops. FFmpeg is interactive and will 
    # 'eat' the loop's input variables if not disconnected from stdin.
    # Using libx265 (HEVC) with CRF 28 for maximum compression. 
    # -vtag hvc1 ensures compatibility with Apple devices.
    ffmpeg -i "$video" \
        -c:v libx265 -crf 28 -vtag hvc1 \
        -c:a aac -b:a 96k \
        -movflags +faststart \
        -loglevel error \
        -y "$mp4_file" < /dev/null

    # Check if the command succeeded (exit code 0)
    if [ $? -eq 0 ]; then
        echo "✔ Success. Removing original."
        rm "$video"
    else
        echo "✘ Failed to convert '$filename'. Keeping original."
        # Cleanup partial file if it exists
        [ -f "$mp4_file" ] && rm "$mp4_file"
    fi
done

if [ $found_files -eq 0 ]; then
    echo "No .avi files found in '$TARGET_DIR'."
fi

echo "Done."
