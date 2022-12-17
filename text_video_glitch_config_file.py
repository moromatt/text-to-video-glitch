# path configs
text_path = './source_text/text.txt'
video_name = 'text_to_chaos_video.mp4'

# glitch sets
# percentage of variation in chars
f_percent = 0.3
# min number of words per chunk
min_word_range = 1
# max number of words per chunk      
max_word_range = 5

# image sets
# font
unicode_font_name = "./fonts/CODE2000.TTF"  # "simsun.ttc"
# font size
text_size = 140
# center text 
pad_img = (50, 100)
# text color
text_color = (255, 255, 255)
# background color
background_color = (0, 0, 0)


# video sets
# fps image
fps = 100.0
# set number of frames per chunk, add at the end C frames with the correct chunk
# number of corrupted frames per chunk
n_frames_per_chunk_chaos = 50
# number of correct frames per chunk
n_frames_per_correct_chunk = 50
# empty chunk between chunks
n_empty_chunk = 1

