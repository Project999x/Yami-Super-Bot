# +++ Made By Sanjiii [telegram username: @Urr_Sanjiii] +++

from bot import Bot
import asyncio
from pyrogram.enums import ParseMode, ChatAction
from helper_func import is_admin, banUser
from plugins.FORMATS import *
from plugins.autoDelete import convert_time
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import OWNER_ID
from pyrogram import Client, filters
from database.database import kingdb 


#Advance commands for adding force sub....
@Bot.on_message(filters.command('add_fsub') & filters.private & filters.user(OWNER_ID))
async def add_forcesub(client:Client, message:Message):
    pro = await message.reply("<b><i>Processing....</i></b>", quote=True)
    check=0
    channel_ids = await kingdb.get_all_channels()
    fsubs = message.text.split()[1:]

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("•  ᴄʟᴏsᴇ  •", callback_data = "close")]])
    
    if not fsubs:
        await pro.edit("<b>ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴀᴅᴅ ᴄʜᴀɴɴᴇʟ ɪᴅs\n<blockquote><u>EXAMPLE</u> :\n/add_fsub [channel_ids] :</b> ʏᴏᴜ ᴄᴀɴ ᴀᴅᴅ ᴏɴᴇ ᴏʀ ᴍᴜʟᴛɪᴘʟᴇ ᴄʜᴀɴɴᴇʟ ɪᴅ ᴀᴛ ᴀ ᴛɪᴍᴇ.</blockquote>", reply_markup=reply_markup)
        return

    channel_list = ""
    for id in fsubs:
        try:
            id = int(id)
        except:
            channel_list += f"<b><blockquote>ɪɴᴠᴀʟɪᴅ ɪᴅ: <code>{id}</code></blockquote></b>\n\n"
            continue
            
        if id in channel_ids:
            channel_list += f"<blockquote><b>ɪᴅ: <code>{id}</code>, ᴀʟʀᴇᴀᴅʏ ᴇxɪsᴛ..</b></blockquote>\n\n"
            continue
            
        id = str(id)
        if id.startswith('-') and id[1:].isdigit() and len(id)==14:
            try:
                data = await client.get_chat(id)
                link = data.invite_link
                cname = data.title

                if not link:
                    link = await client.export_chat_invite_link(id)
                    
                channel_list += f"<b><blockquote>NAME: <a href = {link}>{cname}</a> (ID: <code>{id}</code>)</blockquote></b>\n\n"
                check+=1
                
            except:
                channel_list += f"<b><blockquote>ɪᴅ: <code>{id}</code>\n<i>ᴜɴᴀʙʟᴇ ᴛᴏ ᴀᴅᴅ ғᴏʀᴄᴇ-sᴜʙ, ᴄʜᴇᴄᴋ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ ɪᴅ ᴏʀ ʙᴏᴛ ᴘᴇʀᴍɪsɪᴏɴs ᴘʀᴏᴘᴇʀʟʏ..</i></blockquote></b>\n\n"
            
        else:
            channel_list += f"<b><blockquote>ɪɴᴠᴀʟɪᴅ ɪᴅ: <code>{id}</code></blockquote></b>\n\n"
            continue
    
    if check == len(fsubs):
        for id in fsubs:
            await kingdb.add_channel(int(id))
        await pro.edit(f'<b>ғᴏʀᴄᴇ-sᴜʙ ᴄʜᴀɴɴᴇʟ ᴀᴅᴅᴇᴅ ✅</b>\n\n{channel_list}', reply_markup=reply_markup, disable_web_page_preview = True)
        
    else:
        await pro.edit(f'<b>❌ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ ᴡʜɪʟᴇ ᴀᴅᴅɪɴɢ ғᴏʀᴄᴇ-sᴜʙ ᴄʜᴀɴɴᴇʟs</b>\n\n{channel_list.strip()}\n\n<b><i>ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ...</i></b>', reply_markup=reply_markup, disable_web_page_preview = True)


