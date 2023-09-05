import logging

from openai_api_wrapper import chat_completion, constants, logs, parser

logger = logging.getLogger(logs.LOGGER_NAME)


def main() -> None:
    args = parser.get_parser().parse_args()
    if args.model in constants.CHAT_MODELS:
        response = chat_completion.cli_entrypoint(
            api_key=args.api_key,
            model=args.model,
            system_prompt=args.system_prompt,
            messages=args.message,
        )
    else:
        raise NotImplementedError(
            f"Model {args.model} is not supported. Supported models are: {constants.SUPPORTED_MODELS}"
        )
    print(response)


if __name__ == "__main__":
    main()
