# ✈️ Airport Smart Band Server

A Flask-based web application for managing airport smart band systems.  
This project handles devices, passengers, flights, and notifications, enabling smooth airport operations and real-time data access.

---

## 🚀 Features

- 🔐 User Authentication (Secure login system)
- 📊 Dashboard with device, flight, and notification overview
- 📱 Device Monitoring (battery, signal strength, status)
- ✈️ Flight Management (view & update boarding time)
- 🧑‍✈️ Passenger Search using PNR
- 🔔 Notifications system
- 🔄 Device Sync API for ESP32 / IoT devices
- 🗄️ SQLite database (auto-created)

---

## 🛠️ Technologies Used

- Backend: Python (Flask)
- Frontend: HTML, Bootstrap
- Database: SQLite
- Authentication: Werkzeug Security
- Templating: Jinja2

---

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/murthythiru97/aerolinkers-server.git
cd aerolinkers-server
Install dependencies:
pip install flask werkzeug
Run the server:
python server.py
Open in browser:
http://127.0.0.1:7000
🔑 Default Login
Username: Aerolinkers
Password: Aerolinkers123
🧩 API Endpoints
🔄 Sync Device

POST /sync

Request:

{
  "device_id": "08:3A:F2:A8:31:F8",
  "pnr": "TB2376"
}

Response:

{
  "device_id": "DEV001",
  "pnr": "TB2376",
  "name": "Thiru",
  "flight": "AI202",
  "seat": "12B",
  "boarding_time": "18:30"
}
✈️ Flights

GET /flights

🧑 Passenger

GET /passenger/<pnr>

🗄️ Database Tables
users
devices
flights
passenger
notifications
💡 Use Case
Airport smart band system
IoT-based passenger tracking
ESP32 / RFID projects
Academic projects
🔒 Security Notes
Change secret_key before deployment
Use strong credentials
Disable debug mode in production
