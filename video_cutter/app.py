# -*- coding: utf-8 -*-
import os
from os.path import join, split, dirname, normpath
import re
from glob import glob
import datetime
import json
from PySide2 import QtCore, QtGui, QtWidgets
from main_window import Ui_MainWindow

os.environ['PATH'] += normpath(join(dirname(__file__), 'ffmpeg'))
if not os.getenv('SHOTS'):
    os.environ['SHOTS'] = normpath(join(split(dirname(__file__))[0], 'output'))


class VideoCutter(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(VideoCutter, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        main_icon = QtGui.QPixmap(normpath(join(dirname(__file__), 'video-editing.png')))
        self.setWindowIcon(main_icon.scaledToHeight(32, QtCore.Qt.SmoothTransformation))
        self.ui.output_path.setPlaceholderText(os.getenv('SHOTS'))
        self.video_information = None
        self.ui.btn_execute.setEnabled(False)
        self.ui.btn_execute.clicked.connect(self.cut_thish_shit)
        self.ui.btn_in_browse.clicked.connect(lambda x: self.open_file_dialog('input'))
        self.ui.btn_out_browse.clicked.connect(lambda x: self.open_file_dialog('output'))

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

        saved = os.getcwd()
        os.chdir(_dir)
        _edl = normpath(join(_dir, glob('*.EDL')[0]))
        os.chdir(saved)
        # _edl = _pth.rsplit('.')[0] + '.EDL'
        _out = normpath(join(_dir, 'info.log'))
        self.ui.input_path.setText(_pth)
        # получаем json об видосе
        cmd = 'ffprobe -i {} -v quiet -print_format json -show_format -hide_banner > {}'.format(_pth, _out)
        os.system(cmd)
        text = ''
        with open(_out, 'r') as f:
            self.video_information = json.load(f)

        self.parsing_edl(_edl)
        xx = self.video_information
        dt = xx.get('duration_time')
        text = '  Shots: {}    |    Movie Duration: {}'.format(xx.get('shots'), dt)

        for n,t in enumerate(xx.get('time_code')):
            text += '\n\r  sh: {}   |   start: {}  |  end: {}'.format(n + 1, t[0], t[1])

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
        t = '0' + str(datetime.timedelta(seconds=float(d_time)))
        xx = self.video_information
        xx['duration_time'] = t
        xx['time_code'] = []
        aim_time = t.rsplit('.',1)[0]
        for e in _edl_data:
            x = time_group.findall(e[-1])[0]
            wo_millisekonds = (x[0][:-3], x[1][:-3])
            if aim_time != wo_millisekonds[-1]:
                print(aim_time, ' ', wo_millisekonds[-1])
                xx['time_code'].append(('.'.join(x[0].rsplit(":", 1)), '.'.join(x[1].rsplit(":", 1))))
            elif aim_time == wo_millisekonds[-1]:
                print(aim_time, ' ', wo_millisekonds[-1])
                xx['time_code'].append(('.'.join(x[0].rsplit(":", 1)), '.'.join(x[1].rsplit(":", 1))))
                break
        xx['shots'] = str(len(xx.get('time_code')))

        logFile = normpath(join(dirname(_edl), 'info.log'))
        with open(logFile, 'w', encoding='utf-8') as f:
            json.dump(self.video_information, f, sort_keys=True, indent=4)

    def cut_thish_shit(self):
        xx = self.video_information

        root_dir = self.ui.output_path.text()
        if not root_dir:
            root_dir = self.ui.output_path.placeholderText()
        video = self.ui.input_path.text()
        template = re.compile('(part\d{2})')
        part_n = template.findall(split(video)[-1])[0]
        print(part_n, root_dir)
        for n, x in enumerate(xx.get('time_code')):
            n += 1
            _output = normpath(join(root_dir, '{}_sc{:02d}.mp4'.format(part_n, n)))
            _audio_out = normpath(join(root_dir, '{}_sc{:02d}.m4a'.format(part_n, n)))
            if not os.path.exists(dirname(_output)):
                print('not exists {}'.format(dirname(_output)))
                os.makedirs(dirname(_output))
            cmd = 'ffmpeg -i {} -ss {} -to {} -c copy {}'.format(video, x[0], x[1], _output)
            os.system(cmd)
            print(cmd)

            cmd = 'ffmpeg -i {} -vn -acodec copy {}'.format(_output, _audio_out)
            os.system(cmd)
            print(cmd)

    def open_file_dialog(self, field):
        filter = 'Mp4 files (*.mp4)'
        dialog = QtWidgets.QFileDialog
        if field == 'input':
            path, __ = dialog.getOpenFileName(self, 'Choose your video', os.getcwd(), filter)
            print(path, ">> ", __)
            _dir, _file = split(path)
            self.analyze_video(_dir, _file)
            x = self.ui.input_path
        else:
            path = dialog.getExistingDirectory(self, 'Choose your destiny')
            x = self.ui.output_path

        x.setText(path)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = VideoCutter()
    win.setWindowTitle('Shot cutter')
    win.setGeometry(QtCore.QRect(150, 180, 450, 285))
    win.show()
    sys.exit(app.exec_())





