# CloudWatchLogs出力内容をSNSでメール送信
import base64
import json
import zlib
import datetime
import os
import boto3
from botocore.exceptions import ClientError

print('Loading function')


def lambda_handler(event, context):
    data = zlib.decompress(base64.b64decode(
        event['awslogs']['data']), 16+zlib.MAX_WBITS)
    data_json = json.loads(data)
    log_json = json.loads(json.dumps(
        data_json["logEvents"][0], ensure_ascii=False))

    print(log_json)
    message = """
管理画面よりコンテンツ登録が行われましたのでお知らせいたします。

<登録内容>
{0}
""".format(log_json['message'])

    try:
        sns = boto3.client('sns')

        # SNS Publish
        publishResponse = sns.publish(
            TopicArn=os.environ['SNS_TOPIC_ARN'],
            Message=message,
            Subject=os.environ['ALARM_SUBJECT']
        )

    except Exception as e:
        print(e)
