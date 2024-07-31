import logging
import re
from datetime import datetime

import feedparser
from feedparser.util import FeedParserDict

from .config import settings
from .logger import logger
from .utils.feishu import send_to_lark


class LarkLKMLBot(object):
    last_update: str = ""

    def __init__(self) -> None:
        if logger.level == logging.DEBUG:
            self.last_update = "2024-07-20T10:19:08Z"
        else:
            self.last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_feed(self) -> list[FeedParserDict]:
        """
        Fetch the feed from the configured URL and return the entries that are newer than the last update.
        """

        logger.info(f"Fetching feed from {settings.feed_url}")

        feed: FeedParserDict = feedparser.parse(settings.feed_url)

        entries = []
        for entry in feed.entries:
            if entry.updated > self.last_update:
                entries.append(entry)
            else:
                break

        return entries

    def run(self) -> None:
        """
        Run the bot to fetch the feed and send the new entries to the Lark group.
        """
        logger.info(
            f"Running LarkLKMLBot @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        new_count = 0
        reply_count = 0
        entry_list = []

        entries = self.get_feed()
        for entry in entries:
            logger.info(f"New entry: {entry.title}")

            if entry.title.lower().startswith("re:"):
                reply_count += 1
            else:
                new_count += 1

            email = re.search(r"\((.*?)\)", entry.author).group(1)

            # TODO: 通过人名检索用户ID
            user_dict = {
                "example@test.com": "000001",
            }

            user_id = user_dict.get(email, None)

            if user_id is None:
                logger.warning(f"User ID not found for email: {email}")
                entry_list.append(
                    {
                        "email": email,
                        "title": entry.title,
                        "url": entry.link,
                    }
                )
            else:
                entry_list.append(
                    {
                        "user_id": user_id,
                        "email": email,
                        "title": entry.title,
                        "url": entry.link,
                    }
                )

        if len(entries) == 0:
            logger.info("No new entries found.")
            return

        logger.info(f"New entries: {new_count}, replies: {reply_count}")
        self.last_update = entries[0].updated

        try:
            send_to_lark(
                settings.lark_template_id,
                settings.lark_webhook_url,
                settings.lark_webhook_secret,
                {
                    "new_count": new_count,
                    "reply_count": reply_count,
                    "entry_list": entry_list,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                },
            )
            logger.info("Sent to Lark successfully.")

        except Exception as e:
            logger.error(f"Failed to send to Lark: {e}")
            return
