import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy, QScrollArea, QMainWindow
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from database import get_connection

class ClassList(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Class List')
        self.setGeometry(400, 100, 700, 600)
        self.setFixedSize(700, 600)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        self.setStyleSheet("""
            QWidget {
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }
            QLabel {
                color: #000087;
                font-weight: bold;
            }
        """)

        self.content_widget = QWidget()
        scroll_area.setWidget(self.content_widget)

        self.layout = QVBoxLayout(self.content_widget)

        self.label = QLabel('Class List')
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont('Cambria', 27, QFont.Bold))
        self.label.setStyleSheet("color: #000087;")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Search by Level or Name')
        self.search_input.setMinimumHeight(30)
        self.search_input.textChanged.connect(self.search_class)
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: #000087;
                border: 1px solid #4169E1;
                padding: 5px;
                font-weight: bold;
            }
        """)

        self.list_widget = QListWidget()
        self.list_widget.setMinimumHeight(400)
        self.list_widget.setStyleSheet("""
            QListWidget {
                background-color: white;
                color: #000087;
                border: 1px solid #4169E1;
                padding: 5px;
                font-weight: bold;
                font-size: 13px;                       
            }
        """)

        self.list_widget.itemDoubleClicked.connect(self.show_class_details)

        self.back_button = QPushButton('Back')
        self.back_button.setMinimumHeight(40)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #000087;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4169E1;
            }
        """) 
        self.back_button.clicked.connect(self.back_to_dashboard)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)

        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.search_input)
        self.layout.addWidget(self.list_widget)
        self.layout.addLayout(button_layout)
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        self.load_classes()

    def load_classes(self):
        self.classes = []
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT idClass, classLevel, className FROM Classes")
        classes = cursor.fetchall()
        connection.close()

        self.list_widget.clear()
        for i, clas in enumerate(classes, start=1):
            class_info = f"{i}. {clas[1]} - {clas[2]}"
            self.classes.append(class_info)
            self.list_widget.addItem(class_info)

    def search_class(self):
        search_text = self.search_input.text().lower()
        self.list_widget.clear()
        for clas in self.classes:
            if search_text in clas.lower():
                self.list_widget.addItem(clas)

    def show_class_details(self, item):
        class_id = item.text().split('.')[0].strip()
        self.main_app.show_class_detail(class_id)


    def back_to_dashboard(self):
            self.main_app.show_admin_dashboard()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = QMainWindow()
    window = ClassList(mainWin)
    window.show()
    sys.exit(app.exec_())
