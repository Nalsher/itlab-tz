from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.text import Format, Text


class TasksTextFormatter(Text):
    async def _render_text(self, data: dict, manager: DialogManager) -> str:
        tasks = manager.dialog_data.get("tasks", [])
        if not tasks:
            return "Нет задач "

        lines = ["Задачи:"]
        for t in tasks:
            tags = []
            for item in t["tags"]:
                tags.append(item["title"])
            lines.append(
                f"• {t['title']} - {t['description']} (до {t['due_date']}) Теги - ({tags})"
            )
        return "\n".join(lines)
