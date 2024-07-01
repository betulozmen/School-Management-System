from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy, QDateEdit, QScrollArea, QListWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QDate
from database import get_connection

class AttendanceReports(QWidget):
    def __init__(self, parent_id, main_app):
        super().__init__()
        self.parent_id = parent_id
        self.main_app = main_app
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Attendance Report')

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

        self.label = QLabel('Absence Reports')
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont('Cambria', 27, QFont.Bold))
        self.label.setStyleSheet("color: #000087;")

        self.start_date_label = QLabel("Start Date:")
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDisplayFormat('yyyy-MM-dd')

        self.end_date_label = QLabel("End Date:")
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDisplayFormat('yyyy-MM-dd')
        self.end_date_edit.setDate(QDate.currentDate())

        one_year_ago = QDate.currentDate().addYears(-1)
        self.start_date_edit.setMinimumDate(one_year_ago)
        self.start_date_edit.setMaximumDate(QDate.currentDate())
        self.end_date_edit.setMinimumDate(one_year_ago)
        self.end_date_edit.setMaximumDate(QDate.currentDate())

        self.student_label = QLabel("Select Student:")
        self.student_combo = QComboBox()
        self.student_combo.addItem("All Students")

        self.list_widget = QListWidget()
        self.list_widget.setMinimumHeight(250) 
        self.list_widget.setStyleSheet("""
        QListWidget {
            font-size: 14px;
            font-weight: bold;
            color:  #000087; 
            margin-top: 20px;
        }
        QListWidget::item {
            color:  #000087; 
        }
    """)
        self.list_widget.setMinimumHeight(150)  
        self.list_widget.setMaximumHeight(200)

        self.generate_button = QPushButton("Report")
        self.generate_button.setMinimumHeight(45)
        self.generate_button.setStyleSheet("""
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
        self.generate_button.clicked.connect(self.generate_report)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.generate_button)

        button_widget = QWidget()
        button_widget.setLayout(button_layout)
        
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.start_date_label)
        self.layout.addWidget(self.start_date_edit)
        self.layout.addWidget(self.end_date_label)
        self.layout.addWidget(self.end_date_edit)
        self.layout.addWidget(self.student_label)
        self.layout.addWidget(self.student_combo)
        self.layout.addWidget(button_widget)
        self.layout.addWidget(self.list_widget)
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        self.load_students()


    def load_students(self):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("""
                SELECT S.idStudent, S.studentName, S.studentSurname
                FROM Students S
                JOIN Parents_has_Students PHS ON S.idStudent = PHS.Students_idStudent
                WHERE PHS.Parents_idParent = %s
            """, (self.parent_id,))
            students = cursor.fetchall()
            connection.close()

            self.student_combo.clear()
            self.student_combo.addItem("All Students", 0)
            for student in students:
                self.student_combo.addItem(f"{student[1]} {student[2]}", student[0])
        except Exception as e:
            QMessageBox.warning(self, 'Error', f"Error loading students: {e}")

    def generate_report(self):
        start_date = self.start_date_edit.date().toString('yyyy-MM-dd')
        end_date = self.end_date_edit.date().toString('yyyy-MM-dd')
        student_id = self.student_combo.currentData()
        if student_id is None:
            QMessageBox.warning(self, 'Error', 'Please select a student.')
            return

        try:
            self.list_widget.clear()

            connection = get_connection()
            cursor = connection.cursor()
            if student_id == 0:  # All students
                cursor.execute("""
                    SELECT S.studentName, S.studentSurname, A.attendanceDate, A.attendanceType
                    FROM Attendance A
                    JOIN Students S ON A.Students_idStudent = S.idStudent
                    JOIN Parents_has_Students PHS ON S.idStudent = PHS.Students_idStudent
                    WHERE PHS.Parents_idParent = %s AND A.attendanceDate BETWEEN %s AND %s
                    """, (self.parent_id, start_date, end_date))
                attendance_records = cursor.fetchall()
            else:  # Specific student
                cursor.execute("""
                    SELECT S.studentName, S.studentSurname, A.attendanceDate, A.attendanceType
                    FROM Attendance A
                    JOIN Students S ON A.Students_idStudent = S.idStudent
                    WHERE A.Students_idStudent = %s AND A.attendanceDate BETWEEN %s AND %s
                    """, (student_id, start_date, end_date))
                
                attendance_records = cursor.fetchall()      
            connection.close()

            for index, record in enumerate(attendance_records, start=1):
                self.list_widget.addItem(f"{index}. {record[0]} {record[1]} was absent from {record[3]} on {record[2].strftime('%Y-%m-%d')}.")

        except Exception as e:
            QMessageBox.warning(self, 'Error', f"Error loading attendance records: {e}")