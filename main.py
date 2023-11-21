from subprocess import run
from platform import system
from pathlib import Path
from json import load
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon


def get_lang() -> dict:
    with open('language.json', 'r', encoding='utf-8') as js:
        return load(js)['lang']


def set_lang(addition=False) -> None | tuple:
    current_text = window.comboBox_2.currentText()
    if not addition:
        current_text = window.comboBox_2.currentText()
        window.label.setText(lang[current_text]['1'])
        window.label_2.setText(lang[current_text]['2'])
        window.label_3.setText(lang[current_text]['0'])
        window.label_5.setText(lang[current_text]['3'])
        window.label_4.setText(lang[current_text]['13'])
        window.label_6.setText(lang[current_text]['14'])
        window.pushButton.setText(lang[current_text]['4'])
        window.comboBox.clear()
        item = lang[current_text]
        window.comboBox.addItems([item['5'], item['6'], item['7'], item['8']])
    else:
        return (lang[current_text]['9'], lang[current_text]['10'],
                lang[current_text]['11'], lang[current_text]['12'])


def select_file_path(choice) -> None:
    _src, _dst, *_ = set_lang(addition=True)
    src, dst = _src.split(' '), _dst.split(' ')
    msg = src[1] if choice == 'input' else dst[1]
    message = f'{src[0]} {msg} {src[2]}'
    file_path = ''
    if window.comboBox.currentIndex() == 3 and choice == 'input':
        files_path = QtWidgets.QFileDialog.getOpenFileNames(window, message, '.')[0]
        files = [Path(i).name for i in files_path]
        file_path = ', '.join(files)
        with open('concat.txt', 'w', encoding='utf-8') as txt:
            text = ''
            for file in files:
                text += f'file {file}\n'
            txt.write(text)
    elif choice == 'input':
        file_path = QtWidgets.QFileDialog.getOpenFileName(window, message, '.')[0]
    elif choice == 'output':
        file_path = QtWidgets.QFileDialog.getSaveFileName(window, message, '.')[0]
    (window.lineEdit.setText(file_path) if choice == 'input'
     else window.lineEdit_3.setText(file_path))


def select_input_file_path() -> None:
    select_file_path('input')


def select_output_file_path() -> None:
    select_file_path('output')


def command() -> None:
    window.textBrowser.clear()
    text = get_sys_info()
    if text:
        window.textBrowser.append(text)
        return
    input_file = window.lineEdit.displayText()
    output_file = window.lineEdit_3.displayText()
    if not input_file or not output_file:
        return
    start_time = window.timeEdit.time().toPyTime()
    end_time = window.timeEdit_2.time().toPyTime()
    action = {
        0: f'ffmpeg -i "{input_file}" "{output_file}"',
        1: (f'ffmpeg -ss {start_time} -to {end_time} -i "{input_file}" '
            f'-c copy "{output_file}"'),
        2: (f'ffmpeg -y -ss {start_time} -to {end_time} '
            f'-i "{input_file}" "{output_file}"'),
        3: f'ffmpeg -f concat -i concat.txt "{output_file}"'
    }
    for index in action:
        if window.comboBox.currentIndex() == index:
            cmd = action[index]
            try:
                run(cmd, shell=True)
            except Exception as e:
                window.textBrowser.append(str(e))
            else:
                window.textBrowser.append(set_lang(addition=True)[3])


def functional() -> None:
    window.toolButton.clicked.connect(select_input_file_path)
    window.toolButton_2.clicked.connect(select_output_file_path)
    window.pushButton.clicked.connect(command)
    window.pushButton_2.clicked.connect(set_lang)
    window.textBrowser.setOpenLinks(False)
    set_lang()
    window.show()
    app.setWindowIcon(QIcon('images/favicon.ico'))
    app.exec_()


def get_sys_info() -> str | None:
    url = 'https://ffmpeg.org/download.html'
    os_system = system()
    if os_system == 'Windows':
        url_link = ('https://github.com/BtbN/FFmpeg-Builds/releases/download/'
                    'latest/ffmpeg-master-latest-win64-gpl.zip')
        if not Path('ffmpeg.exe').exists():
            return (f"{set_lang(addition=True)[2]}<a href='{url_link}'>"
                    f"ffmpeg-master-latest-win64-gpl.zip</a>, "
                    f"(<a href='{url}'>ffmpeg</a>)")


if __name__ == "__main__":
    lang = get_lang()
    app = QtWidgets.QApplication([])
    window = uic.loadUi("ffmpeg.ui")
    functional()
