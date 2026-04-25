from collections import defaultdict

def analyze_logs(logs):
    analyzed = []
    failed_attempts = defaultdict(int)
    ip_activity = defaultdict(int)

    for log in logs:
        try:
            parts = log.strip().split("|")

            timestamp = parts[0].strip()
            ip = parts[1].split(":")[1].strip()
            username = parts[2].split(":")[1].strip()
            status = parts[3].split(":")[1].strip()

            flag = "NORMAL"

            ip_activity[ip] += 1

            if status == "FAILED":
                failed_attempts[ip] += 1
                if failed_attempts[ip] >= 4:
                    flag = "BRUTE_FORCE"

            if username.lower() == "unknown":
                flag = "UNKNOWN_USER"

            hour = int(timestamp.split(" ")[1].split(":")[0])
            if hour < 5:
                flag = "ODD_HOURS"

            if ip_activity[ip] > 6:
                flag = "DDOS_SUSPECT"

            analyzed.append((timestamp, ip, username, status, flag))

        except:
            continue

    return analyzed

def save_report(data):
    with open("report.txt","w") as f:
        for row in data:
            f.write(str(row)+"\n")