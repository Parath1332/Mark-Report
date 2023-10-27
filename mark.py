import streamlit as st
import mysql.connector
from fpdf import FPDF
from io import BytesIO
import os


# Establish a MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1332",
    database="marksheet"
)
cursor = conn.cursor()

# Function to retrieve student details from the database
def get_student_info(username):
    query = "SELECT student_name, student_class FROM students WHERE username = %s"
    cursor.execute(query, (username,))
    student_info = cursor.fetchone()
    return student_info

# Function to retrieve teacher details from the database
def get_teacher_info(username):
    query = "SELECT teacher_name, teacher_class FROM teachers WHERE username = %s"
    cursor.execute(query, (username,))
    teacher_info = cursor.fetchone()
    return teacher_info

# Function to generate and save marksheet report as PDF
def generate_marksheet_report_pdf(username, student_name, student_class):
    # Retrieve the student's marks
    student_marks = get_student_marks(username)

    # Create a PDF object with a landscape layout
    pdf = FPDF(orientation='P')
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_font("Lexend", fname="Lexend-Regular.ttf", uni=True)
    pdf.set_font("Lexend", size=12)


    # Header
    pdf.set_fill_color(105, 105, 105)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(190, 10, txt="Student Marksheet Report", ln=1, align='C', fill=True)

    # Student Informatio
    pdf.set_fill_color(200, 200, 200)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(95, 10, txt=f"Student Name: {student_name}", border=1, fill=True)
    pdf.cell(95, 10, txt=f"Class: {student_class}", border=1, fill=True)
    pdf.ln(10)

    # Calculate the position to center the table horizontally
    table_x = 15  # X-coordinate of the table
    table_width = pdf.w - 2 * table_x  # Width of the table
    table_y = pdf.y  # Y-coordinate of the table (current position)

    # Table Header
    pdf.set_fill_color(0,0, 0)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(95, 10, txt="Subject", border=1, fill=True, align='C')
    pdf.cell(95, 10, txt="Marks", border=1, fill=True, align='C')
    pdf.ln()

    # Set the position to center the table horizontally
    pdf.x = table_x

    # Subject Marks
    subjects = ['English', 'Tamil', 'Maths', 'Science', 'Social Science', 'Computer Science']
    total_marks = 0

    pdf.set_fill_color(0, 255, 0)
    pdf.set_text_color(255, 0, 0)
    for subject, mark in zip(subjects, student_marks):
        pdf.cell( 95, 10, txt=subject, border=1, fill=True, align='C')
        pdf.cell( 95, 10, txt=str(mark), border=1, fill=True, align='C')
        pdf.ln()
        total_marks += mark

    # Set the position to center the total marks and percentage
    pdf.x = table_x

    # Total Percentage
    total_percentage = (total_marks / 480) * 100
    pdf.set_fill_color(200, 2, 2)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(93, 10, txt="Total Marks", border=1, fill=True, align='C')
    pdf.cell(93, 10, txt=str(total_marks), border=1, fill=True, align='C')
    pdf.ln()
    pdf.cell(95, 10, txt="Total Percentage", border=1, fill=True, align='C')
    pdf.cell(95, 10, txt=f"{total_percentage:.2f}%", border=1, fill=True, align='C')
    
    pdf.ln()
    # Save the PDF to a BytesIO object
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)

    return pdf_buffer



