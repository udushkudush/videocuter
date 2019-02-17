import os
import subprocess
from os.path import join, split, dirname, normpath
import re
import glob
import json
from PySide2 import QtCore, QtGui, QtWidgets
from video_cutter.main_window import Ui_MainWindow

os.environ['PATH'] += normpath(join(split(dirname(__file__))[0], 'ffmpeg_4.1', 'bin'))


class VideoCutter(QtWidgets.QMainWindow):
    def __init__(self):
        super(VideoCutter, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.setAcceptDrops(True)

    # def dragEnterEvent(self, event:QtGui.QDragEnterEvent):
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            print('ignore event')
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if os.path.isfile(path):
                _dir, _file = split(path)
                if _file.endswith(".mp4"):
                    print('path: {} | file: {}'.format(_dir, _file))
                    self.analyze_video(_dir, _file)
                else:
                    print('path: {} | drop video: {}'.format(_dir, _file))

    def analyze_video(self, _dir, _file):
        mask = join(_dir, '*.EDL')
        files = glob.glob(mask)
        # for f in files:
        #     print(f)
        _pth = normpath(join(_dir, _file))
        _out = normpath(join(_dir, 'info.log'))
        self.ui.input_path.setText(_pth)
        cmd = 'ffprobe -i {} -v quiet -print_format json -show_format -hide_banner > {}'.format(_pth, _out)
        os.system(cmd)
        data = ''
        text = ''
        with open(_out, 'r') as f:
            data = json.load(f)
        for d in data.keys():
            c = data[d]
            for i in c.keys():
                if i != 'tags':
                    text += '>> {}\t: {}\n\r'.format(i, c[i])
                    # print('>> {}\t: {}'.format(i, c[i]))
        self.ui.output_info.setText(text)

    def video_cutter(self, video, info):
        root_dir = join(split(dirname(__file__))[0])
        _edl = normpath(join(root_dir, 'data', info))
        my_clip = normpath(join(root_dir, 'data', video))
        _output = ""

        template = r"(\d{2}:\d{2}:\d{2}:\d{2})\s(\d{2}:\d{2}:\d{2}:\d{2})\n"
        with open(_edl, 'r') as f:
            _edl_data = re.findall(template, f.read())

        for x, t in enumerate(_edl_data):
            _output = normpath(join(root_dir, 'output', 'out_clip_{:03d}.mp4'.format(x)))
            _audio_out = normpath(join(root_dir, 'output', 'out_clip_{:03d}.m4a'.format(x)))

            if not os.path.exists(dirname(_output)):
                print('not exists {}'.format(dirname(_output)))
                os.makedirs(dirname(_output))

            xx = ('.'.join(t[0].rsplit(':', 1)), '.'.join(t[1].rsplit(':', 1)))

            cmd = 'ffmpeg -i {} -ss {} -t {} -c copy {}'.format(my_clip, xx[0], xx[1], _output)
            os.system(cmd)
            print(cmd)

            cmd = 'ffmpeg -i {} -vn -acodec copy {}'.format(_output, _audio_out)
            os.system(cmd)
            print(cmd)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = VideoCutter()
    win.show()
    sys.exit(app.exec_())





