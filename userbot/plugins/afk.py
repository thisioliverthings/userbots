import asyncio
from datetime import datetime

import humanize
from pyrogram import filters
from pyrogram.types import Message

from userbot import UserBot
from userbot.helpers.PyroHelpers import GetChatID, ReplyCheck
from userbot.plugins.help import add_command_help

AFK = False
AFK_REASON = ""
AFK_TIME = ""
USERS = {}
GROUPS = {}


def subtract_time(start, end):
    return str(humanize.naturaltime(start - end))


@UserBot.on_message(
    ((filters.group & filters.mentioned) | filters.private) & ~filters.me & ~filters.service, group=3
)
async def collect_afk_messages(bot: UserBot, message: Message):
    if AFK:
        last_seen = subtract_time(datetime.now(), AFK_TIME)
        is_group = message.chat.type in ["supergroup", "group"]
        CHAT_TYPE = GROUPS if is_group else USERS

        if GetChatID(message) not in CHAT_TYPE:
            text = (
                f"أنا حالياً غير متوفر.\n"
                f"- الغياب منذ: {last_seen}\n"
                f"- السبب: {AFK_REASON if AFK_REASON else 'غير محدد'}"
            )
            await bot.send_message(
                chat_id=GetChatID(message),
                text=text,
                reply_to_message_id=ReplyCheck(message),
            )
            CHAT_TYPE[GetChatID(message)] = 1
            return
        elif CHAT_TYPE[GetChatID(message)] == 50:
            text = (
                f"ذكرتني أكثر من 50 مرة.\n"
                f"آخر ظهور: {last_seen}\n"
                f"الرجاء الانتظار حتى أعود."
            )
            await bot.send_message(
                chat_id=GetChatID(message),
                text=text,
                reply_to_message_id=ReplyCheck(message),
            )
        elif CHAT_TYPE[GetChatID(message)] % 5 == 0:
            text = (
                f"ما زلت غير متوفر.\n"
                f"- آخر ظهور: {last_seen}\n"
                f"- مشغول بسبب: {AFK_REASON if AFK_REASON else 'غير محدد'}"
            )
            await bot.send_message(
                chat_id=GetChatID(message),
                text=text,
                reply_to_message_id=ReplyCheck(message),
            )

        CHAT_TYPE[GetChatID(message)] += 1


@UserBot.on_message(filters.command(["afk", "بعيد"], ".") & filters.me, group=3)
async def afk_set(bot: UserBot, message: Message):
    global AFK_REASON, AFK, AFK_TIME

    reason = " ".join(message.command[1:]) if len(message.command) > 1 else ""
    AFK_REASON = reason
    AFK = True
    AFK_TIME = datetime.now()

    await message.delete()


@UserBot.on_message(filters.command(["afk", "رجعت"], "!") & filters.me, group=3)
async def afk_unset(bot: UserBot, message: Message):
    global AFK, AFK_TIME, AFK_REASON, USERS, GROUPS

    if AFK:
        last_seen = subtract_time(datetime.now(), AFK_TIME).replace("ago", "").strip()
        total_msgs = sum(USERS.values()) + sum(GROUPS.values())
        total_chats = len(USERS) + len(GROUPS)

        await message.edit(
            f"خلال غيابك ({last_seen})، استلمت {total_msgs} رسالة من {total_chats} محادثة."
        )

        AFK = False
        AFK_TIME = ""
        AFK_REASON = ""
        USERS.clear()
        GROUPS.clear()
        await asyncio.sleep(5)

    await message.delete()


@UserBot.on_message(filters.me, group=3)
async def auto_afk_unset(bot: UserBot, message: Message):
    global AFK, AFK_TIME, AFK_REASON, USERS, GROUPS

    if AFK:
        last_seen = subtract_time(datetime.now(), AFK_TIME).replace("ago", "").strip()
        total_msgs = sum(USERS.values()) + sum(GROUPS.values())
        total_chats = len(USERS) + len(GROUPS)

        reply = await message.reply(
            f"خلال غيابك ({last_seen})، استلمت {total_msgs} رسالة من {total_chats} محادثة."
        )

        AFK = False
        AFK_TIME = ""
        AFK_REASON = ""
        USERS.clear()
        GROUPS.clear()
        await asyncio.sleep(5)
        await reply.delete()


# قسم المساعدة - عربي
add_command_help(
    "وضع الغياب",
    [
        [".afk <السبب> / .بعيد", "تفعيل وضع الغياب مع سبب اختياري."],
        ["!afk / !رجعت", "إلغاء وضع الغياب والعودة للحالة النشطة."],
    ],
)