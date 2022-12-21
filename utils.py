import re
import cv2
import math
import random
import string
import pathlib
import numpy as np
from PIL import ImageDraw, Image
from confusables.confusables import Confusables


def get_similar_char(string):
    confusables = Confusables('./confusables/confusables.txt')
    cpattern = confusables.confusables_regex(string)
    return cpattern.replace("[","").replace("]","").split("\\")


# https://stackoverflow.com/questions/73426687/change-ascii-text-font-to-unicode-font-in-python
def random_printable_unicode():
    def very_random_chars():
        out = np.random.choice(np.random.randint(1,65533))
        return out

    def random_chars():
        cyrillic_range = (int('0410', 16), int('0450', 16))  
        jappo_range = (int('3040', 16), int('309F', 16)) 
        greek_range = (int('0370', 16), int('03FF', 16)) 
        arr1 = np.random.randint(*cyrillic_range)
        arr2 = np.random.randint(*jappo_range)
        arr3 = np.random.randint(*greek_range)
        out = np.stack((arr1, arr2, arr3))
        out = np.stack((arr1, arr2, arr3))
        out = np.random.choice(out)
        return out

    while True:
        # i = random_chars()
        i = very_random_chars()
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
        # get vertical_motion random step between 1 and set word_range
        idx = np.random.randint(*word_range)
        # if between the two indexes we found vertical_motion \n, split and update idx
        for pos, word in enumerate(text[idx_prev: idx + idx_prev]):
            if word.find('\n') != -1 or False:  # or word.find(',') != -1:
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
    random_chars = ''.join([random_printable_unicode() for _ in range(40)])
    replace = ''.join(random.choices(random_chars + string.ascii_uppercase + string.digits, k=len_chunk))
    # append chunks
    new_text_chunk = ''
    for i, pos in enumerate(pos_random_letters):
        new_text_chunk += text_chunk[i] if pos is 0 else replace[i]

    ## alternative if similar chars will ever works
    # new_text_chunk = ''
    # for letter in text_chunk:
    #     similar_chars = get_similar_char(letter)
    #     similar_char = random.choices(similar_chars, k=1)[0]
    #     new_text_chunk += similar_char
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
        ext_text_list.append(np.random.randint(0,  len(max(text_list, key=len))) * " ")
        ext_text_list.append(word)
    return ext_text_list


def create_blur_(f):
    """
    in: img 4 dimensions
    in function: 2 dimensions
    out: same
    """
    # Suppress/hide the warning
    np.seterr(invalid='ignore')
    f = f[:,:,0]
    f = f/f.max() # normalize

    # F(u,v), image in frequency domain
    F = np.fft.fft2(f)

    # H(u,v), motion blur function in frequency domain
    # Create matrix H (motion blur function H(u,v))
    M,N = F.shape 
    H = np.zeros((M+1,N+1), dtype=np.complex128) # +1 to avoid zero division

    # Motion blur parameters
    exposure_duration = 0.5     # duration of exposure
    vertical_motion = 0         # vertical motion
    horizontal_motion = 0.05    # horizontal motion

    # Fill matrix H
    for u in range(1,M+1):
        for v in range(1,N+1):
            s = np.pi*(u*vertical_motion + v*horizontal_motion)
            H[u,v] = (exposure_duration/s) * np.sin(s) * np.exp(-1j*s)

    # index slicing
    H = H[1:,1:]     
    
    # G(u,v), blurred image in frequency domain
    G = H * F

    # g(x,y), blurred image in spatial domain
    g = np.fft.ifft2(G)
    g = np.abs(g)
    return np.repeat(g[:, :, np.newaxis], 4, axis=2)

def create_blur(img, size=30):

    # generating the kernel
    kernel_motion_blur = np.zeros((size, size))
    kernel_motion_blur[int((size-1)/2), :] = np.ones(size)
    kernel_motion_blur = kernel_motion_blur / size

    # applying the kernel to the input image
    output = cv2.filter2D(img, -1, kernel_motion_blur)
    output = np.uint8(output / 2)
    return np.asarray(output)