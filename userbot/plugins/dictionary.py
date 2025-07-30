import asyncio
from pyrogram import filters
from pyrogram.types import Message

from userbot import UserBot
from userbot.helpers.aiohttp_helper import AioHttp
from userbot.plugins.help import add_command_help


@UserBot.on_message(filters.command(["define", "dict", "معنى", "قاموس"], ".") & filters.me)
async def define(bot: UserBot, message: Message):
    cmd = message.command

    input_string = ""
    if len(cmd) > 1:
        input_string = " ".join(cmd[1:])
    elif message.reply_to_message and len(cmd) == 1:
        input_string = message.reply_to_message.text
    else:
        await message.edit("يرجى كتابة الكلمة أو الرد على الكلمة التي تريد معناها.")
        await asyncio.sleep(3)
        await message.delete()
        return

    def format_meanings(entries, category_name):
        formatted = f"**{category_name.title()}**\n"
        for entry in entries:
            if "definition" in entry:
                definition = entry["definition"]
                example = entry.get("example")
                formatted += f"\n- **تعريف:** `{definition}`"
                if example:
                    formatted += f"\n  **مثال:** `{example}`"
        formatted += "\n"
        return formatted

    def build_output(data):
        result = ""
        if "meaning" in data:
            meaning = data["meaning"]
            for key, value in meaning.items():
                result += format_meanings(value, key)
        elif "title" in data:
            result += (
                f"**خطأ**\n\n"
                f"▪️ `{data['title']}`\n"
                f"▪️ {data['message']}\n"
                f"▪️ _{data['resolution']}_"
            )
        return result

    # Fetch word definition
    response = await AioHttp().get_json(f"https://api.dictionaryapi.dev/api/v1/entries/en/{input_string}")
    word_data = response[0] if isinstance(response, list) else response
    word_name = word_data.get("word", input_string)
    output_text = build_output(word_data)

    if output_text:
        await message.edit(f"**نتيجة البحث عن:** `{word_name}`\n\n{output_text}")
    else:
        await message.edit("لم يتم العثور على نتائج.")


# قسم المساعدة
add_command_help(
    "dictionary",
    [
        [".define / .dict / .معنى / .قاموس", "يعرض تعريف الكلمة الإنجليزية التي ترسلها أو ترد عليها."],
    ],
)