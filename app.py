import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMessageBox, QLineEdit, QWidget, QVBoxLayout, QLabel, QPushButton, QDialog, QComboBox, QSpacerItem, QSizePolicy, QHBoxLayout, QGroupBox, QVBoxLayout, QScrollArea
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt 
from settings import ADMIN_CREDENTIALS
from settings import CANTEENMANAGER_CREDENTIALS
from database import get_connection, create_tables
from student.student_list import StudentList
from student.student_detail import StudentDetail
from student.student_form import StudentRegistration
from classes.class_student_add import StudentAdd
from teacher.teacher_list import TeacherList
from teacher.teacher_form import TeacherForm
from teacher.teacher_detail import TeacherDetail
from classes.class_list import ClassList
from classes.class_detail import ClassDetail
from canteen.product_list import ProductList
from canteen.product_form import ProductRegistration
from family_restrictions.restriction_list import RestrictionList
from family_restrictions.self_rest import ViewRestrictions
from attendance.attendance_report import AttendanceReport
from attendance.student_entry import StudentEntry
from family_restrictions.set_restriction import SetRestriction
from attendance.attendance_family import AttendanceReports
from canteen.canteen_shop import CanteenShop
from canteen.canteen_shopping import CanteenShopping

class RoleSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('School Management System')
        self.setGeometry(400, 100, 700, 600)
        self.setFixedSize(700, 600) 

        self.setStyleSheet("""
            QDialog {
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }
        """)

        layout = QVBoxLayout()

        self.label1 = QLabel('School Management System')
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setFont(QFont('Times New Roman', 45, QFont.Bold))
        self.label1.setWordWrap(True)
        self.label1.setStyleSheet("""
            color: #000080;
            font-weight: bold;
        """)

        self.label = QLabel('Select Role')
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont('Cambria', 27, QFont.Bold))
        self.label.setStyleSheet("color: #000087;")

        self.roles = ('Admin', 'Parent', 'Canteen Manager')
        self.combo_box = QComboBox()
        self.combo_box.addItems(self.roles)
        self.combo_box.setMinimumHeight(40)
        self.combo_box.setStyleSheet("""
            QComboBox {
                background-color: white;
                color: #000087;
                border: 1px solid #4169E1;
                padding: 5px;
                font-weight: bold;
            }
            QComboBox::item {
                text-align: center;
            }
            QComboBox QAbstractItemView {
                background-color: solid gray;
                color: #000087;
                selection-background-color: #4169E1;
                selection-color: white;
                text-align: center;
                font-weight: bold;
            }
        """)

        self.ok_button = QPushButton('OK')
        self.ok_button.setMinimumHeight(40)
        self.ok_button.setStyleSheet("""
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
        self.ok_button.clicked.connect(self.accept)
        
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(self.label1)
        spacer = QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout.addSpacerItem(spacer)
        layout.addWidget(self.label)
        layout.addWidget(self.combo_box)
        layout.addWidget(self.ok_button)
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    def get_role(self):
        return self.combo_box.currentText()

class LoginDialogBase(QDialog):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setGeometry(400, 100, 700, 600)
        self.setFixedSize(700, 600) 
        self.back_button_pressed = False  

        self.setStyleSheet("""
            QDialog {
                background-repeat: no-repeat;
                background-position: center;
                background-size: cover;
            }
        """)

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
        self.back_button.clicked.connect(self.on_back_button_clicked)

        back_layout = QHBoxLayout()
        back_layout.addWidget(self.back_button)
        back_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.layout = QVBoxLayout()
        self.layout.addLayout(back_layout)
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def on_back_button_clicked(self):
        self.back_button_pressed = True
        self.reject()
    
    def closeEvent(self, event):
        msg_box = QMessageBox()
        msg_box.setWindowTitle('Exit Application')
        msg_box.setText("Are you sure you want to exit?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)

        msg_box.setStyleSheet("")

        reply = msg_box.exec_()

        if reply == QMessageBox.Yes:
            event.accept()
            sys.exit()
        else:
            event.ignore()

class AdminLoginDialog(LoginDialogBase):
    def __init__(self, parent=None):
        super().__init__('Admin Login', parent)
        
        self.label = QLabel('Admin Login')
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont('Cambria', 27, QFont.Bold))
        self.label.setStyleSheet("color: #000087;")

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('Username')
        self.username_input.setMinimumHeight(40)
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: #000087;
                border: 1px solid #4169E1;
                padding: 5px;
                font-weight: bold;
            }
        """)
        self.username_input.returnPressed.connect(self.login)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(40)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: #000087;
                border: 1px solid #4169E1;
                padding: 5px;
                font-weight: bold;
            }
        """)
        self.password_input.returnPressed.connect(self.login)

        self.login_button = QPushButton('Login')
        self.login_button.setMinimumHeight(40)
        self.login_button.setStyleSheet("""
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
        self.login_button.clicked.connect(self.accept)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(self.layout)

    def get_credentials(self):
        return self.username_input.text(), self.password_input.text()
    def login(self):
        self.accept()

