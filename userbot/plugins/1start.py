import asyncio
from datetime import datetime
from platform import python_version

from pyrogram import __version__, filters
from pyrogram.types import Message

from userbot import START_TIME, UserBot
from userbot.helpers.constants import First
from userbot.plugins.help import add_command_help


@UserBot.on_message(filters.command(["alive", "حي"], ".") & filters.me)
async def alive(bot: UserBot, message: Message):
    txt = (
        "**البوت يعمل**\n"
        f"- مدة التشغيل: `{str(datetime.now() - START_TIME).split('.')[0]}`\n"
        f"- إصدار Python: `{python_version()}`\n"
        f"- إصدار Pyrogram: `{__version__}`"
    )
    await message.edit(txt)


@UserBot.on_message(filters.command(["repo", "المصدر"], ".") & filters.me)
async def repo(bot: UserBot, message: Message):
    await message.edit(First.REPO)


@UserBot.on_message(filters.command(["creator", "المطور"], ".") & filters.me)
async def creator(bot: UserBot, message: Message):
    await message.edit(First.CREATOR)


@UserBot.on_message(filters.command(["uptime", "up", "المدة"], ".") & filters.me)
async def uptime(bot: UserBot, message: Message):
    await message.edit(
        f"مدة التشغيل الحالية: `{str(datetime.now() - START_TIME).split('.')[0]}`"
    )


@UserBot.on_message(filters.command(["id", "ايدي"], ".") & filters.me)
async def get_id(bot: UserBot, message: Message):
    file_id = None
    user_id = None

    if message.reply_to_message:
        rep = message.reply_to_message

        if rep.audio:
            file_id = f"File ID: `{rep.audio.file_id}`\nالنوع: Audio"

        elif rep.document:
            file_id = f"File ID: `{rep.document.file_id}`\nالنوع: `{rep.document.mime_type}`"

        elif rep.photo:
            file_id = f"File ID: `{rep.photo.file_id}`\nالنوع: Photo"

        elif rep.sticker:
            file_id = f"Sticker ID: `{rep.sticker.file_id}`\n"
            if rep.sticker.set_name and rep.sticker.emoji:
                file_id += f"المجموعة: `{rep.sticker.set_name}`\n"
                file_id += f"الإيموجي: `{rep.sticker.emoji}`\n"
                file_id += f"متحرك: `{rep.sticker.is_animated}`"
            else:
                file_id += "المجموعة: غير متوفرة\nالإيموجي: غير متوفر"

        elif rep.video:
            file_id = f"File ID: `{rep.video.file_id}`\nالنوع: Video"

        elif rep.animation:
            file_id = f"File ID: `{rep.animation.file_id}`\nالنوع: GIF"

        elif rep.voice:
            file_id = f"File ID: `{rep.voice.file_id}`\nالنوع: Voice Note"

        elif rep.video_note:
            file_id = f"File ID: `{rep.video_note.file_id}`\nالنوع: Video Note"

        elif rep.location:
            file_id = "الموقع:\n"
            file_id += f"خط الطول: `{rep.location.longitude}`\n"
            file_id += f"خط العرض: `{rep.location.latitude}`"

        elif rep.venue:
            file_id = "الموقع:\n"
            file_id += f"خط الطول: `{rep.venue.location.longitude}`\n"
            file_id += f"خط العرض: `{rep.venue.location.latitude}`\n\n"
            file_id += "العنوان:\n"
            file_id += f"الاسم: `{rep.venue.title}`\n"
            file_id += f"التفاصيل: `{rep.venue.address}`"

        elif rep.from_user:
            user_id = rep.from_user.id

    if user_id:
        user_detail = (
            f"User ID: `{rep.from_user.id}`\nMessage ID: `{rep.id}`"
        )
        await message.edit(user_detail)

    elif file_id:
        detail = f"User ID: `{rep.from_user.id}`\nMessage ID: `{rep.id}`\n\n{file_id}"
        await message.edit(detail)

    else:
        await message.edit(f"Chat ID: `{message.chat.id}`")


@UserBot.on_message(filters.command(["restart", "اعادة"], ".") & filters.me)
async def restart(bot: UserBot, message: Message):
    await message.edit("جارٍ إعادة تشغيل البوت...")
    await bot.send_message("me", f"#userbot_restart, {message.chat.id}, {message.id}")

    if "p" in message.text and "g" in message.text:
        asyncio.get_event_loop().create_task(UserBot.restart(git_update=True, pip=True))
    elif "p" in message.text:
        asyncio.get_event_loop().create_task(UserBot.restart(pip=True))
    elif "g" in message.text:
        asyncio.get_event_loop().create_task(UserBot.restart(git_update=True))
    else:
        asyncio.get_event_loop().create_task(UserBot.restart())


# قسم المساعدة - عربي
add_command_help(
    "الأساسية",
    [
        [".alive / .حي", "عرض حالة البوت الحالية ومعلومات النظام."],
        [".repo / .المصدر", "عرض رابط المستودع الخاص بالبوت."],
        [".creator / .المطور", "عرض معلومات مطور البوت."],
        [".id / .ايدي", "عرض معرف الرسالة أو الملف أو المستخدم."],
        [".uptime / .up / .المدة", "عرض مدة تشغيل البوت الحالية."],
    ],
)

add_command_help(
    "إعادة التشغيل",
    [
        [".restart / .اعادة", "إعادة تشغيل البوت."],
        [".restart g", "تحديث الكود من Git ثم إعادة التشغيل."],
        [".restart p", "تحديث الحزم (pip) ثم إعادة التشغيل."],
        [".restart gp", "تحديث Git و pip ثم إعادة التشغيل."],
    ],
)