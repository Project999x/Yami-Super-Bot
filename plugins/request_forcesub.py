# +++ Made By Sanjiii [telegram username: @Urr_Sanjiii] +++

from bot import Bot
from database.database import kingdb
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import ChatMemberUpdated

# This handler captures membership updates (like when a user leaves, banned)
@Bot.on_chat_member_updated()
async def handle_Chatmembers(client, chat_member_updated: ChatMemberUpdated):    
    chat_id = chat_member_updated.chat.id

    if await kingdb.reqChannel_exist(chat_id):
        old_member = chat_member_updated.old_chat_member

        if not old_member:
            return
    
        if old_member.status == ChatMemberStatus.MEMBER:
            user_id = old_member.user.id

            if await kingdb.reqSent_user_exist(chat_id, user_id):
                await kingdb.del_reqSent_user(chat_id, user_id)
            
      
# This handler will capture any join request to the channel/group where the bot is an admin
@Bot.on_chat_join_request()
async def handle_join_request(client, chat_join_request):
    chat_id = chat_join_request.chat.id  
    
    if await kingdb.reqChannel_exist(chat_id):
        user_id = chat_join_request.from_user.id 

        if not await kingdb.reqSent_user_exist(chat_id, user_id):
            await kingdb.reqSent_user(chat_id, user_id)

        

  

