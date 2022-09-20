from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
from flask_cors import CORS
from models import setup_db, db_drop_and_create_all, AddressPublicEncryptionKeys, Messages

app = Flask(__name__)
setup_db(app)
CORS(app)

messages = []

# """ uncomment at the first time running the app """
# db_drop_and_create_all()

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

        except IntegrityError as error:
            #if reconnecting a wallet that has been connected before - we will have already stored a the public encryption key
            if "already exists" in error.args[0]:
                return jsonify(success=True, data="Public encryption key already stored")
            else:
                return jsonify(success=False, data="Error collecting public encryption key. Please try reconnecting to MetaMask.")
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

        recipient_public_encryption_key = AddressPublicEncryptionKeys.query.filter(AddressPublicEncryptionKeys.wallet_address == recipient).first().public_encryption_key

        if not recipient_public_encryption_key:
            flash('Recipient not currently using w3mail!')

        message_data = {
            "recipient_pub_key": recipient_public_encryption_key,
            "message": message_content,
            "nonce": int(message_sent_at.strftime('%s'))
        }

        return render_template('encrypt_message.html', data=message_data)


    return render_template('compose.html')
