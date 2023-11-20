import os
import subprocess
import platform
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon
from language import lang


def set_lang(addition=False):
    current_text = window.comboBox_2.currentText()
    window.label.setText(lang[current_text][1])
    window.label_2.setText(lang[current_text][2])
    window.label_3.setText(lang[current_text][0])
    window.label_4.setText(lang[current_text][4])
    window.label_5.setText(lang[current_text][3])
    window.pushButton.setText(lang[current_text][5])
    window.comboBox.clear()
    item = lang[current_text]
    window.comboBox.addItems([item[6], item[7], item[8], item[9]])
    if addition:
        return lang[current_text][10], lang[current_text][11]


def select_file_path(choice) -> None:
    _src, _dst = set_lang(addition=True)
    src, dst = _src.split(' '), _dst.split(' ')
    msg = src[1] if choice == 'input' else dst[1]
    message = f'{src[0]} {msg} {src[2]}'
    file_path = QtWidgets.QFileDialog.getOpenFileName(window, message, '.')[0]
    (window.lineEdit.setText(file_path) if choice == 'input'
     else window.lineEdit_3.setText(file_path))


def select_input_file_path() -> None:
    select_file_path('input')


def select_output_file_path() -> None:
    select_file_path('output')


def command():
    input_file = window.lineEdit.displayText()
    output_file = window.lineEdit_3.displayText()
    start_time = '00'
    end_time = '00'
    # 0 - конвертирование, 1 - обрезка !без конвертации,
    # 2 - обрезка и конвертирование, 3 - склеивание видео
    action = {
        0: f"ffmpeg.exe -i {input_file} {output_file}",
        1: (f"ffmpeg.exe -to {start_time} -i {input_file} "
            f"-c copy {output_file}"),
        2: (f"ffmpeg.exe -y -ss {start_time} -to {end_time} "
            f"-i {input_file} {output_file}"),
        3: f"ffmpeg -f concat -i concat.txt out.mkv"
    }
    # os.system('mkdir OSSS')
    # os.system('cmd --window -- cmd -c "ipconfig"')
    for index in action:
        if window.comboBox.currentIndex() == index:
            cmd = action[index]
            subprocess.run(cmd, shell=True, encoding='866')


def functional():
    window.toolButton.clicked.connect(select_input_file_path)
    window.toolButton_2.clicked.connect(select_output_file_path)
    window.pushButton.clicked.connect(command)
    window.pushButton_2.clicked.connect(set_lang)
    set_lang()
    window.show()
    app.setWindowIcon(QIcon('images/favicon.ico'))
    app.exec_()


def get_sys_info():
    url = 'https://ffmpeg.org/download.html'
    if platform.system() == 'Windows':
        url_link = ('https://github.com/BtbN/FFmpeg-Builds/releases/download/'
                    'latest/ffmpeg-master-latest-win64-gpl.zip')


if __name__ == "__main__":
    get_sys_info()
    app = QtWidgets.QApplication([])
    window = uic.loadUi("ffmpeg.ui")
    functional()
