import sqlite3

conn = sqlite3.connect("airport.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS flights(
    flight_id TEXT PRIMARY KEY,
    boarding_time TEXT,
    departure TEXT,
    gate TEXT,
    status TEXT,
    aircraft TEXT,
    origin TEXT,
    destination TEXT,
    display_time TEXT,
    last_update TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS passenger(
    passenger_id TEXT PRIMARY KEY,
    name TEXT,
    ticket_number TEXT,
    flight_id TEXT,
    boarding_status TEXT,
    seat_number TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS devices(
    device_id TEXT PRIMARY KEY,
    mac_address TEXT,
    status TEXT,
    battery_level INTEGER,
    signal_strength INTEGER,
    last_seen TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS notifications(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT,
    type TEXT,
    created_at TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY,
    password_hash TEXT
)
""")

conn.commit()
conn.close()

print("Tables created")