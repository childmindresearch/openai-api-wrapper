"""This module provides an ArgumentParser object for the CLI."""

import argparse
import logging

from openai_api_wrapper import logs

LOGGER_NAME = logs.LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

SUPPORTED_MODELS = {"gpt4", "gpt-4-32k", "gpt-3.5-turbo", "gpt-3.5-turbo-16k"}


def get_parser() -> argparse.ArgumentParser:
    """Returns an ArgumentParser object for the CLI.

    Returns:
        argparse.ArgumentParser: An ArgumentParser object for the CLI.
    """
    parser = argparse.ArgumentParser(
        prog="OpenAI API Wrapper",
        description="OpenAI API Wrapper",
        epilog="Issues can be reported to: https://github.com/cmi-dair/openai-api-wrapper",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    mandatory_group = parser.add_argument_group(
        "Mandatory arguments", "Mandatory arguments for all models."
    )
    chat_completion_group = parser.add_argument_group(
        "Chat Completion arguments", "Arguments for chat completion models."
    )
    optional_group = parser.add_argument_group(
        "Optional arguments", "Optional arguments for all models."
    )

    mandatory_group.add_argument(
        "model",
        type=str,
        help="The model to use for the API call",
        choices=SUPPORTED_MODELS,
    )

    chat_completion_group.add_argument(
        "--system-prompt",
        type=str,
        help="The prompt to use for the system.",
    )
    chat_completion_group.add_argument(
        "--message",
        type=str,
        help="A message to add to the conversation. Can be used multiple times. Each message must start with 'user:' or 'assistant:'",
        action="append",
    )

    optional_group.add_argument(
        "--api-key",
        type=str,
        help="Your OpenAI API key. If not provided, the OPENAI_API_KEY environment variable will be used.",
        default=None,
    )

    return parser
