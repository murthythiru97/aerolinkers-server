import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("airport.db")
cursor = conn.cursor()

flights = [
    ("AI202", "18:30", "19:00", "Gate 12", "On Time", "Boeing 737", "Delhi", "Mumbai", "18:30", "2023-10-01 10:00:00"),
    ("AI305", "19:00", "19:30", "Gate 15", "Delayed", "Airbus A320", "Mumbai", "Bangalore", "19:15", "2023-10-01 10:30:00")
]

cursor.executemany(
    "INSERT OR IGNORE INTO flights VALUES (?,?,?,?,?,?,?,?,?,?)",
    flights
)

passengers = [
    ("TB2376", "THIRU", "TB2376", "AI202", "Boarded", "12B"),
    ("AB1234", "John Doe", "AB1234", "AI305", "Waiting", "14A")
]

cursor.executemany(
    "INSERT OR IGNORE INTO passenger VALUES (?,?,?,?,?,?)",
    passengers
)

devices = [
    ("DEV001", "08:3A:F2:A8:31:F8", "Online", 85, 90, "2023-10-01 10:00:00"),
    ("DEV002", "08:3A:F2:A8:31:F9", "Offline", 20, 30, "2023-10-01 09:00:00")
]

cursor.executemany(
    "INSERT OR IGNORE INTO devices VALUES (?,?,?,?,?,?)",
    devices
)

notifications = [
    (1, "Flight AI202 boarding now", "info", "2023-10-01 10:00:00"),
    (2, "Device DEV001 battery low", "warning", "2023-10-01 09:30:00")
]

cursor.executemany(
    "INSERT OR IGNORE INTO notifications VALUES (?,?,?,?)",
    notifications
)

users = [
    ("Aerolinkers", generate_password_hash("Aerolinkers123"))
]

cursor.executemany(
    "INSERT OR IGNORE INTO users VALUES (?,?)",
    users
)

conn.commit()
conn.close()

print("Data inserted")