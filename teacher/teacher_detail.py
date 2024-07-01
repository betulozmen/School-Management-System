import sys
from PyQt5.QtWidgets import QApplication , QDialog, QVBoxLayout, QLabel, QMessageBox, QPushButton, QWidget, QScrollArea, QSpacerItem, QHBoxLayout, QSizePolicy, QTableWidget, QTableWidgetItem
from database import get_connection

class TeacherDetail(QDialog):
    def __init__(self, teacherId, main_app):
        super().__init__()
        self.teacherId = teacherId
        self.main_app = main_app
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Teacher Detail")

        self.layout = QVBoxLayout()

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
        self.back_button.clicked.connect(self.back_to_teacher_list)

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
        self.table.setHorizontalHeaderLabels(['Teacher', 'Information'])
        self.table.setColumnWidth(0, 308)
        self.table.setColumnWidth(1, 308)
        content_layout.addWidget(self.table)

        self.content_widget.setLayout(content_layout)
        self.layout.addWidget(scroll_area)
        self.setLayout(self.layout)
    
        self.load_teacher_details()

    def load_teacher_details(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Teachers WHERE idTeacher = %s ", (self.teacherId,))
        teacher = cursor.fetchone()
        connection.close()

        if teacher :
            attributes = ["ID", "Name", "Surname", "Profession", "Email", "Phone Number", "Class"]
            values = [teacher[0], teacher[1], teacher[2], teacher[3], teacher[4], teacher[5]]
            self.table.setRowCount(len(attributes))
            for i, (attr, val) in enumerate(zip(attributes, values)):
                self.table.setItem(i, 0, QTableWidgetItem(attr))
                self.table.setItem(i, 1, QTableWidgetItem(str(val)))
                self.table.setRowHeight(i, 60) 

            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Classes WHERE idClass = %s", (teacher[6],))
            classLN = cursor.fetchone()
            connection.close()
            if classLN:
                self.table.setItem(6, 0, QTableWidgetItem("Class"))
                self.table.setItem(6, 1, QTableWidgetItem(f"{classLN[1]}-{classLN[2]}"))
                self.table.setRowHeight(6, 61) 
            else:
                QMessageBox.warning(self, 'Error', 'Class information not found.')
        else :
            QMessageBox.warning(self,"Error", "Teacher not found.")
        
        self.adjustSize()
        self.resize(self.table.width() + 50, self.table.height() + 150)  # Adjust size to fit the content

    def back_to_teacher_list(self):
        self.main_app.show_teacher_list()

    def showEvent(self, event):
        super().showEvent(event)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TeacherDetail(None)  
    window.show()
    sys.exit(app.exec_())
