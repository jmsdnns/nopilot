import os
import sys
import tempfile
import subprocess
import argparse

from dotenv import load_dotenv
from openai import OpenAI

from .prompts import JUST_CODE


# Settings
DEFAULT_EDITOR = "nano"
DEFAULT_MODEL = "gpt-3.5-turbo-0125  # https://platform.openai.com/docs/models/overview"
NP_DOTENV_PATH = os.path.join(os.path.expanduser("~"), ".nopilot")
NP_DOTENV_DEFAULT = f"""\
OPENAI_MODEL={DEFAULT_MODEL}
OPENAI_API_KEY=
"""


def parse_cli():
    parser = argparse.ArgumentParser(description="there aint no pilot here")

    parser.add_argument(
        "-e",
        "--editor",
        action="store_true",
        help="Use external editor for entering prompt",
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default=os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo-0125"),
        help="Configure which gpt model is used: gpt-4o, gpt-4-turbo, gpt-4, gpt-3.5",
    )
    parser.add_argument(
        "prompt",
        nargs="*",
        default=None,
        help="Pass a prompt as input if not using stdin or -e",
    )

    args = parser.parse_args()

    # If -e flag is not used and stdin is not used, a prompt must be given
    if not args.editor and sys.stdin.isatty() and not args.prompt:
        parser.error("No prompt provided")

    return args


def init_client():
    # create .nopilot in homedir if not present
    if not os.path.isfile(NP_DOTENV_PATH):
        with open(NP_DOTENV_PATH, "w") as f:
            f.write(NP_DOTENV_DEFAULT)

    # try $HOME/.nopilot
    load_dotenv(NP_DOTENV_PATH)
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ.pop("OPENAI_API_KEY")

    # .env or shell envs can override .nopilot
    load_dotenv(".env")

    # gotta have that key
    if not os.environ.get("OPENAI_API_KEY"):
        raise Exception(f"OPENAI_API_KEY not configured in {NP_DOTENV_PATH}")

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    return client


def read_input(args):
    # piped input
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    # temp file in EDITOR
    elif args.editor:
        return prompt_editor()
    # cli args
    elif args.prompt:
        return " ".join(args.prompt)


def prompt_editor():
    editor = os.environ.get("EDITOR", DEFAULT_EDITOR)
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tf:
        subprocess.call([f"{editor}", tf.name])
        tf.seek(0)
        prompt = tf.read().rstrip()
        return prompt.decode("utf-8")


def gen_code(client, prompt, args):
    # cli param overrides environment variable for OPENAI_MODEL
    model = os.environ.get("OPENAI_MODEL")
    if args.model:
        model = args.model

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": JUST_CODE},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content


def run():
    args = parse_cli()
    prompt = read_input(args)
    client = init_client()

    text = gen_code(client, prompt, args)
    print(text)
