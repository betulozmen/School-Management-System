import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QScrollArea, QShortcut, QHBoxLayout, QSpacerItem, QSizePolicy, QWidget, QComboBox, QDateEdit
from database import get_connection
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtCore import Qt, QDate

class StudentEntry(QWidget):
    def __init__(self, main_app, previous_screen=None):
        super().__init__()
        self.main_app = main_app
        self.previous_screen = previous_screen
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Add Absence")
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
            QLineEdit {
                background-color: white;
                color: #000087;
                border: 1px solid #000087;
                padding: 5px;
                font-weight: bold;
            }
            QComboBox {
                background-color: white;
                color: #000087;
                border: 1px solid #000087;
                padding: 5px;
                font-weight: bold;
            }
        """)
        self.content_widget = QWidget()
        scroll_area.setWidget(self.content_widget)

        self.layout = QVBoxLayout(self.content_widget)

        self.title_label = QLabel('Add Absence')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont('Cambria', 27, QFont.Bold))

        self.student_id_label = QLabel("Student ID:", self)
        self.student_id_combo = QComboBox(self)
        self.student_id_combo.addItem('Select ID')
        self.load_students()

        self.date_label = QLabel('Date:', self)
        self.date_input = QDateEdit(self)
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat('yyyy-MM-dd')
        self.date_input.setDate(QDate.currentDate())

        one_year_ago = QDate.currentDate().addYears(-1)
        self.date_input.setMinimumDate(one_year_ago)
        self.date_input.setMaximumDate(QDate.currentDate())

        self.attendanceType_label = QLabel('Type:', self)
        self.roles = ('Select', 'Full Day', 'Half Day', '1 lesson', '2 lessons', '3 lessons', '4 lessons', '5 lessons', '6 lessons', '7 lessons')
        self.attendanceType_combo = QComboBox()
        self.attendanceType_combo.addItems(self.roles)

        self.submit_button = QPushButton("Submit", self)
        self.submit_button.setMinimumHeight(40)
        self.submit_button.setStyleSheet("""
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
        self.submit_button.clicked.connect(self.submit_form)

        submit_shortcut = QShortcut(QKeySequence(Qt.Key_Return), self)
        submit_shortcut.activated.connect(self.submit_button.click)

        self.back_button = QPushButton('Back', self)
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

        form_layout = QVBoxLayout()
        form_layout.addWidget(self.title_label)
        form_layout.addWidget(self.student_id_label)
        form_layout.addWidget(self.student_id_combo)
        form_layout.addWidget(self.date_label)
        form_layout.addWidget(self.date_input)
        form_layout.addWidget(self.attendanceType_label)
        form_layout.addWidget(self.attendanceType_combo)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        button_layout.addWidget(self.submit_button)

        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.layout.addLayout(form_layout)
        self.layout.addLayout(button_layout)
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.content_widget.setLayout(self.layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def load_students(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT idStudent, studentName, studentSurname FROM Students")
        students = cursor.fetchall()
        connection.close()

        for student in students:
            display_text = f"{student[0]}: {student[1]} {student[2]}"
            self.student_id_combo.addItem(display_text, student[0])  


    def submit_form(self):
        connection = None
        cursor = None
        try:
            student_id = self.student_id_combo.currentData()
            date = self.date_input.date().toString('yyyy-MM-dd')
            attendanceType = self.attendanceType_combo.currentText()

            if student_id is not None and date and attendanceType and student_id != 0 and attendanceType != 0:
                connection = get_connection()
                cursor = connection.cursor()
                cursor.execute("INSERT INTO Attendance (Students_idStudent, attendanceDate, attendanceType) VALUES (%s, %s, %s)", (student_id, date, attendanceType))
                connection.commit()
                connection.close()
                QMessageBox.information(self, "Success", "Student attendance recorded.")
                self.student_id_combo.setCurrentIndex(0)
                self.date_input.setDate(QDate.currentDate())  
            else:
                QMessageBox.warning(self, "Error", "Please fill all the required fields")
                connection.close()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f"An error occurred: {str(e)}")
        finally:
            if cursor is not None :
                cursor.close()
            if connection is not None :
                connection.close()

        self.student_id_combo.setCurrentIndex(0)
        self.date_input.setDate(QDate.currentDate())  
        self.attendanceType_combo.setCurrentIndex(0)

    def back_to_previous_screen(self):
        if self.previous_screen == 'report':
            self.main_app.show_attendance_report()
        else:
            self.main_app.back_to_dashboard()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentEntry(None)
    window.show()
    sys.exit(app.exec_())
