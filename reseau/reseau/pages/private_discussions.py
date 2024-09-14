from datetime import datetime, timezone
from itertools import groupby
import reflex as rx
import sqlalchemy as sa
import time

from ..common.base_state import BaseState
from ..common.translate import format_to_date
from ..models import PrivateMessage, UserAccount, UserPrivateMessage


class PrivateDiscussionsState(BaseState):
    """State for managing private messages."""

    # A collection of discussions, with a flag associated with each one
    # to know if the discussion is read,
    # containing the UserAccount to which the current User talks to
    # and all the private messages between them
    private_discussions: list[tuple[UserAccount, bool]] = []
    # Messages of the current discussion
    discussion_messages: list[tuple[list[UserPrivateMessage], str]] = []

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
                .options(
                    sa.orm.selectinload(UserPrivateMessage.sender),
                    sa.orm.selectinload(UserPrivateMessage.recipient),
                    sa.orm.selectinload(UserPrivateMessage.private_message),
                )
                .where(
                    (UserPrivateMessage.sender_id ==
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
                sender = message.sender
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
                .where(
                    (UserPrivateMessage.sender_id == discussion_id) &
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
            messages = session.exec(
                UserPrivateMessage.select()
                .options(
                    sa.orm.selectinload(UserPrivateMessage.private_message),
                    sa.orm.selectinload(UserPrivateMessage.sender),
                    sa.orm.selectinload(UserPrivateMessage.recipient),
                ).where(
                    ((UserPrivateMessage.sender_id ==
                      self.authenticated_user.id) &
                     (UserPrivateMessage.recipient_id == discussion_id)) |
                    ((UserPrivateMessage.recipient_id ==
                      self.authenticated_user.id) &
                     (UserPrivateMessage.sender_id == discussion_id))
                )
            ).all()

            import logging
            # Convert all published_at to Paris time
            for message in messages:
                logging.debug("before", message.private_message.published_at)
                now = time.time()
                logging.debug("now", now)
                logging.debug("fromts(now)", datetime.fromtimestamp(now))
                logging.debug("utcfromts(now)", datetime.utcfromtimestamp(now))
                offset = (datetime.fromtimestamp(now) -
                          datetime.utcfromtimestamp(now))
                logging.debug("offset", offset)
                message.private_message.published_at = (
                    message.private_message.published_at + offset
                )
                logging.debug("after", message.private_message.published_at)

            messages = sorted(
                messages,
                key=lambda x: x.private_message.published_at
            )

            # Function with which we group the messages by date
            def get_date(message: UserPrivateMessage):
                return message.private_message.published_at.date()

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
                .where(
                    ((UserPrivateMessage.recipient_id ==
                      self.authenticated_user.id) &
                     (UserPrivateMessage.sender_id == discussion_id))
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
        with rx.session() as session:
            new_message = PrivateMessage(
                content=form_data["message"],
                published_at=datetime.now(timezone.utc),
            )
            session.add(new_message)
            session.commit()
            session.refresh(new_message)

            user_private_message = UserPrivateMessage(
                sender_id=self.authenticated_user.id,
                recipient_id=form_data["recipient_id"],
                private_message_id=new_message.id,
            )
            session.add(user_private_message)
            session.commit()

            self.load_private_messages(form_data["recipient_id"])
