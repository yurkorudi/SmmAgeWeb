from flask import Flask, request, redirect, url_for, render_template
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "smmageofficialpage@gmail.com"
APP_PASSWORD = "dlrz aipj hrxa tsmq"

@app.route('/')
def home():
    return render_template('Homepage.html')

@app.route('/about')
def about():
    return render_template('About.html')




@app.route('/contacts')
def contacts():
    return render_template('Contacts.html')


@app.route('/send-request', methods=['POST'])
def send_request():
    name = request.form.get("name", "—")
    phone = request.form.get("phone", "—")
    business = request.form.get("business", "—")
    message = request.form.get("message", "—")

    text = f"""Нова заявка з сайту

Ім'я:      {name}
Телефон:   {phone}
Бізнес:    {business}

Повідомлення:
{message}
"""

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = SENDER_EMAIL
    msg['Subject'] = "Нова заявка з сайту"
    msg.attach(MIMEText(text, 'plain', 'utf-8'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
            server.starttls()
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)

        print("Лист успішно відправлено!")
        return redirect(url_for('home'))

    except Exception as e:
        print("ПОМИЛКА при відправці пошти:", str(e))
        return f"""
        <h2>Щось пішло не так</h2>
        <p>Не вдалося надіслати заявку. Спробуйте пізніше або напишіть нам напряму.</p>
        <p style="color: #e74c3c; font-family: monospace;">Помилка: {str(e)}</p>
        <a href="/">На головну</a>
        """, 500


if __name__ == '__main__':
    app.run(debug=True)