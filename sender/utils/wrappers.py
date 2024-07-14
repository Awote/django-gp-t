import asyncio
from concurrent.futures import ThreadPoolExecutor


async def run_in_thread_pool(func, *args, **kwargs):
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, func, *args, **kwargs)
    return result