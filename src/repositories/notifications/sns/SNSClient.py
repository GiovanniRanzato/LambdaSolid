import boto3

from repositories.interfaces.MessageI import MessageI
from repositories.interfaces.NotificactionI import NotificationI


class SNSClient(NotificationI):
    def __init__(self, region_name, topic_arn: str, endpoint_url: str = None):
        self.topic_arn = topic_arn
        self.client = boto3.client("sns", region_name=region_name, endpoint_url=endpoint_url)

    def publish(self, event: MessageI):
        self.client.publish(Message=str(event), TopicArn=self.topic_arn)