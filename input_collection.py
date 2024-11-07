import sqlite3

def collect_class_info():
    classes = {}
    while True:
        class_name = input("Enter class room name (or 'done' to finish): ")
        if class_name.lower() == 'done':
            break
        year = input(f"Enter year for {class_name}: ")
        
        courses = collect_course_info()
        
        # Calculate professor availability based on courses
        professors = calculate_professor_availability(courses)
        
        classes[class_name] = {
            'year': year,
            'courses': courses,
            'professors': professors
        }
    return classes

def collect_course_info():
    courses = {}
    while True:
        course_name = input("Enter course name (or 'done' to finish): ")
        if course_name.lower() == 'done':
            break
        weekly_hours = int(input(f"Enter weekly hours for {course_name}: "))
        courses[course_name] = weekly_hours
    return courses

def calculate_professor_availability(courses):
    professors = {}
    for course, hours in courses.items():
        professor_name = input(f"Enter professor name for {course}: ")
        if professor_name in professors:
            professors[professor_name] += hours  # Accumulate hours
        else:
            professors[professor_name] = hours  # Initialize with hours
    return {name: f"{hours} hours weekly" for name, hours in professors.items()}

def collect_lab_info(courses):
    labs = {}
    for course in courses:
        lab_duration = int(input(f"Enter lab duration (in hours) for {course} (0 if no lab): "))
        if lab_duration > 0:
            labs[course] = lab_duration
    return labs

def save_to_db(classes):
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()

    for class_name, details in classes.items():
        year = details['year']
        for name, weekly_hours in details['courses'].items():
            cursor.execute("INSERT INTO Courses (name, weekly_hours) VALUES (?, ?)", (name, weekly_hours))

        for name, availability in details['professors'].items():
            cursor.execute("INSERT INTO Professors (name, availability) VALUES (?, ?)", (name, availability))

        labs = collect_lab_info(details['courses'].keys())
        for course_name, duration in labs.items():
            cursor.execute("SELECT id FROM Courses WHERE name = ?", (course_name,))
            course_id = cursor.fetchone()
            if course_id:
                cursor.execute("INSERT INTO Labs (course_id, duration) VALUES (?, ?)", (course_id[0], duration))

    conn.commit()
    conn.close()
    print("Data saved to database.")

if __name__ == "__main__":
    print("Collecting Class Information...")
    classes = collect_class_info()
    save_to_db(classes)
