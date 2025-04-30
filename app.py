from flask import Flask, request, jsonify
from flask_cors import CORS  # ← Add this line
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, origins=["https://shawncportfolio.uk"])  # ← Allow CORS for your portfolio domain

EMAIL_ADDRESS = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASS')

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.get_json()
    name = data.get('name')
    sender_email = data.get('email')
    message_body = data.get('message')

    if not all([name, sender_email, message_body]):
        return jsonify({'error': 'Missing fields'}), 400

    try:
        msg = EmailMessage()
        msg['Subject'] = f"New message from {name}"
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS
        msg.set_content(f"From: {name} <{sender_email}>\n\nMessage:\n{message_body}")

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)


        return jsonify({'message': 'Email sent successfully!'}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Failed to send email'}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
