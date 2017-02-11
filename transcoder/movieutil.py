#https://github.com/mwicat/httptranscode

from subprocess import Popen, PIPE
import subprocess

def is_movie(path):
    return subprocess.call(["ffprobe", path]) == 0

def transcode(path):
    return Popen(("ffmpeg -i " + path + " -movflags empty_moov -f mp4 -"), shell=True, stdout=PIPE).stdout
