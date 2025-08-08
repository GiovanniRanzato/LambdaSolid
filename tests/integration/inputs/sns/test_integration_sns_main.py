import json

import pytest
from src import main


class TestMain:
    @pytest.fixture
    def sns_event(self):
        return {
            "EventSource": "aws:sns",
            "EventVersion": "1.0",
            "EventSubscriptionArn": "arn:aws:sns:eu-south-1:051061611576:B23MicroLayer_Queue-staging:334e3626-f4af-42b2"
                                    "-8f93-0934f9d09d49",
            "Sns": {
                "Type": "Notification",
                "MessageId": "7f840f13-77ec-516c-b165-5384bdc50919",
                "TopicArn": "arn:aws:sns:eu-south-1:051061611576:B23MicroLayer_Queue-staging",
                "Subject": None,
                "Message": "The message body",
                "Timestamp": "2023-03-24T15:55:21.505Z",
                "SignatureVersion": "1",
                "Signature": "CPz7NmV3KIPYQyr9NqKTG0E7cSnG9HFRVdM2R6WgUYThMbo7CtzrJYdTOzmGI1GT9yGEWCzxP7KwS/Q4manYFNe5Q"
                             "teSq4AYxy6UjojdmzLRUIoT+BYNArjD2+GIJZ9GjvLSu4ous1BTGEJyp00oPQkOdFI7EJLRM5CkTJx66NFmdDUfz2"
                             "Dm+j8UT+iEOWSkI4B/c9Y0Hz8lAnHqd46lRkt2NU7y4AE+HLqO15baVdarXMYzjuse4e0Poh/Z9LVLo7fr+rzTBc6"
                             "d0gCgwEyXeIf95FzKkg6FejJQsZ3t7KJNliPXY7BVdorb4c/5p1caNW9hgQQzU5WOrmiwEAEglg==",
                "SigningCertUrl": "https://sns.eu-south-1.amazonaws.com/SimpleNotificationService-08e3ac09e3c5c4a53e8f2"
                                  "b37fe5847c0.pem",
                "UnsubscribeUrl": "https://sns.eu-south-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns"
                                  ":eu-south-1:051061611576:B23MicroLayer_Queue-staging:334e3626-f4af-42b2-8f93-0934f9d"
                                  "09d49",
                "MessageAttributes": {},
            },
        }

    def test_sns_event(self, sns_event, mocker):
        logging_error_mock = mocker.patch("logging.error")
        sns_event["Sns"]["Message"] = json.dumps({"type": "SNSEventSample", "name": "The sample name"})
        main.lambda_handler(sns_event, None)

        logging_error_mock.assert_not_called()
