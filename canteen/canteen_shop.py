from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy, QHeaderView
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from database import get_connection

class CanteenShop(QWidget):
    def __init__(self, parent_id):
        super().__init__()
        self.parent_id = parent_id
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Canteen Shopping Information')
        
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

        self.layout = QVBoxLayout()
        
        self.student_label = QLabel('Select Student:')
        self.student_label.setAlignment(Qt.AlignCenter)
        self.student_label.setFont(QFont('Cambria', 20, QFont.Bold))

        self.student_combo = QComboBox()
        self.load_students()

        self.view_report_button = QPushButton('View Shopping Information')
        self.view_report_button.clicked.connect(self.view_shop_info)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(['Product', 'Quantity', 'Amount Paid', 'Date', 'Student Name'])
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  

        self.layout.addWidget(self.student_label)
        self.layout.addWidget(self.student_combo)
        self.layout.addWidget(self.view_report_button)
        self.layout.addWidget(self.table_widget)

        self.setLayout(self.layout)

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

    def view_shop_info(self):
        student_id = self.student_combo.currentData()
        if student_id is None:
            QMessageBox.warning(self, 'Error', 'Please select a student.')
            return

        try:
            connection = get_connection()
            cursor = connection.cursor()
            if student_id == 0:  # All students
                cursor.execute("""
                    SELECT CP.productName, CS.shoppingAmount, CP.productPrice, CS.shoppingDATE, S.studentName, S.studentSurname
                    FROM Canteen_Shopping CS
                    JOIN Canteen_Shopping_has_Canteen_Products CSHCP ON CS.idShopping = CSHCP.Canteen_Shopping_idShopping
                    JOIN Canteen_Products CP ON CSHCP.Canteen_Products_idProduct = CP.idProduct
                    JOIN Students S ON CS.Students_idStudent = S.idStudent
                    JOIN Parents_has_Students PHS ON S.idStudent = PHS.Students_idStudent
                    WHERE PHS.Parents_idParent = %s
                """, (self.parent_id,))
                shop_records = cursor.fetchall()
            else:  # Specific student
                cursor.execute("""
                    SELECT CP.productName, CS.shoppingAmount, CP.productPrice, CS.shoppingDATE, S.studentName, S.studentSurname
                    FROM Canteen_Shopping CS
                    JOIN Students S ON CS.Students_idStudent = S.idStudent
                    JOIN Canteen_Shopping_has_Canteen_Products CSHCP ON CS.idShopping = CSHCP.Canteen_Shopping_idShopping
                    JOIN Canteen_Products CP ON CSHCP.Canteen_Products_idProduct = CP.idProduct
                    WHERE CS.Students_idStudent = %s
                """, (student_id,))
                shop_records = cursor.fetchall()
                
            connection.close()

            self.table_widget.setRowCount(0)  # Clear previous records

            if not shop_records:
                QMessageBox.information(self, 'No Records', 'No shop records found.')
                return

            self.table_widget.setRowCount(len(shop_records))
            for row_index, row_data in enumerate(shop_records):
                self.table_widget.setItem(row_index, 0, QTableWidgetItem(row_data[0]))
                self.table_widget.setItem(row_index, 1, QTableWidgetItem(str(row_data[1])))
                self.table_widget.setItem(row_index, 2, QTableWidgetItem(str(row_data[2])))
                self.table_widget.setItem(row_index, 3, QTableWidgetItem(row_data[3].strftime('%Y-%m-%d')))
                self.table_widget.setItem(row_index, 4, QTableWidgetItem(f"{row_data[4]} {row_data[5]}"))

        except Exception as e:
            QMessageBox.warning(self, 'Error', f"Error loading shop records: {e}")
