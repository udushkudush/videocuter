import os
import subprocess
from os.path import join, split, dirname, normpath
import re
import glob
import datetime
import json
from PySide2 import QtCore, QtGui, QtWidgets
from video_cutter.main_window import Ui_MainWindow

os.environ['PATH'] += normpath(join(split(dirname(__file__))[0], 'ffmpeg_4.1', 'bin'))
os.environ['SHOTS'] = normpath(join(split(dirname(__file__))[0], 'output'))

class VideoCutter(QtWidgets.QMainWindow):
    def __init__(self):
        super(VideoCutter, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.output_path.setPlaceholderText(os.getenv('SHOTS'))
        # self.setAcceptDrops(True)
        self.video_information = None
        self.ui.btn_execute.setEnabled(False)

    # def dragEnterEvent(self, event:QtGui.QDragEnterEvent):
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if os.path.isfile(path):
                _dir, _file = split(path)
                if _file.endswith(".mp4"):
                    self.analyze_video(_dir, _file)
                else:
                    print('This format not compatible\n\rpath: {} | drop video: {}'.format(_dir, _file))

    def analyze_video(self, _dir, _file):
        # путь к файлу который бум резать
        _pth = normpath(join(_dir, _file))
        _edl = _pth.rsplit('.')[0] + '.EDL'
        _out = normpath(join(_dir, 'info.log'))
        self.ui.input_path.setText(_pth)
        cmd = 'ffprobe -i {} -v quiet -print_format json -show_format -hide_banner > {}'.format(_pth, _out)
        os.system(cmd)
        text = ''
        with open(_out, 'r') as f:
            self.video_information = json.load(f)

        # self.video_information['edl_data'] = self.parsing_edl(_edl)
        self.parsing_edl(_edl)
        xx = self.video_information
        dt = xx.get('duration_time')
        text = 'Shots: {}\t|\tDuration: {}'.format(xx.get('shots'), dt)
        fuck = []
        for n,x in enumerate(xx.get('time_code')):
            z = (dt.rsplit('.', 1)[0], x[1].rsplit('.', 1)[0])
            if z[0] not in z[1]:
                print(z)
                data = (x[0], x[1])
                a = '\n\r  sh: {} | start: {} | end: {}'.format(n + 1, x[0], x[1])
                text += a
                fuck.append(data)
            elif z[0] in z[1]:
                data = (x[0], x[1])
                fuck.append(data)
                a = '\n\r  sh: {} | start: {} | end: {}'.format(n + 1, x[0], x[1])
                text += a
                # print('blo: {}\n\rcapture: {}'.format(a, z))
                break
        self.ui.output_info.setText(text)
        self.ui.btn_execute.setEnabled(True)

    def parsing_edl(self, _edl):
        template = re.compile(
            r"(^\d{3}\s+\D{2}\s+\D?\s+\D?\s+)(\d{2}:\d{2}:\d{2}:\d{2}\s?\d{2}:\d{2}:\d{2}:\d{2}\s)(\d{2}:\d{2}:\d{2}:\d{2}\s\d{2}:\d{2}:\d{2}:\d{2})\n",
            re.MULTILINE)
        time_group = re.compile(r"(\d{2}:\d{2}:\d{2}:\d{2})\s(\d{2}:\d{2}:\d{2}:\d{2})")
        with open(_edl, 'r') as f:
            _edl_data = template.findall(f.read())
        d_time = self.video_information.get('format').get('duration')
        t = str(datetime.timedelta(seconds=float(d_time)))
        xx = self.video_information
        xx['shots'] = str(len(_edl_data))
        xx['duration_time'] = t
        xx['time_code'] = []
        for e in _edl_data:
            x = time_group.findall(e[-1])[0]
            xx['time_code'].append(('.'.join(x[0].rsplit(":", 1)), '.'.join(x[1].rsplit(":", 1))))

    def cut_thish_shit(self, video):

        xx = self.video_information
        for n, x in enumerate(xx.get('time_code')):
            _output = normpath(join(root_dir, 'output', 'out_clip_{:03d}.mp4'.format(x)))
            _audio_out = normpath(join(root_dir, 'output', 'out_clip_{:03d}.m4a'.format(x)))
            z = (dt.rsplit('.', 1)[0], x[1].rsplit('.', 1)[0])
            if z[0] not in z[1]:
                a = '\n\r  sh: {} | start: {} | end: {}'.format(n + 1, x[0], x[1])
            elif z[0] in z[1]:
                a = '\n\r  sh: {} | start: {} | end: {}'.format(n + 1, x[0], x[1])
                break

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
    win.setGeometry(QtCore.QRect(150, 180, 450, 285))
    win.show()
    sys.exit(app.exec_())





