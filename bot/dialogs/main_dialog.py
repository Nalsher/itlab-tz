from aiogram_dialog.dialog import Dialog

from windows.create.date.window import create_date_window
from windows.create.description.window import create_description_window
from windows.create.tags.window import create_tags_window
from windows.create.title.window import create_title_window
from windows.registry.window import registry_window
from windows.start.window import start_window
from windows.view.window import tasks_window

main_dialog = Dialog(
    registry_window,
    start_window,
    tasks_window,
    create_description_window,
    create_tags_window,
    create_title_window,
    create_date_window,
)
