import telebot

from config import TOKEN
from database import (
    init_db,
    add_task,
    get_tasks,
    delete_task,
    clear_tasks
)

bot = telebot.TeleBot(TOKEN)

init_db()


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Добро пожаловать в Task Manager Bot!\n\n"
        "Доступные команды:\n\n"
        "/add <задача> — добавить задачу\n"
        "/tasks — показать список задач\n"
        "/complete <id> — завершить задачу\n"
        "/clear — удалить все задачи\n"
        "/help — помощь"
    )


@bot.message_handler(commands=["help"])
def help_command(message):
    bot.send_message(
        message.chat.id,
        "📚 Список команд:\n\n"
        "/add <задача>\n"
        "/tasks\n"
        "/complete <id>\n"
        "/clear\n"
        "/help"
    )


@bot.message_handler(commands=["add"])
def add(message):
    task = message.text.replace("/add", "").strip()

    if not task:
        bot.reply_to(
            message,
            "❌ Укажите задачу.\n\nПример:\n/add Изучить Python"
        )
        return

    add_task(message.from_user.id, task)

    bot.reply_to(
        message,
        "✅ Задача успешно добавлена."
    )


@bot.message_handler(commands=["tasks"])
def tasks(message):
    user_tasks = get_tasks(message.from_user.id)

    if not user_tasks:
        bot.reply_to(
            message,
            "📭 У вас пока нет задач."
        )
        return

    text = "📋 Ваши задачи:\n\n"

    for task_id, task in user_tasks:
        text += f"{task_id}. {task}\n"

    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["complete"])
def complete(message):
    try:
        task_id = int(
            message.text.replace("/complete", "").strip()
        )

        delete_task(task_id)

        bot.reply_to(
            message,
            "✅ Задача выполнена и удалена."
        )

    except ValueError:
        bot.reply_to(
            message,
            "❌ Используйте:\n/complete <id>"
        )


@bot.message_handler(commands=["clear"])
def clear(message):
    clear_tasks(message.from_user.id)

    bot.reply_to(
        message,
        "🗑 Все задачи удалены."
    )


print("🚀 Bot started...")

bot.infinity_polling()