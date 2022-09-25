import logging
import os
import w3storage
from models import Messages
from sqlalchemy.exc import IntegrityError

# for mocking ipfs interaction
import time

API_KEY = os.getenv("W3STORAGE_API_TOKEN")
w3 = w3storage.API(token=API_KEY)

mock_ipfs_interaction = {
}

def generate_fake_cid():
    from random import choice
    from string import ascii_lowercase

    return ''.join(choice(ascii_lowercase) for i in range(59))

def ipfs_upload(encrypted_message:str, sender: str, recipient:str) -> bool:
    cid = generate_fake_cid() 
    
    #this is the actual code we need here to upload to ipfs
    #w3.post_car(encrypted_message)

    #remove once tested the encryption and decryption functions 
    #and replace with real interaction with ipfs
    mock_ipfs_interaction[cid]=encrypted_message

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
    #test code
    time.sleep(1)
    encrypted_message = mock_ipfs_interaction[cid]
    return encrypted_message

    #this is the actual code we need here to download from ipfs
    # return w3.car(cid)



