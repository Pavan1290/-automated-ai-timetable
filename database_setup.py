import sqlite3

# Connect to SQLite database (or create it)
conn = sqlite3.connect('timetable.db')
cursor = conn.cursor()

# Create Courses table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Courses (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    weekly_hours INTEGER NOT NULL
)
''')

# Create Professors table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Professors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    availability TEXT NOT NULL
)
''')

# Create Classrooms table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Classrooms (
    id INTEGER PRIMARY KEY,
    room_number TEXT NOT NULL,
    capacity INTEGER NOT NULL
)
''')

# Create Timetable table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Timetable (
    id INTEGER PRIMARY KEY,
    course_id INTEGER,
    professor_id INTEGER,
    classroom_id INTEGER,
    day TEXT NOT NULL,
    time_slot TEXT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES Courses (id),
    FOREIGN KEY (professor_id) REFERENCES Professors (id),
    FOREIGN KEY (classroom_id) REFERENCES Classrooms (id)
)
''')
# Create Labs table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Labs (
    id INTEGER PRIMARY KEY,
    course_id INTEGER,
    duration INTEGER NOT NULL,  -- duration in hours
    FOREIGN KEY (course_id) REFERENCES Courses (id)
)
''')


# Commit changes and close the connection
conn.commit()
conn.close()
