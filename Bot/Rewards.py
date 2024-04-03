import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('points.db')
if conn:
    print("Connected to SQLite database")
c = conn.cursor()

# Create a table to store user points data
c.execute('''CREATE TABLE IF NOT EXISTS user_points (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                points INTEGER DEFAULT 0
             )''')
conn.commit()

# Function to award points to a user
def award_points(user_id, username, points):
    c.execute('''INSERT INTO user_points (user_id, username, points)
                  VALUES (?, ?, ?)
                  ON CONFLICT(user_id) DO UPDATE SET points = points + ?''', (user_id, username, points, points))
    conn.commit()

# Function to view points of a user
def view_points(user_id):
    try:
        c.execute('''SELECT username, points FROM user_points WHERE user_id = ?''', (user_id,))
        result = c.fetchone()
        if result:
            return f"{result[0]}'s points: {result[1]}"
        else:
            return "User not found."
    except sqlite3.Error as e:
        print("Error retrieving user points:", e)
        return "An error occurred while retrieving user points."
