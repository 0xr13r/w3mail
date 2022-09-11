from datetime import datetime, timezone
from sre_constants import SUCCESS
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
import os
from flask_cors import CORS
from models import setup_db, db_drop_and_create_all, AddressPublicEncryptionKeys, Messages

app = Flask(__name__)
setup_db(app)
CORS(app)

messages = []

""" uncomment at the first time running the app """
db_drop_and_create_all()

@app.route('/', methods=['GET','POST'])
def home():
    if request.method=='POST':
        data = request.get_json()

        try:
            AddressPublicEncryptionKeys(
                wallet_address=data.get('wallet_address'),
                public_encryption_key=data.get('public_key')
            ).insert()

            return jsonify(success=True, data="Public encryption key stored U+1F50F")
        except Exception as e:
            return jsonify(success=False, data="Public encryption key already stored. ")

    else:
        return render_template('homepage.html')

@app.route('/inbox')
def inbox():
    if messages:
        return render_template('messages.html', messages=messages, heading_message="Recieved Messages")
    else:
        return render_template('no_messages.html')

@app.route('/outbox')
def outbox():
    if messages:
        return render_template('messages.html', messages=messages, heading_message="Sent Messages")
    else:
        return render_template('no_messages.html')

@app.route('/compose/', methods=('GET', 'POST'))
def compose():
    if request.method == 'POST':
        recipient = request.form['recipient']
        message_content = request.form['content']
        message_sent_at = datetime.now().replace(tzinfo=timezone.utc)

        if not recipient:
            flash('Recipient is required!')
        elif not message_content:
            flash('Message is required!')
        else:
            messages.append({'recipient': recipient, 'message': message_content, "sent_at": message_sent_at})

    return render_template('compose.html')