@Bot.on_message(filters.command('del_fsub') & filters.private & filters.user(OWNER_ID))
async def delete_all_forcesub(client:Client, message:Message):
    pro = await message.reply("<b><i>Processing....</i></b>", quote=True)
    channels = await kingdb.get_all_channels()
    fsubs = message.text.split()[1:]

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("•  ᴄʟᴏsᴇ  •", callback_data = "close")]])

    if not fsubs:
        return await pro.edit("<b>⁉️ ᴘʟᴇᴀsᴇ, ᴘʀᴏᴠɪᴅᴇ ᴠᴀʟɪᴅ ɪᴅs ᴏʀ ᴀʀɢᴜᴍᴇɴᴛs\n<blockquote><u>EXAMPLES</u> :\n/del_fsub [channel_ids] :</b> ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴏɴᴇ ᴏʀ ᴍᴜʟᴛɪᴘʟᴇ sᴘᴇᴄɪғɪᴇᴅ ɪᴅs\n<code>/del_fsub all</code> : ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀʟʟ ᴀᴠᴀɪʟᴀʙʟᴇ ғᴏʀᴄᴇ-sᴜʙ ɪᴅs</blockquote>", reply_markup=reply_markup)

    if len(fsubs) == 1 and fsubs[0].lower() == "all":
        if channels:
            for id in channels:
                await kingdb.del_channel(id)
                    
            ids = "\n".join(f"<blockquote><code>{channel}</code> ✅</blockquote>" for channel in channels)
            return await pro.edit(f"<b>⛔️ ᴀʟʟ ᴀᴠᴀɪʟᴀʙʟᴇ ᴄʜᴀɴɴᴇʟ ɪᴅ ᴀʀᴇ ᴅᴇʟᴇᴛᴇᴅ :\n{ids}</b>", reply_markup=reply_markup)
        else:
            return await pro.edit("<b><blockquote>⁉️ ɴᴏ ᴄʜᴀɴɴᴇʟ ɪᴅ ᴀᴠᴀɪʟᴀʙʟᴇ ᴛᴏ ᴅᴇʟᴇᴛᴇ</blockquote></b>", reply_markup=reply_markup)
            
    if len(channels) >= 1:
        passed = ''
        for sub_id in fsubs:
            try:
                id = int(sub_id)
            except:
                passed += f"<b><blockquote><i>ɪɴᴠᴀʟɪᴅ ɪᴅ: <code>{sub_id}</code></i></blockquote></b>\n"
                continue
            if id in channels:
                await kingdb.del_channel(id)
                    
                passed += f"<blockquote><code>{id}</code> ✅</blockquote>\n"
            else:
                passed += f"<b><blockquote><code>{id}</code> ɴᴏᴛ ɪɴ ғᴏʀᴄᴇ-sᴜʙ ᴄʜᴀɴɴᴇʟs </blockquote></b>\n"
                
        await pro.edit(f"<b>⛔️ ᴘʀᴏᴠɪᴅᴇᴅ ᴄʜᴀɴɴᴇʟ ɪᴅs ᴀʀᴇ ᴅᴇʟᴇᴛᴇᴅ :\n\n{passed}</b>", reply_markup=reply_markup)
        
    else:
        await pro.edit("<b><blockquote>⁉️ ɴᴏ ᴄʜᴀɴɴᴇʟ ɪᴅ ᴀᴠᴀɪʟᴀʙʟᴇ ᴛᴏ ᴅᴇʟᴇᴛᴇ</blockquote></b>", reply_markup=reply_markup)
      

@Bot.on_message(filters.command('fsub_chnl') & filters.private & is_admin)
async def get_forcesub(client:Client, message: Message):
    pro = await message.reply("<b><i>Processing....</i></b>", quote=True)
    channels = await kingdb.get_all_channels()
    channel_list = "<b><blockquote>❌ ɴᴏ ғᴏʀᴄᴇ sᴜʙ ᴄʜᴀɴɴᴇʟ ғᴏᴜɴᴅ !</b></blockquote>"
    if channels:
        channel_list = ""
        for id in channels:
            await message.reply_chat_action(ChatAction.TYPING)
            try:
                data = await client.get_chat(id)
                link = data.invite_link
                cname = data.title

                if not link:
                    link = await client.export_chat_invite_link(id)
                    
                channel_list += f"<b><blockquote>NAME: <a href = {link}>{cname}</a>\n(ID: <code>{id}</code>)</blockquote></b>\n\n"
                
            except:
                channel_list += f"<b><blockquote>ɪᴅ: <code>{id}</code>\n<i>ᴜɴᴀʙʟᴇ ᴛᴏ ʟᴏᴀᴅ ᴏᴛʜᴇʀ ᴅᴇᴛᴀɪʟs..</i></blockquote></b>\n\n"
                
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data = "close")]])
    await message.reply_chat_action(ChatAction.CANCEL)
    await pro.edit(f"<b>ғᴏʀᴄᴇ-sᴜʙ ᴄʜᴀɴɴᴇʟs ʟɪsᴛ :</b>\n\n{channel_list}", reply_markup=reply_markup, disable_web_page_preview = True)


