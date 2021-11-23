import mysql.connector as mysql

db = mysql.connect(host="localhost",user="root",password="",database="vikoak")
command_handler = db.cursor(buffered=True)

#git test

def teacher_session(username):
    while 1:
        print("")
        print("Teacher menu")
        print("1. Grade the student")
        print("2. Student list and marks")
        print("3. Log out")
        print("")
        user_option = input(str("Select menu function: "))
        if user_option == "1":
            print("")
            print("New grade for students")
            teachername = (str(username),)
            command_handler.execute("SELECT lecture_name FROM lecture WHERE username = %s",teachername)
            pupos = command_handler.fetchall()
            for pupa in pupos:
                pupa = str(pupa).replace("'","")
                pupa = str(pupa).replace(",","")
                pupa = str(pupa).replace("(","")
                pupa = str(pupa).replace(")","")
            print("Grading students for: " + str(pupa))
            pavadinimas = (str(pupa),)
            command_handler.execute("SELECT username FROM grupe WHERE lecture_name = %s",pavadinimas)
            records = command_handler.fetchone()
            date = input(str("Date format: DD/MM/YYYY: "))              
            for record in records:
                record = str(record).replace("'","")
                record = str(record).replace(",","")
                record = str(record).replace("(","")
                record = str(record).replace(")","")
                mark = input(str("Enter grade " + str(record) + " 1-10: "))
                username = str(record)
                lecture_name = str(pupa)
                query_vals = (username,date,mark,lecture_name)
                command_handler.execute("INSERT INTO mark (username, date, mark, lecture_name) VALUES(%s,%s,%s,%s)",query_vals)
                db.commit()
                print(username + " grade " + mark + " " + lecture_name )
        elif user_option == "2":
            print("")
            print("Viewing student grades")
            teachername = (str(username),)
            command_handler.execute("SELECT lecture_name FROM lecture WHERE username = %s",teachername)
            records = command_handler.fetchall()
            for record in records:
                record = str(record).replace("'","")
                record = str(record).replace(",","")
                record = str(record).replace("(","")
                record = str(record).replace(")","")
            paskaita = (str(record),)
            command_handler.execute("SELECT username, mark, date FROM mark WHERE lecture_name = %s",paskaita)
            records = command_handler.fetchall()
            print("Graded students: ")
            for record in records:
                print(record)
        elif user_option == "3":
            break
        else:
            print("Error! Please select number from 1 to 3")


def student_session(username):
    while 1:
        print("")
        print("Student menu")
        print("1. View grades")
        print("2. Download gradebook")
        print("3. Log out")
    
        user_option = input(str("Select option: "))
        if user_option == "1":
            username = (str(username),)
            command_handler.execute("SELECT username, date, mark, lecture_name FROM mark WHERE username = %s",username)
            records = command_handler.fetchall()
            for record in records:
                print(record)
        elif user_option == "2":
            print("Downloading gradebook...")
            username = (str(username),)
            command_handler.execute("SELECT username, date, mark, lecture_name FROM mark WHERE username = %s",username)
            records = command_handler.fetchall()
            for record in records:
                with open("C:/Users/ITWORK/Desktop/gradebook.txt", "w") as f:
                    f.write(str(records)+"\n")
                f.close
            print("Download succesfull! ")
        elif user_option == "3":
            break
        else:
            print("Error! Please select number from 1 to 3")


