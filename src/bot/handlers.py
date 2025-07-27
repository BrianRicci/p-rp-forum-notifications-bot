from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.utils.formatting import (Bold, Text, Code, as_marked_section, as_numbered_section)
from aiogram.utils.markdown import link

import database.requests as rq


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)

    content = Text(
        Bold('Привет! Я бот для отслеживания новых сообщений на форумах.\n\n'),
        as_marked_section(
            Bold('📌 Доступные команды:'),
            Text(Code("/add <ссылка>"), " — добавить топик для отслеживания."),
            Text(Code("/list"), " — список отслеживаемых топиков."),
            Text(Code("/remove <номер>"), " — удалить топик из списка."),
            Text(Code("/help"), " — показать справку."),
            marker='🔹 ',
        ),
        '\n\nОтправь мне ссылку на топик, и я буду присылать уведомления о новых постах!\n',
        'По всем вопросам обращаться сюда @ricci_141',
    )

    await message.answer(**content.as_kwargs())

# /add <url>
# Здесь надо будет добавить ссылку для отслеживания с привязкой к пользователю
@router.message(Command('add'))
async def add_topic(message: Message, command: CommandObject):
    url = command.args
    await message.answer(f'url: {link('Топик', url)}')

# /list
# Здесь надо будет сделать вывод списка
@router.message(Command('list'))
async def list_topic(message: Message):
    content = Text(
        as_numbered_section(
            Bold('📋 Ваши отслеживаемые топики:\n'),
            link('Топик', 'https://proxima-rp.ru/threads/sly_reaver-prizyv-k-smerti-i-oskorblenie-bobbi-nrp.64493/'),
        ),
        '\n\nЧтобы удалить топик, используйте /remove <номер>',
    )
    await message.answer(**content.as_kwargs())

# /remove <number>
# Здесь надо будет сделать удаление поста из списка
@router.message(Command('remove'))
async def remove_topic(message: Message, command: CommandObject):
    topic_number = command.args

    await message.answer(f'Удален топик под номером: {topic_number}')
