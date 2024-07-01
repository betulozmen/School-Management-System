import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QMessageBox, QScrollArea, QHeaderView
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from database import get_connection

class RestrictionList(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('View Restrictions')
        self.setGeometry(400, 100, 700, 600)
        self.setFixedSize(700, 600)
    
        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #000087;
                font-weight: bold;
            }
            QLineEdit {
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
        self.layout.setContentsMargins(20, 20, 45, 250)  

        self.search_label = QLabel('Search by Student Name or ID:')
        self.search_label.setAlignment(Qt.AlignCenter)
        self.search_label.setFont(QFont('Cambria', 20, QFont.Bold))

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Enter student name or ID')
        self.search_input.textChanged.connect(self.search_restrictions)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(['Student ID', 'Student Name', 'Restriction Type', 'Restriction Value', 'Parent Name'])
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Sütunları tabloya sığdırmak için
        self.table_widget.setMinimumHeight(400)
        self.table_widget.setStyleSheet("QTableWidget { margin-bottom: 70px; }")

        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_input)

        self.layout.addWidget(self.search_label)
        self.layout.addLayout(search_layout)
        
        self.layout.addWidget(self.table_widget)

        self.setLayout(self.layout)
        self.load_restrictions()

    def load_restrictions(self):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("""
                SELECT R.Students_idStudent, S.studentName, S.studentSurname, R.restrictionType, R.restrictionValue, P.parentName, P.parentSurname
                FROM Restrictions R
                JOIN Students S ON R.Students_idStudent = S.idStudent
                JOIN Parents P ON R.Parents_idParent = P.idParent
            """)
            self.restrictions = cursor.fetchall()
            connection.close()

            self.update_table(self.restrictions)

        except Exception as e:
            QMessageBox.warning(self, 'Error', f"Error loading restrictions: {e}")

    def update_table(self, restrictions):
        self.table_widget.setRowCount(0)  # Clear previous records
        self.table_widget.setRowCount(len(restrictions))
        for row_index, row_data in enumerate(restrictions):
            self.table_widget.setItem(row_index, 0, QTableWidgetItem(str(row_data[0])))
            self.table_widget.setItem(row_index, 1, QTableWidgetItem(f"{row_data[1]} {row_data[2]}"))
            self.table_widget.setItem(row_index, 2, QTableWidgetItem(row_data[3]))
            self.table_widget.setItem(row_index, 3, QTableWidgetItem(str(row_data[4])))
            self.table_widget.setItem(row_index, 4, QTableWidgetItem(f"{row_data[5]} {row_data[6]}"))

    def search_restrictions(self):
        search_text = self.search_input.text().lower()
        if search_text:
            filtered_restrictions = [restriction for restriction in self.restrictions if search_text in str(restriction[0]).lower() or search_text in restriction[1].lower()]
        else:
            filtered_restrictions = self.restrictions

        self.update_table(filtered_restrictions)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RestrictionList()
    window.show()
    sys.exit(app.exec_())