def admin_session():
    while 1:
        print("")
        print("Admin menu")
        print("1. New student registration")
        print("2. New teacher registraction")
        print("3. delete student account")
        print("4. Delete teacher account")
        print("5. Add group and lecture to the student")
        print("6. Add lecture to teacher")
        print("7. Log out")

        user_option = input(str("Selection : "))
        if user_option == "1":
            print("")
            print("New student registration")
            username = input(str("Enter student name (username): "))
            password = input(str("Enter student surname (password): "))
            query_vals = (username,password)
            command_handler.execute("INSERT INTO users (username,password,privilege) VALUE (%s,%s,'student')",query_vals)
            db.commit()
            print(username + " been succesfully registered as a student! ")
        elif user_option == "2":
            print("")
            print("New teacher registraction")
            username = input(str("Enter teacher name (username): "))
            password = input(str("Enter teacher surname (password): "))
            query_vals = (username,password)
            command_handler.execute("INSERT INTO users (username,password,privilege) VALUE (%s,%s,'teacher')",query_vals)
            db.commit()
            print(username + " been succesfully registered as a teacher! ")
        elif user_option == "3":
            print("")
            print("Delete student account")
            username = input(str("Enter student account name(username): "))
            query_vals = (username,"student")
            command_handler.execute("DELETE FROM users WHERE username = %s AND privilege = %s", query_vals)
            db.commit()
            if command_handler.rowcount < 1:
                print("Error! User not found ")
            else:
                print(username + " account been succesfully deleted")
        elif user_option == "4":
            print("")
            print("Delete teacher account")
            username = input(str("Enter teacher account name(username) "))
            query_vals = (username,"teacher")
            command_handler.execute("DELETE FROM users WHERE username = %s AND privilege = %s", query_vals)
            db.commit()
            if command_handler.rowcount < 1:
                print("Error! User not found ")
            else:
                print(username + " account been succesfully deleted")
        elif user_option == "5":
            print("")
            print("Add student to the group and lecture")
            command_handler.execute("SELECT username FROM users WHERE privilege = 'student'")
            records = command_handler.fetchall()
            for record in records:
                record = str(record).replace("'","")
                record = str(record).replace(",","")
                record = str(record).replace("(","")
                record = str(record).replace(")","")
                print("Student: " + str(record))
                group_name = input(str(" Please enter group name: "))
                lecture_name = input(str(" Enter lecture name: " ))
                query_vals = (str(record),group_name, lecture_name)
                command_handler.execute("INSERT INTO grupe (username, group_name, lecture_name) VALUES(%s,%s,%s)",query_vals)
                db.commit()
                print(record + " has been added to group " + group_name + " and to the following lecture " + lecture_name)
        elif user_option == "6":
            print("")
            print("Add lecture to the teacher")
            command_handler.execute("SELECT username FROM users WHERE privilege = 'teacher'")
            records = command_handler.fetchall()
            for record in records:
                record = str(record).replace("'","")
                record = str(record).replace(",","")
                record = str(record).replace("(","")
                record = str(record).replace(")","")
                print("Teacher: " + str(record))
                lecture_name = input(str(" Enter lecture name: " ))
                query_vals = (str(record), lecture_name)
                command_handler.execute("INSERT INTO lecture (username, lecture_name) VALUES(%s,%s)",query_vals)
                db.commit()
                print(record + " has been assigned and to the following lecture " + lecture_name)
        elif user_option == "7":
            break
        else:
            print("Error! Please select number from 1 to 7")
            
def auth_student():
    print("")
    print("Student login")
    print("") 
    username = input(str("Enter student username : "))
    password = input(str("Password : "))
    query_vals = (username, password, "student")
    command_handler.execute("SELECT username FROM users WHERE username = %s AND password = %s AND privilege = %s",query_vals)
    if command_handler.rowcount <= 0:
        print("Incorrect password! ")
    else:
        print("Login succesful! ")
        student_session(username)       

def auth_teacher():
    print("")
    print("Teacher login")
    print("")
    username = input(str("Enter teacher username : "))
    password = input(str("Password : "))
    query_vals = (username, password)
    command_handler.execute("SELECT * FROM users  WHERE username = %s AND password = %s AND privilege = 'teacher'",query_vals)
    if command_handler.rowcount <=0:
        print("Incorrect password! ")
    else:
        print("Login succesful! ")
        teacher_session(username)

def auth_admin():
    print("")
    print("Admin login")
    print("")
    username = input(str("Enter admin username : "))
    password = input(str("Password : "))
    query_vals = (username, password)
    command_handler.execute("SELECT * FROM users  WHERE username = %s AND password = %s AND privilege = 'admin'",query_vals)
    if command_handler.rowcount <=0:
        print("Incorrect password! ")
    else:
        print("Login succesful! ")
        admin_session()

def main():
    while 1:
        print("Welcome to VIKO AIS")
        print("")
        print("1. Student login")
        print("2. Teacher login")
        print("3. Admin login")

        user_option = input(str("Option : "))
        if user_option == "1":
            auth_student()
        elif user_option == "2":
            auth_teacher()
        elif user_option == "3":
            auth_admin()
        else:
            print("Incorrect number! Select number from 1 to 3")

main()

