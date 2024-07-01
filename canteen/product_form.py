import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QScrollArea, QShortcut, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtCore import Qt
from database import get_connection
import re

class ProductRegistration(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Product Registration')

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

        self.title_label = QLabel('Product Registration')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont('Cambria', 27, QFont.Bold))

        self.product_name_label = QLabel('Product Name:', self)
        self.product_name_input = QLineEdit(self)

        self.product_price_label = QLabel('Product Price:', self)
        self.product_price_input = QLineEdit(self)

        self.product_stock_label = QLabel('Product Stock:', self)
        self.product_stock_input = QLineEdit(self)

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
        self.back_button.clicked.connect(self.back_to_product_list)

        form_layout = QVBoxLayout()
        form_layout.addWidget(self.title_label)
        form_layout.addWidget(self.product_name_label)
        form_layout.addWidget(self.product_name_input)
        form_layout.addWidget(self.product_price_label)
        form_layout.addWidget(self.product_price_input)
        form_layout.addWidget(self.product_stock_label)
        form_layout.addWidget(self.product_stock_input)
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
        name_pattern = r"^[a-zA-ZçÇğĞıİöÖşŞüÜ\s'-]+$"

        if not self.product_stock_input.text().isdigit():
            raise ValueError('Product stock must be numeric')

        if not self.product_price_input.text().isdigit():
            raise ValueError('Product price must be numeric')
        
        if not re.match(name_pattern, self.product_name_input.text()):
            raise ValueError('Product name contains invalid characters')
     
    def submit_form(self):
        
        product_name = self.product_name_input.text().title()
        product_price = self.product_price_input.text()
        product_stock = self.product_stock_input.text()

        if product_name and product_price and product_stock:
            self.validate_inputs()
            self.save_to_database(product_name, product_price, product_stock)
            QMessageBox.information(self, 'Success', 'Product registered successfully!')

            self.product_name_input.clear()
            self.product_price_input.clear()
            self.product_stock_input.clear()  
        else:
            QMessageBox.warning(self, 'Error', 'Please fill all the required fields.')

    def save_to_database(self, product_name, product_price, product_stock):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO Canteen_Products (productName, productPrice, productStock)
        VALUES (%s, %s, %s)
        """, (product_name, product_price, product_stock))
        connection.commit()
        connection.close()
    
    def back_to_product_list(self):
        self.main_app.show_product_list()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProductRegistration()
    window.show()
    sys.exit(app.exec_())
