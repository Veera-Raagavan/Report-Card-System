# Report Card Management System

A console-based application written in **Python** with a **MySQL** backend. It stores students and their subject-wise marks in a `school` database and generates a formatted report card showing total marks, average and grade.

> Built as a Computer Science school project to demonstrate Python–MySQL connectivity, CRUD operations and parameterized SQL queries.

---

## Table of Contents

1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Database Design](#database-design)
5. [Grading Scheme](#grading-scheme)
6. [Prerequisites](#prerequisites)
7. [Installation and Setup](#installation-and-setup)
8. [Usage](#usage)
9. [Sample Output](#sample-output)
10. [How It Works](#how-it-works)
11. [Known Limitations](#known-limitations)
12. [Future Improvements](#future-improvements)

---

## Features

| # | Menu option | What it does |
|---|-------------|--------------|
| 1 | Add Student | Adds a student with roll number, name and class |
| 2 | View Students | Lists all students sorted by roll number |
| 3 | Delete Student | Deletes a student along with all of their marks |
| 4 | Add Marks | Adds marks for a subject (blocks duplicate subject entries) |
| 5 | View Marks | Shows all subject marks of one student |
| 6 | Update Marks | Changes the marks of an existing subject |
| 7 | Generate Report Card | Prints a report card with total, average and grade |
| 8 | Exit | Closes the program |

Other highlights:

- **Automatic setup**: the database and both tables are created on first run, so no manual SQL step is needed.
- **Parameterized queries** (`%s` placeholders) protect against SQL injection.
- **Validation checks**: confirms the student exists before adding marks and rejects duplicate subject entries.
- **Safe cleanup**: connections and cursors are closed in `finally` blocks.

---

## Tech Stack

- **Language:** Python 3.x
- **Database:** MySQL
- **Library:** `mysql-connector-python`

---

## Project Structure

```
report-card-management/
├── report_card_system.py   # Main application
├── school.sql              # Optional manual database setup script
├── sample_output.txt       # Recorded sample run of the program
├── .gitignore
└── README.md
```

---

## Database Design

**Database name:** `school`

### `students` table

| Column | Type | Constraint |
|--------|------|------------|
| roll_no | INT | PRIMARY KEY |
| name | VARCHAR(50) | |
| class | VARCHAR(10) | |

### `marks` table

| Column | Type | Constraint |
|--------|------|------------|
| roll_no | INT | FOREIGN KEY → `students(roll_no)` |
| subject | VARCHAR(30) | |
| marks | INT | |

**Relationship:** one student has many marks rows (one-to-many).

```
students (roll_no PK, name, class)
    │
    └──< marks (roll_no FK, subject, marks)
```

---

## Grading Scheme

The grade is based on the **average** of all subject marks:

| Average | Grade |
|---------|-------|
| 90 and above | A+ |
| 80 – 89.99 | A |
| 70 – 79.99 | B |
| 60 – 69.99 | C |
| Below 60 | Fail |

---

## Prerequisites

- [Python 3.8+](https://www.python.org/downloads/)
- [MySQL Server](https://dev.mysql.com/downloads/mysql/) running on `localhost`
- The `mysql-connector-python` package

---

## Installation and Setup

**1. Clone the repository**

```bash
git clone https://github.com/<your-username>/report-card-management.git
cd report-card-management
```

**2. Install the MySQL connector**

```bash
pip install mysql-connector-python
```

**3. Configure your MySQL credentials**

Open `report_card_system.py` and set your MySQL password. By default the code connects as `root` with an **empty password**:

```python
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',        # change this to your MySQL password
    database='school'
)
```

The same credentials appear in two functions (`connect_database` and `create_database_and_tables`), so update both.

**4. (Optional) Create the database manually**

The program creates everything automatically, but you can also run the script yourself:

```bash
mysql -u root -p < school.sql
```

**5. Run the program**

```bash
python report_card_system.py
```

---

## Usage

On start, the program initializes the database and shows this menu:

```
========================================
MENU
========================================
1. Add Student
2. View Students
3. Delete Student
4. Add Marks
5. View Marks
6. Update Marks
7. Generate Report Card
8. Exit
========================================
Enter your choice (1-8):
```

A typical workflow:

1. Choose **1** to add a student (for example, roll no. `101`).
2. Choose **4** repeatedly to add marks for each subject.
3. Choose **6** if a mark needs correcting.
4. Choose **7** to print the report card.

---

## Sample Output

Report card generated for roll number 101:

```
============================================================
REPORT CARD
============================================================
Roll Number: 101
Name: John Smith
Class: 10A
============================================================
Subject                   Marks
============================================================
English                   82
History                   88
Mathematics               85
Science                   92
============================================================
Total Marks: 347
Average Marks: 86.75
Grade: A
============================================================
```

A full recorded session (adding students, entering and updating marks, report cards for three students, and deleting a student) is available in [`sample_output.txt`](sample_output.txt).

---

## How It Works

| Function | Purpose |
|----------|---------|
| `connect_database()` | Opens a connection to the `school` database, returns `None` on failure |
| `create_database_and_tables()` | Creates the database and both tables if they don't exist |
| `add_student()` | Inserts a row into `students` |
| `view_students()` | Selects and prints all students |
| `delete_student()` | Deletes the student's marks first, then the student (to respect the foreign key) |
| `add_marks()` | Verifies the student exists, checks for duplicates, then inserts marks |
| `view_marks()` | Prints all subject marks of a student |
| `update_marks()` | Updates marks for a given roll number and subject |
| `calculate_grade(average)` | Maps an average to a grade |
| `generate_report_card()` | Combines student details, marks, total, average and grade |
| `main()` | Runs the menu loop |

---

## Known Limitations

- The MySQL credentials are written directly in the source code.
- Entering text where a number is expected (for example in the roll number or marks prompt) raises a `ValueError` that is not caught, which closes the program.
- Marks are not range-checked, so values below 0 or above 100 are accepted.
- The `marks` table has no primary key, so duplicate `(roll_no, subject)` rows are prevented only by a check in Python, not by the database.
- The grade is based on the average only; there is no per-subject pass mark.
- Each subject is assumed to be out of 100.

---

## Future Improvements

- Read database credentials from environment variables or a `.env` file.
- Validate input (marks between 0 and 100, non-empty names, numeric roll numbers).
- Add a composite primary key `(roll_no, subject)` to the `marks` table.
- Add an update option for student details (name, class).
- Show class rank or topper lists, and class-wise reports.
- Export report cards to PDF or a text file.
- Add a login for teachers.

---

## Author

**Veera Raagavan**
Computer Science School Project

---

## License

This project is intended for educational purposes. Feel free to use and modify it for learning.
