"""
Apply deduplication and quality filter to NetArkivet TextCorpus.
"""
from typing import Iterable, Optional, List, Union
from pathlib import Path
import random

from contextlib import ExitStack

from .shuffle_bufferimport import shuffle_buffer

import ndjson


def jsonl_merge(
    jsonl_files: List[Union[Path, str]],
    buffer_size: Optional[int] = None,
    sample: bool = True,
) -> Iterable[dict]:
    """
    Merge a list of jsonl files into an iterable of json objects

    Args:
        json_files (List[Union[Path, str]]): A list of jsonl or ndjson file paths.
        buffer_size (Optional[int], optional): Buffer size. I specified add a shuffle buffer with the defined
            buffer size. Default to None.
        sample (bool, optional): Should the iterable sample from the json files (True) or should it read then in order?
            Defaults to True.
    """

    def __sample_yield(readers: list) -> Iterable:
        while readers:
            i = random.randint(0, len(readers) - 1)
            reader = readers[i]
            try:
                yield next(reader)
            except StopIteration:
                readers.pop(i)

    def __iterative_yield(readers: list) -> Iterable:
        for reader in readers:
            for sample in reader:
                yield sample

    yield_fn = __sample_yield if sample is True else __iterative_yield

    if buffer_size:
        json_gen = shuffle_buffer(
            jsonl_merge(jsonl_files=jsonl_files, buffer_size=None, sample=sample),
            buffer_size=buffer_size,
        )
        for sample in json_gen:
            yield sample
    else:
        with ExitStack() as stack:
            files = [stack.enter_context(open(filename)) for filename in jsonl_files]
            readers = [ndjson.reader(f) for f in files]

            for sample in yield_fn(readers):
                yield sample
