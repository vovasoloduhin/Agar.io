from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QLabel, QFrame, QFileDialog
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class GameLauncher(QWidget):
    def __init__(self):
        super().__init__()
        self.name = None
        self.port = None
        self.host = None
        self.photo_path = None
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(600, 500)
        self.setWindowTitle('Game Launcher')

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #ffecd2,
                    stop: 1 #fcb69f
                );
            }
            QLineEdit {
                padding: 10px;
                font-size: 16px;
                border: 2px solid #ffffff;
                border-radius: 8px;
                background-color: rgba(255, 255, 255, 0.8);
            }
            QPushButton {
                background-color: #ffffff;
                border-radius: 10px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                color: #f27a54;
            }
            QPushButton:hover {
                background-color: #ffe0d0;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)

        title_frame = QFrame()
        title_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #f7971e,
                    stop: 1 #ffd200
                );
                border: 3px solid white;
                border-radius: 15px;
                padding: 10px;
            }
        """)
        title_layout = QVBoxLayout()
        title_label = QLabel("GAME LAUNCHER")
        title_label.setFont(QFont("Verdana", 22, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white;")
        title_layout.addWidget(title_label)
        title_frame.setLayout(title_layout)
        layout.addWidget(title_frame)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Ваше ім\'я')
        layout.addWidget(self.name_input)

        self.host_input = QLineEdit()
        self.host_input.setPlaceholderText('IP сервера')
        layout.addWidget(self.host_input)

        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText('Порт сервера')
        layout.addWidget(self.port_input)

        # Кнопка вибору фото
        self.photo_btn = QPushButton('Обрати фото гравця')
        self.photo_btn.clicked.connect(self.select_photo)
        layout.addWidget(self.photo_btn)

        self.photo_label = QLabel('Фото не обране')
        self.photo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.photo_label)

        self.btn = QPushButton('Почати гру')
        self.btn.clicked.connect(self.join_server)
        layout.addWidget(self.btn)

        self.setLayout(layout)

    def select_photo(self):
        file_dialog = QFileDialog()
        path, _ = file_dialog.getOpenFileName(self, "Оберіть фото", "", "Images (*.png *.jpg *.bmp)")
        if path:
            self.photo_path = path
            self.photo_label.setText(f"Вибране фото:\n{path.split('/')[-1]}")

    def join_server(self):
        self.name = self.name_input.text()
        self.port = self.port_input.text()
        self.host = self.host_input.text()
        self.close()
