#!/usr/bin/env python
"""text_video_glitch.py."""
__author__ = "amxrfe"
__copyright__ = "Copyright 2020, Planet Earth"


import imageio
import argparse
import datetime
from tqdm import tqdm
from PIL import ImageFont

from utils import *
from text_video_glitch_config_file import *

if __name__ == '__main__':
    # set text config
    word_range = sorted([min_word_range, max_word_range])
    # set font type and size
    unicode_font = ImageFont.truetype(unicode_font_name, text_size)
    # get text and sanitize
    text = get_text(text_path)
    # split in random chunks
    text_list = create_chunks(text, word_range)
    # extend text list
    text_list = add_space_btw_chunks(text_list)
    # get larger chunk to print and calculate necessary min img dimension
    image_size = find_max_chunk(text_list, pad_img, unicode_font)
    list_of_images = list()
    for chunk in tqdm(text_list):
        # print(chunk)
        # get N random chunks
        chaos_chunk_order = list()
        chaos_chunk = list()
        for _ in range(n_frames_per_chunk_chaos):
            chaos_chunk_order.append(make_chaos(chunk, f_percent))
        # double C randomic frames
        for i in range(len(chaos_chunk_order)):
            chaos_chunk.append(chaos_chunk_order[i])
            if random.choice([True, False]):
                chaos_chunk.extend([chaos_chunk_order[i]] * 2)
        # union of N random chunks with K times the original chunk
        tot_chunks = chaos_chunk + [chunk] * n_frames_per_correct_chunk + [""] * n_empty_chunk
        for index, word in enumerate(tot_chunks):
            img_pil = Image.new("RGBA", image_size, color=background_color)
            draw = ImageDraw.Draw(img_pil)
            w, h = draw.textsize(word, font=unicode_font)
            draw.text(((image_size[0] - w) / 2, (image_size[1] - h) / 2), word, font=unicode_font, fill=text_color)
            img = np.array(img_pil)
            if (np.random.randint(1,100) > 65) and (index > 1): 
                if not np.array_equal(img, img_old):
                    img = img - img_old
            if index > 0: img_old = img
            # append image
            list_of_images.append(img)

    timestamp = str(datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))
    imageio.mimwrite(path_img + '/' + timestamp + "_" + video_name, np.array(list_of_images), fps=fps)
