
import pytest

from nanoevent import Dispatcher

def create_event_listener(text: str):
    def listener(event_arg: dict):
        event_arg.append(text)

    return listener

def test_dispatch_will_trigger_wildcard_listener():
    d = Dispatcher()
    l = []

    d.attach_to_all(create_event_listener('first test message'))

    d.emit('event:name', l)

    assert 1 == len(l)
    assert l[0] == 'first test message'

def test_remove_wildcard_listener():
    d = Dispatcher()
    l = []

    first_listener = create_event_listener('first test message')
    second_listener = create_event_listener('second test message')

    d.attach_to_all(first_listener)
    d.attach_to_all(second_listener)

    d.remove_from_all(second_listener)

    d.emit('event:name', l)

    assert len(l) == 1
    assert l[0] == 'first test message'