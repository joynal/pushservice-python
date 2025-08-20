import json
from unittest.mock import AsyncMock
from unittest.mock import Mock
from unittest.mock import patch
from uuid import UUID
from uuid import uuid4

import pytest
from kafka.consumer.fetcher import ConsumerRecord
from pushservice.core.domain.entities import Subscriber
from pushservice.core.use_cases.push_parser import PushParser
from pushservice.settings import KafkaSettings
from pushservice.settings import Settings
from pushservice.settings import WorkerSettings


class TestPushParser:
    @pytest.fixture
    def mock_settings(self):
        """Create mock settings for testing."""
        kafka_settings = KafkaSettings(
            enabled=True, brokers=["localhost:9092"], heartbeat=60
        )
        sender_settings = WorkerSettings(
            topic="sender-topic", group_id="sender-group", log_level="info"
        )

        settings = Mock(spec=Settings)
        settings.kafka = kafka_settings
        settings.sender = sender_settings
        return settings

    @pytest.fixture
    def mock_subscriber_repo(self):
        """Create mock subscriber repository."""
        return Mock()

    @pytest.fixture
    def sample_push_data(self):
        """Create sample push data for testing."""
        push_id = uuid4()
        site_id = uuid4()

        return {
            "id": str(push_id),
            "site_id": str(site_id),
            "title": "Test Notification",
            "status": "pending",
            "launch_url": "https://example.com",
            "priority": "normal",
            "time_to_live": 3600,
            "options": {
                "body": "This is a test notification",
                "icon": "https://example.com/icon.png",
            },
            "vapid_private_key": "test-private-key",
        }

    @pytest.fixture
    def sample_subscriber(self):
        """Create sample subscriber for testing."""
        return Subscriber(
            id=uuid4(),
            site_id=uuid4(),
            subscription_info={
                "endpoint": "https://fcm.googleapis.com/fcm/send/test",
                "keys": {"p256dh": "test-p256dh-key", "auth": "test-auth-key"},
            },
            subscribed=True,
        )

    @pytest.fixture
    def kafka_message(self, sample_push_data):
        """Create a mock Kafka ConsumerRecord."""
        message = Mock(spec=ConsumerRecord)
        message.value = json.dumps(sample_push_data).encode("utf-8")
        return message

    @pytest.fixture
    def push_parser(self, mock_settings, mock_subscriber_repo):
        """Create PushParser instance with mocked dependencies."""
        with patch("pushservice.core.use_cases.push_parser.KafkaPublisher"):
            parser = PushParser(mock_settings, mock_subscriber_repo)
            parser.producer = Mock()
            return parser

    @pytest.mark.asyncio
    async def test_process_successful_push_parsing(
        self,
        push_parser,
        kafka_message,
        sample_subscriber,
        mock_subscriber_repo,
        sample_push_data,
    ):
        """Test successful processing of a push message."""
        # Setup
        mock_subscriber_repo.get_all = AsyncMock()

        # Configure the get_all method to call the callback with our sample subscriber
        async def mock_get_all(site_id, callback):
            await callback(sample_subscriber)

        mock_subscriber_repo.get_all.side_effect = mock_get_all

        # Execute
        await push_parser.process(kafka_message)

        # Verify
        mock_subscriber_repo.get_all.assert_called_once()
        call_args = mock_subscriber_repo.get_all.call_args

        # Check that site_id was passed correctly
        assert call_args.kwargs["site_id"] == UUID(sample_push_data["site_id"])

        # Verify that producer.publish was called
        push_parser.producer.publish.assert_called_once()
        publish_call_args = push_parser.producer.publish.call_args

        # Check topic
        assert publish_call_args[0][0] == "sender-topic"

        # Check that the published data contains expected fields
        published_data = json.loads(publish_call_args[0][1].decode("utf-8"))
        assert (
            published_data["push_id"] == UUID(sample_push_data["id"]).hex
        )  # UUIDEncoder converts to hex
        assert (
            published_data["subscription_info"] == sample_subscriber.subscription_info
        )
        assert published_data["ttl"] == sample_push_data["time_to_live"]
        assert (
            published_data["vapid_private_key"] == sample_push_data["vapid_private_key"]
        )
        assert published_data["vapid_claims"]["sub"] == "https://joynal.dev"

        # Check the data payload
        data_payload = json.loads(published_data["data"])
        assert data_payload["title"] == sample_push_data["title"]
        assert data_payload["launch_url"] == sample_push_data["launch_url"]
        assert data_payload["priority"] == sample_push_data["priority"]
        assert data_payload["options"] == sample_push_data["options"]

    @pytest.mark.asyncio
    async def test_process_with_invalid_json(self, push_parser):
        """Test processing with invalid JSON in message."""
        # Setup
        invalid_message = Mock(spec=ConsumerRecord)
        invalid_message.value = b"invalid json"

        # Execute & Verify
        with pytest.raises(json.JSONDecodeError):
            await push_parser.process(invalid_message)

    @pytest.mark.asyncio
    async def test_process_calls_subscriber_repo_with_correct_site_id(
        self, push_parser, kafka_message, mock_subscriber_repo, sample_push_data
    ):
        """Test that subscriber repository is called with correct site_id."""
        # Setup
        mock_subscriber_repo.get_all = AsyncMock()

        # Execute
        await push_parser.process(kafka_message)

        # Verify
        mock_subscriber_repo.get_all.assert_called_once()
        call_args = mock_subscriber_repo.get_all.call_args
        assert call_args.kwargs["site_id"] == UUID(sample_push_data["site_id"])
        assert "callback" in call_args.kwargs

    @pytest.mark.asyncio
    async def test_process_multiple_subscribers(
        self, push_parser, kafka_message, mock_subscriber_repo, sample_push_data
    ):
        """Test processing with multiple subscribers."""
        # Setup
        subscriber1 = Subscriber(
            id=uuid4(),
            site_id=UUID(sample_push_data["site_id"]),
            subscription_info={"endpoint": "https://fcm1.test"},
            subscribed=True,
        )
        subscriber2 = Subscriber(
            id=uuid4(),
            site_id=UUID(sample_push_data["site_id"]),
            subscription_info={"endpoint": "https://fcm2.test"},
            subscribed=True,
        )

        # Configure mock to call callback for each subscriber
        async def mock_get_all(site_id, callback):
            await callback(subscriber1)
            await callback(subscriber2)

        mock_subscriber_repo.get_all = AsyncMock(side_effect=mock_get_all)

        # Execute
        await push_parser.process(kafka_message)

        # Verify
        assert push_parser.producer.publish.call_count == 2

        # Check that both subscribers' data was published
        calls = push_parser.producer.publish.call_args_list
        published_data_1 = json.loads(calls[0][0][1].decode("utf-8"))
        published_data_2 = json.loads(calls[1][0][1].decode("utf-8"))

        assert published_data_1["subscription_info"] == subscriber1.subscription_info
        assert published_data_2["subscription_info"] == subscriber2.subscription_info
