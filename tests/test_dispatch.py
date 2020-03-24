import pytest

from nanoevent import Dispatcher

def create_event_handler(text: str):
    def handler(event_arg: dict):
        event_arg.append(text)

    return handler

def test_dispatch_will_trigger_handler():
    d = Dispatcher()
    l = []

    d.attach('event:name', create_event_handler('first test message'))
    d.attach('event:name', create_event_handler('second test message'))

    d.emit('event:name', l)

    assert l[0] == 'first test message'
    assert l[1] == 'second test message'

def test_remove_listener():
    d = Dispatcher()

    first_handler = create_event_handler('first test message')
    second_handler = create_event_handler('second test message')

    d.attach('event:name', first_handler)
    d.attach('event:name', second_handler)

    d.remove('event:name', second_handler)

    l = []
    d.emit('event:name', l)

    assert len(l) == 1
    assert l[0] == 'first test message'


def test_respects_args_and_kwargs():
    d = Dispatcher()

    def create_handler():
        def handler(l: list, *args, **kwargs):
            text = 'args = %s and kwargs = %s' % (args, kwargs)

            l.append(text)
            
        return handler

    d.attach('event:name', create_handler())

    l = []
    d.emit('event:name', l, 'foo', bar="bar")

    assert "args = ('foo',) and kwargs = {'bar': 'bar'}" == l[0]
    

