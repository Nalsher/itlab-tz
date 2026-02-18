from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.text import Format


class ResultFormatter(Format):
    def __init__(self, base_text: str):
        super().__init__(text="")
        self.base_text = base_text

    async def _render_text(self, data: dict, manager: DialogManager) -> str:
        # Берём результат, если он есть
        result = manager.dialog_data.pop("result", None)
        if result:
            return f"{self.base_text}\n\n{result}"
        return self.base_text
