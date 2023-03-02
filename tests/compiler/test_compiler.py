"""This module tests BQSKit's Compiler object."""
from __future__ import annotations

import logging
from io import StringIO

import pytest

from bqskit.compiler.basepass import BasePass
from bqskit.compiler.compiler import Compiler
from bqskit.compiler.passdata import PassData
from bqskit.ir.circuit import Circuit


class ErrorPass(BasePass):
    async def run(self, circuit: Circuit, data: PassData) -> None:
        raise RuntimeError()


class LogPass(BasePass):
    async def run(
        self,
        circuit: Circuit,
        data: PassData,
    ) -> None:
        logging.getLogger('bqskit.dummy').debug('Test.')


def test_errors_raised_locally() -> None:
    with pytest.raises(RuntimeError):
        with Compiler() as compiler:
            compiler.compile(Circuit(1), [ErrorPass()])


def test_log_msg_printed_locally() -> None:
    logger = logging.getLogger('bqskit')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(StringIO())
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    with Compiler() as compiler:
        compiler.compile(Circuit(1), [LogPass()])
    assert 'Test.' in handler.stream.getvalue()
    logger.removeHandler(handler)
    logger.setLevel(logging.WARNING)
