from functools import wraps

from flask import (
    Flask,
    request,
    jsonify,
    render_template_string,
    redirect,
    url_for,
    session,
    flash,
)
from jinja2 import DictLoader
from werkzeug.security import check_password_hash, generate_password_hash
import os
import sqlite3
import datetime

app = Flask(__name__)
app.secret_key = "change-me-to-a-secure-random-value"

# Default credentials (shown on the login page for demo purposes)
DEFAULT_USERNAME = "Aerolinkers"
DEFAULT_PASSWORD = "Aerolinkers123"

# Templates stored in memory so the app works without a templates folder.
app.jinja_loader = DictLoader(
    {
        "base.html": """<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>{% block title %}Airport Smart Band{% endblock %}</title>

    <!-- Bootstrap (CDN) -->
    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css\" rel=\"stylesheet\" crossorigin=\"anonymous\"> 

    <style>
      body {
        min-height: 100vh;
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://images.unsplash.com/photo-1436491865332-7a61a109cc05?ixlib=rb-4.0.3&auto=format&fit=crop&w=1950&q=80') no-repeat center center fixed;
        background-size: cover;
        color: #333;
      }

      .brand {
        font-weight: 700;
        letter-spacing: 0.07em;
      }

      .card {
        border: 0;
        border-radius: 14px;
        box-shadow: 0 10px 35px rgba(46, 61, 73, 0.12);
      }

      .form-control:focus {
        box-shadow: 0 0 0 0.2rem rgba(9, 132, 227, 0.25);
      }

      footer {
        font-size: 0.85rem;
        color: #6c757d;
      }
    </style>

    {% block extra_head %}{% endblock %}
  </head>
  <body>
    <nav class=\"navbar navbar-expand-lg navbar-light bg-white shadow-sm\">
      <div class=\"container\">
        <a class=\"navbar-brand brand\" href=\"{{ url_for('dashboard') }}\">Airport Smart Band</a>
        <div class=\"collapse navbar-collapse\">
          <ul class=\"navbar-nav ms-auto\">
            {% if session.get('user') %}
            <li class=\"nav-item\">
              <a class=\"nav-link\" href=\"{{ url_for('logout') }}\">Logout</a>
            </li>
            {% endif %}
          </ul>
        </div>
      </div>
    </nav>

    <main class=\"container py-5\">
      {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
      <div class=\"row justify-content-center mb-4\">
        <div class=\"col-md-8\">
          {% for category, message in messages %}
          <div class=\"alert alert-{{ category }} alert-dismissible fade show\" role=\"alert\">
            {{ message }}
            <button type=\"button\" class=\"btn-close\" data-bs-dismiss=\"alert\" aria-label=\"Close\"></button>
          </div>
          {% endfor %}
        </div>
      </div>
      {% endif %}
      {% endwith %}

      {% block content %}{% endblock %}
    </main>

    <footer class=\"text-center py-4\">
      <div class=\"container\">
        <span class=\"text-muted\">© {{ config.get('APP_NAME', 'Airport Smart Band') }} {{ current_year }}</span>
      </div>
    </footer>

    <script src=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js\" crossorigin=\"anonymous\"></script>
    {% block extra_scripts %}{% endblock %}
  </body>
</html>
""",
        "login.html": """{% extends 'base.html' %}

{% block title %}Login – Airport Smart Band{% endblock %}

{% block content %}
<div class=\"row justify-content-center\">
  <div class=\"col-md-6 col-lg-5\">
    <div class=\"card p-4\">
      <h3 class=\"mb-3 text-center\">Sign in</h3>
      <form method=\"post\" novalidate>
        <div class=\"mb-3\">
          <label for=\"username\" class=\"form-label\">Username</label>
          <input
            id=\"username\"
            name=\"username\"
            type=\"text\"
            class=\"form-control\"
            placeholder="Enter username"
            autocomplete="username"
            required
          />
        </div>

        <div class=\"mb-3\">
          <label for=\"password\" class=\"form-label\">Password</label>
          <input
            id=\"password\"
            name=\"password\"
            type=\"password\"
            class=\"form-control\"
            placeholder="Enter password"
            autocomplete="current-password"
            required
          />
        </div>

        <button type=\"submit\" class=\"btn btn-primary w-100\">Login</button>
      </form>

      <div class=\"text-muted text-center mt-3\">
        Enter your login credentials.        <br />
        <small>Demo credentials: <strong>Username:</strong> <code>{{ default_username }}</code> <strong>Password:</strong> <code>{{ default_password }}</code></small>      </div>
    </div>
  </div>
</div>
{% endblock %}
""",
        "dashboard.html": """{% extends 'base.html' %}

{% block title %}Dashboard – Airport Smart Band{% endblock %}

{% block content %}
<div class=\"row mb-4\">
  <div class=\"col-md-3\">
    <div class=\"card p-3 shadow-sm\">
      <div class=\"d-flex align-items-center\">
        <div class=\"me-3\">
          <div class=\"bg-primary rounded-circle text-white d-flex align-items-center justify-content-center\" style=\"width:44px;height:44px;\">
            <span class=\"fs-4\">📱</span>
          </div>
        </div>
        <div>
          <div class=\"text-muted\">Total Devices</div>
          <div class=\"fs-4 fw-bold\">{{ total_devices }}</div>
        </div>
      </div>
    </div>
  </div>
  <div class=\"col-md-3\">
    <div class=\"card p-3 shadow-sm\">
      <div class=\"d-flex align-items-center\">
        <div class=\"me-3\">
          <div class=\"bg-success rounded-circle text-white d-flex align-items-center justify-content-center\" style=\"width:44px;height:44px;\">
            <span class=\"fs-4\">✅</span>
          </div>
        </div>
        <div>
          <div class=\"text-muted\">Active Devices</div>
          <div class=\"fs-4 fw-bold\">{{ active_devices }}</div>
        </div>
      </div>
    </div>
  </div>
  <div class=\"col-md-3\">
    <div class=\"card p-3 shadow-sm\">
      <div class=\"d-flex align-items-center\">
        <div class=\"me-3\">
          <div class=\"bg-info rounded-circle text-white d-flex align-items-center justify-content-center\" style=\"width:44px;height:44px;\">
            <span class=\"fs-4\">✈️</span>
          </div>
        </div>
        <div>
          <div class=\"text-muted\">Total Flights</div>
          <div class=\"fs-4 fw-bold\">{{ total_flights }}</div>
        </div>
      </div>
    </div>
  </div>
  <div class=\"col-md-3\">
    <div class=\"card p-3 shadow-sm\">
      <div class=\"d-flex align-items-center\">
        <div class=\"me-3\">
          <div class=\"bg-warning rounded-circle text-white d-flex align-items-center justify-content-center\" style=\"width:44px;height:44px;\">
            <span class=\"fs-4\">🔔</span>
          </div>
        </div>
        <div>
          <div class=\"text-muted\">Notifications</div>
          <div class=\"fs-4 fw-bold\">{{ notifications|length }}</div>
        </div>
      </div>
    </div>
  </div>
</div>

{% if passenger %}
<div class=\"row mb-4\">
  <div class=\"col-12\">
    <div class=\"card\">
      <div class=\"card-header\">
        <h5>Passenger Search Result</h5>
      </div>
      <div class=\"card-body\">
        <p><strong>PNR:</strong> {{ passenger[0] }}</p>
        <p><strong>Name:</strong> {{ passenger[1] }}</p>
        <p><strong>Flight:</strong> {{ passenger[2] }}</p>
        <p><strong>Seat:</strong> {{ passenger[3] }}</p>
        <p><strong>Boarding Time:</strong> {{ passenger[4] }}</p>
      </div>
    </div>
  </div>
</div>
{% endif %}

<div class=\"row\">
  <div class=\"col-lg-8\">
    <div class=\"card mb-4\">
      <div class=\"card-header\">
        <ul class=\"nav nav-tabs card-header-tabs\" role=\"tablist\">
          <li class=\"nav-item\">
            <a class=\"nav-link active\" data-bs-toggle=\"tab\" href=\"#devices\" role=\"tab\">Devices</a>
          </li>
          <li class=\"nav-item\">
            <a class=\"nav-link\" data-bs-toggle=\"tab\" href=\"#flights\" role=\"tab\">Flights</a>
          </li>
          <li class=\"nav-item\">
            <a class=\"nav-link\" data-bs-toggle=\"tab\" href=\"#notifications\" role=\"tab\">Notifications</a>
          </li>
        </ul>
      </div>
      <div class=\"card-body tab-content\">
        <div class=\"tab-pane fade show active\" id=\"devices\" role=\"tabpanel\">
          <h5 class=\"card-title\">Devices</h5>
          <p class=\"text-muted\">List of registered devices (mock data).</p>
          <div class=\"table-responsive\">
            <table class=\"table table-sm table-hover\">
              <thead>
                <tr>
                  <th>Device ID</th>
                  <th>MAC Address</th>
                  <th>Status</th>
                  <th>Battery</th>
                  <th>Signal</th>
                  <th>Last Seen</th>
                </tr>
              </thead>
              <tbody>
                {% for device in devices %}
                <tr>
                  <td>{{ device[0] }}</td>
                  <td>{{ device[1] }}</td>
                  <td>{{ device[2] or 'unknown' }}</td>
                  <td>{{ device[3] if device[3] is not none else '-' }}%</td>
                  <td>{{ device[4] if device[4] is not none else '-' }} dBm</td>
                  <td>{{ device[5][:16].replace('T', ' ') if device[5] else '-' }}</td>
                </tr>
                {% endfor %}
              </tbody>
            </table>
          </div>
        </div>

        <div class=\"tab-pane fade\" id=\"flights\" role=\"tabpanel\">
          <h5 class=\"card-title\">Flights</h5>
          <div class=\"table-responsive\">
            <table class=\"table table-sm table-hover\">
              <thead>
                <tr>
                  <th>Flight</th>
                  <th>Departure</th>
                  <th>Gate</th>
                  <th>Status</th>
                  <th>Boarding</th>
                  <th class=\"text-end\">Update</th>
                </tr>
              </thead>
              <tbody>
                {% for flight, boarding, departure, gate, status in flights %}
                <tr>
                  <td>{{ flight }}</td>
                  <td>{{ departure or '-' }}</td>
                  <td>{{ gate or '-' }}</td>
                  <td>{{ status or '-' }}</td>
                  <td>{{ boarding }}</td>
                  <td class=\"text-end\">
                    <form method=\"post\" action=\"{{ url_for('update') }}\" class=\"d-inline\">
                      <input type=\"hidden\" name=\"flight\" value=\"{{ flight }}\">
                      <div class=\"input-group input-group-sm\">
                        <input type=\"text\" name=\"new_time\" class=\"form-control\" placeholder=\"HH:MM\" value=\"{{ boarding }}\" required>
                        <button class=\"btn btn-outline-primary btn-sm\" type=\"submit\">Update</button>
                      </div>
                    </form>
                  </td>
                </tr>
                {% endfor %}
              </tbody>
            </table>
          </div>
        </div>

        <div class=\"tab-pane fade\" id=\"notifications\" role=\"tabpanel\">
          <h5 class=\"card-title\">Recent Notifications</h5>
          {% if notifications %}
          <div class=\"list-group\">
            {% for n in notifications %}
            <div class=\"list-group-item list-group-item-action py-3\">
              <div class=\"d-flex w-100 justify-content-between\">
                <h6 class=\"mb-1\">{{ n[1] }}</h6>
                <small class=\"text-muted\">{{ n[3][:16].replace('T', ' ') }}</small>
              </div>
              <small class=\"text-muted\">Type: {{ n[2] }}</small>
            </div>
            {% endfor %}
          </div>
          {% else %}
          <p class=\"text-muted\">No notifications yet.</p>
          {% endif %}
        </div>
      </div>
    </div>
  </div>
</div>
{% endblock %}
""",
    }
)

