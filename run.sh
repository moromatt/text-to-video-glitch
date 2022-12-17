#!/bin/bash
eval "$(conda shell.bash hook)"
conda activate glitch
python ./text_video_glitch.py
echo "Done, press any key to close"
rundll32 user32.dll,MessageBeep
read
