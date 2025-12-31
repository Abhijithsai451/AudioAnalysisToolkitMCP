from assemblyai_config import client_connect, stream_microphone, close_streaming
import assemblyai as aai
client = client_connect()

#@mcp_tool()
async def transcribe_audio(audio: bytes) -> str:
    pass

