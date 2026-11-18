import time
from functools import wraps
import asyncio
import logging

logger = logging.getLogger(__name__)

# comment this line to stop debugging in terminal
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s  %(message)s")


def clock(methodToRun):
    asyncFlag = asyncio.iscoroutinefunction(methodToRun)
    if asyncFlag:
        @wraps(methodToRun)
        async def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = await methodToRun(*args, **kwargs)
            end_time = time.perf_counter()
            logger.debug(f"[CLOCK] {methodToRun.__name__} async mode: {end_time - start_time:.4f} seconds \n" )
            return result
        return wrapper
    else:
        @wraps(methodToRun)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = methodToRun(*args, **kwargs)
            end_time = time.perf_counter()
            logger.debug(f"[CLOCK] {methodToRun.__name__} normal mode:  {end_time - start_time:.4f} seconds \n")
            return result
        return wrapper