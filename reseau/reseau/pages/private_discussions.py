from datetime import datetime, timezone
from itertools import groupby
import os
import reflex as rx
import sqlalchemy as sa
import time

from ..common.base_state import BaseState
from ..common import email
from ..common.translate import format_to_date
from ..models import (
    Message,
    UserAccount,
    UserPreference,
    UserPrivateMessage,
)


class PrivateDiscussionsState(BaseState):
    """State for managing private messages."""

    # A collection of discussions, with a flag associated with each one
    # to know if the discussion is read,
    # containing the UserAccount to which the current User talks to
    # and all the private messages between them
    private_discussions: list[tuple[UserAccount, bool]] = []
    # Messages of the current discussion
    # discussion_messages: list[tuple[list[UserPrivateMessage], str]] = []
    discussion_messages: list[tuple[list[Message], str]] = []

    def load_private_discussions(self, event: bool = True):
        """
        Load existing private discussions for the current user.
        """
        # To prevent the loading of the private discussions
        # when the discussions dropdown is closed
        if not event:
            return

        self.private_discussions = []

        with rx.session() as session:
            user_messages = session.exec(
                UserPrivateMessage.select()
                .join(Message)
                .options(
                    sa.orm.selectinload(
                        UserPrivateMessage.private_message
                    ).selectinload(Message.sender),
                    sa.orm.selectinload(UserPrivateMessage.recipient),
                )
                .where(
                    (Message.sender_id ==
                     self.authenticated_user.id) |
                    (UserPrivateMessage.recipient_id ==
                     self.authenticated_user.id)
                )
            ).all()
            # Sort the messages by the date of publication (most recent first)
            # so we can after set the most recent discussions first
            user_messages = sorted(
                user_messages,
                key=lambda x: x.private_message.published_at,
                reverse=True
            )
            # Temporary list to store existing users for the following loop
            existing_users = set()
            # Iterate over the messages and add the sender or recipient
            # (not the current user) to the private discussions if
            # they are not already in the list
            for message in user_messages:
                sender = message.private_message.sender
                recipient = message.recipient

                if (sender.id != self.authenticated_user.id
                        and sender.id not in existing_users):
                    is_read = self.is_discussion_read(sender.id)
                    self.private_discussions.append((sender, is_read))
                    existing_users.add(sender.id)

                if (recipient.id != self.authenticated_user.id
                        and recipient.id not in existing_users):
                    is_read = self.is_discussion_read(recipient.id)
                    self.private_discussions.append((recipient, is_read))
                    existing_users.add(recipient.id)

    @rx.var()
    def is_there_unread_messages(self):
        """
        Check if there are unread messages.
        """
        self.load_private_discussions()
        for discussion in self.private_discussions:
            # As the discussions are sorted by the most recent message,
            # if the first discussion is not read, there are unread messages
            if not discussion[1]:
                return True
        return False

    def is_discussion_read(self, discussion_id: int):
        """
        Check if a discussion is read.
        """
        with rx.session() as session:
            messages = session.exec(
                UserPrivateMessage.select()
                .join(Message)
                .where(
                    (Message.sender_id == discussion_id) &
                    (UserPrivateMessage.recipient_id ==
                     self.authenticated_user.id)
                )
            ).all()
            if not messages:
                return True

            messages = sorted(
                messages,
                key=lambda x: x.private_message.published_at
            )
            # If atleast the last received message is read,
            # the discussion is considered read
            if messages[-1].is_read:
                return True
            return False

    def load_private_messages(
        self,
        discussion_id: int,
        mark_as_read: bool = False
    ):
        """
        Load private messages for a discussion.
        """
        self.discussion_messages = []

        with rx.session() as session:
            # messages = session.exec(
            #     UserPrivateMessage.select()
            #     .join(Message)
            #     .options(
            #         sa.orm.selectinload(
            #             UserPrivateMessage.private_message
            #         ).selectinload(Message.sender),
            #         sa.orm.selectinload(UserPrivateMessage.recipient),
            #     ).where(
            #         ((Message.sender_id ==
            #           self.authenticated_user.id) &
            #          (UserPrivateMessage.recipient_id == discussion_id)) |
            #         ((UserPrivateMessage.recipient_id ==
            #           self.authenticated_user.id) &
            #          (Message.sender_id == discussion_id))
            #     )
            # ).all()
            messages = session.exec(
                Message.select()
                .join(UserPrivateMessage)
                .options(
                    sa.orm.selectinload(Message.sender),
                    sa.orm.selectinload(Message.user_private_message)
                    .selectinload(UserPrivateMessage.recipient),
                ).where(
                    ((Message.sender_id ==
                      self.authenticated_user.id) &
                     (UserPrivateMessage.recipient_id == discussion_id)) |
                    ((UserPrivateMessage.recipient_id ==
                      self.authenticated_user.id) &
                     (Message.sender_id == discussion_id))
                )
            ).all()
            # Convert all published_at to Paris time
            os.environ['TZ'] = 'Europe/Paris'
            time.tzset()
            for message in messages:
                paris_now = datetime.now().timestamp()
                offset = (datetime.fromtimestamp(paris_now) -
                          datetime.utcfromtimestamp(paris_now))
                message.published_at = (
                    message.published_at + offset
                )

            messages = sorted(
                messages,
                key=lambda x: x.published_at
            )

            # Function with which we group the messages by date
            def get_date(message: Message):
                return message.published_at.date()

            self.discussion_messages = [
                (list(group), format_to_date(date))
                for date, group in groupby(messages, key=get_date)
            ]

        if mark_as_read:
            self.mark_discussion_as_read(discussion_id)

    def mark_discussion_as_read(self, discussion_id: int):
        """
        Mark a discussion as read.
        """
        # Mark only the messages received as read
        with rx.session() as session:
            messages = session.exec(
                UserPrivateMessage.select()
                .join(Message)
                .where(
                    ((UserPrivateMessage.recipient_id ==
                      self.authenticated_user.id) &
                     (Message.sender_id == discussion_id))
                )
            ).all()
            for message in messages:
                if not message.is_read:
                    message.is_read = True
                    session.add(message)
            session.commit()

    def send_message(self, form_data: dict):
        """
        Send a message to a discussion.
        """
        recipient_id = form_data["recipient_id"]
        with rx.session() as session:
            new_message = Message(
                content=form_data["message"],
                published_at=datetime.now(timezone.utc),
                sender_id=self.authenticated_user.id
            )
            session.add(new_message)
            session.commit()
            session.refresh(new_message)

            user_private_message = UserPrivateMessage(
                recipient_id=recipient_id,
                private_message_id=new_message.id,
            )
            session.add(user_private_message)
            session.commit()

        self.load_private_messages(recipient_id)

        # Notify the recipient of the new message
        # if he has enabled notifications for private messages
        with rx.session() as session:
            recipient = session.exec(
                UserAccount.select()
                .options(
                    sa.orm.selectinload(UserAccount.preference_list)
                )
                .where(
                    (UserAccount.id == recipient_id) &
                    (UserPreference.useraccount_id == UserAccount.id) &
                    (UserPreference.preference_id == '2')
                )
            ).first()
            if recipient:
                msg = email.write_email_file(
                    f"./other_mails/{recipient.id}_mail_file.txt",
                    email.pm_notification_template(
                        recipient,
                        self.authenticated_user
                    )
                )
                email.send_email(
                    msg,
                    'Nouveau message sur Reseau',
                    recipient.email
                )
