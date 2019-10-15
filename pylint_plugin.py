"""Plugin to disable certain messages for test modules"""

from collections import Callable  # pylint:disable=no-name-in-module

from pylint.lint import PyLinter

TESTS_DISABLED = ['line-too-long',
                  'missing-docstring',
                  'invalid-name',
                  'no-member',
                  'too-few-public-methods',
                  'super-init-not-called',
                  'broad-except',
                  'comparison-with-callable',
                  'attribute-defined-outside-init']


def register(linter: PyLinter):
    """disable certain messages for test modules"""
    msg_ids = _get_msg_ids(linter)
    base = linter.add_one_message
    linter.add_one_message = lambda *args: \
        add_one_message(*args, linter=linter, base=base, msg_ids=msg_ids)  # pylint:disable=no-value-for-parameter


def _get_msg_ids(linter: PyLinter):
    msg_ids = []
    for msg_symbol in TESTS_DISABLED:
        for msg_def in linter.msgs_store.get_message_definitions(msg_symbol):
            msg_ids.append(msg_def.msgid)
    return msg_ids


def add_one_message(message_definition, *args,
                    linter: PyLinter = None, base: Callable = None, msg_ids=None):
    """skips disabled messages for test modules"""
    if linter.current_name \
            and 'test' in linter.current_name \
            and message_definition.msgid in msg_ids:
        return
    base(message_definition, *args)
