[PortAudio C-Thread]
↓
asyncio.run_coroutine_threadsafe() <-- creates a brand-new coroutine task ~16 times/sec!
↓
async def process_mic_audio_chunk() <-- middleman function that does almost nothing
↓
self.mic_audio_input_queue.put_nowait()
