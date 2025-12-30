import logging
from typing import Type
from config import get_assemblyai_api_key
from assemblyai.streaming.v3 import (
    StreamingClient,
    TurnEvent,
    BeginEvent,
    TerminationEvent,
    StreamingError, StreamingClientOptions, StreamingEvents
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
client = StreamingClient(
    StreamingClientOptions(
        api_key=aai_api_key,
        api_host="streaming.assemblyai.com"
    )
)

client.on(StreamingEvents.Begin, on_begin)
client.on(StreamingEvents.Turn, on_turn)
client.on(StreamingEvents.Termination, on_terminated)
client.on(StreamingEvents.Error, on_error)

def client_connect():
