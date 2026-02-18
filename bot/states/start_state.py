from aiogram.fsm.state import StatesGroup, State


class StartStateGroup(StatesGroup):
    start = State()
    registry = State()
    viewTasks = State()
    createTaskTitle = State()
    createTaskDescription = State()
    createTaskDueDate = State()
    createTaskTags = State()
