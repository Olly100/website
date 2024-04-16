from flask import Flask, render_template, request, redirect
from datetime import datetime
import smtplib
from email.message import EmailMessage
import csv

# settings.py
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

EMAIL_TO = os.environ.get("EMAIL_TO")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
EMAIL_LOGIN = os.environ.get("EMAIL_LOGIN")


app = Flask(__name__)


@app.route("/")
def my_home():
    return render_template('index.html')


@app.route("/<string:page_name>")
def page_template(page_name):
    return render_template(page_name)

def write_to_csv(timestamp, email, subject,message):
    with open('database.csv', newline='', mode='a') as db2:
        csv_writer = csv.writer(db2,delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([timestamp, email, subject,message])


def email_notification(timestamp, email, subject,message):
    email_msg = EmailMessage()
    email_msg['from'] = "Olly Smith Website"
    email_msg['to'] = EMAIL_TO
    email_msg['subject'] = 'User Form Submitted!'
    email_msg.set_content(f'Submitted: {timestamp}\n Email: {email}\n Subject: {subject}\n Message: {message}')

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(EMAIL_LOGIN, EMAIL_PASSWORD)
        smtp.send_message(email_msg)
        

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method== 'POST':
        try:
            data = request.form.to_dict()
            email = data["email"]
            subject = data["subject"]
            message = data["message"]
            timestamp = datetime.now()
            write_to_csv(timestamp, email, subject,message)
            email_notification(timestamp, email, subject,message)
            return redirect('/thankyou.html')
        except:
            return 'did not save to db'
    else:
        return 'Something went wrong, you might need to try again or just email me osmith100@gmail.com'
