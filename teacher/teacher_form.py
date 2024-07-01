import sys
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QMessageBox, QApplication, QWidget, QLineEdit, QPushButton, QScrollArea, QShortcut, QHBoxLayout, QSpacerItem, QSizePolicy
from database import get_connection
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtCore import Qt
import re

class TeacherForm(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Teacher Registration")
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

        self.title_label = QLabel('Teacher Registration')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont('Cambria', 27, QFont.Bold))

        self.teacherName_label = QLabel("Teacher Name: ", self)
        self.teacherName_input = QLineEdit(self)
        
        self.teacherSurname_label = QLabel("Teacher Surname: ", self)
        self.teacherSurname_input = QLineEdit(self)

        self.teacherProfession_label = QLabel("Teacher Profession: ", self)
        self.teacherProfession_input = QLineEdit(self)

        self.teacherEmail_label = QLabel("Email: ", self)
        self.teacherEmail_input = QLineEdit(self)

        self.teacherPhoneNumber_label = QLabel("Phone Number: ", self)
        self.teacherPhoneNumber_input = QLineEdit(self)

        self.classLevel_label = QLabel('Class Level:', self)
        self.classLevel_input = QLineEdit(self)

        self.className_label = QLabel('Class Name:', self)
        self.className_input = QLineEdit(self)

        self.submit_button = QPushButton("Submit",self)
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
        self.back_button.clicked.connect(self.back_to_teacher_list)

        form_layout = QVBoxLayout()
        form_layout.addWidget(self.title_label)
        form_layout.addWidget(self.teacherName_label)
        form_layout.addWidget(self.teacherName_input)
        form_layout.addWidget(self.teacherSurname_label)
        form_layout.addWidget(self.teacherSurname_input)
        form_layout.addWidget(self.teacherProfession_label)
        form_layout.addWidget(self.teacherProfession_input)
        form_layout.addWidget(self.teacherEmail_label)
        form_layout.addWidget(self.teacherEmail_input)
        form_layout.addWidget(self.teacherPhoneNumber_label)
        form_layout.addWidget(self.teacherPhoneNumber_input)
        form_layout.addWidget(self.classLevel_label)
        form_layout.addWidget(self.classLevel_input)
        form_layout.addWidget(self.className_label)
        form_layout.addWidget(self.className_input)
        
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
        name_pattern = r"^[a-zA-ZçÇğĞıİöÖşŞüÜ\s'-]+$"
        class_level_pattern = r'^\d+$'
        class_name_pattern = r"^[A-Za-z]$"

        if not re.match(email_pattern, self.teacherEmail_input.text()):
            raise ValueError('Invalid email format')

        if not re.match(phone_pattern, self.teacherPhoneNumber_input.text()):
            raise ValueError('Phone number must be between 10 and 15 digits')

        if not re.match(name_pattern, self.teacherName_input.text()):
            raise ValueError('Teacher name contains invalid characters')

        if not re.match(name_pattern, self.teacherSurname_input.text()):
            raise ValueError('Teacher surname contains invalid characters')

        if not re.match(name_pattern, self.teacherProfession_input.text()):
            raise ValueError('Teacher profession contains invalid characters')
        
        if not re.match(class_level_pattern, self.classLevel_input.text()):
            raise ValueError('Class level must be numeric')
        
        if not re.match(class_name_pattern, self.className_input.text()):
            raise ValueError('Class name must be a single letter')
  
    def submit_form(self):
        try:
            teacherName = self.teacherName_input.text().title()
            teacherSurname = self.teacherSurname_input.text().capitalize()
            teacherProfession = self.teacherProfession_input.text().title()            
            email = self.teacherEmail_input.text()            
            phoneNumber = self.teacherPhoneNumber_input.text()
            classLevel = self.classLevel_input.text()
            className = self.className_input.text().upper()

            if teacherName and teacherSurname and teacherProfession and phoneNumber and email and classLevel and className:
                self.validate_inputs()
                idClass = self.get_or_create_class(classLevel, className)
                self.save_to_database(teacherName, teacherSurname, teacherProfession, email, phoneNumber, idClass)
                QMessageBox.information(self, 'Success', 'Teacher registered successfully!')
                self.main_app.show_teacher_list() 
            else:
                QMessageBox.warning(self ,'Error', 'Please fill all the required fields.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f"An error occurred: {str(e)}")

    def save_to_database(self, teacherName, teacherSurname, teacherProfession, email, phoneNumber, idClass):
        try:    
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("""
            INSERT INTO Teachers (teacherName, teacherSurname, teacherProfession, email, phoneNumber, Classes_idClass)
            VALUES (%s,%s,%s,%s,%s,%s)""",(teacherName,teacherSurname,teacherProfession,email,phoneNumber,idClass))
            connection.commit()
            connection.close()
        except Exception as e:
            raise e
        
    def get_or_create_class(self, classLevel, className):
        try:
            connection = get_connection()
            cursor = connection.cursor()

            # Check if the class already exists
            cursor.execute('''
            SELECT idClass FROM Classes WHERE classLevel = %s AND className = %s
            ''',(classLevel, className))

            classRow = cursor.fetchone()
        
            if classRow:
                idClass = classRow[0]
            else:
                # Create a new class if it does not exist
                cursor.execute('''
                INSERT INTO Classes (classLevel, className) VALUES (%s, %s)
                ''',(classLevel, className))
                connection.commit()
                idClass = cursor.lastrowid

            connection.close()
            return idClass
        except Exception as e:
            raise e
        
    def back_to_teacher_list(self):
        self.main_app.show_teacher_list()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TeacherForm(None)
    window.show()
    sys.exit(app.exec_())  