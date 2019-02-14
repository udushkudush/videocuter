import os
from os.path import join, split, dirname, normpath
import re

os.environ['PATH'] += normpath(join(split(dirname(__file__))[0], 'ffmpeg_4.1', 'bin'))

root_dir = join(split(dirname(__file__))[0])
_edl = normpath(join(root_dir, 'data', 'Alisa.EDL'))
my_clip = normpath(join(root_dir, 'data', 'sample.mp4'))
_output = ""

template = r"(\d{2}:\d{2}:\d{2}:\d{2})\s(\d{2}:\d{2}:\d{2}:\d{2})\n"
with open(_edl, 'r') as f:
    _edl_data = re.findall(template, f.read())

_timecode = []
for x, t in enumerate(_edl_data):
    _output = normpath(join(root_dir, 'output', 'out_clip_{:03d}.mp4'.format(x)))
    _audio_out = normpath(join(root_dir, 'output', 'out_clip_{:03d}.m4a'.format(x)))
    # _timecode.append(('.'.join(t[0].rsplit(':', 1)), '.'.join(t[1].rsplit(':', 1))))
    xx = ('.'.join(t[0].rsplit(':', 1)), '.'.join(t[1].rsplit(':', 1)))

    cmd = 'ffmpeg -i {} -ss {} -t {} -c copy {}'.format(my_clip, xx[0], xx[1], _output)
    os.system(cmd)
    print(cmd)

    cmd = 'ffmpeg -i {} -vn -acodec copy {}'.format(_output, _audio_out)
    os.system(cmd)
    print(cmd)