class ParentLoginDialog(LoginDialogBase):
    def __init__(self, parent=None):
        super().__init__('Parent Login', parent)

        self.label = QLabel('Parent Login')
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont('Cambria', 27, QFont.Bold))
        self.label.setStyleSheet("color: #000087;")

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('Email')
        self.username_input.setMinimumHeight(40)
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: #000087;
                border: 1px solid #4169E1;
                padding: 5px;
                font-weight: bold;
            }
        """)
        self.username_input.returnPressed.connect(self.login)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(40)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: #000087;
                border: 1px solid #4169E1;
                padding: 5px;
                font-weight: bold;
            }
        """)
        self.password_input.returnPressed.connect(self.login)

        self.login_button = QPushButton('Login')
        self.login_button.setMinimumHeight(40)
        self.login_button.setStyleSheet("""
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
        self.login_button.clicked.connect(self.accept)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(self.layout)

    def get_credentials(self):
        return self.username_input.text(), self.password_input.text()
    def login(self):
        self.accept()

class CanteenManagerLoginDialog(LoginDialogBase):
    def __init__(self, parent=None):
        super().__init__('Canteen Manager Login', parent)

        self.label = QLabel('Canteen Manager Login')
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont('Cambria', 27, QFont.Bold))
        self.label.setStyleSheet("color: #000087;")

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('Username')
        self.username_input.setMinimumHeight(40)
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: #000087;
                border: 1px solid #4169E1;
                padding: 5px;
                font-weight: bold;
            }
        """)
        self.username_input.returnPressed.connect(self.login)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(40)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: #000087;
                border: 1px solid #4169E1;
                padding: 5px;
                font-weight: bold;
            }
        """)
        self.password_input.returnPressed.connect(self.login)

        self.login_button = QPushButton('Login')
        self.login_button.setMinimumHeight(40)
        self.login_button.setStyleSheet("""
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
        self.login_button.clicked.connect(self.login)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)
        self.layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(self.layout)

    def get_credentials(self):
        return self.username_input.text(), self.password_input.text()

    def login(self):
        self.accept()


class SchoolManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.user_role = None
        self.parent_id = None
        self.current_class_id = None  

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('School Management System')
        self.setGeometry(400, 100, 700, 600)
        self.setFixedSize(700, 600)  # Fixed window size

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout(self.central_widget)
        scroll_area.setWidget(self.central_widget)

        self.setCentralWidget(scroll_area)

        self.statusBar().showMessage('   ')

        menubar = self.menuBar()
        self.setCentralWidget(None)

        self.student_menu = menubar.addMenu('Students')
        self.teacher_menu = menubar.addMenu('Teachers')
        self.class_menu = menubar.addMenu('Classes')
        self.canteen_menu = menubar.addMenu('Canteen')
        self.restriction_menu = menubar.addMenu('Restrictions')
        self.attendance_menu = menubar.addMenu('Attendance')
        self.login_menu = menubar.addMenu('Login')

        # Exit action
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        menubar.addAction(exit_action)

        self.show_login_dialog()

    def show_login_dialog(self):
        while True:
            dialog = RoleSelectionDialog(self)
            if dialog.exec_() == QDialog.Accepted:
                role = dialog.get_role()
                if role:
                    while True:
                        if role == 'Admin':
                            self.user_role = 'Admin'
                            if self.admin_login():
                                self.init_admin_menu()
                                self.show_admin_dashboard()
                                return
                            elif self.admin_dialog.back_button_pressed:
                                break  # Back to role selection
                            else:
                                QMessageBox.warning(self, 'Login Failed', 'Invalid admin credentials.')
                        elif role == 'Parent':
                            self.user_role = 'Parent'
                            if self.parent_login():
                                self.init_parent_menu()
                                self.show_parent_dashboard()
                                return
                            elif self.parent_dialog.back_button_pressed:
                                break  # Back to role selection
                            else:
                                QMessageBox.warning(self, 'Login Failed', 'Invalid parent credentials.')
                        elif role == 'Canteen Manager':
                            self.user_role = 'Canteen Manager'
                            if self.canteen_manager_login():
                                self.init_canteen_manager_menu()
                                self.show_canteen_manager_dashboard()
                                return
                            elif self.canteen_dialog.back_button_pressed:
                                break  # Back to role selection
                            else:
                                QMessageBox.warning(self, 'Login Failed', 'Invalid canteen manager credentials.')
            else:
                sys.exit()  # Kullanıcı rol seçim ekranını kapattıysa uygulamayı kapat

    def parent_login(self):
        self.parent_dialog = ParentLoginDialog(self)
        if self.parent_dialog.exec_() == QDialog.Accepted:
            email, password = self.parent_dialog.get_credentials()
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM parents WHERE email=%s AND passwd=%s", (email, password))
            parent = cursor.fetchone()
            if parent:
                self.parent_id = parent[0]  # Assume parent ID is the first column
                return True
        return False


    def admin_login(self):
        self.admin_dialog = AdminLoginDialog(self)
        if self.admin_dialog.exec_() == QDialog.Accepted:
            username, password = self.admin_dialog.get_credentials()
            if username == ADMIN_CREDENTIALS['username'] and password == ADMIN_CREDENTIALS['password']:
                return True
        return False

    def canteen_manager_login(self):
        self.canteen_dialog = CanteenManagerLoginDialog(self)
        if self.canteen_dialog.exec_() == QDialog.Accepted:
            username, password = self.canteen_dialog.get_credentials()
            if username == CANTEENMANAGER_CREDENTIALS['username'] and password == CANTEENMANAGER_CREDENTIALS['password']:
                return True
        return False


    def init_admin_menu(self):
        self.student_menu.clear()
        self.teacher_menu.clear()
        self.class_menu.clear()
        self.canteen_menu.clear()
        self.restriction_menu.clear()
        self.attendance_menu.clear()

        # Student actions
        student_list_action = QAction('Student List', self)
        student_list_action.triggered.connect(self.show_student_list)
        self.student_menu.addAction(student_list_action)

        # Teacher actions
        teacher_list_action = QAction('Teacher List', self)
        teacher_list_action.triggered.connect(self.show_teacher_list)
        self.teacher_menu.addAction(teacher_list_action)

        # Class actions
        class_list_action = QAction('Class List', self)
        class_list_action.triggered.connect(self.show_class_list)
        self.class_menu.addAction(class_list_action)
        

        # Restriction actions
        restriction_list_action = QAction('Restriction List', self)
        restriction_list_action.triggered.connect(self.show_restriction_list)
        self.restriction_menu.addAction(restriction_list_action)

        # Attendance actions
        attendance_report_action = QAction('Attendance Report', self)
        attendance_report_action.triggered.connect(self.show_attendance_report)
        self.attendance_menu.addAction(attendance_report_action)

        attendance_add_action = QAction('Add Attendance', self)
        attendance_add_action.triggered.connect(self.show_attendance_entry)
        self.attendance_menu.addAction(attendance_add_action)

    def init_parent_menu(self):
        self.student_menu.clear()
        self.teacher_menu.clear()
        self.class_menu.clear()
        self.canteen_menu.clear()
        self.restriction_menu.clear()
        self.attendance_menu.clear()

        # Student actions
        attendance_report_action = QAction('Attendance Report', self)
        attendance_report_action.triggered.connect(self.show_attendance_reports)
        self.attendance_menu.addAction(attendance_report_action)

        canteen_info_action = QAction('Canteen Shopping Information', self)
        canteen_info_action.triggered.connect(self.show_canteen_shop)
        self.canteen_menu.addAction(canteen_info_action)

        restriction_info_action = QAction('View Restrictions', self)
        restriction_info_action.triggered.connect(self.show_view_restriction)
        self.restriction_menu.addAction(restriction_info_action)

    def init_canteen_manager_menu(self):
        self.student_menu.clear()
        self.teacher_menu.clear()
        self.class_menu.clear()
        self.canteen_menu.clear()
        self.restriction_menu.clear()
        self.attendance_menu.clear()

        # Canteen actions
        product_list_action = QAction('Product List', self)
        product_list_action.triggered.connect(self.show_product_list)
        self.canteen_menu.addAction(product_list_action)

        restriction_list_action = QAction('Restriction List', self)
        restriction_list_action.triggered.connect(self.show_restriction_list)
        self.restriction_menu.addAction(restriction_list_action)

        canteen_shopping_action = QAction('Canteen Shopping Information', self)
        canteen_shopping_action.triggered.connect(self.show_canteen_shopping)
        self.canteen_menu.addAction(canteen_shopping_action)

    def show_student_list(self):
        self.setCentralWidget(StudentList(self))
    
    def show_student_registration(self):
        self.student_registration = StudentRegistration(self)
        self.setCentralWidget(self.student_registration)

    def show_student_add(self, class_id):
        self.setCentralWidget(StudentAdd(self, class_id))

    def show_teacher_list(self):
        self.setCentralWidget(TeacherList(self))
    
    def show_teacher_detail(self, teacher_id):
        self.setCentralWidget(TeacherDetail(teacher_id, self))
    
    def show_teacher_registration(self):
        self.teacher_registration = TeacherForm(self)
        self.setCentralWidget(self.teacher_registration)
    
    def show_product_registration(self):
        self.product_registration = ProductRegistration(self)
        self.setCentralWidget(self.product_registration)

    def show_attendance_entry(self, previous_screen=None):
        self.setCentralWidget((StudentEntry(self, previous_screen=previous_screen)))

    def show_canteen_shop(self):
        self.setCentralWidget(self.create_module_widget(CanteenShop, parent_id=self.parent_id))

    def show_class_list(self):
        self.setCentralWidget(ClassList(self))
    
    def show_class_detail(self, class_id):
        self.current_class_id = class_id
        self.setCentralWidget(ClassDetail(class_id, self))

    def show_student_detail(self, student_id, previous_screen=None):
        self.setCentralWidget(StudentDetail(student_id, self, previous_screen=previous_screen))

    def show_product_list(self):
        self.setCentralWidget(self.create_module_widget(ProductList, main_app=self))

    def show_canteen_shopping(self):
        self.setCentralWidget(self.create_module_widget(CanteenShopping, main_app=self))

    def show_restriction_list(self):
        self.setCentralWidget(self.create_module_widget(RestrictionList))

    def show_set_restriction(self, parent_id):
        self.setCentralWidget(SetRestriction(parent_id, self))

    def show_view_restriction(self):
        self.setCentralWidget(self.create_module_widget(ViewRestrictions, parent_id=self.parent_id, main_app=self))

    def show_attendance_report(self):
        self.setCentralWidget((AttendanceReport(self)))

    def show_attendance_reports(self):
        self.setCentralWidget(self.create_module_widget(AttendanceReports, parent_id=self.parent_id, main_app=self))

    def create_module_widget(self, widget_class, *args, **kwargs):
        widget = widget_class(*args, **kwargs)
        main_layout = QVBoxLayout()
        top_layout = QHBoxLayout()


        back_button = QPushButton('Back')
        back_button.setFixedSize(100, 40) 
        back_button.clicked.connect(self.back_to_dashboard)
        main_layout.addWidget(back_button)

        back_button.setStyleSheet("""
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

        top_layout.addWidget(back_button, alignment=Qt.AlignLeft)
        top_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
    
        main_layout.addLayout(top_layout)
        main_layout.addWidget(widget)

        container = QWidget()
        container.setLayout(main_layout)
        return container



    def back_to_dashboard(self):
        if self.user_role == 'Admin':
            self.show_admin_dashboard()
        elif self.user_role == 'Parent':
            self.show_parent_dashboard()
        elif self.user_role == 'Canteen Manager':
            self.show_canteen_manager_dashboard()
        else:
            self.show_login_dialog()


    def show_admin_dashboard(self):
        dashboard_widget = QWidget()
        layout = QVBoxLayout()

        # Welcome message
        self.welcome_label = QLabel('Welcome, Admin!')
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setFont(QFont('Cambria', 30, QFont.Bold))
        self.welcome_label.setWordWrap(True)
        self.welcome_label.setStyleSheet("color: #000087; margin-bottom: 20px;")

        instructions_label = QLabel('Please select an option from the menu.')
        instructions_label.setAlignment(Qt.AlignCenter)
        instructions_label.setFont(QFont('Cambria', 20))
        instructions_label.setStyleSheet("color: #000087; margin-bottom: 20px;")

        # Group box for admin actions
        group_box = QGroupBox()
        group_box_layout = QVBoxLayout()

        # Adding buttons for admin actions
        student_button = QPushButton('Student List')
        student_button.setMinimumHeight(40)
        student_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #000087;
                border: 1px solid #4169E1;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4169E1;
                color: white;
            }
        """)
        student_button.clicked.connect(self.show_student_list)

        teacher_button = QPushButton('Teacher List')
        teacher_button.setMinimumHeight(40)
        teacher_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #000087;
                border: 1px solid #4169E1;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4169E1;
                color: white;
            }
        """)
        teacher_button.clicked.connect(self.show_teacher_list)

        class_button = QPushButton('Class List')
        class_button.setMinimumHeight(40)
        class_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #000087;
                border: 1px solid #4169E1;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4169E1;
                color: white;
            }
        """)
        class_button.clicked.connect(self.show_class_list)

        restriction_button = QPushButton('Restriction List')
        restriction_button.setMinimumHeight(40)
        restriction_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #000087;
                border: 1px solid #4169E1;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4169E1;
                color: white;
            }
        """)
        restriction_button.clicked.connect(self.show_restriction_list)

        attendance_button = QPushButton('Attendance Report')
        attendance_button.setMinimumHeight(40)
        attendance_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #000087;
                border: 1px solid #4169E1;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4169E1;
                color: white;
            }
        """)
        attendance_button.clicked.connect(self.show_attendance_report)

        attendance_add_button = QPushButton('Add Absence')
        attendance_add_button.setMinimumHeight(40)
        attendance_add_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #000087;
                border: 1px solid #4169E1;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4169E1;
                color: white;
            }
        """)
        attendance_add_button.clicked.connect(self.show_attendance_entry)

        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(student_button)
        buttons_layout.addWidget(teacher_button)
        buttons_layout.addWidget(class_button)
        buttons_layout.addWidget(restriction_button)
        buttons_layout.addWidget(attendance_button)
        buttons_layout.addWidget(attendance_add_button)

        group_box_layout.addLayout(buttons_layout)
        group_box.setLayout(group_box_layout)
        group_box.setStyleSheet("""
            QGroupBox {
                border: 2px solid #4169E1;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px;
                background-color: #000087;
                color: white;
                font-weight: bold;
            }
        """)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(self.welcome_label)
        layout.addWidget(instructions_label)
        layout.addWidget(group_box)
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Adding logout button
        logout_button = QPushButton('Logout')
        logout_button.setMinimumHeight(50)
        logout_button.setStyleSheet("""
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
        logout_button.clicked.connect(self.logout)
        layout.addWidget(logout_button)


        dashboard_widget.setLayout(layout)
        self.setCentralWidget(dashboard_widget)


    def show_parent_dashboard(self):
        dashboard_widget = QWidget()
        layout = QVBoxLayout()

        # Welcome message
        self.welcome_label = QLabel('Welcome, Parent!')
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setFont(QFont('Cambria', 30, QFont.Bold))
        self.welcome_label.setWordWrap(True)
        self.welcome_label.setStyleSheet("color: #000087; margin-bottom: 20px;")

        instructions_label = QLabel('Please select an option from the menu.')
        instructions_label.setAlignment(Qt.AlignCenter)
        instructions_label.setFont(QFont('Cambria', 20))
        instructions_label.setStyleSheet("color: #000087; margin-bottom: 20px;")

        # Group box for parent actions
        group_box = QGroupBox()
        group_box_layout = QVBoxLayout()

        # Adding buttons for parent actions
        attendance_button = QPushButton('View Attendance Report')
        attendance_button.setMinimumHeight(40)
        attendance_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #000087;
                border: 1px solid #4169E1;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4169E1;
                color: white;
            }
        """)
        attendance_button.clicked.connect(self.show_attendance_reports)

        canteen_button = QPushButton('View Shopping Information')
        canteen_button.setMinimumHeight(40)
        canteen_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #000087;
                border: 1px solid #4169E1;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4169E1;
                color: white;
            }
        """)
        canteen_button.clicked.connect(self.show_canteen_shop)

        restriction_button = QPushButton('View Restrictions')
        restriction_button.setMinimumHeight(40)
        restriction_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #000087;
                border: 1px solid #4169E1;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4169E1;
                color: white;
            }
        """)
        restriction_button.clicked.connect(self.show_view_restriction)

        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(attendance_button)
        buttons_layout.addWidget(canteen_button)
        buttons_layout.addWidget(restriction_button)

        group_box_layout.addLayout(buttons_layout)
        group_box.setLayout(group_box_layout)
        group_box.setStyleSheet("""
            QGroupBox {
                border: 2px solid #4169E1;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px;
                background-color: #000087;
                color: white;
                font-weight: bold;
            }
        """)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(self.welcome_label)
        layout.addWidget(instructions_label)
        layout.addWidget(group_box)
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Adding logout button
        logout_button = QPushButton('Logout')
        logout_button.setMinimumHeight(50)
        logout_button.setStyleSheet("""
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
        logout_button.clicked.connect(self.logout)
        layout.addWidget(logout_button)

        dashboard_widget.setLayout(layout)
        self.setCentralWidget(dashboard_widget)

    def show_canteen_manager_dashboard(self):
        dashboard_widget = QWidget()
        layout = QVBoxLayout()

        # Welcome message
        self.welcome_label = QLabel('Welcome, Canteen Manager!')
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setFont(QFont('Cambria', 30, QFont.Bold))
        self.welcome_label.setWordWrap(True)
        self.welcome_label.setStyleSheet("color: #000087; margin-bottom: 20px;")

        instructions_label = QLabel('Please select an option from the menu.')
        instructions_label.setAlignment(Qt.AlignCenter)
        instructions_label.setFont(QFont('Cambria', 20))
        instructions_label.setStyleSheet("color: #000087; margin-bottom: 20px;")

        # Group box for canteen manager actions
        group_box = QGroupBox()
        group_box_layout = QVBoxLayout()

        # Adding buttons for canteen manager actions
        product_button = QPushButton('Product List')
        product_button.setMinimumHeight(40)
        product_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #000087;
                border: 1px solid #4169E1;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4169E1;
                color: white;
            }
        """)
        product_button.clicked.connect(self.show_product_list)

        restriction_button = QPushButton("Student Restriction List")
        restriction_button.setMinimumHeight(40)
        restriction_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #000087;
                border: 1px solid #4169E1;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4169E1;
                color: white;
            }
        """)
        restriction_button.clicked.connect(self.show_restriction_list)

        canteen_button = QPushButton('Sales List')
        canteen_button.setMinimumHeight(40)
        canteen_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #000087;
                border: 1px solid #4169E1;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4169E1;
                color: white;
            }
        """)
        canteen_button.clicked.connect(self.show_canteen_shopping)

        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(product_button)
        buttons_layout.addWidget(restriction_button)
        buttons_layout.addWidget(canteen_button)

        group_box_layout.addLayout(buttons_layout)
        group_box.setLayout(group_box_layout)
        group_box.setStyleSheet("""
            QGroupBox {
                border: 2px solid #4169E1;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 3px;
                background-color: #000087;
                color: white;
                font-weight: bold;
            }
        """)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(self.welcome_label)
        layout.addWidget(instructions_label)
        layout.addWidget(group_box)
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Adding logout button
        logout_button = QPushButton('Logout')
        logout_button.setMinimumHeight(50)
        logout_button.setStyleSheet("""
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
        logout_button.clicked.connect(self.logout)
        layout.addWidget(logout_button)

        dashboard_widget.setLayout(layout)
        self.setCentralWidget(dashboard_widget)

    def logout(self):
        self.user_role = None
        self.parent_id = None
        self.current_class_id = None 
        self.central_widget = QWidget()  
        self.setCentralWidget(self.central_widget)
        self.menuBar().clear()  
        self.show_login_dialog()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Exit Application',
                                     "Are you sure you want to exit?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            sys.exit()  
        else:
            event.ignore()

if __name__ == '__main__':
    create_tables()  
    app = QApplication(sys.argv)
    mainWin = SchoolManagementApp()
    mainWin.show()
    sys.exit(app.exec_())
