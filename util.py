from dataclasses import dataclass
from datetime import datetime
from logging import info, basicConfig, INFO
from os import makedirs
from os.path import dirname
from typing import Optional

from pyrogram.types import Chat
from yaml import load, Loader, safe_dump



def info_from_dict(input_dict: dict[int, dict]):
    output = list()

    for key, value in input_dict.items():
        element = ChatInfo(
            key,
            value["name"],
            value.get("username",None),
            value.get("invite",None),
        )
        output.append(element)
    return output


@dataclass
class ChatInfo:
    id: int
    name: str
    username: Optional[str] = None
    invite: Optional[str] = None

    def to_dict(self) -> dict:
        inner = {
            "name": self.name
        }

        if self.username is not None:
            inner.update({
                "username": self.username
            })

        if self.invite is not None:
            inner.update({
                "invite": self.invite
            })

        return {
            self.id: inner
        }


def read_yaml(filename: str) -> dict:
    with open(f'input/{filename}.yaml', 'rb') as stream:
        contents = load(stream, Loader=Loader)
    info(f"READ yaml {filename}! Contents:\n\n{contents}")
    return contents


def write_yaml(filename: str, contents: dict):
    with open(f'output/{filename}.yaml', "w", encoding="utf-8") as f:
        safe_dump(contents, f,allow_unicode=True)
    info(f"WROTE yaml {filename}! Contents:\n\n{contents}")
