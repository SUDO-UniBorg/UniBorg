"""Greetings
Commands:
.clearwelcome
.setwelcome <Welcome Message>
.listwelcome"""

from telethon import events
from telethon.utils import pack_bot_file_id
from sql_helpers.welcome_sql import get_current_welcome_settings, \
    add_welcome_setting, rm_welcome_setting, update_previous_welcome
from uniborg.util import admin_cmd


@borg.on(events.ChatAction())  # pylint:disable=E0602
async def _(event):
    cws = get_current_welcome_settings(event.chat_id)
    if cws:
        # logger.info(event.stringify())
        """user_added=False,
        user_joined=True,
        user_left=False,
        user_kicked=False,"""
        if event.user_joined:
            if cws.should_clean_welcome:
                try:
                    await borg.delete_messages(  # pylint:disable=E0602
                        event.chat_id,
                        cws.previous_welcome
                    )
                except Exception as e:  # pylint:disable=C0103,W0703
                    logger.warn(str(e))  # pylint:disable=E0602
            a_user = await event.get_user()
            chat = await event.get_chat()

            title = chat.title if chat.title else "this chat"
            participants = await event.client.get_participants(chat)
            count = len(participants)
            current_saved_welcome_message = cws.custom_welcome_message
            mention = "[{}](tg://user?id={})".format(a_user.first_name, a_user.id)
            first = a_user.first_name
            last = a_user.last_name
            if last:
                fullname = f"{first} {last}"
            else:
                fullname = first
            username = f"@{a_user.username}" if a_user.username else mention
            userid = a_user.id
            current_saved_welcome_message = cws.custom_welcome_message
            mention = "[{}](tg://user?id={})".format(a_user.first_name, a_user.id)
            
            current_message = await event.reply(
                current_saved_welcome_message.format(mention=mention, title=title, count=count, first=first, last=last, fullname=fullname, username=username, userid=userid),
                file=cws.media_file_id
            )
            update_previous_welcome(event.chat_id, current_message.id)


@borg.on(admin_cmd("setwelcome"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    msg = await event.get_reply_message()
    if msg and msg.media:
        bot_api_file_id = pack_bot_file_id(msg.media)
        add_welcome_setting(event.chat_id, msg.message, True, 0, bot_api_file_id)
        await event.edit("Welcome Message saved. ")
    else:
        input_str = event.text.split(None, 1)
        add_welcome_setting(event.chat_id, input_str[1], True, 0)
        await event.edit("Welcome Message saved. ")


@borg.on(admin_cmd("clearwelcome"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    cws = get_current_welcome_settings(event.chat_id)
    rm_welcome_setting(event.chat_id)
    await event.edit(
        "Welcome Message cleared. " + \
        "The previous welcome message was `{}`.".format(cws.custom_welcome_message)
    )
    
    
@borg.on(admin_cmd("listwelcome"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    cws = get_current_welcome_settings(event.chat_id)
    if hasattr(cws, 'custom_welcome_message'):
        await event.edit(
            "Welcome Message found.\n " + \
            "Your Welcome Message is as follows:\n `{}`.".format(cws.custom_welcome_message)
        )
        return
    else:
        await event.edit(
            "No Welcome Message found"
        )
         

    
