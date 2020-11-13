#!/usr/bin/env python
"""text_video_glitch.py."""
__author__ = "amxrfe"
__copyright__ = "Copyright 2020, Planet Earth"


import argparse
from utils import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='maskrcnn-training')
    parser.add_argument('--text_path', type=str, default='./text_file/text.txt',
                        help='path/to/text.txt')
    parser.add_argument('--out_name', type=str, default='text_to_chaos_video.mp4',
                        help='video name output')
    parser.add_argument('--min_word_range', type=int, default=10,
                        help='max number of words per chunk')
    parser.add_argument('--max_word_range', type=int, default=50,
                        help='max number of words per chunk')
    parser.add_argument('--f_percent', type=float, default=0.3,
                        help='set the percentage of how many letters should vary')
    parser.add_argument('--text_size', type=int, default=140,
                        help='set the percentage of how many letters should vary')

    args = parser.parse_args()

    # load text file
    text_path = args.text_path
    # output video name
    video_name = args.out_name
    # set text config
    word_range = sorted([args.min_word_range, args.max_word_range])
    # set image pad size
    pad_img = (50, 100)
    # set the percentage of how many letters should vary
    f_percent = args.f_percent

    # aesthetics configs
    text_size = args.text_size
    # set text color
    text_color = (255, 255, 255)
    # background color
    background_color = (0, 0, 0)
    # set number of frames per chunk, add at the end C frames with the correct chunk
    n_frames_per_chunk = 20
    n_frames_per_chunk_chaos = 15
    n_frames_per_correct_chunk = 10
    n_empty_chunk = 5

    # set font type and size
    unicode_font = ImageFont.truetype("simsun.ttc", text_size, encoding='unic')

    # fps image
    fps = float(n_frames_per_chunk + n_frames_per_correct_chunk + n_empty_chunk)

    # get text and sanitize
    text = get_text(text_path)

    # split in random chunks
    text_list = create_chunks(text, word_range)

    # get larger chunk and calculate min necessary img dimension
    image_size = find_max_chunk(text_list, pad_img, unicode_font)

    list_of_images = list()
    for idx, chunk in enumerate(text_list):
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

        for word in tot_chunks:
            img_pil = Image.new("RGBA", image_size, color=background_color)
            draw = ImageDraw.Draw(img_pil)
            w, h = draw.textsize(word, font=unicode_font)
            draw.text(((image_size[0] - w) / 2, (image_size[1] - h) / 2), word, font=unicode_font, fill=text_color)
            img = np.array(img_pil)

            # display results
            list_of_images.append(img)

    imageio.mimwrite(path_imgs + '/' + video_name, np.array(list_of_images), fps=fps)
