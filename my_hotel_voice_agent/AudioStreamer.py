import pyaudio
import asyncio
import  logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format="%(level)s %(name)s %(message)s")


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
    
    def listening_handler(self, audio_chunk , frame_count, time_info, status):
        """Callback function that schedules audio processing in the asyncio event loop"""
        
        if self.is_listening and audio_chunk :
            # Schedule the task in the event loop
            self.event_loop.call_soon_threadsafe(
                self.mic_audio_input_queue.put_nowait, 
                audio_chunk
                )
        # or (None, pyaudio.paComplete) to stop; paContinue is the heartbeat signal that keeps the microphone streaming chunk after chunk.
        return (None, pyaudio.paContinue) 

