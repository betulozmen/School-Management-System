import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, QMessageBox, QLineEdit, QLabel, QSpacerItem, QSizePolicy, QScrollArea
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from database import get_connection

class ProductList(QWidget):
    def __init__(self, main_app=None, parent_id=None):
        super().__init__()
        self.main_app = main_app  
        self.parent_id = parent_id
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Product List')

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

        self.label = QLabel('Product List')
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont('Cambria', 27, QFont.Bold))
        self.label.setStyleSheet("color: #000087;")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Search by ID or Name')
        self.search_input.setMinimumHeight(30)
        self.search_input.textChanged.connect(self.search_product)
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: #000087;
                border: 1px solid #4169E1;
                padding: 5px;
                font-weight: bold;
            }
        """)

        self.list_widget = QListWidget()
        self.list_widget.setMinimumHeight(300)
        self.list_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.list_widget.setStyleSheet("""
            QListWidget {
                background-color: white;
                color: #000087;
                border: 1px solid #4169E1;
                padding: 5px;
                font-weight: bold;
                font-size: 13px;                       
            }
        """)

        self.add_button = QPushButton('Add Product')
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
        self.add_button.clicked.connect(self.add_product)

        self.delete_button = QPushButton('Delete Product')
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
        self.delete_button.clicked.connect(self.delete_product)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)

        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.search_input)
        self.layout.addWidget(self.list_widget)
        self.layout.addLayout(button_layout)
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        self.load_products()

    def load_products(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT idProduct, productName, productPrice FROM Canteen_Products")
        self.products = cursor.fetchall()
        connection.close()

        self.update_product_list(self.products)

    def update_product_list(self, products):
        self.list_widget.clear()
        for product in products:
            self.list_widget.addItem(f"{product[0]}: {product[1]} - ${product[2]}")

    def search_product(self):
        search_text = self.search_edit.text().lower()
        filtered_products = [product for product in self.products if search_text in str(product[0]).lower() or search_text in product[1].lower()]
        self.update_product_list(filtered_products)

    def add_product(self):
        self.main_app.show_product_registration()
            
    def delete_product(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            product_id = selected_item.text().split(':')[0]
            connection = get_connection()
            cursor = connection.cursor()
            try:
                cursor.execute("DELETE FROM Canteen_Products WHERE idProduct = %s", (product_id,))
                connection.commit()
                QMessageBox.information(self, 'Success', 'Product deleted successfully.')
                self.load_products()
            except Exception as e:
                QMessageBox.warning(self, 'Error', f"Error deleting product: {e}")
            finally:
                connection.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProductList()
    window.show()
    sys.exit(app.exec_())
