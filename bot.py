import os

from dotenv import load_dotenv
from pytimeparse import parse
import ptbot


load_dotenv()

TG_TOKEN = os.getenv('TOKEN')


def wait(bot, chat_id, message):
    seconds = parse(message)
    if seconds is None:
        bot.send_message(chat_id, "Не понял время. Напиши, например: 5s, 2m, 1.5 minutes")
        return

    message_id = bot.send_message(chat_id, "Осталось: {} секунд".format(seconds))
    bot.create_countdown(
        seconds,
        notify_progress,
        chat_id=chat_id,
        message_id=message_id,
        total=seconds,
        bot=bot
    )


def notify_progress(secs_left, chat_id, message_id, total, bot):
    if secs_left > 0:
        progress = render_progressbar(total, total - secs_left)
        bot.update_message(chat_id, message_id, "Осталось: {} секунд\n{}".format(secs_left, progress))
    else:
        bot.update_message(chat_id, message_id, "Время вышло!")


def render_progressbar(total, iteration, length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}".format(100 * (iteration / total))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '|{}| {}%'.format(pbar, percent)


def main():
    bot = ptbot.Bot(TG_TOKEN)

    def handle_message(chat_id, message):
        wait(bot, chat_id, message)

    bot.reply_on_message(handle_message)
    bot.run_bot()


if __name__ == '__main__':
    main()
