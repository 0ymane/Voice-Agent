import sys
from pathlib import Path
import asyncio


sys.path.insert(0, str(Path(__file__).parent))

from my_hotel_voice_agent.diagnostics import clock
import time

@clock
def download_simulation():
    time.sleep(3)

download_simulation()


@clock
async def download_async_simulation():
    await asyncio.sleep(3)

asyncio.run(download_async_simulation())