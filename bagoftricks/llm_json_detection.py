"""
A powerful implementation of JSON detection in generative LLM output.

pip install demjson3
"""
import ast
import json
import re
import warnings
from typing import Any

import demjson3
import regex


def detect_json(text: str) -> Any | None:
    # if it is a json
    try:
        return load_json(text)  # type: ignore
    except json.decoder.JSONDecodeError as e:
        err = e
    # if it is a code block
    pattern = r"```(\w*)\s*(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    if matches:
        block_type, block_content = matches[0]
        try:
            return load_json(block_content)  # type: ignore
        except json.decoder.JSONDecodeError as e:
            err = e
    # if it contains the start of a code block
    pattern = r"```(\w*)\s*(.*?)"
    matches = re.findall(pattern, text, re.DOTALL)
    if matches:
        block_type, block_content = matches[0]
        try:
            return load_json(block_content)  # type: ignore
        except json.decoder.JSONDecodeError:
            pass
    # try to find any json in the text
    pattern = r"\{(?:[^{}]|(?R))*\}"
    try:
        json_data = regex.search(pattern, text)
        if json_data:
            return load_json(json_data.group())  # type: ignore
    except Exception as e:
        pass
    warnings.warn(err)  # type: ignore


def add_comma(json_str: str) -> str:
    """Attempt to add commas to a json string, i.e. if it is a relaxed json string"""
    json_str = json_str.strip()

    def _add_comma(t):  # allow for relaxed json
        if t.endswith(",") or t.endswith("{") or t.endswith("["):
            return t
        return t + ","

    json_str = "\n".join([_add_comma(l) for l in json_str.split("\n")])
    json_str = json_str.strip()[:-1]  # remove last comma
    return json_str


def load_json(text: str):
    """A function to load json from a string with error handling e.g. for json using single quotes"""
    # load as pure json
    try:
        return json.loads(text)
    except json.decoder.JSONDecodeError as e:
        err = e
        pass
    # if it fails try to load it as a python object (dict or list)
    try:
        obj = ast.literal_eval(text)
        if isinstance(obj, (dict, list)):
            return obj
    except Exception:
        pass
    # if it fails try to load it as a demjson object
    try:
        return demjson3.decode(text)
    except demjson3.JSONDecodeError as e:
        if e.message == "Values must be separated by a comma":  # type: ignore
            text = add_comma(text)
            return load_json(text)
    raise err
