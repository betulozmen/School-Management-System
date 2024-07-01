import sys
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy, QApplication, QScrollArea, QComboBox, QShortcut
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtCore import Qt
from database import get_connection
import re

class StudentAdd(QWidget):
    def __init__(self, main_app, classId):
        super().__init__()
        self.main_app = main_app
        self.classId = classId
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Student Registration')
        self.setGeometry(400, 100, 700, 600)
        self.setFixedSize(700, 600)  # Fixed window size

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

        self.title_label = QLabel('Student Registration')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont('Cambria', 27, QFont.Bold))

        self.studentName_label = QLabel('Student Name:', self)
        self.studentName_input = QLineEdit(self)

        self.studentSurname_label = QLabel('Student Surname:', self)
        self.studentSurname_input = QLineEdit(self)

        self.dob_label = QLabel('Date of Birth (YYYY-MM-DD):', self)
        self.dob_input = QLineEdit(self)

        self.idStudent_label = QLabel('Student No:', self)
        self.idStudent_input = QLineEdit(self)

        self.studentGender_label = QLabel('Gender:', self)
        self.roles = ('Kız', 'Erkek')
        self.gender_combo_box = QComboBox()
        self.gender_combo_box.addItems(self.roles)
        
        self.identificationNo_label = QLabel('Identification No:', self)
        self.identificationNo_input = QLineEdit(self)

        self.parentName_label = QLabel("Parent Name: ", self)
        self.parentName_input = QLineEdit(self)

        self.parentSurname_label = QLabel("Parent Surname: ", self)
        self.parentSurname_input = QLineEdit(self)

        self.phoneNumber_label = QLabel("Parent Phone Number: ", self)
        self.phoneNumber_input = QLineEdit(self)

        self.email_label = QLabel("Parent E-Mail: ", self)
        self.email_input = QLineEdit(self)

        self.passwd_label = QLabel("Parent Password: ", self)
        self.passwd_input = QLineEdit(self)

        self.submit_button = QPushButton('Submit', self)
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
        self.back_button.clicked.connect(self.back_to_class_detail)

        form_layout = QVBoxLayout()
        form_layout.addWidget(self.title_label)
        form_layout.addWidget(self.idStudent_label)
        form_layout.addWidget(self.idStudent_input)
        form_layout.addWidget(self.studentName_label)
        form_layout.addWidget(self.studentName_input)
        form_layout.addWidget(self.studentSurname_label)
        form_layout.addWidget(self.studentSurname_input)
        form_layout.addWidget(self.dob_label)
        form_layout.addWidget(self.dob_input)
        form_layout.addWidget(self.studentGender_label)
        form_layout.addWidget(self.gender_combo_box)
        form_layout.addWidget(self.identificationNo_label)
        form_layout.addWidget(self.identificationNo_input)
        form_layout.addWidget(self.parentName_label)
        form_layout.addWidget(self.parentName_input)
        form_layout.addWidget(self.parentSurname_label)
        form_layout.addWidget(self.parentSurname_input)
        form_layout.addWidget(self.phoneNumber_label)
        form_layout.addWidget(self.phoneNumber_input)
        form_layout.addWidget(self.email_label)
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(self.passwd_label)
        form_layout.addWidget(self.passwd_input)
        
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

    def validate_inputs(self):
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        phone_pattern = r'^\d{10,15}$'
        id_pattern = r'^\d{11}$'
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        name_pattern = r"^[a-zA-ZçÇğĞıİöÖşŞüÜ\s'-]+$"

        if not self.idStudent_input.text().isdigit():
            raise ValueError('Student ID must be numeric')

        if not re.match(email_pattern, self.email_input.text()):
            raise ValueError('Invalid email format')

        if not re.match(phone_pattern, self.phoneNumber_input.text()):
            raise ValueError('Phone number must be between 10 and 15 digits')

        if not re.match(id_pattern, self.identificationNo_input.text()):
            raise ValueError('Identification number must be 11 digits')

        if not re.match(date_pattern, self.dob_input.text()):
            raise ValueError('Date of birth must be in the format YYYY-MM-DD')

        if len(self.passwd_input.text()) < 8:
            raise ValueError('Password must be at least 8 characters long')
        
        if len(self.passwd_input.text()) > 15:
            raise ValueError('Password must be at most 15 characters long')
        
        if not re.match(name_pattern, self.studentName_input.text()):
            raise ValueError('Student name contains invalid characters')

        if not re.match(name_pattern, self.studentSurname_input.text()):
            raise ValueError('Student surname contains invalid characters')

        if not re.match(name_pattern, self.parentName_input.text()):
            raise ValueError('Parent name contains invalid characters')

        if not re.match(name_pattern, self.parentSurname_input.text()):
            raise ValueError('Parent surname contains invalid characters')
    
    def submit_form(self):
        
        try:
            idStudent = self.idStudent_input.text()
            studentName = self.studentName_input.text().title()
            studentSurname = self.studentSurname_input.text().capitalize()
            dob = self.dob_input.text()
            studentGender = self.gender_combo_box.currentText()
            identificationNo = self.identificationNo_input.text()
            parentName = self.parentName_input.text().title()
            parentSurname = self.parentSurname_input.text().capitalize()
            phoneNumber = self.phoneNumber_input.text()
            email = self.email_input.text()
            passwd = self.passwd_input.text()

            if idStudent and studentName and studentSurname and dob and studentGender and identificationNo and parentName and parentSurname and phoneNumber and email and passwd:
                self.validate_inputs()
                idParent = self.get_or_create_parent(parentName, parentSurname, phoneNumber, email, passwd)
                self.save_to_database(idStudent, studentName, studentSurname, dob, studentGender, identificationNo, self.classId)
                self.saveParentData(idParent, idStudent)
                QMessageBox.information(self, 'Success', 'Student registered successfully!')
                self.main_app.show_class_detail(self.classId) 
            else:
                QMessageBox.warning(self, 'Error', 'Please fill all the required fields.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f"An error occurred: {str(e)}")

    def get_or_create_parent(self, parentName, parentSurname, phoneNumber, email, passwd):
        try:
            connection = get_connection()
            cursor = connection.cursor()

            # Check if the parent already exists
            cursor.execute('''
            SELECT idParent FROM Parents WHERE parentName = %s AND parentSurname = %s AND phoneNumber = %s AND email = %s AND passwd = %s
            ''',(parentName, parentSurname, phoneNumber, email, passwd))

            classRow = cursor.fetchone()
        
            if classRow:
                idParent = classRow[0]
            else:
                # Create a new parent if it does not exist
                cursor.execute('''
                INSERT INTO Parents (parentName, parentSurname, phoneNumber, email, passwd) VALUES (%s, %s, %s, %s, %s)
                ''',(parentName, parentSurname, phoneNumber, email, passwd))
                connection.commit()
                idParent = cursor.lastrowid

            connection.close()
            return idParent
        except Exception as e:
            raise e

    def save_to_database(self, idStudent, studentName, studentSurname, dob, studentGender, identificationNo, idClass):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO Students (idStudent, studentName, studentSurname, birthOfDate, studentGender, identificationNo, Classes_idClass)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (idStudent, studentName, studentSurname, dob, studentGender, identificationNo, idClass))
            connection.commit()
            connection.close()
        except Exception as e:
            raise e

    def saveParentData(self, idParent, idStudent):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO Parents_has_Students (Parents_idParent, Students_idStudent)
            VALUES (%s, %s)
            """, (idParent, idStudent))
            connection.commit()
            connection.close()
        except Exception as e:
            raise e
        
    def back_to_class_detail(self):
        self.main_app.show_class_detail(self.classId)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentAdd(None)
    window.show()
    sys.exit(app.exec_())
