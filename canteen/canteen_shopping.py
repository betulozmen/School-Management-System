from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy, QHeaderView, QLineEdit, QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from database import get_connection
import sys

class CanteenShopping(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app  
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

        self.label = QLabel('Sales List')
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont('Cambria', 27, QFont.Bold))
        self.label.setStyleSheet("color: #000087;")

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels(['Product', 'Quantity', 'Amount Paid', 'Date', 'Student Name', 'Student ID'])
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.table_widget)

        self.setLayout(self.layout)

        self.load_all_shop_info()

    def load_all_shop_info(self):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("""
            SELECT CP.productName, CS.shoppingAmount, CP.productPrice, CS.shoppingDATE, S.studentName, S.studentSurname, S.idStudent
            FROM Canteen_Shopping CS
            JOIN Canteen_Shopping_has_Canteen_Products CSHCP ON CS.idShopping = CSHCP.Canteen_Shopping_idShopping
            JOIN Canteen_Products CP ON CSHCP.Canteen_Products_idProduct = CP.idProduct
            JOIN Students S ON CS.Students_idStudent = S.idStudent
            """)
            shop_records = cursor.fetchall()
            
            connection.close()

            if not shop_records:
                QMessageBox.information(self, 'No Records', 'No sales records found.')
                return

            self.table_widget.setRowCount(len(shop_records))

            for row_index, row_data in enumerate(shop_records):
                self.table_widget.setItem(row_index, 0, QTableWidgetItem(row_data[0]))
                self.table_widget.setItem(row_index, 1, QTableWidgetItem(str(row_data[1])))
                self.table_widget.setItem(row_index, 2, QTableWidgetItem(str(row_data[2])))
                self.table_widget.setItem(row_index, 3, QTableWidgetItem(row_data[3].strftime('%Y-%m-%d')))
                self.table_widget.setItem(row_index, 4, QTableWidgetItem(f"{row_data[4]} {row_data[5]}"))
                self.table_widget.setItem(row_index, 5, QTableWidgetItem(str(row_data[6])))

        except Exception as e:
            QMessageBox.warning(self, 'Error', f"Error loading sales records: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CanteenShopping(None)
    window.show()
    sys.exit(app.exec_())