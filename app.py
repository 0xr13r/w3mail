from datetime import datetime, timezone
import base64
import logging
import os
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
from flask_cors import CORS
from models import setup_db, db_drop_and_create_all, AddressPublicEncryptionKeys, Messages
from ipfs_interact import ipfs_upload, ipfs_download

app = Flask(__name__)
app.secret_key = os.urandom(12)

setup_db(app)
CORS(app)

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
                logging.info(f'Public key for {data.get("wallet_address")} already exists in the database')
                return jsonify(success=True, data="Public encryption key already stored")
            else:
                logging.error(f'Error getting public key for {data.get("wallet_address")}: {error}')
                return jsonify(success=False, data="Error collecting public encryption key. Please try reconnecting to MetaMask.")
    else:
        return render_template('homepage.html')

@app.route('/check_for_messages')
def check_for_messages():
    wallet_address = request.args.get('walletAddress')
    check_wallet = AddressPublicEncryptionKeys.query.filter(AddressPublicEncryptionKeys.wallet_address == wallet_address).first()
    if check_wallet:
        return jsonify(success=True, data=wallet_address)
    else:
        return jsonify(success=False)

@app.route('/fetch_cid_data', methods=['GET','POST'])
def fetch_cid_data():
    data = request.get_json()
    ipfs_cid = data['ipfs_cid']
    try:
        encryptedMessage = ipfs_download(ipfs_cid)
    except Exception as e:
        logging.error(e)
        encryptedMessage = None

    if encryptedMessage:
        return jsonify(success=True, data=encryptedMessage)
    else:
        return jsonify(success=False)
    

@app.route('/inbox/<walletAddress>')
def inbox(walletAddress):
    messages = Messages.query.filter(Messages.recipient_address == walletAddress).order_by(desc(Messages.message_sent_timestamp)).all()
    if messages:
        return render_template('messages.html', messages=messages, heading_message="Recieved Messages 📥")
    else:
        return render_template('no_messages.html')

@app.route('/outbox/<walletAddress>',  methods=('GET', 'POST'))
def outbox(walletAddress):
    if request.method == 'POST':
        send_data = request.get_json()
        successful_upload = ipfs_upload(
            encrypted_message = send_data.get("encryptedMessage"),
            sender = send_data.get("sender"),
            recipient = send_data.get("recipient")
        )
        if successful_upload:
            return jsonify(success=True)
        else:
            return jsonify(success=False)
        
    messages = Messages.query.filter(Messages.sender_address == walletAddress).order_by(desc(Messages.message_sent_timestamp)).all()

    if messages:
        return render_template('messages.html', messages=messages, heading_message="Sent Messages 📤")
    else:
        return render_template('no_messages.html')

@app.route('/compose/', methods=('GET', 'POST'))
def compose():
    if request.method == 'POST':
        sender=request.form['sender']
        recipient = request.form['recipient']
        message_content = request.form['content']
        message_sent_at = datetime.now().replace(tzinfo=timezone.utc)

        recipient_public_encryption_key = AddressPublicEncryptionKeys.query.filter(AddressPublicEncryptionKeys.wallet_address == recipient).first()
        
        if not recipient_public_encryption_key:
            logging.error("Since the recipient is currently not using w3mail we don't have their public encryption key. You cannot send a message at this time")
            flash(f'{recipient} is not currently using w3mail.')
            return render_template('compose.html')

        public_key = recipient_public_encryption_key.public_encryption_key

        message_data = {
            "sender": sender,
            "recipient": recipient,
            "recipient_pub_key": public_key,
            "message": base64.b64encode(message_content.encode('utf8')),
            "nonce": int(message_sent_at.strftime('%s'))
        }

        return render_template('encrypt_message.html', data=message_data)


    return render_template('compose.html')