#Commands for adding Admins by Owner
@Bot.on_message(filters.command('add_admins') & filters.private & filters.user(OWNER_ID))
async def add_admins(client:Client, message:Message):        
    pro = await message.reply("<b><i>Processing....</i></b>", quote=True)
    check = 0
    admin_ids = await kingdb.get_all_admins()
    admins = message.text.split()[1:]

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data = "close")]])
    
    if not admins:
        return await pro.edit("<b>ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴀᴅᴅ ᴀᴅᴍɪɴ ɪᴅs\n<blockquote><u>EXAMPLE</u> :\n/add_admins [user_id] :</b> ʏᴏᴜ ᴄᴀɴ ᴀᴅᴅ ᴏɴᴇ ᴏʀ ᴍᴜʟᴛɪᴘʟᴇ ᴜsᴇʀ ɪᴅ ᴀᴛ ᴀ ᴛɪᴍᴇ.</blockquote>", reply_markup=reply_markup)
    
    admin_list = ""
    for id in admins:
        try:
            id = int(id)
        except:
            admin_list += f"<blockquote><b>ɪɴᴠᴀʟɪᴅ ɪᴅ: <code>{id}</code></b></blockquote>\n"
            continue
            
        if id in admin_ids:
            admin_list += f"<blockquote><b>ɪᴅ: <code>{id}</code>, ᴀʟʀᴇᴀᴅʏ ᴇxɪsᴛ..</b></blockquote>\n"
            continue
            
        id = str(id)  
        if id.isdigit() and len(id) == 10:
            admin_list += f"<b><blockquote>(ID: <code>{id}</code>)</blockquote></b>\n"
            check += 1
        else:
            admin_list += f"<blockquote><b>ɪɴᴠᴀʟɪᴅ ɪᴅ: <code>{id}</code></b></blockquote>\n"
            continue            
    
    if check == len(admins):
        for id in admins:
            await kingdb.add_admin(int(id))
        await pro.edit(f'<b>ɴᴇᴡ ɪᴅs ᴀᴅᴅᴇᴅ ɪɴ ᴀᴅᴍɪɴ ʟɪsᴛ ✅</b>\n\n{admin_list}', reply_markup=reply_markup)
        
    else:
        await pro.edit(f'<b>❌ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ ᴡʜɪʟᴇ ᴀᴅᴅɪɴɢ ᴀᴅᴍɪɴs</b>\n\n{admin_list.strip()}\n\n<b><i>ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ...</i></b>', reply_markup=reply_markup)
    #await update_fsub(1)


