from database import get_connection
import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QMessageBox, QSpacerItem, QSizePolicy, QApplication, QHBoxLayout, QLineEdit, QMainWindow, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class StudentList(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Student List')
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

        self.label = QLabel('Student List')
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

        self.add_button = QPushButton('Add Student')
        self.add_button.setMinimumHeight(40)
        self.add_button.setStyleSheet("""
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
        self.add_button.clicked.connect(self.add_student)

        self.delete_button = QPushButton('Delete Student')
        self.delete_button.setMinimumHeight(40)
        self.delete_button.setStyleSheet("""
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
        self.delete_button.clicked.connect(self.delete_student)

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
        self.back_button.clicked.connect(self.back_to_admin_dashboard)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
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

        self.load_students()

    def load_students(self):
        self.students = []  # Store student information for search functionality
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT idStudent, studentName, studentSurname FROM Students")
        students = cursor.fetchall()
        connection.close()

        self.list_widget.clear()
        for i, student in enumerate(students, start=1):
            student_info = f"{i}. {student[0]}: {student[1]} {student[2]}"
            self.students.append(student_info)
            self.list_widget.addItem(student_info)

    def search_students(self):
        query = self.search_input.text().lower()
        self.list_widget.clear()
        for student in self.students:
            if query in student.lower():
                self.list_widget.addItem(student)

    def add_student(self):
        self.main_app.show_student_registration()

    def delete_student(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            student_id = selected_item.text().split(':')[0].split('.')[1].strip()
            connection = get_connection()
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT Parents_idParent FROM Parents_has_Students WHERE Students_idStudent = %s", (student_id,))
                parent_id = cursor.fetchone()[0]
                cursor.execute("DELETE FROM Parents_has_Students WHERE Students_idStudent = %s", (student_id,))
                cursor.execute("DELETE FROM Attendance WHERE Students_idStudent = %s", (student_id,))
                cursor.execute("DELETE FROM StudentBalances WHERE Students_idStudent = %s", (student_id,))
                cursor.execute("DELETE FROM Restrictions WHERE Students_idStudent = %s", (student_id,))
                cursor.execute("DELETE FROM Canteen_Payment WHERE Students_idStudent = %s", (student_id,))
                cursor.execute("DELETE FROM Canteen_Shopping WHERE Students_idStudent = %s", (student_id,))

                cursor.execute("DELETE FROM Students WHERE idStudent = %s", (student_id,))
                connection.commit()

                # Check if the parent has any other students
                cursor.execute("SELECT COUNT(*) FROM Parents_has_Students WHERE Parents_idParent = %s", (parent_id,))
                count = cursor.fetchone()[0]

                # If the parent has no other students, delete the parent
                if count == 0:
                    cursor.execute("DELETE FROM Parents WHERE idParent = %s", (parent_id,))
                connection.commit()
                
                QMessageBox.information(self, 'Success', 'Student deleted successfully.')
                self.load_students() 
            except Exception as e:
                QMessageBox.warning(self, 'Error', f"Error deleting student: {e}")
            finally:
                connection.close()

    def show_student_details(self, item):
        student_id = item.text().split('.')[1].split(":")[0].strip()
        self.main_app.show_student_detail(student_id)
        
    def back_to_admin_dashboard(self):
        self.main_app.show_admin_dashboard()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = QMainWindow()
    window = StudentList(mainWin)
    mainWin.setCentralWidget(window)
    mainWin.show()
    sys.exit(app.exec_())
