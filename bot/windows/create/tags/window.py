from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Cancel

from handlers.create_task.task_tags.handler import tags_handler
from states.start_state import StartStateGroup

from formatters.result.formatter import ResultFormatter

create_tags_window = Window(
    ResultFormatter("Отправьте tags задачи"),
    # Const(),
    MessageInput(tags_handler),
    Cancel(Const("Отмена")),
    state=StartStateGroup.createTaskTags,
)