@Bot.on_message(filters.command('del_admins') & filters.private & filters.user(OWNER_ID))
async def delete_admins(client:Client, message:Message):        
    pro = await message.reply("<b><i>Processing....</i></b>", quote=True)
    admin_ids = await kingdb.get_all_admins()
    admins = message.text.split()[1:]

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data = "close")]])

    if not admins:
        return await pro.edit("<b>⁉️ ᴘʟᴇᴀsᴇ, ᴘʀᴏᴠɪᴅᴇ ᴠᴀʟɪᴅ ɪᴅs ᴏʀ ᴀʀɢᴜᴍᴇɴᴛs</b>\n<blockquote><b><u>EXAMPLES:</u>\n/del_admins [user_ids] :</b> ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴏɴᴇ ᴏʀ ᴍᴜʟᴛɪᴘʟᴇ sᴘᴇᴄɪғɪᴇᴅ ɪᴅs\n<code>/del_admins all</code> : ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀʟʟ ᴀᴠᴀɪʟᴀʙʟᴇ ᴜsᴇʀ ɪᴅs</blockquote>", reply_markup=reply_markup)

    if len(admins) == 1 and admins[0].lower() == "all":
        if admin_ids:
            for id in admin_ids:
                await kingdb.del_admin(id)
            ids = "\n".join(f"<blockquote><code>{admin}</code> ✅</blockquote>" for admin in admin_ids)
            return await pro.edit(f"<b>⛔️ ᴀʟʟ ᴀᴠᴀɪʟᴀʙʟᴇ ᴀᴅᴍɪɴ ɪᴅ ᴀʀᴇ ᴅᴇʟᴇᴛᴇᴅ :\n{ids}</b>", reply_markup=reply_markup)
        else:
            return await pro.edit("<b><blockquote>⁉️ ɴᴏ ᴀᴅᴍɪɴ ʟɪsᴛ ᴀᴠᴀɪʟᴀʙʟᴇ ᴛᴏ ᴅᴇʟᴇᴛᴇ</blockquote></b>", reply_markup=reply_markup)
  
    if len(admin_ids) >= 1:
        passed = ''
        for ad_id in admins:
            try:
                id = int(ad_id)
            except:
                passed += f"<blockquote><b>ɪɴᴠᴀʟɪᴅ ɪᴅ: <code>{ad_id}</code></b></blockquote>\n"
                continue
                
            if id in admin_ids:
                await kingdb.del_admin(id)
                passed += f"<blockquote><code>{id}</code> ✅</blockquote>\n"
            else:
                passed += f"<blockquote><b><code>{id}</code> ɴᴏᴛ ɪɴ ᴀᴅᴍɪɴ ʟɪsᴛ</b></blockquote>\n"
                
        await pro.edit(f"<b>⛔️ ᴘʀᴏᴠɪᴅᴇᴅ ᴀᴅᴍɪɴ ɪᴅ ᴀʀᴇ ᴅᴇʟᴇᴛᴇᴅ :\n\n{passed}</b>", reply_markup=reply_markup)
        
    else:
        await pro.edit("<b><blockquote>⁉️ ɴᴏ ᴀᴅᴍɪɴ ʟɪsᴛ ᴀᴠᴀɪʟᴀʙʟᴇ ᴛᴏ ᴅᴇʟᴇᴛᴇ</blockquote></b>", reply_markup=reply_markup)


@Bot.on_message(filters.command('admin_list') & filters.private & filters.user(OWNER_ID))
async def get_admin_list(client:Client, message: Message):        
    pro = await message.reply("<b><i>Processing....</i></b>", quote=True)
    admin_ids = await kingdb.get_all_admins()
    admin_list = "<b><blockquote>❌ ɴᴏ ᴀᴅᴍɪɴs ɪᴅ ʟɪsᴛ ғᴏᴜɴᴅ ! !</blockquote></b>"
    
    if admin_ids:
        admin_list = ""
        for id in admin_ids:
            await message.reply_chat_action(ChatAction.TYPING)
            try:
                user = await client.get_users(id)
                user_link = f"tg://openmessage?user_id={id}"
                first_name = user.first_name if user.first_name else "No first name !"
                    
                admin_list += f"<b><blockquote>NAME: <a href = {user_link}>{first_name}</a>\n(ID: <code>{id}</code>)</blockquote></b>\n\n"
                
            except:
                admin_list += f"<b><blockquote>ɪᴅ: <code>{id}</code>\n<i>ᴜɴᴀʙʟᴇ ᴛᴏ ʟᴏᴀᴅ ᴏᴛʜᴇʀ ᴅᴇᴛᴀɪʟs..</i></blockquote></b>\n\n"
                
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("•  ᴄʟᴏsᴇ  •", callback_data = "close")]])
    await message.reply_chat_action(ChatAction.CANCEL)
    await pro.edit(f"<b>🤖 ʙᴏᴛs ᴀᴅᴍɪɴ ʟɪsᴛ :</b>\n\n{admin_list}", reply_markup=reply_markup, disable_web_page_preview = True)


