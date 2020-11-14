import math
import random
import string
import pathlib
import numpy as np
from PIL import ImageDraw, Image


path_img = "./video_out/"
pathlib.Path(path_img).mkdir(parents=True, exist_ok=True)


def random_printable_unicode():
    def random_chars():
        cyrillic_range = (int('0410', 16), int('0450', 16))  # from the Cyrillic alphabet
        jappo_range = (int('3040', 16), int('309F', 16))  # from the Cyrillic alphabet
        greek_range = (int('0370', 16), int('03FF', 16))  # from the Cyrillic alphabet
        arr1 = np.random.randint(*cyrillic_range)
        arr2 = np.random.randint(*jappo_range)
        arr3 = np.random.randint(*greek_range)
        out = np.stack((arr1, arr2, arr3))
        out = np.random.choice(out)
        return out

    while True:
        i = random_chars()
        c = chr(i)
        if c.isprintable():
            return c
        # should add another conditional break
        # to avoid infinite loop


def get_text(text_path):
    # get text and sanitize
    file = open(text_path, 'rU', encoding='utf8')
    text = file.readlines()
    text = ' '.join(text)
    return text


def create_chunks(text, word_range):
    text = text.split(' ')
    idx_prev = 0
    text_list = list()
    while idx_prev <= len(text):
        # get a random step between 1 and set word_range
        idx = np.random.randint(*word_range)
        # if between the two indexes we found a \n, split and update idx
        for pos, word in enumerate(text[idx_prev: idx + idx_prev]):
            if word.find('\n') != -1:  # or word.find(',') != -1:
                idx = pos + 1
                break
        text_list.append(' '.join(text[idx_prev: idx + idx_prev]))
        idx_prev += idx
    return text_list


def make_chaos(text_chunk, f_percent):
    # get len chunk
    len_chunk = len(text_chunk)
    if len_chunk < 4:
        f_percent = 1 + (len_chunk - 1) * (-0.13)
    # modify chunk with len == 0
    if len_chunk is 0:
        len_chunk += 1
        text_chunk += " "
    # set number of letters to modify
    n_chaos_letters = np.random.randint(0, math.ceil(len_chunk * f_percent))
    # random number of letters that we change
    pos_letters = [0] * (len_chunk - n_chaos_letters) + [1] * n_chaos_letters
    pos_random_letters = random.sample(pos_letters, len(pos_letters))
    # random number (0 to 3) of extra letters in random place
    cyrillic = ''.join([random_printable_unicode() for _ in range(40)])
    replace = ''.join(random.choices(cyrillic + string.ascii_uppercase + string.digits, k=len_chunk))
    # append chunks
    new_text_chunk = ''
    for i, pos in enumerate(pos_random_letters):
        new_text_chunk += text_chunk[i] if pos is 0 else replace[i]
    return new_text_chunk


def find_max_chunk(text_list, pad_img, unicode_font):
    max_chunk = max(text_list, key=len)
    draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    w, h = draw.textsize(max_chunk, font=unicode_font)
    # add padding
    w += pad_img[0]
    h += pad_img[1]
    # make size divisible in block of 16 pixels
    h = h - h % 16
    w = w - w % 16
    return w, h


def add_space_btw_chunks(text_list):
    ext_text_list = list()
    for word in text_list:
        ext_text_list.append(np.random.randint(10,  len(max(text_list, key=len))) * " ")
        ext_text_list.append(word)
    return ext_text_list


