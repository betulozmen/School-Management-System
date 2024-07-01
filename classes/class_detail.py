import sys
from database import get_connection
from PyQt5.QtWidgets import QVBoxLayout, QDialog, QWidget, QApplication, QPushButton, QScrollArea, QHBoxLayout, QSpacerItem, QSizePolicy, QListWidget, QLineEdit, QLabel
from student.student_detail import StudentDetail
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class ClassDetail(QDialog):
    def __init__(self, classId, main_app, previous_screen=None):
        super().__init__()
        self.classId = classId
        self.main_app = main_app
        self.previous_screen = previous_screen

        self.Window = []
        self.init_ui()

    def init_ui(self):

        self.setWindowTitle = ("Class Student Detail")

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

        self.label = QLabel('Class Student List')
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont('Cambria', 27, QFont.Bold))
        self.label.setStyleSheet("color: #000087;")


        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Search by ID, Name, Surname...')
        self.search_input.setMinimumHeight(30)
        self.search_input.textChanged.connect(self.search_students)
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
        self.list_widget.itemDoubleClicked.connect(self.show_student_details)
        
        self.add_student_button = QPushButton('Add Student')
        self.add_student_button.setMinimumHeight(40)
        self.add_student_button.setStyleSheet("""
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
        self.add_student_button.clicked.connect(self.show_add_student)

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
        self.back_button.clicked.connect(self.back_to_previous_screen)

        back_layout = QHBoxLayout()
        back_layout.addWidget(self.back_button)
        back_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        button_layout.addWidget(self.add_student_button) 

        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.search_input)
        self.layout.addWidget(self.list_widget)
        self.layout.addLayout(button_layout)
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        self.classDetails()

    def classDetails(self):
        self.students = []
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(' SELECT * FROM Students WHERE Classes_idClass = %s',(self.classId,))
        classStudents = cursor.fetchall()
        connection.close()

        self.list_widget.clear()
        if classStudents:
            for i, student in enumerate(classStudents, start=1):
                student_info = f"{i}. {student[0]}: {student[1]} {student[2]}"
                self.students.append(student_info)
                self.list_widget.addItem(student_info)
        else:
            self.list_widget.addItem("No students in this class.")
    
    def search_students(self):
        query = self.search_input.text().lower()
        self.list_widget.clear()
        for student in self.students:
            if query in student.lower():
                self.list_widget.addItem(student)

    def show_student_details(self, item):
        student_id = item.text().split('.')[1].split(":")[0].strip()
        self.main_app.show_student_detail(student_id, previous_screen='class_detail')

    def back_to_previous_screen(self):
        self.main_app.show_class_list()

    def show_add_student(self):  # Add this method
        self.main_app.show_student_add(self.classId)

    def showEvent(self, event):
        super().showEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClassDetail(None)
    window.show()
    sys.exit(app.exec_())
    