from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QComboBox, QHeaderView, QSpacerItem, QSizePolicy
from database import get_connection
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class ViewRestrictions(QWidget):
    def __init__(self, parent_id, main_app):
        super().__init__()
        self.parent_id = parent_id
        self.main_app = main_app
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('View Restrictions')
        
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #000087;
                font-weight: bold;
            }
            QComboBox {
                background-color: white;
                color: #000087;
                border: 1px solid #4169E1;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #4169E1;
                color: white;
                border: none;
                padding: 5px 10px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 12px;
                margin: 4px 2px;
                border-radius: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3154A5;
            }
            QTableWidget {
                background-color: white;
                color: #000087;
                border: 1px solid #4169E1;
                font-weight: bold;
            }
            QHeaderView::section {
                background-color: #4169E1;
                color: white;
            }
        """)

        layout = QVBoxLayout()

        self.student_label = QLabel('Select Student:')
        self.student_label.setAlignment(Qt.AlignCenter)
        self.student_label.setFont(QFont('Cambria', 20, QFont.Bold))

        self.student_combo = QComboBox()
        self.load_students()

        self.view_restrictions = QPushButton('View Restrictions')
        self.view_restrictions.setMinimumHeight(37)
        self.view_restrictions.setStyleSheet("""
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
        self.view_restrictions.clicked.connect(self.load_restrictions)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(['Student ID', 'Student Name', 'Restriction Type', 'Restriction Value', ''])
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 

        self.add_button = QPushButton('Add Restriction')
        self.add_button.setMinimumHeight(37)
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
        self.add_button.clicked.connect(self.add_restriction)

        layout.addWidget(self.student_label)
        layout.addWidget(self.student_combo)
        layout.addWidget(self.view_restrictions)
        layout.addWidget(self.table_widget)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)

        layout.addLayout(button_layout) 

        self.setLayout(layout)

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

    def load_restrictions(self):
        try:
            student_id = self.student_combo.currentData()
            connection = get_connection()
            cursor = connection.cursor()
            if student_id == 0:  # All students
                cursor.execute("""
                SELECT Students.idStudent, Students.studentName, Students.studentSurname, Restrictions.restrictionType, Restrictions.restrictionValue, Restrictions.idRestriction
                FROM Restrictions 
                JOIN Students ON Restrictions.Students_idStudent = Students.idStudent 
                WHERE Parents_idParent = %s
                """, (self.parent_id,))
            else:
                cursor.execute("""
                SELECT Students.idStudent, Students.studentName, Students.studentSurname, Restrictions.restrictionType, Restrictions.restrictionValue, Restrictions.idRestriction
                FROM Restrictions 
                JOIN Students ON Restrictions.Students_idStudent = Students.idStudent 
                WHERE Parents_idParent = %s AND Students_idStudent = %s
            """, (self.parent_id, student_id))
        
            restrictions = cursor.fetchall()
            connection.close()

            self.table_widget.setRowCount(0)  # Clear previous records

            if not restrictions:
                QMessageBox.information(self, 'No Records', 'No restrictions records found.')
                return
            
            self.update_table(restrictions)
            
        except Exception as e:
            QMessageBox.warning(self, 'Error', f"Error loading restrictions: {e}")

    def update_table(self, restrictions):
        self.table_widget.setRowCount(0)  # Clear previous records
        
        for row_index, row_data in enumerate(restrictions):
            self.table_widget.insertRow(row_index)
            self.table_widget.setItem(row_index, 0, QTableWidgetItem(str(row_data[0])))
            self.table_widget.setItem(row_index, 1, QTableWidgetItem(f"{row_data[1]} {row_data[2]}"))
            self.table_widget.setItem(row_index, 2, QTableWidgetItem(str(row_data[3])))
            self.table_widget.setItem(row_index, 3, QTableWidgetItem(str(row_data[4])))

            delete_button = QPushButton('Delete')
            delete_button.setMinimumHeight(25)
            delete_button.clicked.connect(lambda ch, restriction_id=row_data[5]: self.delete_restriction(restriction_id))
            self.table_widget.setCellWidget(row_index, 4, delete_button)
       
    def delete_restriction(self, restriction_id):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("""
                DELETE FROM Restrictions
                WHERE Restrictions.idRestriction = %s 
            """, (restriction_id,))
            connection.commit()
            connection.close()
            self.load_restrictions()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f"Error deleting restriction: {e}")

    def add_restriction(self):
        self.main_app.show_set_restriction(self.parent_id)
