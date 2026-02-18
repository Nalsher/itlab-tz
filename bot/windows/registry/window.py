from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Cancel

from handlers.register_token.handler import token_handler
from states.start_state import StartStateGroup


from formatters.result.formatter import ResultFormatter

registry_window = Window(
    ResultFormatter("Отправьте ваш API токен сообщением"),
    # Const("🔐 Отправьте ваш API токен сообщением"),
    MessageInput(token_handler),
    Cancel(Const("Отмена")),
    state=StartStateGroup.registry,
)
