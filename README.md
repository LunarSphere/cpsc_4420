# CPSC 4420 Artificial Intelligence
## Assignment_1
This folder contains the code for our Homework on early implementations of Tree Search for Artificial Intelligence. such as Depth-First Search (DFS) and Breadth-First Search (BFS), and Uniform Cost Search (UCS) for solving pathfinding problems on a grid-based map.

## Assignment_2 
This folder contains the code for our homework on implementing Markov Decision Processes (MDPs) and to find the optimal policy using Value Iteration and Policy Iteration algorithms in a grid-based environment.

## Assignment_3
This folder contains our homework for using Minimax, Alpha-Beta Pruning algorithms, and expectimax to create an AI agent that plays connect 4 optimally.

## Other Files
- The Rest of the code in this repo contains Data handling code for the files in my final project for CPSC 4420 Artificial Intelligence. Whch has turned into a research project. I will likely link its own repo later.
 
- These scripts are specifically for handling data from Googles Sanpo dataset for Visually Impaired Navigation research.

- The below scripts are in order of how I would run them to redownload the 

1. data_down.bash -> Downloads sanpo_real portion just the body mounted camera footage stereo left and right.

2. frames_to_video.py -> the intial download is individual frames so and they are massive so this script converts them to avi videos for easier handling. reduces 1tb of data to around 200gb.

3. Compression_og.bash -> further compresses the avi videos to h264 mp4 format for even easier handling and storage. reduces 200gb to around 40gb.

    ***Use this compression on the output of #2***

4. compress_smol.sh -> compresses videos to 512 x 512 resolution for model training. reduces 40gb to around 2gb.

    ***Use this compression on the output of #3***

5. video_annotation.py -> script to annotate videso with Q&A pairs for model training/testing

6. convert_csv_to_json.py -> converts the output of #5 from csv to json format for model training/testing

7. hf_upload.py -> upload final json and dataset to huggingface for model training/testing
    ***Kinda Unecessary I think doing this by had is faster***



