import sqlite3
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus

# Connect to the database
def get_data():
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()

    # Retrieve courses, professors, classrooms
    cursor.execute("SELECT * FROM Courses")
    courses = cursor.fetchall()
    
    cursor.execute("SELECT * FROM Professors")
    professors = cursor.fetchall()
    
    cursor.execute("SELECT * FROM Classrooms")
    classrooms = cursor.fetchall()
    
    conn.close()
    return courses, professors, classrooms

# Scheduling function using PuLP
def generate_schedule():
    courses, professors, classrooms = get_data()
    
    # Create the optimization problem
    prob = LpProblem("Timetable_Scheduling", LpMinimize)

    # Create decision variables
    schedule_vars = {}
    for course in courses:
        for professor in professors:
            for classroom in classrooms:
                # Creating a variable for each course-professor-room combo
                schedule_vars[(course[0], professor[0], classroom[0])] = LpVariable(
                    f"schedule_{course[0]}_{professor[0]}_{classroom[0]}", cat="Binary"
                )

    # Add constraints
    # Simplify: Allow each course to be assigned to any professor and classroom without strict constraints
    for course in courses:
        prob += lpSum([schedule_vars[(course[0], prof[0], room[0])] for prof in professors for room in classrooms]) >= 1

    # Simplified objective function (no optimization just checking feasibility)
    prob += 0  # No objective to optimize yet

    # Solve the problem
    prob.solve()

    # Display the results
    schedule = []
    for (course_id, professor_id, classroom_id), variable in schedule_vars.items():
        if variable.value() == 1:
            schedule.append((course_id, professor_id, classroom_id))
            print(f"Course {course_id} assigned to Professor {professor_id} in Classroom {classroom_id}")

    # Return the generated schedule
    return schedule

if __name__ == "__main__":
    generate_schedule()
