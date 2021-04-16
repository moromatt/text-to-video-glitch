# text_to_video_glitch:
Generate a glitched video from a txt file, chunks of randomic sizes are taken from the txt and then displayed for N frames.  
K of N frames will be created with "glitched" characters.  
Set: number of glitched frames, number of maximum words per chunk, number of stable frames, background color, text color, image size, font.  
  
Have fun!
  
```python text_video_glitch.py --text_path ./text_file/text.txt --out_name text_to_chaos_video.mp4 --min_word_range 5 --max_word_range 10 --text_size 140 --f_percent 0.3```
  
# Example:
**text**:  
"_Ayy, I just decided by the grace of the god Poseidon  
That you're so dead to me I dug a hole for you to lie in  
I'm sick and disowning, all the moments, and the key components  
That led me to follow hollow promises from empty monads_"  

**output video:**  
<p align="center">
  <img src="output.gif" alt="animated" />
</p>
