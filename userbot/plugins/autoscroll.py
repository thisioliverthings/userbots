from pyrogram import filters
from pyrogram.types import Message

from userbot import UserBot
from userbot.plugins.help import add_command_help

# قائمة الدردشات المفعّل فيها التمرير التلقائي
auto_read_chats = set()


@UserBot.on_message(filters.chat(auto_read_chats))
async def auto_read(bot: UserBot, message: Message):
    await bot.read_history(message.chat.id)
    message.continue_propagation()


@UserBot.on_message(filters.command(["autoscroll", "تمرير"], ".") & filters.me)
async def toggle_autoscroll(bot: UserBot, message: Message):
    chat_id = message.chat.id

    if chat_id in auto_read_chats:
        auto_read_chats.remove(chat_id)
        await message.edit("تم إيقاف التمرير التلقائي في هذه المحادثة.")
    else:
        auto_read_chats.add(chat_id)
        await message.edit("تم تفعيل التمرير التلقائي في هذه المحادثة.")


# قسم المساعدة - عربي
add_command_help(
    "التمرير التلقائي",
    [
        [".autoscroll / .تمرير", "تفعيل أو إيقاف قراءة الرسائل تلقائيًا في المحادثة الحالية."],
    ],
)