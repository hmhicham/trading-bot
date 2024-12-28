from datetime import datetime

class Message:
    def __init__(self, id, reply_id, text, date):
        self.id = id
        self.reply_id = reply_id
        self.text = text
        self.date = date

    def __repr__(self):
        return f"Message(id={self.id}, reply_id={self.reply_id}, text={self.text}, date={self.date})"
