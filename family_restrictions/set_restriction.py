from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QMessageBox, QScrollArea, QHBoxLayout, QSpacerItem, QSizePolicy
from database import get_connection
import sys
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtCore import Qt

class SetRestriction(QWidget):
    def __init__(self, parent_id, main_app):
        super().__init__()
        self.parent_id = parent_id
        self.main_app = main_app
        self.previous_screen = "add"
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Add Restriction')

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

        self.title_label = QLabel('Add Restriction')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont('Cambria', 27, QFont.Bold))

        self.student_label = QLabel('Select Student:')
        self.student_combo = QComboBox()
        self.student_combo.addItem('Select Student')
        self.load_students()

        self.restriction_type_label = QLabel('Restriction Type:')
        self.restriction_type_combo = QComboBox()
        self.restriction_type_combo.addItems(['Select Restriction Type', 'Balance', 'Product Type', 'Product Quantity'])
        self.restriction_type_combo.currentIndexChanged.connect(self.toggle_restriction_input)

        self.amount_label = QLabel('Restriction Balance:')
        self.amount_input = QLineEdit()
        self.amount_label.setVisible(False)
        self.amount_input.setVisible(False)

        self.product_label = QLabel('Select Product Type:')
        self.product_combo = QComboBox()
        self.product_combo.addItem('Select Product Type')
        self.product_label.setVisible(False)
        self.product_combo.setVisible(False)
        self.load_products()

        self.quantity_label = QLabel('Restriction Product Quantity:')
        self.quantity_input = QLineEdit()
        self.quantity_label.setVisible(False)
        self.quantity_input.setVisible(False)

        self.set_restriction_button = QPushButton('Add Restriction')
        self.set_restriction_button.setMinimumHeight(40)
        self.set_restriction_button.setStyleSheet("""
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
        self.set_restriction_button.clicked.connect(self.set_restriction)

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
        self.back_button.clicked.connect(self.back_to_self_rest)

        form_layout = QVBoxLayout()
        form_layout.addWidget(self.title_label)
        form_layout.addWidget(self.student_label)
        form_layout.addWidget(self.student_combo)
        form_layout.addWidget(self.restriction_type_label)
        form_layout.addWidget(self.restriction_type_combo)
        form_layout.addWidget(self.amount_label)
        form_layout.addWidget(self.amount_input)
        form_layout.addWidget(self.product_label)
        form_layout.addWidget(self.product_combo)
        form_layout.addWidget(self.quantity_label)
        form_layout.addWidget(self.quantity_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        button_layout.addWidget(self.set_restriction_button)

        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.layout.addLayout(form_layout)
        self.layout.addLayout(button_layout)
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.content_widget.setLayout(self.layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def load_students(self):
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

        for student in students:
            self.student_combo.addItem(f"{student[1]} {student[2]}", student[0])

    def load_products(self):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT idProduct, productName FROM Canteen_Products")
        products = cursor.fetchall()
        connection.close()

        for product in products:
            self.product_combo.addItem(f"{product[1]}", product[0])

    def toggle_restriction_input(self):
        restriction_type = self.restriction_type_combo.currentText()

        if restriction_type == 'Balance':
            self.amount_label.setVisible(True)
            self.amount_input.setVisible(True)
            self.product_label.setVisible(False)
            self.product_combo.setVisible(False)
            self.quantity_label.setVisible(False)
            self.quantity_input.setVisible(False)
        elif restriction_type == 'Product Type':
            self.amount_label.setVisible(False)
            self.amount_input.setVisible(False)
            self.product_label.setVisible(True)
            self.product_combo.setVisible(True)
            self.quantity_label.setVisible(False)
            self.quantity_input.setVisible(False)
        elif restriction_type == 'Product Quantity':
            self.amount_label.setVisible(False)
            self.amount_input.setVisible(False)
            self.product_label.setVisible(True)
            self.product_combo.setVisible(True)
            self.quantity_label.setVisible(True)
            self.quantity_input.setVisible(True)
        else:
            self.amount_label.setVisible(False)
            self.amount_input.setVisible(False)
            self.product_label.setVisible(False)
            self.product_combo.setVisible(False)
            self.quantity_label.setVisible(False)
            self.quantity_input.setVisible(False)

    def set_restriction(self):
        student_id = self.student_combo.currentData()
        restriction_type = self.restriction_type_combo.currentText()
        restriction_value = None

        if restriction_type == 'Balance':
            restriction_value = self.amount_input.text()
        elif restriction_type == 'Product Type':
            product_name = self.product_combo.currentText()
            restriction_value = f"{product_name}"
        elif restriction_type == 'Product Quantity':
            product_name = self.product_combo.currentText()
            restriction_value = f"{product_name} - {self.quantity_input.text()}"

        if not student_id or not restriction_type or not restriction_value:
            QMessageBox.warning(self, 'Error', 'Please fill all fields.')
            return

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("INSERT INTO Restrictions (restrictionType, restrictionValue, Parents_idParent, Students_idStudent) VALUES (%s, %s, %s, %s)",
                       (restriction_type, restriction_value, self.parent_id, student_id))

        connection.commit()
        connection.close()

        QMessageBox.information(self, 'Success', 'Restriction set successfully.')
        
        self.student_combo.setCurrentIndex(0)
        self.restriction_type_combo.setCurrentIndex(0)
        self.amount_input.clear()
        self.product_combo.setCurrentIndex(0)
        self.quantity_input.clear()

        self.amount_label.setVisible(False)
        self.amount_input.setVisible(False)
        self.product_label.setVisible(False)
        self.product_combo.setVisible(False)
        self.quantity_label.setVisible(False)
        self.quantity_input.setVisible(False)

    def back_to_self_rest(self):
        self.main_app.show_view_restriction()