DB = os.path.join(os.path.dirname(__file__), "airport.db")

# Keep these endpoints open without requiring login.
NO_AUTH_ENDPOINTS = {"login", "static", "sync"}


def init_db():
    """Ensure required tables exist and seed a default admin user.

    If the database file is corrupted, it is deleted and rebuilt.
    """

    if os.path.exists(DB):
        try:
            os.remove(DB)
        except OSError:
            pass

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    def ensure_column(table: str, column: str, col_type: str):
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [row[1] for row in cursor.fetchall()]
        if column not in columns:
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}")

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS flights(
            flight_id TEXT PRIMARY KEY,
            boarding_time TEXT
        )
        """
    )
    ensure_column("flights", "departure", "TEXT")
    ensure_column("flights", "gate", "TEXT")
    ensure_column("flights", "status", "TEXT")
    ensure_column("flights", "aircraft", "TEXT")
    ensure_column("flights", "origin", "TEXT")
    ensure_column("flights", "destination", "TEXT")
    ensure_column("flights", "display_time", "TEXT")
    ensure_column("flights", "last_update", "TEXT")

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS passenger(
            passenger_id TEXT PRIMARY KEY,
            name TEXT,
            ticket_number TEXT,
            flight_id TEXT,
            boarding_status TEXT
        )
        """
    )
    ensure_column("passenger", "seat_number", "TEXT")

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS devices(
            device_id TEXT PRIMARY KEY,
            mac_address TEXT
        )
        """
    )
    ensure_column("devices", "status", "TEXT")
    ensure_column("devices", "battery_level", "INTEGER")
    ensure_column("devices", "signal_strength", "INTEGER")
    ensure_column("devices", "last_seen", "TEXT")

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS notifications(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT,
            type TEXT,
            created_at TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users(
            username TEXT PRIMARY KEY,
            password_hash TEXT
        )
        """
    )

    # Seed default admin user (only if not already present)
    password_hash = generate_password_hash(DEFAULT_PASSWORD)
    cursor.execute(
        "INSERT OR REPLACE INTO users(username, password_hash) VALUES (?, ?)",
        (DEFAULT_USERNAME, password_hash),
    )

    # Seed sample flights (only if not already present)
    cursor.execute(
        "INSERT OR IGNORE INTO flights(flight_id, boarding_time, departure, gate, status, aircraft, origin, destination, display_time, last_update) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        ("AI202", "18:30", "19:00", "Gate 12", "On Time", "Boeing 737", "Delhi", "Mumbai", "18:30", "2023-10-01 10:00:00"),
    )
    cursor.execute(
        "INSERT OR IGNORE INTO flights(flight_id, boarding_time, departure, gate, status, aircraft, origin, destination, display_time, last_update) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        ("AI305", "19:00", "19:30", "Gate 15", "Delayed", "Airbus A320", "Mumbai", "Bangalore", "19:15", "2023-10-01 10:30:00"),
    )
    # Ensure sample flight status is populated if row already existed without those columns
    cursor.execute(
        "UPDATE flights SET departure = ?, gate = ?, status = ?, aircraft = ?, origin = ?, destination = ?, display_time = ?, last_update = ? WHERE flight_id = ? AND (departure IS NULL OR gate IS NULL OR status IS NULL)",
        ("19:00", "Gate 12", "On Time", "Boeing 737", "Delhi", "Mumbai", "18:30", "2023-10-01 10:00:00", "AI202"),
    )
    cursor.execute(
        "UPDATE flights SET departure = ?, gate = ?, status = ?, aircraft = ?, origin = ?, destination = ?, display_time = ?, last_update = ? WHERE flight_id = ? AND (departure IS NULL OR gate IS NULL OR status IS NULL)",
        ("19:30", "Gate 15", "Delayed", "Airbus A320", "Mumbai", "Bangalore", "19:15", "2023-10-01 10:30:00", "AI305"),
    )

    # Seed sample passengers (only if not already present)
    cursor.execute(
        "INSERT OR IGNORE INTO passenger(passenger_id, name, ticket_number, flight_id, boarding_status, seat_number) VALUES (?, ?, ?, ?, ?, ?)",
        ("TB2376", "Thiru", "TB2376", "AI202", "Boarded", "12B"),
    )
    cursor.execute(
        "INSERT OR IGNORE INTO passenger(passenger_id, name, ticket_number, flight_id, boarding_status, seat_number) VALUES (?, ?, ?, ?, ?, ?)",
        ("AB1234", "John Doe", "AB1234", "AI305", "Waiting", "14A"),
    )

    # Seed sample devices (only if not already present)
    cursor.execute(
        "INSERT OR IGNORE INTO devices(device_id, mac_address, status, battery_level, signal_strength, last_seen) VALUES (?, ?, ?, ?, ?, ?)",
        ("DEV001", "08:3A:F2:A8:31:F8", "active", 95, -45, datetime.datetime.now().isoformat()),
    )

    # Seed sample notifications (only if not already present)
    cursor.execute(
        "INSERT OR IGNORE INTO notifications(message, type, created_at) VALUES (?, ?, ?)",
        ("Flight AI202 boarding now", "info", datetime.datetime.now().isoformat()),
    )
    cursor.execute(
        "INSERT OR IGNORE INTO notifications(message, type, created_at) VALUES (?, ?, ?)",
        ("Device DEV001 battery low", "warning", datetime.datetime.now().isoformat()),
    )

    conn.commit()
    conn.close()


