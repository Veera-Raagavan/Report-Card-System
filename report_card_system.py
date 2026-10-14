import mysql.connector
from mysql.connector import Error

def connect_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='school'
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_database_and_tables():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS school")
        cursor.close()
        connection.close()
        
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='school'
        )
        cursor = connection.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                roll_no INT PRIMARY KEY,
                name VARCHAR(50),
                class VARCHAR(10)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS marks (
                roll_no INT,
                subject VARCHAR(30),
                marks INT,
                FOREIGN KEY (roll_no) REFERENCES students(roll_no)
            )
        """)
        
        connection.commit()
        cursor.close()
        connection.close()
        print("Database and tables created successfully!")
    except Error as e:
        print(f"Error creating database: {e}")

def add_student():
    connection = connect_database()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        roll_no = int(input("Enter Roll Number: "))
        name = input("Enter Student Name: ")
        class_name = input("Enter Class: ")
        
        query = "INSERT INTO students (roll_no, name, class) VALUES (%s, %s, %s)"
        cursor.execute(query, (roll_no, name, class_name))
        connection.commit()
        print(f"Student {name} added successfully!")
    except Error as e:
        print(f"Error adding student: {e}")
    finally:
        cursor.close()
        connection.close()

def view_students():
    connection = connect_database()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students ORDER BY roll_no")
        results = cursor.fetchall()
        
        if results:
            print("\n" + "="*60)
            print(f"{'Roll No':<10} {'Name':<30} {'Class':<10}")
            print("="*60)
            for row in results:
                print(f"{row[0]:<10} {row[1]:<30} {row[2]:<10}")
            print("="*60)
        else:
            print("No students found!")
    except Error as e:
        print(f"Error viewing students: {e}")
    finally:
        cursor.close()
        connection.close()

def delete_student():
    connection = connect_database()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        roll_no = int(input("Enter Roll Number to delete: "))
        
        cursor.execute("SELECT * FROM students WHERE roll_no = %s", (roll_no,))
        if cursor.fetchone():
            cursor.execute("DELETE FROM marks WHERE roll_no = %s", (roll_no,))
            cursor.execute("DELETE FROM students WHERE roll_no = %s", (roll_no,))
            connection.commit()
            print(f"Student with roll number {roll_no} deleted successfully!")
        else:
            print(f"Student with roll number {roll_no} not found!")
    except Error as e:
        print(f"Error deleting student: {e}")
    finally:
        cursor.close()
        connection.close()

def add_marks():
    connection = connect_database()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        roll_no = int(input("Enter Roll Number: "))
        
        cursor.execute("SELECT * FROM students WHERE roll_no = %s", (roll_no,))
        if not cursor.fetchone():
            print(f"Student with roll number {roll_no} not found!")
            cursor.close()
            connection.close()
            return
        
        subject = input("Enter Subject Name: ")
        marks = int(input("Enter Marks: "))
        
        cursor.execute("SELECT * FROM marks WHERE roll_no = %s AND subject = %s", (roll_no, subject))
        if cursor.fetchone():
            print("Marks for this subject already exist! Use Update Marks option.")
        else:
            query = "INSERT INTO marks (roll_no, subject, marks) VALUES (%s, %s, %s)"
            cursor.execute(query, (roll_no, subject, marks))
            connection.commit()
            print(f"Marks added successfully!")
    except Error as e:
        print(f"Error adding marks: {e}")
    finally:
        cursor.close()
        connection.close()

def view_marks():
    connection = connect_database()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        roll_no = int(input("Enter Roll Number: "))
        
        cursor.execute("SELECT * FROM students WHERE roll_no = %s", (roll_no,))
        student = cursor.fetchone()
        if not student:
            print(f"Student with roll number {roll_no} not found!")
            cursor.close()
            connection.close()
            return
        
        cursor.execute("SELECT subject, marks FROM marks WHERE roll_no = %s ORDER BY subject", (roll_no,))
        results = cursor.fetchall()
        
        if results:
            print(f"\nMarks for Roll No: {roll_no} - {student[1]}")
            print("="*40)
            print(f"{'Subject':<20} {'Marks':<10}")
            print("="*40)
            for row in results:
                print(f"{row[0]:<20} {row[1]:<10}")
            print("="*40)
        else:
            print("No marks found for this student!")
    except Error as e:
        print(f"Error viewing marks: {e}")
    finally:
        cursor.close()
        connection.close()

def update_marks():
    connection = connect_database()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        roll_no = int(input("Enter Roll Number: "))
        subject = input("Enter Subject Name: ")
        new_marks = int(input("Enter New Marks: "))
        
        cursor.execute("SELECT * FROM marks WHERE roll_no = %s AND subject = %s", (roll_no, subject))
        if cursor.fetchone():
            query = "UPDATE marks SET marks = %s WHERE roll_no = %s AND subject = %s"
            cursor.execute(query, (new_marks, roll_no, subject))
            connection.commit()
            print("Marks updated successfully!")
        else:
            print("Marks not found for this student and subject!")
    except Error as e:
        print(f"Error updating marks: {e}")
    finally:
        cursor.close()
        connection.close()

def calculate_grade(average):
    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    else:
        return "Fail"

def generate_report_card():
    connection = connect_database()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        roll_no = int(input("Enter Roll Number: "))
        
        cursor.execute("SELECT * FROM students WHERE roll_no = %s", (roll_no,))
        student = cursor.fetchone()
        if not student:
            print(f"Student with roll number {roll_no} not found!")
            cursor.close()
            connection.close()
            return
        
        cursor.execute("SELECT subject, marks FROM marks WHERE roll_no = %s ORDER BY subject", (roll_no,))
        results = cursor.fetchall()
        
        if not results:
            print("No marks found for this student!")
            cursor.close()
            connection.close()
            return
        
        print("\n" + "="*60)
        print("REPORT CARD")
        print("="*60)
        print(f"Roll Number: {student[0]}")
        print(f"Name: {student[1]}")
        print(f"Class: {student[2]}")
        print("="*60)
        print(f"{'Subject':<25} {'Marks':<10}")
        print("="*60)
        
        total_marks = 0
        for row in results:
            print(f"{row[0]:<25} {row[1]:<10}")
            total_marks += row[1]
        
        average = total_marks / len(results)
        grade = calculate_grade(average)
        
        print("="*60)
        print(f"Total Marks: {total_marks}")
        print(f"Average Marks: {average:.2f}")
        print(f"Grade: {grade}")
        print("="*60)
    except Error as e:
        print(f"Error generating report card: {e}")
    finally:
        cursor.close()
        connection.close()

def main():
    print("Report Card Management System")
    print("Initializing database...")
    create_database_and_tables()
    print("\n")
    
    while True:
        print("\n" + "="*40)
        print("MENU")
        print("="*40)
        print("1. Add Student")
        print("2. View Students")
        print("3. Delete Student")
        print("4. Add Marks")
        print("5. View Marks")
        print("6. Update Marks")
        print("7. Generate Report Card")
        print("8. Exit")
        print("="*40)
        
        choice = input("Enter your choice (1-8): ")
        
        if choice == '1':
            add_student()
        elif choice == '2':
            view_students()
        elif choice == '3':
            delete_student()
        elif choice == '4':
            add_marks()
        elif choice == '5':
            view_marks()
        elif choice == '6':
            update_marks()
        elif choice == '7':
            generate_report_card()
        elif choice == '8':
            print("Thank you for using Report Card Management System!")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 8.")

if __name__ == "__main__":
    main()

