import time

import schedule

from larkbot_v2.bot import LarkLKMLBot

bot = LarkLKMLBot()


if __name__ == "__main__":
    from larkbot_v2.logger import logger

    logger.setLevel("DEBUG")

    bot.run()
else:
    schedule.every(5).minutes.do(LarkLKMLBot().run)
    schedule.run_all()

    while True:
        schedule.run_pending()
        time.sleep(1)
