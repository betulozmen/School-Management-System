import mysql.connector
from mysql.connector import Error
from settings import DATABASE_CONFIG


def get_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=DATABASE_CONFIG['host'],
            user=DATABASE_CONFIG['user'],
            password=DATABASE_CONFIG['password'],
            database=DATABASE_CONFIG['database']
        )
        if connection.is_connected():
            print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def create_tables():
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Students (
        idStudent INT PRIMARY KEY,
        studentName VARCHAR(20),
        studentSurname VARCHAR(15),
        birthOfDate DATE,
        studentGender VARCHAR(5),
        identificationNo VARCHAR(11),
        Classes_idClass INT,
        FOREIGN KEY (Classes_idClass) REFERENCES Classes(idClass)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Teachers (
        idTeacher INT AUTO_INCREMENT PRIMARY KEY,
        teacherName VARCHAR(20),
        teacherSurname VARCHAR(15),
        teacherProfession VARCHAR(45),
        email VARCHAR(45),
        phoneNumber VARCHAR(13),
        Classes_idClass INT,
        FOREIGN KEY (Classes_idClass) REFERENCES Classes(idClass)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Classes (
        idClass INT AUTO_INCREMENT PRIMARY KEY,
        classLevel INT,                
        className VARCHAR(1)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Parents (
        idParent INT AUTO_INCREMENT PRIMARY KEY,
        parentName VARCHAR(20),
        parentSurname VARCHAR(15),
        phoneNumber VARCHAR(13),
        email VARCHAR(45),
        passwd VARCHAR(15)

    )
    ''')              

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Canteen_Products (
        idProduct INT AUTO_INCREMENT PRIMARY KEY,
        productName VARCHAR(20),
        productPrice FLOAT,
        productStock INT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS StudentBalances (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Students_idStudent INT,
        balance VARCHAR(10),
        FOREIGN KEY (Students_idStudent) REFERENCES Students(idStudent)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Restrictions (
        idRestriction INT AUTO_INCREMENT PRIMARY KEY,
        restrictionType VARCHAR(17),
        restrictionValue VARCHAR(45),
        Parents_idParent INT,
        Students_idStudent INT,                     
        FOREIGN KEY (Students_idStudent) REFERENCES Students(idStudent),
        FOREIGN KEY (Parents_idParent) REFERENCES Parents(idParent)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Parents_has_Students (
        Parents_idParent INT,
        Students_idStudent INT,
        FOREIGN KEY (Students_idStudent) REFERENCES Students(idStudent),
        FOREIGN KEY (Parents_idParent) REFERENCES Parents(idParent)           
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Attendance (
        idAttendance INT AUTO_INCREMENT PRIMARY KEY,
        attendanceDate DATE,
        attendanceType VARCHAR(10),
        Students_idStudent INT,
        FOREIGN KEY (Students_idStudent) REFERENCES Students(idStudent)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Canteen_Payment (
        idPayment INT AUTO_INCREMENT PRIMARY KEY,
        paymentDate DATE,
        paymentAmount FLOAT,
        Students_idStudent INT,      
        FOREIGN KEY (Students_idStudent) REFERENCES Students(idStudent)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Canteen_Shopping(
        idShopping INT AUTO_INCREMENT PRIMARY KEY,
        shoppingDATE DATE,
        shoppingAmount INT,
        Students_idStudent INT,
        FOREIGN KEY (Students_idStudent) REFERENCES Students(idStudent)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Classes_has_Teachers(
        Classes_idClass INT,
        Teachers_idTeacher INT,
        FOREIGN KEY (Classes_idClass) REFERENCES Classes(idClass),
        FOREIGN KEY (Teachers_idTeacher) REFERENCES Teachers(idTeacher)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Canteen_Shopping_has_Canteen_Products(
        Canteen_Shopping_idShopping INT,
        Canteen_Products_idProduct INT,
        FOREIGN KEY (Canteen_Shopping_idShopping) REFERENCES Canteen_Shopping(idShopping),
        FOREIGN KEY (Canteen_Products_idProduct) REFERENCES Canteen_Products(idProduct)
    )
    ''')
    

    
    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_tables()

