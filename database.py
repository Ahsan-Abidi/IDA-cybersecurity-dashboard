import mysql.connector

def connect_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="project_user",
        password="1234",
        database="cyber_logs"
    )
    cursor = conn.cursor()
    return conn, cursor

def insert_logs(cursor, conn, data):
    cursor.execute("DELETE FROM logs")

    if not data:
        return

    query = """
    INSERT INTO logs (timestamp, ip, username, status, flag, ai_flag)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.executemany(query, data)
    conn.commit()