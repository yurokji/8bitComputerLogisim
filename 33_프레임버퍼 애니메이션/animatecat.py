import os
url = 'https://www.youtube.com/watch?v=IGRgOhUqNyc'
filename = 'cat_meme.mp4'
download_command = 'youtube-dl -o ' + filename + ' ' + url

print(download_command)
os.system(download_command)