# Function to send an email with the PDF attachment
# Streamlit login form
st.markdown("<h1 style='text-align:center;color:white;'>Mark Report Management</h1>",unsafe_allow_html=True)
st.title("Login")
hide_st_style = """
            <style>
            #MainMenu { visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style,unsafe_allow_html=True)
user_type = st.selectbox("Select User Type", ["Student", "Teacher"])

if user_type == "Student":
    username = st.text_input("Student Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Add your login validation logic here (e.g., check if the username and password are correct)
        # Replace the condition with your authentication logic
        query = "SELECT COUNT(*) FROM students WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()[0]
        if result == 1:
            st.session_state.is_logged_in = True
            st.session_state.username = username
            st.success("Student logged in successfully.")
        else:
            st.error("Invalid username or password. Please try again.")

elif user_type == "Teacher":
    username = st.text_input("Teacher Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Add your login validation logic here (e.g., check if the username and password are correct)
        # Replace the condition with your authentication logic
        query = "SELECT COUNT(*) FROM teachers WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()[0]
        if result == 1:
            st.session_state.is_logged_in = True
            st.session_state.username = username
            st.success("Teacher logged in successfully.")
        else:
            st.error("Invalid username or password. Please try again.")
def get_student_marks(username):
    query = "SELECT English, Tamil, Maths, Science, Social_Science, Computer_Science FROM students WHERE username = %s"
    cursor.execute(query, (username,))
    marks = cursor.fetchone()
    return marks
def get_all_student_data():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1332",
        database="marksheet"
    )

    cursor = connection.cursor(dictionary=True)

    # Query to retrieve student data
    query = "SELECT student_name, student_class, English, Tamil, Maths, Science, Social_Science, Computer_Science FROM students"

    cursor.execute(query)
    student_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return student_data
def update_student_marks(student_name, updated_marks):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1332",
        database="marksheet"
    )

    cursor = connection.cursor()

    # Query to update student marks
    query = "UPDATE students SET English=%s, Tamil=%s, Maths=%s, Science=%s, Social_Science=%s, Computer_Science=%s WHERE student_name=%s"
    values = (updated_marks['English'], updated_marks['Tamil'], updated_marks['Maths'], updated_marks['Science'], updated_marks['Social_Science'], updated_marks['Computer_Science'], student_name)

    print("Query:", query)
    print("Values:", values)

    try:
        cursor.execute(query, values)
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error updating marks: {err}")

    cursor.close()
    connection.close()

def get_all_students():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1332",
        database="marksheet"
    )

    cursor = connection.cursor()

    # Query to retrieve all student usernames, names, and classes
    query = "SELECT username, student_name, student_class FROM students"
    
    cursor.execute(query)
    all_students = cursor.fetchall()

    cursor.close()
    connection.close()

    return all_students

def delete_student_marks(student_name):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1332",
        database="marksheet"
    )

    cursor = connection.cursor()

    # Query to delete student marks
    query = "DELETE FROM students WHERE student_name=%s"
    values = (student_name,)

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()


if st.session_state.get('is_logged_in', False):
    username = st.session_state.username

    if user_type == "Student":
        student_info = get_student_info(username)
        if student_info:
            student_name,student_class= student_info
            st.write(f"Welcome, {student_name}!")

            # Create a table title
            st.title("Student Marks Table")

            # Create a table with only "Subject" and "Marks" columns
            subjects = ['English', 'Tamil', 'Maths', 'Science', 'Social_Science', 'Computer_Science']
            student_marks = get_student_marks(username)
            marks_data = [(subject, mark) for subject, mark in zip(subjects, student_marks)]

            table_html = '<table style="margin: 0 auto; text-align: center;"><tr><th>Subject</th><th>Marks</th></tr>'
            for subject, mark in marks_data:
                table_html += f'<tr><td>{subject}</td><td>{mark}</td></tr>'
            table_html += '</table>'
            st.write(table_html, unsafe_allow_html=True)

            # Create a button to generate and save the marksheet report as PDF
            if st.button("Generate Marksheet Report PDF"):
                pdf_buffer = generate_marksheet_report_pdf(username, student_name,student_class)
                st.write("Marksheet report generated.")

                # Create a download button for the PDF file
                st.download_button(
                    label="Download Marksheet Report PDF",
                    data=pdf_buffer.getvalue(),
                    key="download_pdf",
                    file_name="marksheet_"+username+"_report.pdf",
                )

    elif user_type == "Teacher":
        teacher_info = get_teacher_info(username)
        if teacher_info:
            teacher_name, teacher_class = teacher_info
            st.write(f"Welcome, {teacher_name}!")
            teacher_option = st.selectbox("Select an option:", ("View Student Marks", "Update Student Marks", "Delete Student Marks"))

        if teacher_option == "View Student Marks":
            # Teacher can view student marks
            st.title("View Student Marks")

            # List students and their marks
            student_data = get_all_student_data()
            st.table(student_data)

        elif teacher_option == "Update Student Marks":
            # Teacher can update student marks
            st.title("Update Student Marks")

            all_students = get_all_students()
            student_name = st.selectbox("Select a student:", [student[1] for student in all_students])

            if student_name:
                selected_student = [student for student in all_students if student[1] == student_name][0]
                student_name, _, student_class = selected_student
                st.write(f"Updating marks for {student_name} in class {student_class}:")

                updated_marks = {}
                for subject in ('English', 'Tamil', 'Maths', 'Science', 'Social_Science', 'Computer_Science'):
                    updated_marks[subject] = st.number_input(f"{subject}:", min_value=0, max_value=100)

                if st.button("Update Marks"):
                    update_student_marks(student_name, updated_marks)
                    st.success(f"Marks updated successfully for {student_name}!")
        elif teacher_option == "Delete Student Marks":
            # Teacher can delete student marks
            st.title("Delete Student Marks")

            all_students = get_all_students()
            student_name = st.selectbox("Select a student:", [student[1] for student in all_students])

            if student_name:
                selected_student = [student for student in all_students if student[1] == student_name][0]
                student_name, _, student_class = selected_student
                st.write(f"Deleting {student_name} Of class {student_class}:")
                if st.button("Delete Marks"):
                    delete_student_marks(student_name)
                    st.success(f"Deleted successfully {student_name}!")
                