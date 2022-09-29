import datetime
import os
import json
from sqlalchemy import Column, String, BigInteger, Boolean, create_engine
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

'''
setup_db(app):
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    database_name ='w3mail_web_app'
    default_database_path= "postgresql://{}:{}@{}/{}".format('postgres', 'password', 'localhost:5432', database_name)
    database_path = os.getenv('DATABASE_URL', default_database_path)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

'''
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.configure_mappers()
    db.create_all()
    db.session.commit()


class AddressPublicEncryptionKeys(db.Model):
    __tablename__ = 'address_public_encryption_key_map'

    id = Column(BigInteger, primary_key=True)
    wallet_address = Column(String(255), unique=True)
    public_encryption_key = Column(String(255), unique=True)


    def __init__(
        self, 
        wallet_address, 
        public_encryption_key, 
    ):
        self.wallet_address = wallet_address
        self.public_encryption_key = public_encryption_key

    def __repr__(self): 
        return "(%r, %r)" %(self.wallet_address, self.public_encryption_key)

    def insert(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self):
        db.session.commit()

class Messages(db.Model):
    __tablename__ = 'messages'

    id = Column(BigInteger, primary_key=True)
    sender_address = Column(String(255))
    recipient_address = Column(String(255))
    ipfs_cid = Column(String(255), unique=True)
    message_sent_timestamp = Column(db.DateTime)
    is_message_read = Column(Boolean)
    message_last_read_timestamp = Column(db.DateTime)

    def __init__(
        self, 
        sender_address, 
        recipient_address, 
        ipfs_cid,
        is_message_read= False,
        message_last_read_timestamp = None,

    ):
        self.sender_address = sender_address
        self.recipient_address = recipient_address
        self.ipfs_cid = ipfs_cid
        self.message_sent_timestamp = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc)
        self.is_message_read = is_message_read
        self.message_last_read_timestamp = message_last_read_timestamp

    def __repr__(self): 
        return json.dumps({
            "sender":self.sender_address,
            "recipient": self.recipient_address,
            "ipfs_cid": self.ipfs_cid,
            "sent_at": self.message_sent_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "is_read":self.is_message_read,
            "read_at": None if not self.message_last_read_timestamp else self.message_last_read_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })
        # return "(%r, %r, %r, %r, %r, %r)" %(
        #     self.sender_address,
        #     self.recipient_address,
        #     self.ipfs_cid,
        #     self.message_sent_timestamp,
        #     self.is_message_read,
        #     self.message_read_timestamp
        # )

    def insert(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def update(self):
        db.session.commit()
