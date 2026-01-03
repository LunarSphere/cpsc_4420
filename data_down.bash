#!/usr/bin/env bash
SRC=gs://gresearch/sanpo_dataset/v0
#download sanpo real just the body cam footage right and left
EXCLUDES=""

# Exclude frames from the right lens (stereo)
# EXCLUDES=$EXCLUDES'|.*/right'
# Exclude segmentation maps
EXCLUDES=$EXCLUDES'|.*/segmentation_masks'
# # Exclude SANPO-synthetic depth maps and CREStereo depth maps
EXCLUDES=$EXCLUDES'|.*/depth_maps'
# Exclude depth maps from the ZED API (sparse depth)
EXCLUDES=$EXCLUDES'|.*/zed_depth_maps'

# Exclude SANPO-Real
# EXCLUDES=$EXCLUDES'|sanpo-real'
# Exclude SANPO-Synthetic
EXCLUDES=$EXCLUDES'|sanpo-synthetic'
# Exclude camera head images
EXCLUDES=$EXCLUDES'|.*/camera_head'

echo Running: gsutil -m rsync -r -x \'${EXCLUDES#|}\' $SRC .
gsutil -m rsync -r -x ${EXCLUDES#|} $SRC .