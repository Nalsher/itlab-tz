import asyncio
import os

import aiohttp


async def fetch_tasks_page(page: int, chat_id: int):
    url = os.getenv("BACKEND_URL") + "/api/task"
    params = {"page": page + 1}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                url, headers={"Chat-Id": str(chat_id)}, params=params, timeout=10
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    return {
                        "results": [],
                        "next": None,
                        "previous": None,
                        "error": f"Ошибка сервера: {resp.status}",
                    }
        except aiohttp.ClientError as e:
            return {
                "results": [],
                "next": None,
                "previous": None,
                "error": f"Ошибка сети: {str(e)}",
            }
        except asyncio.TimeoutError:
            return {
                "results": [],
                "next": None,
                "previous": None,
                "error": "Таймаут при соединении с сервером",
            }
