from unittest.mock import MagicMock

import pytest
from app.events.EventFactory import EventFactory
from app.events.EventI import EventI
from app.events.EventsRegistry import EventsRegistry


class TestEventFactory:
    @pytest.fixture
    def events_registry(self):
        return MagicMock(spec=EventsRegistry)

    @pytest.fixture
    def event_factory(self, events_registry):
        return EventFactory(events_registry=events_registry)

    def test_init(self, event_factory, events_registry):
        assert isinstance(event_factory, EventFactory)
        assert event_factory.events_registry == events_registry

    def test_create_event(self, event_factory, events_registry):
        event = {'key': 'value'}
        context = {'context_key': 'context_value'}

        expected_event = MagicMock(spec=EventI)

        registered_event= MagicMock(spec=EventI)
        registered_event.is_valid.return_value = True
        registered_event.from_dict.return_value = expected_event

        events_registry.get_events_registry.return_value = {'registered_event': registered_event}
        parsed_event = event_factory.create_event(event, context)

        assert parsed_event == expected_event
        registered_event.is_valid.assert_called_once_with(event)
        registered_event.from_dict.assert_called_once_with(event, context)

    def test_fail_create_event(self, event_factory, events_registry):
        event = {'key': 'value'}
        context = {'context_key': 'context_value'}

        registered_event= MagicMock(spec=EventI)
        registered_event.is_valid.return_value = False

        events_registry.get_events_registry.return_value = {'registered_event': registered_event}

        with pytest.raises(ValueError, match="Unknown event type: {'key': 'value'}"):
            event_factory.create_event(event, context)
            registered_event.is_valid.assert_called_once_with(event)
