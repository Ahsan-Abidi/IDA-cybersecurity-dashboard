import smtplib

def send_email_alert(message):
    sender = "your_email@gmail.com"
    receiver = "receiver_email@gmail.com"
    password = "your_app_password"

    try:
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(sender,password)

        msg = f"Subject: ALERT\n\n{message}"
        server.sendmail(sender,receiver,msg)
        server.quit()

        print("Email sent")

    except Exception as e:
        print("Email error:", e)