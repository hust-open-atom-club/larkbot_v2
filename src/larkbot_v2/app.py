import time

import schedule

from larkbot_v2.bot import LarkLKMLBot

if __name__ == "__main__":
    from larkbot_v2.logger import logger

    logger.setLevel("DEBUG")

    bot = LarkLKMLBot()
    bot.run()
else:

    bot = LarkLKMLBot()

    schedule.every(5).minutes.do(LarkLKMLBot().run)
    schedule.run_all()

    while True:
        schedule.run_pending()
        time.sleep(1)
