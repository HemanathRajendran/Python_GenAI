import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Grade Manager")

st.title("🎓 Student Grade Manager")

# Initialize session state
if "students" not in st.session_state:
    st.session_state.students = []

# Function to calculate grade
def calculate_grade(mark):
    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    else:
        return "F"

# Input Form
with st.form("student_form"):
    name = st.text_input("Student Name")
    mark = st.number_input("Marks", min_value=0, max_value=100)
    submit = st.form_submit_button("Add Student")

    if submit:
        grade = calculate_grade(mark)

        st.session_state.students.append({
            "Name": name,
            "Marks": mark,
            "Grade": grade
        })

        st.success(f"{name} added successfully!")

# Display Data
if st.session_state.students:
    st.subheader("Student Records")

    df = pd.DataFrame(st.session_state.students)

    st.dataframe(df, use_container_width=True)

    avg_marks = df["Marks"].mean()

    st.metric("Average Marks", f"{avg_marks:.2f}")

    st.subheader("Grade Distribution")
    st.bar_chart(df["Grade"].value_counts())

else:
    st.info("No student records available.")