#Commands for banned user function............
@Bot.on_message(filters.command('add_banuser') & filters.private & is_admin)
async def add_banuser(client:Client, message:Message):        
    pro = await message.reply("<b><i>Processing....</i></b>", quote=True)
    check, autho_users = 0, []
    banuser_ids = await kingdb.get_ban_users()
    autho_users = await kingdb.get_all_admins(); autho_users.append(OWNER_ID)
    banusers = message.text.split()[1:]

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("•  ᴄʟᴏsᴇ  •", callback_data = "close")]])
    
    if not banusers:
        return await pro.edit("<b>ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴀᴅᴅ ʙᴀɴɴᴇᴅ ᴜsᴇʀ ɪᴅs\n<blockquote><u>EXAMPLE</u> :\n/add_banuser [user_id] :</b> ʏᴏᴜ ᴄᴀɴ ᴀᴅᴅ ᴏɴᴇ ᴏʀ ᴍᴜʟᴛɪᴘʟᴇ ᴜsᴇʀ ɪᴅ ᴀᴛ ᴀ ᴛɪᴍᴇ.</blockquote>", reply_markup=reply_markup)

    banuser_list = ""
    for id in banusers:
        try:
            id = int(id)
        except:
            banuser_list += f"<blockquote><b>ɪɴᴠᴀʟɪᴅ ɪᴅ: <code>{id}</code></b></blockquote>\n"
            continue

        if id in autho_users:
            banuser_list += f"<blockquote><b>ɪᴅ: <code>{id}</code>, ᴄᴏᴜʟᴅ ʙᴇ ᴀᴅᴍɪɴ ᴏʀ ᴏᴡɴᴇʀ</b></blockquote>\n"
            continue
            
        if id in banuser_ids:
            banuser_list += f"<blockquote><b>ɪᴅ: <code>{id}</code>, ᴀʟʀᴇᴀᴅʏ ᴇxɪsᴛ..</b></blockquote>\n"
            continue
            
        id = str(id)  
        if id.isdigit() and len(id) == 10:
            banuser_list += f"<b><blockquote>(ID: <code>{id}</code>)</blockquote></b>\n"
            check += 1
        else:
            banuser_list += f"<blockquote><b>ɪɴᴠᴀʟɪᴅ ɪᴅ: <code>{id}</code></b></blockquote>\n"
            continue            
    
    if check == len(banusers):
        for id in banusers:
            await kingdb.add_ban_user(int(id))
        await pro.edit(f'<b>ɴᴇᴡ ɪᴅs ᴀᴅᴅᴇᴅ ɪɴ ʙᴀɴɴᴇᴅ ᴜsᴇʀ ʟɪsᴛ ✅</b>\n\n{banuser_list}', reply_markup=reply_markup)
        
    else:
        await pro.edit(f'<b>❌ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ ᴡʜɪʟᴇ ᴀᴅᴅɪɴɢ ʙᴀɴɴᴇᴅ ᴜsᴇʀs</b>\n\n{banuser_list.strip()}\n\n<b><i>ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ...</i></b>', reply_markup=reply_markup)
    #await update_fsub(1)


