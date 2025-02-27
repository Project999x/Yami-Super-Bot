
import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

from bot import Bot
from config import CHANNEL_ID
from helper_func import encode, is_admin
command_list = ['start', 'users', 'broadcast', 'batch', 'genlink', 'help', 'cmd', 'info', 'add_fsub', 'fsub_chnl', 'restart', 'del_fsub', 'add_admins', 'del_admins', 'admin_list', 'cancel', 'auto_del', 'forcesub', 'files', 'add_banuser', 'del_banuser', 'banuser_list', 'status', 'req_fsub']

@Bot.on_message(~filters.command(command_list) & filters.private & is_admin)
async def channel_post(client: Client, message: Message):
        
    reply_text = await message.reply_text("<b><i>ᴘʀᴏᴄᴇssɪɴɢ....</i></b>", quote=True)
    try:
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("<b>sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ..!</b>")
        return
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("📫 Sʜᴀʀᴇ URL", url=f'https://telegram.me/share/url?url={link}')]])

    await reply_text.edit(f"<b>›› ʙᴇʟᴏᴡ ɪs ʏᴏᴜʀ ʟɪɴᴋ::</b>\n\n<blockquote expandable>{link}</blockquote>", reply_markup=reply_markup, disable_web_page_preview=True)

    #if not DISABLE_CHANNEL_BUTTON:
        #await post_message.edit_reply_markup(reply_markup)

"""@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):

    if True:
        return

    converted_id = message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("📫 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    try:
        await message.edit_reply_markup(reply_markup)
    except Exception as e:
        print(e)
        pass"""
