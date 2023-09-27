import mailbox
from dataclasses import dataclass, asdict
import email

__version__ = "1.0.0"


@dataclass
class Message:
    frm: str = 'Unknown sender'
    to: str = 'Unknown recipient'
    subj: str = 'Default subj'
    content: str = 'This is default text'
    state: str = 'Unread'
    id: str = 'None'

    @staticmethod
    def __version__():
        return __version__

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
    ID = 'ID'
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
        self._path = f"{path}/smartiqa.mbox"
        self.mbox = mailbox.mbox(path=self._path)

    def path(self):
        return self._path

    def add_message(self, message: Message):
        msg = self._message_to_struct(message)
        id = self.mbox.add(msg)
        msg['ID'] = str(id)
        self.mbox.update({id: msg})
        self._flush()
        return id

    def update_message(self, id: str, message: Message):
        self.mbox.update({id: self._message_to_struct(message)})

    def get_message(self, id: str):
        msg = self.mbox.get(id)
        if not msg:
            raise InvalidIdError(f"Error with {id} does not exist")
        return Message(frm=msg.get(MessageHeader.FROM),
                       to=msg.get(MessageHeader.TO),
                       subj=msg.get(MessageHeader.SUBJECT),
                       content=msg.get_payload().replace('\n', ''),
                       state=msg.get(MessageHeader.STATE),
                       id=str(id))

    def answer_message(self, id: str):
        message = self.get_message(id)
        message.state = MessageState.ANSWERED
        self.update_message(id, message)

    def read_message(self, id: str):
        message = self.get_message(id)
        message.state = MessageState.READ
        self.update_message(id, message)

    def list_messages(self):
        return [self._struct_to_message(msg) for msg in self.mbox.values()]

    def count(self):
        return self.mbox.__len__()

    def remove_message(self, id: str):
        self.mbox.remove(id)

    def clear(self):
        self.mbox.clear()

    def clear_and_close(self):
        self.mbox.clear()
        self.mbox.close()

    def close(self):
        self.mbox.close()

    def unused_method(self):
        print('This method is unused')
        print('We added it to the module in order to check Code coverage')
        print('These three lines are missed from testing')

    @staticmethod
    def _message_to_struct(message: Message) -> email.message:
        msg = mailbox.mboxMessage()
        msg['From'] = message.frm
        msg['To'] = message.to
        msg['Subject'] = message.subj
        msg['State'] = message.state
        msg.set_payload(message.content)
        return msg

    @staticmethod
    def _struct_to_message(struct: email.message) -> Message:
        return Message(frm=struct.get(MessageHeader.FROM),
                       to=struct.get(MessageHeader.TO),
                       subj=struct.get(MessageHeader.SUBJECT),
                       content=struct.get_payload().replace('\n', ''),
                       state=struct.get(MessageHeader.STATE),
                       id=struct.get(MessageHeader.ID))

    def _flush(self):
        return self.mbox.flush()
