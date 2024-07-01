from database import get_connection
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QMessageBox, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QSizePolicy, QSpacerItem, QScrollArea, QWidget

class StudentDetail(QDialog):
    def __init__(self, student_id, main_app, previous_screen=None):
        super().__init__()
        self.student_id = student_id
        self.main_app = main_app
        self.previous_screen = previous_screen
        print(f"Initializing StudentDetail for student ID: {self.student_id}")  # Debug print
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Student Detail')

        self.layout = QVBoxLayout()
        
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
        self.back_button.clicked.connect(self.back_to_previous_screen)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        self.content_widget = QWidget()
        scroll_area.setWidget(self.content_widget)

        back_layout = QHBoxLayout()
        back_layout.addWidget(self.back_button)
        back_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        content_layout = QVBoxLayout(self.content_widget)
        content_layout.addLayout(back_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Student', 'Information'])
        self.table.setColumnWidth(0, 305)
        self.table.setColumnWidth(1, 305)
        content_layout.addWidget(self.table)

        button_layout = QHBoxLayout()
        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        button_layout.addWidget(self.delete_button)
        
        content_layout.addLayout(button_layout)
        self.content_widget.setLayout(content_layout)

        self.layout.addWidget(scroll_area)
        self.setLayout(self.layout)

        self.load_student_detail()


    def load_student_detail(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Students WHERE idStudent = %s", (self.student_id,))
        student = cursor.fetchone()
        connection.close()

        if student:
            attributes = ["ID", "Name", "Surname", "Date of Birth", "Gender", "Identification No", "Class"]
            values = [student[0], student[1], student[2], student[3], student[4], student[5]]

            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Classes WHERE idClass = %s", (student[6],))
            classLN = cursor.fetchone()
            connection.close()

            if classLN:
                values.append(f"{classLN[1]}-{classLN[2]}")

                connection = get_connection()
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM Parents_has_Students WHERE Students_idStudent = %s", (student[0],))
                idParent = cursor.fetchone()
                connection.close()

                if idParent:
                    connection = get_connection()
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM Parents WHERE idParent = %s", (idParent[0],))
                    parent = cursor.fetchone()
                    connection.close()

                    if parent:
                        attributes.extend(["Parent Name", "Parent Surname", "Parent Phone Number", "Parent E-Mail"])
                        values.extend([parent[1], parent[2], parent[3], parent[4]])
                    else:
                        QMessageBox.warning(self, 'Error', 'Parent information not found.')
                else:
                    QMessageBox.warning(self, 'Error', 'Parent ID not found.')
            else:
                QMessageBox.warning(self, 'Error', 'Class information not found.')

            self.table.setRowCount(len(attributes))
            for i, (attr, val) in enumerate(zip(attributes, values)):
                self.table.setItem(i, 0, QTableWidgetItem(attr))
                self.table.setItem(i, 1, QTableWidgetItem(str(val)))
                self.table.setRowHeight(i, 32) 
        else:
            QMessageBox.warning(self, 'Error', 'Student not found.')

        self.adjustSize()
        self.resize(self.table.width() + 50, self.table.height() + 150)  # Adjust size to fit the content

    def delete_student(self):
        connection = get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM Parents_has_Students WHERE Students_idStudent = %s", (self.student_id,))
            cursor.execute("DELETE FROM Attendance WHERE Students_idStudent = %s", (self.student_id,))
            cursor.execute("DELETE FROM StudentBalances WHERE Students_idStudent = %s", (self.student_id,))
            cursor.execute("DELETE FROM Restrictions WHERE Students_idStudent = %s", (self.student_id,))
            cursor.execute("DELETE FROM Canteen_Payment WHERE Students_idStudent = %s", (self.student_id,))
            cursor.execute("DELETE FROM Canteen_Shopping WHERE Students_idStudent = %s", (self.student_id,))
            cursor.execute("DELETE FROM Students WHERE idStudent = %s", (self.student_id,))
            connection.commit()
            QMessageBox.information(self, 'Success', 'Student deleted successfully.')
            self.back_to_previous_screen()  # Go back to the previous screen after deletion
        except Exception as e:
            QMessageBox.warning(self, 'Error', f"Error deleting student: {e}")
        finally:
            connection.close()

    def back_to_previous_screen(self):
        if self.previous_screen == 'class_detail':
            self.main_app.show_class_detail(self.main_app.current_class_id)
        else:
            self.main_app.show_student_list()

    def showEvent(self, event):
        super().showEvent(event)
        print(f"Student Detail window shown for student ID: {self.student_id}")  # Debug print

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentDetail(354, None)  
    window.show()
    sys.exit(app.exec_())
