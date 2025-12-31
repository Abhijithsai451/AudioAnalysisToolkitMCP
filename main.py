from assemblyai_config import client_connect, stream_microphone, close_streaming, create_client
from logging_config import setup_logger

logger = setup_logger()

if __name__ == '__main__':
    """logger.info("Starting Assembly AI Streaming API connection...")
    client = create_client()
    client = client_connect(client)
    try:
        stream_microphone(client)
    except Exception as e:
        logger.error(e)
    finally:
        close_streaming(client)"""
