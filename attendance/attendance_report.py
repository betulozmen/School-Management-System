import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QDateEdit, QPushButton, QMessageBox, QComboBox, QWidget, QScrollArea, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import QDate
from database import get_connection
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class AttendanceReport(QWidget):
    def __init__(self, main_app, previous_screen=None):
        super().__init__()
        self.main_app = main_app
        self.previous_screen = previous_screen
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Attendance Report")
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

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(['ID', 'Name', 'Surname', 'Date', 'Type'])
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.setColumnWidth(0, 125)
        self.table_widget.setColumnWidth(1, 125)
        self.table_widget.setColumnWidth(2, 125)
        self.table_widget.setColumnWidth(3, 125)
        self.table_widget.setColumnWidth(4, 125)

        self.generate_button = QPushButton("Report")
        self.generate_button.setMinimumHeight(40)
        self.generate_button.setFixedHeight(50)  
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

        self.delete_button = QPushButton('Delete Absence')
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
        self.delete_button.clicked.connect(self.delete_absence)

        self.add_button = QPushButton('Add Absence')
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
        self.add_button.clicked.connect(self.add_absence)

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
        button_layout.addWidget(self.generate_button)

        bottom_button_layout = QHBoxLayout()
        bottom_button_layout.addWidget(self.delete_button)
        bottom_button_layout.addWidget(self.add_button)
        bottom_button_layout.addWidget(self.back_button)
        
        button_widget = QWidget()
        button_widget.setLayout(button_layout)

        bottom_button_widget = QWidget()
        bottom_button_widget.setLayout(bottom_button_layout)

        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.start_date_label)
        self.layout.addWidget(self.start_date_edit)
        self.layout.addWidget(self.end_date_label)
        self.layout.addWidget(self.end_date_edit)
        self.layout.addWidget(self.student_label)
        self.layout.addWidget(self.student_combo)
        self.layout.addWidget(button_widget)
        self.layout.addWidget(self.table_widget)
        self.layout.addWidget(bottom_button_widget)
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        self.load_students()

    def load_students(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT idStudent, studentName, studentSurname FROM Students")
        students = cursor.fetchall()
        connection.close()

        for student in students:
            self.student_combo.addItem(f"{student[1]} {student[2]}", student[0])

    def generate_report(self):
        start_date = self.start_date_edit.date().toString('yyyy-MM-dd')
        end_date = self.end_date_edit.date().toString('yyyy-MM-dd')
        student_text = self.student_combo.currentText()
        student_id = self.student_combo.currentData()

        connection = get_connection()
        cursor = connection.cursor()

        if student_text == "All Students":                
            cursor.execute("""
            SELECT Students.idStudent, Students.studentName, Students.studentSurname, Attendance.attendanceDate, Attendance.attendanceType
            FROM Students 
            JOIN Attendance ON Students.idStudent = Attendance.Students_idStudent 
            WHERE DATE(Attendance.attendanceDate) BETWEEN %s AND %s
            """, (start_date, end_date))
        else:
            cursor.execute("""
            SELECT Students.idStudent, Students.studentName, Students.studentSurname, Attendance.attendanceDate, Attendance.attendanceType 
            FROM Students 
            JOIN Attendance ON Students.idStudent = Attendance.Students_idStudent 
            WHERE Students.idStudent = %s AND DATE(Attendance.attendanceDate) BETWEEN %s AND %s
            """, (student_id, start_date, end_date))

        attendance_records = cursor.fetchall()
        connection.close()

        self.table_widget.setRowCount(0)

        if attendance_records:
            self.table_widget.setRowCount(len(attendance_records))
            for row, record in enumerate(attendance_records):
                self.table_widget.setItem(row, 0, QTableWidgetItem(str(record[0])))
                self.table_widget.setItem(row, 1, QTableWidgetItem(record[1]))
                self.table_widget.setItem(row, 2, QTableWidgetItem(record[2]))
                self.table_widget.setItem(row, 3, QTableWidgetItem(record[3].strftime('%Y-%m-%d')))
                self.table_widget.setItem(row, 4, QTableWidgetItem(record[4]))
        else:
            QMessageBox.information(self, "No Records", "No attendance records found for the selected date range.")

    def delete_absence(self):
        selected_item = self.table_widget.currentRow()
        if selected_item != -1:
            student_id = self.table_widget.item(selected_item, 0).text()
            attendance_date = self.table_widget.item(selected_item, 3).text()
            attendance_type = self.table_widget.item(selected_item, 4).text()

            connection = get_connection()
            cursor = connection.cursor()
            try:
                cursor.execute("DELETE FROM Attendance WHERE Students_idStudent = %s AND attendanceDate = %s AND attendanceType = %s", (student_id, attendance_date, attendance_type))
                connection.commit()
                QMessageBox.information(self, 'Success', 'Attendance record deleted successfully.')
                self.generate_report()
            except Exception as e:
                QMessageBox.warning(self, 'Error', f"Error deleting attendance record: {e}")
            finally:
                connection.close()
        else:
            QMessageBox.warning(self, 'Error', 'No attendance record selected.')

    
    def add_absence(self):
        self.main_app.show_attendance_entry(previous_screen='report')

    def back_to_admin_dashboard(self):
        self.main_app.show_admin_dashboard()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AttendanceReport(None)
    window.show()
    sys.exit(app.exec_())
