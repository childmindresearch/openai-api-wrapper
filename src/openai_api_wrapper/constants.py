"""Constants for the OpenAI API Wrapper."""
import pathlib

LOGGER_NAME = pathlib.Path(__file__).parent.name

CHAT_MODELS = {"gpt4", "gpt-4-32k", "gpt-3.5-turbo", "gpt-3.5-turbo-16k"}
SUPPORTED_MODELS = CHAT_MODELS
