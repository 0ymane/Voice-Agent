import pyaudio
import asyncio



class AudioStreamer:
    """ Handles continuous microphone input and audio output """

    def __init__(self, input_queue :asyncio.Queue[bytes], output_queue :asyncio.Queue[bytes]):
        self.mic_audio_input_queue = input_queue
        self.speaker_audio_output_queue = output_queue
        self.is_listening = False
        self.is_speaking = False
        self.event_loop = asyncio.get_event_loop()

        
        # Initialize PyAudio
        self.audio_engine = pyaudio.PyAudio()
    
    def input_callback(self, audio_chunk , frame_count, time_info, status):
        """Callback function that schedules audio processing in the asyncio event loop"""
        
        if self.is_listening and audio_chunk :
            # Schedule the task in the event loop
            asyncio.run_coroutine_threadsafe(
                self.process_input_audio_chunk(audio_chunk ),
                self.event_loop
            )
        # return (None, pyaudio.paComplete) paContinue is the heartbeat signal that keeps the microphone streaming chunk after chunk.
        return (None, pyaudio.paContinue) 

    
    async def process_input_audio_chunk(self, audio_chunk):
        """Process a single audio chunk directly"""

        try:
            self.mic_audio_input_queue.put_nowait(audio_chunk)

        except Exception as e:
            if self.is_listening:
                print(f"Input queue failed: {e}") 