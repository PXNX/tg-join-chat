from asyncio import sleep
from logging import info, error

import pyrogram.errors
from pyrogram import Client

from util import write_yaml, ChatInfo, read_yaml, info_from_dict


async def list_joined(app: Client):
    output = dict()

    async for dialog in app.get_dialogs():
        if dialog.chat.type in (dialog.chat.type.CHANNEL, dialog.chat.type.GROUP, dialog.chat.type.SUPERGROUP):
            element = ChatInfo(
                dialog.chat.id,
                dialog.chat.title,
                dialog.chat.username
            )
            output.update(element.to_dict())
            info(f"Added chat: {element.to_dict()}")
            await sleep(5)

    write_yaml("list_joined", output)


async def join_list(app: Client):
    success = dict()
    failure = dict()

    for chat in info_from_dict(read_yaml("join_list")):
        info(f"Trying to join {chat.id} :: {chat.name}")
        try:
            if chat.username is not None:
                result = await app.join_chat(f"@{chat.username}")
            elif chat.invite is not None:
                result = await app.join_chat(chat.invite)
            else:
                raise ValueError("Please provide username or invitelink.")

            success.update(chat.to_dict())
            info(result)
        except pyrogram.errors.HashInvalid:
            message = f"Could not join {chat.id} :: {chat.name} - Maybe you are banned or invite link expired."
            error(message)
            failure.update({id: message})
            pass
        except pyrogram.errors.UsernameNotOccupied:
            message = f"Could not join {chat.id} :: {chat.name} - There is no such username {chat.username}."
            error(message)
            failure.update({id: message})
            pass
        except Exception as e:
            message = f"Could not join {chat.id} :: {chat.name} - {e}"
            error(message)
            failure.update({id: message})
            pass

        await sleep(300)

    info(
        f"Done joining chats!\n\nSuccess ({len(success)} entries): {success}\nFailure ({len(failure)} entries): {failure}\n")


# Call functions here
async def run_functions(app: Client):
    await list_joined(app)
    await join_list(app)
