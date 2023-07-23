import sys
import pytube
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QFileDialog, QMessageBox
from bs4 import BeautifulSoup
import requests


class Downloader(QWidget):
    def __init__(self):
        super().__init__()

        # Установка пользовательского интерфейса
        self.initUI()

    def initUI(self):

        # Создание метки и поля ввода для URL-адреса видео
        url_label = QLabel('URL видео:', self)
        url_label.move(20, 20)

        self.url_input = QLineEdit(self)
        self.url_input.move(100, 20)
        self.url_input.resize(280, 20)

        # Создание метки и выпадающего списка для выбора качества видео
        quality_label = QLabel('Качество:', self)
        quality_label.move(20, 80)
        self.quality_select = QComboBox(self)
        self.quality_select.move(100, 80)
        self.quality_select.resize(280, 20)

        # Создание кнопки для получения доступных качеств видео
        get_quality_button = QPushButton('Получить качество', self)
        get_quality_button.move(50, 110)
        get_quality_button.clicked.connect(self.get_quality)

        # Создание кнопки для скачивания видео
        download_button = QPushButton('Скачать', self)
        download_button.move(200, 110)
        download_button.clicked.connect(self.download)

        # Настройка окна
        self.setGeometry(200, 200, 450, 140)
        self.setWindowTitle('YouTube Downloader By R2R')
        self.show()

    def get_video_title(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                video_title = soup.find('meta', {'name': 'title'})['content']
                return video_title
            else:
                return "Название видео не найдено"
        except requests.RequestException:
            return "Ошибка при получении названия видео"

    def get_quality(self):
        # Получение URL-адреса YouTube видео
        url = self.url_input.text()

        # Проверка, что поле ввода URL не пустое
        if not url:
            QMessageBox.warning(self, "Ошибка", "Введите рабочую ссылку")
            return

        # Создание объекта YouTube
        self.youtube = pytube.YouTube(url)

        # Получение доступных потоков (качеств) для видео
        streams = self.youtube.streams.filter(progressive=True).all()

        # Заполнение выпадающего списка качеств видео
        self.quality_select.clear()
        for stream in streams:
            self.quality_select.addItem(stream.resolution)


    def download(self):
        # Проверка, что был получен объект YouTube
        if not hasattr(self, 'youtube'):
            QMessageBox.warning(self, "Ошибка", "Сначала получите доступные качества видео")
            return

        # Получение доступных потоков (качеств) для видео
        streams = self.youtube.streams.filter(progressive=True)

        # Получение выбранного пользователем качества видео
        choice = self.quality_select.currentIndex()
        stream = streams[choice]

        while True:
            # Открытие диалогового окна для выбора места сохранения файла
            save_path, _ = QFileDialog.getSaveFileName(self, "Сохраните файл", "", "Video Files (*.mp4)")

            # Проверка, был ли указан путь для сохранения
            if not save_path:
                reply = QMessageBox.question(
                    self, "Предупреждение",
                    "Вы не выбрали место для сохранения! "
                    "Выбрать повторно?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.No:
                    # Пользователь отменил , выходим из цикла
                    return
            else:
                # Путь для сохранения указан, выполняем скачивание и выходим из цикла
                stream.download(save_path)
                QMessageBox.information(self, "Загрузка завершена", "Успешно скачано!")
                return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    downloader = Downloader()
    sys.exit(app.exec_())