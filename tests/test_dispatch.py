import pytest

from nanoevent import Dispatcher

def create_event_listener(text: str):
    def listener(event_arg: dict):
        event_arg.append(text)

    return listener

def test_dispatch_will_trigger_listener():
    d = Dispatcher()
    l = []

    d.attach('event:name', create_event_listener('first test message'))
    d.attach('event:name', create_event_listener('second test message'))

    d.emit('event:name', l)

    assert l[0] == 'first test message'
    assert l[1] == 'second test message'

def test_remove_listener():
    d = Dispatcher()

    first_listener = create_event_listener('first test message')
    second_listener = create_event_listener('second test message')

    d.attach('event:name', first_listener)
    d.attach('event:name', second_listener)

    d.remove('event:name', second_listener)

    l = []
    d.emit('event:name', l)

    assert len(l) == 1
    assert l[0] == 'first test message'

def test_respects_args_and_kwargs():
    d = Dispatcher()

    def create_listener():
        def listener(l: list, *args, **kwargs):
            text = 'args = %s and kwargs = %s' % (args, kwargs)

            l.append(text)
            
        return listener

    d.attach('event:name', create_listener())

    l = []
    d.emit('event:name', l, 'foo', bar="bar")

    assert "args = ('foo',) and kwargs = {'bar': 'bar'}" == l[0]