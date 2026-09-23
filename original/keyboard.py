from telethon import Button
import base64
from sql import db
import uuid


def encode_base64(data):
    encoded_bytes = base64.b64encode(data.encode('utf-8'))
    encoded_str = encoded_bytes.decode('utf-8')
    return encoded_str

def decode_base64(encoded_str):
    encoded_bytes = encoded_str.encode('utf-8')
    decoded_bytes = base64.b64decode(encoded_bytes)
    decoded_str = decoded_bytes.decode('utf-8')
    return decoded_str


def result_buttons(data, row_width=1):
    buttons = []
    row = []
    for key, value in data.items():
        uicode = uuid.uuid4().hex
        try:
            db.add_user(user_id=uicode, url=value)
        except:
            pass
        row.append(Button.url(f"{key}", f"https://t.me/mistruz_bot?start={str(uicode)}"))
        if len(row) == row_width:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return buttons
