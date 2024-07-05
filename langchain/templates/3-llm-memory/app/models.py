from uuid import uuid4, UUID
from datetime import datetime, timezone
from enum import Enum as StandardEnum

from typing import List, Optional

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column, relationship
from sqlalchemy_serializer import SerializerMixin

from database import db

ISO8601_FORMAT = "%Y-%m-%dT%H:%M:%S"
# "%z not working"
ISO8601_UTC_TZ = "+00:00"


class ChatMessageRole(StandardEnum):
    ASSISTANT = "assistant"
    SYSTEM = "system"
    USER = "user"


class IdMixin:
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, default=None, primary_key=True)

    uuid: Mapped[UUID] = mapped_column(
        default_factory=uuid4, nullable=False, unique=True
    )


class TimestampMixin:
    __abstract__ = True

    # Set format for datetime serializer
    # https://github.com/n0nSmoker/SQLAlchemy-serializer/blob/master/README.md#custom-formats
    datetime_format = f"{ISO8601_FORMAT}{ISO8601_UTC_TZ}"

    created_at: Mapped[DateTime] = mapped_column(
        DateTime, default=datetime.now(timezone.utc)
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )


class BaseModel(MappedAsDataclass, db.Model, IdMixin, TimestampMixin, SerializerMixin):
    __abstract__ = True


class User(BaseModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(50), default=None, nullable=False, unique=True
    )

    chats: Mapped[List["Chat"]] = relationship(
        back_populates="users", default_factory=list, secondary="chat_users", repr=False
    )

    chat_messages: Mapped[List["ChatMessage"]] = relationship(
        back_populates="user", default_factory=list, repr=False
    )

    serialize_rules = (
        "-chats",
        "-chat_messages",
    )

    def __repr__(self) -> str:
        return f"<User {self.username}({self.id})>"


class Chat(BaseModel):
    __tablename__ = "chats"

    title: Mapped[str] = mapped_column(default=None, unique=True)

    users: Mapped[List["User"]] = relationship(
        back_populates="chats", default_factory=list, secondary="chat_users", repr=False
    )

    chat_messages: Mapped[List["ChatMessage"]] = relationship(
        back_populates="chat",
        default_factory=list,
        order_by="ChatMessage.id",
        repr=False,
    )

    chat_summary: Mapped["ChatSummary"] = relationship(
        back_populates="chat", default=None, repr=False
    )

    serialize_rules = (
        "-users.chats",
        "-chat_messages.chat",
        "-chat_summary",
    )

    def __repr__(self) -> str:
        return f"<Chat {self.title}({self.id})>"


class ChatUser(MappedAsDataclass, db.Model):
    __tablename__ = "chat_users"

    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), default=None)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), default=None)

    __table_args__ = (
        db.PrimaryKeyConstraint(
            chat_id,
            user_id,
        ),
    )

    def __repr__(self) -> str:
        return f"<ChatUser {self.chat_id}-{self.user_id}>"


class ChatMessage(BaseModel):
    @classmethod
    def convert_chat_message_to_llm_format(cls, role: str, content: str) -> dict:
        return {
            "role": role,
            "content": content,
        }

    __tablename__ = "chat_messages"

    body: Mapped[Text] = mapped_column(Text, default=None, nullable=False)

    role: Mapped[Enum[ChatMessageRole]] = mapped_column(
        Enum(ChatMessageRole), default=None, nullable=False
    )

    chat_summary: Mapped["ChatSummary"] = relationship(
        back_populates="last_message", default=None, repr=False
    )

    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), default=None)
    chat: Mapped["Chat"] = relationship(
        back_populates="chat_messages", default=None, foreign_keys=[chat_id], repr=False
    )

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), default=None)
    user: Mapped[Optional["User"]] = relationship(
        back_populates="chat_messages", default=None, foreign_keys=[user_id], repr=False
    )

    serialize_rules = (
        "-chat_summary.last_message",
        "-chat.chat_messages",
        "-user.chat_messages",
    )

    def __repr__(self) -> str:
        return f"<ChatMessage {self.id}>"

    def as_llm_format(self):
        return self.convert_chat_message_to_llm_format(
            role=self.role.value, content=self.body
        )


class ChatSummary(BaseModel):
    __tablename__ = "chat_summaries"

    body: Mapped[Text] = mapped_column(Text, default=None, nullable=False)

    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), default=None)
    chat: Mapped["Chat"] = relationship(
        back_populates="chat_summary", default=None, foreign_keys=[chat_id], repr=False
    )

    last_message_id: Mapped[int] = mapped_column(
        ForeignKey("chat_messages.id"), default=None
    )
    last_message: Mapped["ChatMessage"] = relationship(
        back_populates="chat_summary",
        default=None,
        foreign_keys=[last_message_id],
        repr=False,
    )

    serialize_rules = (
        "-chat",
        "-last_message",
    )

    def __repr__(self) -> str:
        return f"<ChatSummary {self.id}>"
