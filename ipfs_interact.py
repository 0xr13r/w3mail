import logging
import os
import w3storage
from models import Messages
from sqlalchemy.exc import IntegrityError

API_KEY = os.getenv("W3STORAGE_API_TOKEN")
w3 = w3storage.API(token=API_KEY)

def generate_fake_cid():
    from random import choice
    from string import ascii_lowercase

    return ''.join(choice(ascii_lowercase) for i in range(59))

def ipfs_upload(encrypted_message:str, sender: str, recipient:str) -> bool:
    cid = generate_fake_cid() #w3.post_car(encrypted_message)

    try:
        Messages(
            sender_address = sender,
            receipient_address = recipient,
            ipfs_cid = cid
        ).insert()
        return True
    except IntegrityError as error:
        logging.error(error)
        return False

def ipfs_download(cid):
    return w3.car(cid)



