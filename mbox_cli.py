from contextlib import contextmanager
from io import StringIO
from typing import List
import rich
from rich.table import Table

import typer

import mbox
from mbox import MBox, Message, MessageState, InvalidIdError

app = typer.Typer(add_completion=False)


@app.command()
def version():
    """ Return app version """
    print(mbox.__version__)


@app.command()
def path():
    """ Return mailbox file path """
    with mailbox() as mbox:
        print(mbox.path())


@app.command()
def add(frm: str, to: str, subj: str, content: List[str], state: str = typer.Option(None, "-st", "--state")):
    """ Add message to mailbox """
    content = " ".join(content) if content else None
    if not state:
        state = MessageState.UNREAD
    with mailbox() as mbox:
        message = Message(frm, to, subj, content, state)
        id = mbox.add_message(message)
    print(f"Created message with {id} id")


@app.command()
def delete(id: int):
    """ Remove message from mailbox with given id """
    with mailbox() as mbox:
        try:
            mbox.remove_message(id)
            print(f"Removed message with {id} id")
        except InvalidIdError:
            print(f"Error: Invalid message id {id}")


@app.command("list")
def list_messages():
    """ List messages in mailbox """
    with mailbox() as mbox:
        messages = mbox.list_messages()
        table = Table(box=rich.box.SIMPLE)
        table.add_column("ID")
        table.add_column("From")
        table.add_column("To")
        table.add_column("Subject")
        table.add_column("Content")

        for message in messages:
            table.add_row(message.id, message.frm, message.to, message.subj, message.content)
        out = StringIO()
        rich.print(table, file=out)
        print(out.getvalue())


@contextmanager
def mailbox():
    mbox = MBox('.')
    yield mbox
    mbox.close()


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    print(f"Executing command: {ctx.invoked_subcommand} ...")
    if ctx.invoked_subcommand is None:
        list_messages()


"""
Usage examples:

# 1. Create message:
$ python3 cli.py add 'Anna K' 'Andrew L' 'Additional changes' 'Im writing to inform you that...'
Executing command: add ...
Created message with 0 id

# 2. List existing messages:
$ python3 cli.py list
Executing command: list ...

ID   From       To                   Subject                           Content
────────────────────────────────────────────────────────────────────────────────
0    Andrew L   Additional changes   Im writng to inform you that...   Unread

# 3. Delete message:
$ python3 cli.py delete 0
Executing command: delete ...
Removed message with 0 id
"""
if __name__ == "__main__":
    app()
