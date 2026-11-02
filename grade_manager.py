students = []

def get_grade(mark):
    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    else:
        return "E"


def add_student():
    name = input("Enter student name: ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    try:
        mark = int(input("Enter mark (0-100): "))

        if mark < 0 or mark > 100:
            print("Mark must be between 0 and 100.")
            return

        grade = get_grade(mark)

        students.append({
            "name": name,
            "mark": mark,
            "grade": grade
        })

        print("Student added successfully!")

    except ValueError:
        print("Invalid mark. Please enter a number.")


def show_results():
    if not students:
        print("No student records available.")
        return

    print("\nName       Mark  Grade")
    print("-" * 25)

    marks = []

    for student in students:
        print(f"{student['name']:<10} {student['mark']:<5} {student['grade']}")
        marks.append(student["mark"])

    average = sum(marks) / len(marks)
    highest = max(marks)
    lowest = min(marks)
