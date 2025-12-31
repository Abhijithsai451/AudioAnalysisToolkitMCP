import assemblyai as aai
from typing import Type
from config import get_assemblyai_api_key
from assemblyai.extras import MicrophoneStream
from assemblyai.streaming.v3 import (
    StreamingClient,
    TurnEvent,
    BeginEvent,
    TerminationEvent,
    StreamingError, StreamingClientOptions, StreamingEvents, StreamingParameters
)
from logging_config import setup_logger

logger = setup_logger()
# Assembly AI API Key
aai_api_key = get_assemblyai_api_key()

# Assembly AI Event Handlers
def on_begin(self: Type[StreamingClient], event: BeginEvent):
    logger.info(f"Session started: {event.id}")
def on_turn(self: Type[StreamingClient], event: TurnEvent):
    logger.info(f"{event.transcript} ({event.end_of_turn})")
def on_terminated(self: Type[StreamingClient], event: TerminationEvent):
    logger.info(
        f"Session terminated: {event.audio_duration_seconds} seconds of audio processed"
    )
def on_error(self: Type[StreamingClient], error: StreamingError):
    logger.info(f"Error occurred: {error}")


# Assembly AI Streaming Client
class MicrophoneStreamer(MicrophoneStream):
    def __next__(self):
        if not self._open:
            raise StopIteration
        try:
            return self._stream.read(self._chunk_size, exception_on_overflow=False)
        except KeyboardInterrupt:
            raise StopIteration

def create_client() -> StreamingClient:
    logger.info("Creating Assembly AI Streaming Client...")
    client = StreamingClient(
        StreamingClientOptions(
            api_key=aai_api_key,
            api_host="streaming.assemblyai.com"
        )

    )
    logger.info("Assembly AI Streaming Client event handlers are being set...")
    client.on(StreamingEvents.Begin, on_begin)
    client.on(StreamingEvents.Turn, on_turn)
    client.on(StreamingEvents.Termination, on_terminated)
    client.on(StreamingEvents.Error, on_error)
    return client

def client_connect(client: StreamingClient)-> StreamingClient:
    logger.info("Connecting to Assembly AI Streaming API...")
    client.connect(
        StreamingParameters(
            sample_rate = 16000,
            format_turns = True
        )
    )
    logger.info("Connection to the Assembly AI Streaming API established.")
    return client


def stream_microphone(client: StreamingClient)-> StreamingClient:
    logger.info("Streaming audio from your microphone...")
    client.stream(
        MicrophoneStreamer(sample_rate=16000)
    )

    return client

def close_streaming(client: StreamingClient)-> StreamingClient:
    logger.info("Assembly AI Streaming API connection is being closed")
    client.disconnect(terminate=True)
    logger.info("Assembly AI Streaming API connection is closed")

    return client


