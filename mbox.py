import mailbox
from dataclasses import dataclass, asdict


@dataclass
class Message:
    frm: str = 'Unknown sender'
    to: str = 'Unknown recipient'
    subj: str = 'Default subj'
    content: str = 'This is default text'
    state: str = 'Unread'

    @staticmethod
    def __version__():
        return '1.0.0'

    def __post_init__(self):
        for (name, field_type) in self.__annotations__.items():
            if not isinstance(self.__dict__[name], field_type):
                current_type = type(self.__dict__[name])
                raise TypeError(f"The field `{name}` has `{current_type}` type instead of `{field_type}`")

    @classmethod
    def from_dict(cls, d):
        return Message(**d)

    def to_dict(self):
        return asdict(self)

    def to_string(self):
        raise NotImplementedError('Method must be implemented in 2.0.0 version')


class MessageHeader:
    FROM = 'From'
    TO = 'To'
    SUBJECT = 'Subject'
    STATE = 'State'


class MessageState:
    UNREAD = 'Unread'
    READ = 'Read'
    ANSWERED = 'Answered'
    FORWARDED = 'Forwarded'
    DELETED = 'Deleted'


class InvalidIdError(Exception):
    pass


class MBox:

    def __init__(self, path):
        self.mbox = mailbox.mbox(path=f'{path}/smartiqa.mbox')

    def add_message(self, message: Message):
        msg = self._dump_message(message)
        id = self.mbox.add(msg)
        self._flush()
        return id

    def update_message(self, id: str, message: Message):
        self.mbox.update({id: self._dump_message(message)})

    def get_message(self, id: str):
        msg = self.mbox.get(id)
        if not msg:
            raise InvalidIdError(f"Error with {id} does not exist")
        return Message(frm=msg.get(MessageHeader.FROM),
                       to=msg.get(MessageHeader.TO),
                       subj=msg.get(MessageHeader.SUBJECT),
                       content=msg.get_payload().replace('\n', ''),
                       state=msg.get(MessageHeader.STATE))

    def answer_message(self, id: str):
        message = self.get_message(id)
        message.state = MessageState.ANSWERED
        self.update_message(id, message)

    def read_message(self, id: str):
        message = self.get_message(id)
        message.state = MessageState.READ
        self.update_message(id, message)

    def count(self):
        return self.mbox.__len__()

    def clear(self):
        self.mbox.clear()

    def close(self):
        self.mbox.clear()
        self.mbox.close()

    def _create_message(self):
        return mailbox.mboxMessage()

    def _dump_message(self, message: Message):
        msg = self._create_message()
        msg['From'] = message.frm
        msg['To'] = message.to
        msg['Subject'] = message.subj
        msg['State'] = message.state
        msg.set_payload(message.content)
        return msg

    def _flush(self):
        return self.mbox.flush()
