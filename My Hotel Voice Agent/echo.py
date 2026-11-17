import pyaudio

p = pyaudio.PyAudio()

# 1. Open input and output streams (16000 Hz, mono, 16-bit)
input_stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input=True,
    frames_per_buffer=1024,
)
output_stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    output=True,
    frames_per_buffer=1024,
)

# 2. Record ~3 seconds (50 chunks * 1024 / 16000s ≈ 3.2s)
print("Recording 3 seconds... Speak now!")
frames = []
for _ in range(50):
    data = input_stream.read(1024)
    frames.append(data)

# 3. Play back the recorded bytes
print("Playing back...")
for chunk in frames:
    output_stream.write(chunk)

print("Done!")

# Clean up
input_stream.stop_stream()
input_stream.close()
output_stream.stop_stream()
output_stream.close()
p.terminate()