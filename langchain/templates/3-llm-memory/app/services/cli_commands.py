import os
import sys

import click

from services.app_logger import AppLogger
from services.chat_manager import ChatManager

# TODO better way to do this (import from parent dir)?
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from database import db
from models import User, Chat


def register_cli_commands(app, chat_manager: ChatManager, logger: AppLogger) -> None:
    @app.cli.command("db_seed")
    def db_seed():
        users_exist = db.session.query(db.session.query(User).exists()).scalar()
        chats_exist = db.session.query(db.session.query(Chat).exists()).scalar()

        if users_exist or chats_exist:
            click.echo("Database already seeded. Skipping seeding.")
            return

        user = User(username="test_user")
        db.session.add(user)
        db.session.commit()
        output = f"Created user: {user}"
        click.echo(output)
        logger.log(output)

        chat = chat_manager.create_chat_and_add_user(title="test_chat", user=user)
        output = f"Created chat: {chat}"
        click.echo(output)
        logger.log(output)

        output = "Database seeded."
        click.echo(output)
        logger.log(output)

    @app.cli.command("clear_logs")
    def clear_logs():
        logger.clear_log_file()
        click.echo("Log files cleared")