@Bot.on_message(filters.command('del_banuser') & filters.private & is_admin)
async def delete_banuser(client:Client, message:Message):        
    pro = await message.reply("<b><i>Processing....</i></b>", quote=True)
    banuser_ids = await kingdb.get_ban_users()
    banusers = message.text.split()[1:]

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("•  ᴄʟᴏsᴇ  •", callback_data = "close")]])

    if not banusers:
        return await pro.edit("<b>⁉️ ᴘʟᴇᴀsᴇ, ᴘʀᴏᴠɪᴅᴇ ᴠᴀʟɪᴅ ɪᴅs ᴏʀ ᴀʀɢᴜᴍᴇɴᴛs</b>\n<blockquote><b><u>EXAMPLES:</u>\n/del_banuser [user_ids] :</b> ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴏɴᴇ ᴏʀ ᴍᴜʟᴛɪᴘʟᴇ sᴘᴇᴄɪғɪᴇᴅ ɪᴅs\n<code>/del_banuser all</code> : ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀʟʟ ᴀᴠᴀɪʟᴀʙʟᴇ ᴜsᴇʀ ɪᴅs</blockquote>", reply_markup=reply_markup)

    if len(banusers) == 1 and banusers[0].lower() == "all":
        if banuser_ids:
            for id in banuser_ids:
                await kingdb.del_ban_user(id)
            ids = "\n".join(f"<blockquote><code>{user}</code> ✅</blockquote>" for user in banuser_ids)
            return await pro.edit(f"<b>⛔️ ᴀʟʟ ᴀᴠᴀɪʟᴀʙʟᴇ ʙᴀɴɴᴇᴅ ᴜsᴇʀ ɪᴅ ᴀʀᴇ ᴅᴇʟᴇᴛᴇᴅ :\n{ids}</b>", reply_markup=reply_markup)
        else:
            return await pro.edit("<b><blockquote>⁉️ɴᴏ ʙᴀɴɴᴇᴅ ᴜsᴇʀ ɪᴅ ʟɪsᴛ ᴀᴠᴀɪʟᴀʙʟᴇ ᴛᴏ ᴅᴇʟᴇᴛᴇ</blockquote></b>", reply_markup=reply_markup)
  
    if len(banuser_ids) >= 1:
        passed = ''
        for ban_id in banusers:
            try:
                id = int(ban_id)
            except:
                passed += f"<blockquote><b>ɪɴᴠᴀʟɪᴅ ɪᴅ: <code>{ban_id}</code></b></blockquote>\n"
                continue
                
            if id in banuser_ids:
                await kingdb.del_ban_user(id)
                passed += f"<blockquote><code>{id}</code> ✅</blockquote>\n"
            else:
                passed += f"<blockquote><b><code>{id}</code> ɴᴏᴛ ɪɴ ʙᴀɴɴᴇᴅ ʟɪsᴛ</b></blockquote>\n"
                
        await pro.edit(f"<b>⛔️ ᴘʀᴏᴠɪᴅᴇᴅ ʙᴀɴɴᴇᴅ ᴜsᴇʀ ɪᴅ ᴀʀᴇ ᴅᴇʟᴇᴛᴇᴅ :</u>\n\n{passed}</b>", reply_markup=reply_markup)
        
    else:
        await pro.edit("<b><blockquote>⁉️ ɴᴏ ʙᴀɴɴᴇᴅ ᴜsᴇʀ ɪᴅ ʟɪsᴛ ᴀᴠᴀɪʟᴀʙʟᴇ ᴛᴏ ᴅᴇʟᴇᴛᴇ</blockquote></b>", reply_markup=reply_markup)


@Bot.on_message(filters.command('banuser_list') & filters.private & is_admin)
async def get_banuser_list(client:Client, message: Message):        
    pro = await message.reply("<b><i>Processing....</i></b>", quote=True)
    
    banuser_ids = await kingdb.get_ban_users()
    banuser_list = "<b><blockquote>❌ ɴᴏ ʙᴀɴɴᴇᴅ ᴜsᴇʀ ʟɪsᴛ ғᴏᴜɴᴅ !</blockquote></b>"
    
    if banuser_ids:
        banuser_list = ""
        for id in banuser_ids:
            await message.reply_chat_action(ChatAction.TYPING)
            try:
                user = await client.get_users(id)
                user_link = f"tg://openmessage?user_id={id}"
                first_name = user.first_name if user.first_name else "No first name !"
                    
                banuser_list += f"<b><blockquote>NAME: <a href = {user_link}>{first_name}</a>\n(ID: <code>{id}</code>)</blockquote></b>\n\n"
                
            except:
                banuser_list += f"<b><blockquote>ɪᴅ: <code>{id}</code>\n<i>ᴜɴᴀʙʟᴇ ᴛᴏ ʟᴏᴀᴅ ᴏᴛʜᴇʀ ᴅᴇᴛᴀɪʟs..</i></blockquote></b>\n\n"
                
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data = "close")]])
    await message.reply_chat_action(ChatAction.CANCEL)
    await pro.edit(f"<b>🚫 ʙᴀɴɴᴇᴅ ᴜsᴇʀs ʟɪsᴛ :</b>\n\n{banuser_list}", reply_markup=reply_markup, disable_web_page_preview = True)


#=====================================================================================##
#.........Extra Functions.......#
#=====================================================================================##

