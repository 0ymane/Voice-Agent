import asyncio
import threading
import time

async def main():
    queue = asyncio.Queue()
    loop = asyncio.get_running_loop()

    # 1. Simulate PortAudio's external C thread
    def portaudio_thread_simulator():
        for i in range(1, 4):
            time.sleep(0.5)  # Blocking sleep on the OS thread
            print(f"[Thread-{threading.get_ident()}] Produced mic chunk #{i}")
            # Safely drop it into the asyncio loop's inbox:
            loop.call_soon_threadsafe(queue.put_nowait, f"chunk_{i}")

    # Start the external OS thread
    t = threading.Thread(target=portaudio_thread_simulator)
    t.start()

    # 2. Consume from the queue inside the event loop
    for _ in range(3):
        item = await queue.get()
        print(f"[EventLoop] Consumed {item} safely!")

    t.join()

if __name__ == "__main__":
    asyncio.run(main())