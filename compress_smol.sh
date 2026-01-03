#!/bin/bash

# Create an output directory so we don't overwrite originals
mkdir -p compressed_videos

# Loop through all mp4 files in the current directory
for file in *.mp4; do
    # Skip if no mp4 files are found
    [ -e "$file" ] || continue

    echo "Processing: $file..."

    # FFmpeg command breakdown:
    # -i: Input file
    # -vf: Video filters (Scale to 512x512, maintain aspect ratio, add padding)
    # -vcodec libx265: Use HEVC for high compression
    # -crf 26: Quality setting (24-28 is great for small file sizes)
    # -preset slow: Takes longer but results in a smaller file size
    # -tag:v hvc1: Ensures compatibility with Apple/iOS devices
    
    ffmpeg -i "$file" \
        -vf "scale=512:512:force_original_aspect_ratio=decrease,pad=512:512:(ow-iw)/2:(oh-ih)/2" \
        -vcodec libx265 \
        -crf 26 \
        -preset slow \
        -tag:v hvc1 \
        -acodec copy \
        "compressed_videos/${file%.mp4}.mp4"

    echo "Finished: $file"
    echo "-----------------------------------------------"
done

echo "All videos processed! Check the 'compressed_videos' folder."