# Auto Delete Setting Commands
@Bot.on_message(filters.command('auto_del') & filters.private & ~banUser)
async def autoDelete_settings(client, message):
    await message.reply_chat_action(ChatAction.TYPING)

    try:
            timer = convert_time(await kingdb.get_del_timer())
            if await kingdb.get_auto_delete():
                autodel_mode = on_txt
                mode = '• ᴅɪsᴀʙʟᴇ ❌'
            else:
                autodel_mode = off_txt
                mode = '• ᴇɴᴀʙʟᴇ ✅'
            
            await message.reply_photo(
                photo = autodel_cmd_pic,
                caption = AUTODEL_CMD_TXT.format(autodel_mode=autodel_mode, timer=timer),
                reply_markup = InlineKeyboardMarkup([
                    [InlineKeyboardButton(mode, callback_data='chng_autodel'), InlineKeyboardButton('• sᴇᴛ ᴛɪᴍᴇʀ •', callback_data='set_timer')],
                    [InlineKeyboardButton('• ʀᴇғʀᴇsʜ', callback_data='autodel_cmd'), InlineKeyboardButton('ᴄʟᴏsᴇ •', callback_data='close')]
                ]),
                message_effect_id = 5107584321108051014 #👍
            )
    except Exception as e:
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data = "close")]])
            await message.reply(f"<b>! ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ..\n<blockquote>ʀᴇᴀsᴏɴ:</b> {e}</blockquote><b><i>ᴄᴏɴᴛᴀɴᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ: @WhiteBeard_Sama</i></b>", reply_markup=reply_markup)
            

#Files related settings command
@Bot.on_message(filters.command('files') & filters.private & ~banUser)
async def files_commands(client: Client, message: Message):
    await message.reply_chat_action(ChatAction.TYPING)
        
    try:
        protect_content = hide_caption = channel_button = off_txt
        pcd = hcd = cbd = '❌'
        if await kingdb.get_protect_content():
            protect_content = on_txt
            pcd = '✅'
        if await kingdb.get_hide_caption():
            hide_caption = on_txt
            hcd = '✅'
        if await kingdb.get_channel_button():
            channel_button = on_txt
            cbd = '✅'
        name, link = await kingdb.get_channel_button_link()
        
        await message.reply_photo(
            photo = files_cmd_pic,
            caption = FILES_CMD_TXT.format(
                protect_content = protect_content,
                hide_caption = hide_caption,
                channel_button = channel_button,
                name = name,
                link = link
            ),
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(f'• ᴘᴄ: {pcd}', callback_data='pc'), InlineKeyboardButton(f'• ʜᴄ: {hcd}', callback_data='hc')],
                [InlineKeyboardButton(f'• ᴄʙ: {cbd}', callback_data='cb'), InlineKeyboardButton(f'• sʙ •', callback_data='setcb')],
                [InlineKeyboardButton('• ʀᴇғʀᴇsʜ', callback_data='files_cmd'), InlineKeyboardButton('ᴄʟᴏsᴇ •', callback_data='close')]
            ]),
            message_effect_id = 5107584321108051014 #👍
        )
    except Exception as e:
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("•  ᴄʟᴏsᴇ  •", callback_data = "close")]])
        await message.reply(f"<b>! ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ..\n<blockquote>ʀᴇᴀsᴏɴ:</b> {e}</blockquote><b><i>ᴄᴏɴᴛᴀɴᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ: @WhiteBeard_Sama</i></b>", reply_markup=reply_markup)


#Request force sub mode commad,,,,,,
@Bot.on_message(filters.command('req_fsub') & filters.private & ~banUser)
async def handle_reqFsub(client: Client, message: Message):
    await message.reply_chat_action(ChatAction.TYPING)
    try:
        on = off = ""
        if await kingdb.get_request_forcesub():
            on = "🟢"
            texting = on_txt
        else:
            off = "🔴"
            texting = off_txt

        button = [
            [InlineKeyboardButton(f"{on} ᴏɴ", "chng_req"), InlineKeyboardButton(f"{off} ᴏғғ", "chng_req")],
            [InlineKeyboardButton("• ᴍᴏʀᴇ sᴇᴛᴛɪɴɢs •", "more_settings")]
        ]
        await message.reply(text=RFSUB_CMD_TXT.format(req_mode=texting), reply_markup=InlineKeyboardMarkup(button), message_effect_id=5046509860389126442)
        
    except Exception as e:
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("•  ᴄʟᴏsᴇ  •", callback_data = "close")]])
        await message.reply(f"<b>! ᴇʀʀᴏʀ ᴏᴄᴄᴜʀᴇᴅ..\n<blockquote>ʀᴇᴀsᴏɴ:</b> {e}</blockquote><b><i>ᴄᴏɴᴛᴀɴᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ: @WhiteBeard_Sama</i></b>", reply_markup=reply_markup)


# +++ Made By Sanjiii [telegram username: @Urr_Sanjiii] +++