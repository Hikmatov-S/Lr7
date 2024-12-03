import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel
from PyQt5.QtGui import QPixmap, QImage
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QHBoxLayout
from PIL import Image, ImageDraw
import numpy as np
from PyQt5.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 900, 700)
        self.setWindowTitle('Лабораторная Работа 7')

        # Основной вертикальный макет
        main_layout = QVBoxLayout()

        # Верхний макет для кнопок
        top_layout = QHBoxLayout()

        self.open_button = QPushButton('Загрузить Изображение')
        self.open_button.clicked.connect(self.open_image)
        top_layout.addWidget(self.open_button)

        self.plot_button = QPushButton('Построить График')
        self.plot_button.clicked.connect(self.create_plot)
        top_layout.addWidget(self.plot_button)

        self.save_button = QPushButton('Сохранить График')
        self.save_button.clicked.connect(self.save_plot)
        top_layout.addWidget(self.save_button)

        # Добавление верхнего макета в основной макет
        main_layout.addLayout(top_layout)

        # Метка для изображения с рамкой и цветным фоном
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid black; background-color: #f0f0f0;")
        main_layout.addWidget(self.image_label)

        # Полотно для графиков с дополнительным отступом
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        canvas_container = QWidget()
        canvas_container.setStyleSheet("border: 1px solid black; padding: 10px;")
        canvas_layout = QVBoxLayout(canvas_container)
        canvas_layout.addWidget(self.canvas)
        main_layout.addWidget(canvas_container)

        self.setLayout(main_layout)
    
    def save_plot(self):
        file_name, _ = QFileDialog.getSaveFileName(self, 'Сохранить график', 
                                                   '', 
                                                   'Images (*.png *.jpg *.bmp)')
        if file_name:
            self.figure.savefig(file_name)

    def open_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Открыть изображение', 
                                                   '', 
                                                   'Images (*.png *.xpm *.jpg *.bmp)')
        if file_name:
            pixmap = QPixmap(file_name)
            self.image_label.setPixmap(pixmap)

    def create_plot(self):
        x = range(-10, 10)
        y = [i**(3/7) for i in x]
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x, y)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.grid(True)
        image_path = self.image_label.pixmap().toImage().save('image.png')
        img = Image.open('image.png')
        width, height = img.size
    
        mask = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(mask)
        
        draw.polygon([(width // 4, height * 3 // 4), (width // 2, height * 3 // 4), (width // 4, height // 2)], fill=255)
    
        img = img.convert('RGBA')
        img.putalpha(mask)
        img = img.crop((width // 4, height // 4, width * 3 // 4, height * 3 // 4))
        
        arr = np.array(img)
        image = OffsetImage(arr, zoom=0.5)
        ab = AnnotationBbox(image, (2.5, 2.5), frameon=False)
        ax.add_artist(ab)
        
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
