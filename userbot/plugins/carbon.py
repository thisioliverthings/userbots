import os
from asyncio import sleep

from pyrogram import filters
from pyrogram.types import Message

from userbot import UserBot
from userbot.plugins.help import add_command_help

CARBON_LANG = "py"


def get_carbon_lang():
    """إرجاع اللغة المستخدمة حالياً للكربون (افتراضي: py)"""
    return CARBON_LANG


@UserBot.on_message(filters.command(["carbon", "كربون"], ".") & filters.me)
async def carbonize_code(bot: UserBot, message: Message):
    """إنشاء صورة كود باستخدام carbon-now-cli"""
    code = message.text[8:].strip()

    if not code:
        await message.edit("يرجى إدخال كود بعد الأمر `.كربون` أو الرد على كود.")
        await sleep(3)
        await message.delete()
        return

    file_path = f"userbot/downloads/carbon.{get_carbon_lang()}"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)

    await message.edit("جارٍ توليد صورة للكود...")

    os.system(f"carbon-now -h -t userbot/downloads/carbon {file_path}")

    image_path = "userbot/downloads/carbon.png"
    if os.path.exists(image_path):
        await bot.send_photo(message.chat.id, image_path)
    else:
        await message.edit("حدث خطأ أثناء إنشاء الصورة.")

    await message.delete()


@UserBot.on_message(filters.command(["carbonlang", "لغة_كربون"], ".") & filters.me)
async def set_carbon_lang(bot: UserBot, message: Message):
    """تعيين لغة الكود المستخدمة في الكربون"""
    global CARBON_LANG

    args = message.command[1:]
    if args:
        CARBON_LANG = args[0].strip()
    elif message.reply_to_message:
        CARBON_LANG = message.reply_to_message.text.strip()
    else:
        await message.edit("يرجى تحديد لغة باستخدام `.لغة_كربون <لغة>` أو الرد على رسالة تحتوي على اسم اللغة.")
        await sleep(3)
        await message.delete()
        return

    await message.edit(f"تم تعيين لغة الكربون إلى: `{CARBON_LANG}`")
    await sleep(2)
    await message.delete()


@UserBot.on_message(filters.command(["carbonlang", "لغة_كربون"], "!") & filters.me)
async def show_carbon_lang(bot: UserBot, message: Message):
    """عرض اللغة الحالية المستخدمة في الكربون"""
    await message.edit(f"اللغة الحالية: `{get_carbon_lang()}`")
    await sleep(5)
    await message.delete()


# قسم المساعدة - عربي
add_command_help(
    "كربون",
    [
        [
            ".كربون / .carbon",
            "إنشاء صورة أنيقة للكود باستخدام [Carbon](https://carbon.now.sh).\nالاستخدام: أرسل `.كربون <الكود>` أو قم بالرد على رسالة تحتوي كود.",
        ],
        [
            ".لغة_كربون / .carbonlang",
            "تعيين لغة الكود من أجل التمييز اللوني (syntax).\nالاستخدام: `.لغة_كربون <امتداد اللغة>` أو الرد على رسالة باسم اللغة.",
        ],
        [
            "!لغة_كربون / !carbonlang",
            "عرض اللغة الحالية المستخدمة في توليد صور الكود.",
        ],
    ],
)