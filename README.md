# text_to_video_glitch
Generate from txt file, a video where chunks of randomic size of the txt are displayed for N frames. K of N frames will be created with "glitched" characters. 

###  load text file
text_path = './text_file/text.txt'
###  output video name
video_name = 'text_to_chaos_video.mp4'
###  set text config
word_range = 5
text_size = 140
###  set text color
text_color = (0, 0, 255)
###  background color
background_color = (200, 200, 200)
###  set image size
image_size = [592, 1920]

# example
text: "Ivan Pregelj nacque in una modesta famiglia di Santa Lucia, oggi Most na Soči in Slovenia da Mohor, sarto, e Marija Modrejc. Perse i genitori da piccolo, e il promettente ragazzino fu seguito dalla nonna paterna e dal parroco, Jožef Fabijan, che riuscì a mandarlo per un breve tempo al Seminario Maggiore di Gorizia."

out:
![](output.gif)
