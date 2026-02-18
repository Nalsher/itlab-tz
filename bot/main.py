import asyncio

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs, DialogManager, StartMode
from aiogram.filters import Command
from aiogram.types import Message
from config.botconfig import botFabric
from dialogs.main_dialog import main_dialog

from states.start_state import StartStateGroup


async def main():
    bot = botFabric()

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(main_dialog)

    setup_dialogs(dp)

    @dp.message(Command("start"))
    async def start_handler(message: Message, dialog_manager: DialogManager):
        await dialog_manager.start(StartStateGroup.start, mode=StartMode.RESET_STACK)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
