from flask import Flask, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import time

app = Flask(__name__)

app.secret_key = "local-development-secret"

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=False,
    SESSION_COOKIE_SAMESITE="Lax"
)

users = {}
login_attempts = {}

SESSION_TIMEOUT = 300
MAX_ATTEMPTS = 5
LOCKOUT_TIME = 60


def validate_input(username, password):
    if not username or not password:
        return False

    if len(username) < 3 or len(username) > 30:
        return False

    if len(password) < 8 or len(password) > 100:
        return False

    return True


def is_rate_limited(username):
    current_time = time.time()

    if username not in login_attempts:
        return False

    attempts, first_attempt = login_attempts[username]

    if current_time - first_attempt > LOCKOUT_TIME:
        del login_attempts[username]
        return False

    return attempts >= MAX_ATTEMPTS


def record_failed_attempt(username):
    current_time = time.time()

    if username not in login_attempts:
        login_attempts[username] = [1, current_time]
    else:
        login_attempts[username][0] += 1


def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):

        if "username" not in session:
            return jsonify({"message": "Authentication required"}), 401

        if time.time() - session.get("login_time", 0) > SESSION_TIMEOUT:
            session.clear()
            return jsonify({"message": "Session expired"}), 401

        return function(*args, **kwargs)

    return wrapper


@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    if not data:
        return jsonify({"message": "Invalid request"}), 400

    username = data.get("username")
    password = data.get("password")

    if not validate_input(username, password):
        return jsonify({"message": "Invalid username or password"}), 400

    if username in users:
        return jsonify({"message": "Registration failed"}), 400

    users[username] = generate_password_hash(password)

    return jsonify({"message": "Registration successful"}), 201


@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return jsonify({"message": "Invalid request"}), 400

    username = data.get("username")
    password = data.get("password")

    if is_rate_limited(username):
        return jsonify({"message": "Invalid username or password"}), 401

    if username not in users:
        record_failed_attempt(username)
        return jsonify({"message": "Invalid username or password"}), 401

    if not check_password_hash(users[username], password):
        record_failed_attempt(username)
        return jsonify({"message": "Invalid username or password"}), 401

    login_attempts.pop(username, None)

    session.clear()
    session["username"] = username
    session["login_time"] = time.time()

    return jsonify({"message": "Login successful"}), 200


@app.route("/profile", methods=["GET"])
@login_required
def profile():

    return jsonify({
        "message": "Authenticated successfully",
        "username": session["username"]
    })


@app.route("/logout", methods=["POST"])
def logout():

    session.clear()

    return jsonify({"message": "Logged out successfully"}), 200


if __name__ == "__main__":
    app.run(debug=False)