# Initialize DB (safe to call on every restart)
init_db()


@app.before_request
def require_login():
    """Redirect users to the login page unless they are authenticated."""
    # Flask uses 'static' for static file serving; we want to allow it.
    if request.endpoint in NO_AUTH_ENDPOINTS or request.endpoint is None:
        return

    if "user" not in session:
        return redirect(url_for("login"))


def get_db_connection():
    """Return a new SQLite connection."""
    return sqlite3.connect(DB)


def login_required(view):
    """Simple login required decorator."""

    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped_view


@app.route("/")
def home():
    return redirect(url_for("dashboard"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE username=?", (username,))
        row = cursor.fetchone()
        conn.close()

        if row and check_password_hash(row[0], password):
            session["user"] = username
            return redirect(url_for("dashboard"))

        flash("Invalid username or password", "danger")

    return render_template_string(
        "{% include 'login.html' %}",
        current_year=datetime.datetime.now().year,
        default_username=DEFAULT_USERNAME,
        default_password=DEFAULT_PASSWORD,
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    """Dashboard showing flights, devices, and notifications."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM devices")
    total_devices = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM flights")
    total_flights = cursor.fetchone()[0]

    cursor.execute("SELECT device_id, mac_address, status, battery_level, signal_strength, last_seen FROM devices")
    devices = cursor.fetchall()

    cursor.execute("SELECT flight_id, boarding_time, departure, gate, status FROM flights ORDER BY flight_id")
    flights = cursor.fetchall()

    cursor.execute("SELECT id, message, type, created_at FROM notifications ORDER BY id DESC LIMIT 10")
    notifications = cursor.fetchall()

    conn.close()

    return render_template_string(
        "{% include 'dashboard.html' %}",
        total_devices=total_devices,
        active_devices=total_devices,
        total_flights=total_flights,
        devices=devices,
        notifications=notifications,
        flights=flights,
        current_year=datetime.datetime.now().year,
    )


@app.route("/search", methods=["POST"])
@login_required
def search():
    pnr = request.form.get("pnr")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT passenger.passenger_id,
               passenger.name,
               passenger.flight_id,
               passenger.seat_number,
               flights.boarding_time
        FROM passenger
        JOIN flights ON passenger.flight_id = flights.flight_id
        WHERE passenger.passenger_id = ?
        """,
        (pnr,),
    )

    passenger = cursor.fetchone()
    conn.close()

    return render_template_string(
        "{% include 'dashboard.html' %}",
        flights=[],
        passenger=passenger,
        search_pnr=pnr,
        current_year=datetime.datetime.now().year,
    )


# Keep the existing APIs for device sync and tooling.

@app.route("/sync", methods=["POST"])
def sync():
    data = request.json

    mac = data.get("device_id")
    pnr = data.get("pnr")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT device_id FROM devices WHERE mac_address=?",
        (mac,)
    )
    device = cursor.fetchone()

    cursor.execute(
        """
        SELECT passenger.passenger_id,
               passenger.name,
               passenger.flight_id,
               passenger.seat_number,
               flights.boarding_time
        FROM passenger
        JOIN flights
        ON passenger.flight_id = flights.flight_id
        WHERE passenger.passenger_id = ?
        """,
        (pnr,),
    )

    result = cursor.fetchone()

    conn.close()

    if device and result:
        return jsonify(
            {
                "device_id": device[0],
                "pnr": result[0],
                "name": result[1],
                "flight": result[2],
                "seat": result[3],
                "boarding_time": result[4],
            }
        )

    return jsonify({"message": "Passenger or device not found"})


@app.route("/flights")
@login_required
def flights():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT flight_id, boarding_time, departure, gate, status, aircraft, origin, destination, display_time, last_update FROM flights")
    data = cursor.fetchall()

    conn.close()

    return jsonify(
        [
            {
                "flight_id": f[0],
                "boarding_time": f[1],
                "departure": f[2],
                "gate": f[3],
                "status": f[4],
                "aircraft": f[5],
                "origin": f[6],
                "destination": f[7],
                "display_time": f[8],
                "last_update": f[9],
            }
            for f in data
        ]
    )


@app.route("/passenger/<pnr>")
@login_required
def passenger(pnr):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT passenger.passenger_id,
               passenger.name,
               passenger.flight_id,
               passenger.seat_number,
               flights.boarding_time
        FROM passenger
        JOIN flights
        ON passenger.flight_id = flights.flight_id
        WHERE passenger.passenger_id = ?
        """,
        (pnr,),
    )

    data = cursor.fetchone()

    conn.close()

    if not data:
        return jsonify({"message": "Passenger not found"}), 404

    return jsonify(
        {
            "pnr": data[0],
            "name": data[1],
            "flight": data[2],
            "seat": data[3],
            "boarding_time": data[4],
        }
    )


@app.route("/update", methods=["POST"])
@login_required
def update():
    flight = request.form.get("flight")
    new_time = request.form.get("new_time")

    if not flight or not new_time:
        flash("Flight and new boarding time are required", "danger")
        return redirect(url_for("dashboard"))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE flights SET boarding_time=? WHERE flight_id=?",
        (new_time, flight),
    )

    conn.commit()
    conn.close()

    flash(f"Boarding time for {flight} updated to {new_time}", "success")
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    # Bind to localhost only so the server is not reachable from other machines.
    # If you want to allow access from other devices on the same network, change
    # host to "0.0.0.0" and ensure the machine has proper network/firewall controls.
    app.run(host="127.0.0.1", port=7000, debug=True)
