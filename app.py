from flask import Flask, render_template, request, redirect, session, jsonify, send_file
from analyzer import analyze_logs, save_report
from log_reader import read_logs
from database import connect_db, insert_logs
from ai_model import detect_anomalies
from monitor import monitor_logs, live_data
from email_alert import send_email_alert
import matplotlib.pyplot as plt
import threading
import os

app = Flask(__name__)
app.secret_key = "secret123"

# 📊 PIE CHART
def generate_chart(cursor):
    cursor.execute("SELECT ai_flag, COUNT(*) FROM logs GROUP BY ai_flag")
    data = cursor.fetchall()

    if not data:
        return

    labels = [row[0] for row in data]
    values = [row[1] for row in data]

    if os.path.exists("static/chart.png"):
        os.remove("static/chart.png")

    plt.figure()
    plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.title("Attack Distribution")
    plt.savefig("static/chart.png")
    plt.close()

# 🔐 LOGIN
@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn, cursor = connect_db()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s",
                       (username,password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect("/dashboard")

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

# 🚀 DASHBOARD
@app.route("/dashboard", methods=["GET","POST"])
def dashboard():
    if "user" not in session:
        return redirect("/")

    data = []
    show_chart = False
    summary = {"total":0, "attacks":0, "normal":0}

    if request.method == "POST":
        file = request.files.get("logfile")

        if not file or file.filename == "":
            return render_template("dashboard.html", data=data, show_chart=False, summary=summary)

        filepath = "uploaded_logs.txt"
        file.save(filepath)

        logs = read_logs(filepath)

        data = analyze_logs(logs)
        data = detect_anomalies(data)

        # 📊 SUMMARY
        summary["total"] = len(data)
        summary["attacks"] = sum(1 for row in data if row[5] == "ATTACK")
        summary["normal"] = sum(1 for row in data if row[5] == "NORMAL")

        # 📧 EMAIL ALERT
        if summary["attacks"] > 0:
            send_email_alert("⚠️ Cyber Attack Detected!")

        conn, cursor = connect_db()
        insert_logs(cursor, conn, data)

        generate_chart(cursor)
        save_report(data)

        show_chart = True
        conn.close()

    return render_template("dashboard.html", data=data, show_chart=show_chart, summary=summary)

# 🔴 LIVE API
@app.route("/live")
def live_monitor():
    return jsonify(live_data)

# 📥 DOWNLOAD REPORT
@app.route("/download")
def download():
    return send_file("report.txt", as_attachment=True)

# 🚪 LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ⚡ BACKGROUND MONITOR
def start_monitor():
    monitor_logs("logs.txt")

if __name__ == "__main__":
    threading.Thread(target=start_monitor, daemon=True).start()
    app.run(debug=True)