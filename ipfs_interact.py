import logging
import os
import w3storage
from models import Messages
from sqlalchemy.exc import IntegrityError

def get_w3_object():
    API_KEY = os.getenv("W3STORAGE_API_TOKEN")
    w3 = w3storage.API(token=API_KEY)

    return w3

def ipfs_upload(encrypted_message:str, sender: str, recipient:str) -> bool:
    
    w3 = get_w3_object()
    cid = w3.post_car(encrypted_message)

    try:
        Messages(
            sender_address = sender,
            recipient_address = recipient,
            ipfs_cid = cid
        ).insert()
        return True
    except IntegrityError as error:
        logging.error(error)
        return False

def ipfs_download(cid):

    w3 = get_w3_object()
    raw_resp = w3.car(cid)
    return '0x'+raw_resp.split(b'0x')[1].decode()



