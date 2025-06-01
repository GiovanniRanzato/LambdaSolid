from unittest.mock import MagicMock

import pytest

from outputs.notifications.interfaces.MessageI import MessageI
from outputs.notifications.interfaces.NotificactionI import NotificationI
from outputs.notifications.sns.SNSClient import SNSClient


class TestSNSClient:
    @pytest.fixture
    def boto3_client(self):
        mock = MagicMock()
        mock.publish.return_value = True
        return mock

    @pytest.fixture
    def sns_client(self, boto3_client, mocker):
        mocker.patch("boto3.client", return_value=boto3_client)
        return SNSClient(
            region_name="us-east-1",
            topic_arn="arn:aws:sns:us-east-1:123456789012:MyTopic",
            endpoint_url="http://localhost:4566"
        )

    def test_init(self, sns_client, boto3_client):
        assert isinstance(sns_client, SNSClient)
        assert isinstance(sns_client, NotificationI)
        sns_client.client = boto3_client

    def test_publish(self, sns_client):
        message = MagicMock(spec=MessageI)
        message.__str__.return_value = "Test message"

        sns_client.publish(message)

        sns_client.client.publish.assert_called_once_with(
            Message="Test message",
            TopicArn=sns_client.topic_arn
        )
