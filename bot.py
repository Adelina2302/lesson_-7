import os
from dotenv import load_dotenv
from pytimeparse import parse
import ptbot


def wait(bot, chat_id, message):
    seconds = parse(message)
    if seconds is None:
        bot.send_message(chat_id, "Не понял время. Напиши, например: 5s, 2m, 1.5 minutes")
        return

    message_id = bot.send_message(chat_id, f"Осталось: {seconds} секунд")
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
        bot.update_message(chat_id, message_id, f"Осталось: {secs_left} секунд\n{progress}")
    else:
        bot.update_message(chat_id, message_id, "Время вышло!")


def render_progressbar(total, iteration, length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}".format(100 * (iteration / total))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return f'|{pbar}| {percent}%'


def handle_message(bot, chat_id, message):
    wait(bot, chat_id, message)


def main():
    load_dotenv()
    tg_token = os.getenv('TOKEN')
    bot = ptbot.Bot(tg_token)

    bot.reply_on_message(lambda chat_id, message: handle_message(bot, chat_id, message))
    bot.run_bot()


if __name__ == '__main__':
    main()
