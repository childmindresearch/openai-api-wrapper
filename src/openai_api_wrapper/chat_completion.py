"""This module provides a wrapper for the OpenAI API's GPT model, allowing you
to easily create and manage conversations with the API.

The `ChatCompletion` class in this module represents a conversation with the
OpenAI API using the GPT model. You can use this class to send messages to the
API and receive responses, as well as to manage the conversation history.

This module also provides a `Message` class, which represents a message in a
conversation. You can use this class to create new messages to add to the
conversation history.

"""
# pylint: disable=no-self-argument
import logging
import os
from typing import Literal

import openai
import pydantic

from openai_api_wrapper import constants, logs

logger = logging.getLogger(logs.LOGGER_NAME)


@pydantic.dataclasses.dataclass
class Message:
    """Represents a message in a conversation.

    Attributes:
        role: The role of the message sender.
        content: The content of the message.
    """

    role: Literal["system", "user", "assistant"]
    content: str

    def __str__(self):
        """Returns a string representation of the Message object.

        Returns:
            str: A string representation of the Message object, in the
                format "{role}: {content}".
        """
        return f"{self.role}: {self.content}"


class ChatCompletion(pydantic.BaseModel, extra="forbid"):
    """A class that represents a conversation with the OpenAI API using the GPT model.

    Attributes:
        api_key: Your OpenAI API key.
        model: The model to use.
        system_prompt: The prompt to use for the system.
        messages: The messages to pre-load the API with.
    """

    api_key: pydantic.SecretStr = pydantic.Field(
        description="Your openAI API key.", frozen=True
    )
    model: str = pydantic.Field("gpt4", description="The model to use.", frozen=True)
    system_prompt: str = pydantic.Field(
        "", description="The prompt to use for the system.", frozen=True
    )
    messages: list[Message] = pydantic.Field(
        [],
        description="The messages to pre-load the API with.",
    )

    @pydantic.field_validator("api_key")
    def api_key_from_env(cls, api_key: pydantic.SecretStr | None) -> pydantic.SecretStr:
        if api_key:
            return api_key
        return pydantic.SecretStr(os.environ["OPENAI_API_KEY"])

    @pydantic.field_validator("model")
    def model_is_supported(cls, model: str) -> str:
        if model in constants.CHAT_MODELS:
            return model
        raise ValueError(
            f"Model {model} is not supported. Supported models are: {constants.CHAT_MODELS}"
        )

    def model_post_init(self, __context) -> None:
        """Initializes the GPT object after it has been constructed.

        Raises:
            ValueError: If neither messages nor system_prompt are provided, or
                if both are provided.
        """
        logger.debug("Initializing GPT object.")
        if not self.messages and not self.system_prompt:
            raise ValueError("You must provide either messages or a system_prompt.")
        if self.messages and self.system_prompt:
            raise ValueError("You cannot provide both messages and a system_prompt.")
        if self.system_prompt:
            self.messages = [Message(role="system", content=self.system_prompt)]

    def add_message(self, role: Literal["user", "assistant"], content: str):
        """Adds a new message to the conversation.

        Args:
            role: The role of the message sender. Must be either "user" or
                "assistant".
            content: The content of the message.
        """
        logger.debug("Adding message: %s: %s", role, content)
        self.messages.append(Message(role=role, content=content))

    def prompt(self) -> str:
        """Sends the conversation history to the OpenAI API and returns the
        response.

        Returns:
            str: The response from the OpenAI API.
        """
        logger.debug("Prompting API.")
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self._messages_as_dicts(),
            api_key=self.api_key.get_secret_value(),
        )
        self.add_message(
            role="assistant", content=response["choices"][0]["message"]["content"]
        )
        return self.messages[-1].content

    def _messages_as_dicts(self) -> list[dict]:
        """Returns a list of dictionaries representing the messages in the
        conversation. Each dictionary contains the message's attributes as key-value pairs.
        """
        logger.debug("Converting messages to dictionaries.")
        return [message.__dict__ for message in self.messages]


def cli_entrypoint(api_key=None, model=None, system_prompt=None, messages=None):
    """Runs the CLI for the OpenAI API Wrapper.

    Args:
        api_key: Your OpenAI API key. If not provided, the OPENAI_API_KEY
            environment variable will be used.
        model: The model to use for the API call. Must be one of the models
            listed in `SUPPORTED_MODELS`.
        system_prompt: The prompt to use for the system.
        messages: A list of messages to add to the conversation. Each message
            must be a string starting with "user:" or "assistant:".
    """
    parsed_messages = [Message(role="system", content=system_prompt)]
    if messages:
        parsed_messages.extend(
            [
                Message(role=message.split(":")[0], content=message.split(":")[1])
                for message in messages
            ]
        )

    logger.info("Initializing ChatCompletion object.")
    chat_completion = ChatCompletion(
        api_key=api_key,
        model=model,
        messages=parsed_messages,
    )
    logger.info("Sending messages to API.")
    return chat_completion.prompt()
