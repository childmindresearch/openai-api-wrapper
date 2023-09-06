# OpenAI API Wrapper

[![Build](https://github.com/cmi-dair/openai-api-wrapper/actions/workflows/test.yaml/badge.svg?branch=main)](https://github.com/cmi-dair/openai-api-wrapper/actions/workflows/test.yaml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/cmi-dair/openai-api-wrapper/branch/main/graph/badge.svg?token=22HWWFWPW5)](https://codecov.io/gh/cmi-dair/openai-api-wrapper)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![stability-wip](https://img.shields.io/badge/stability-work_in_progress-lightgrey.svg)
[![L-GPL License](https://img.shields.io/badge/license-L--GPL-blue.svg)](https://github.com/cmi-dair/openai-api-wrapper/blob/main/LICENSE)
[![pages](https://img.shields.io/badge/api-docs-blue)](https://cmi-dair.github.io/openai-api-wrapper)

This tool provides a thin CLI wrapper around OpenAI's Python API. The intention is to provide a simple way to interact with the API without having to write new code files.

## Features

Currently, only chat completion models are supported.

## Installation

To install this tool, download the repository and install it with Poetry

```sh
cd openai-api-wrapper
poetry install
```

## Usage

See the CLI's help for up-to-date usage:

```sh
poetry run openai_api --help
```
