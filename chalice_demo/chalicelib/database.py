import os
import boto3
from boto3.dynamodb.conditions import Key, Attr
import uuid


def _get_database():
    endpoint = os.environ.get('DB_ENDPOINT')
    if endpoint:
        print('*** DB_ENDPOINT指定あり ***')
        print(endpoint)
        return boto3.resource('dynamodb', endpoint_url=endpoint)
    else:
        print('*** DB_ENDPOINT指定なし ***')
        return boto3.resource('dynamodb')


def get_all_records():
    print('get_all_records****')
    table = _get_database().Table(os.environ['DB_TABLE_NAME'])
    # debug用のプリント
    print('****')
    print(table)
    print('****')
    response = table.scan()
    return response['Items']


def query_records(runner_name):
    table = _get_database().Table(os.environ['DB_TABLE_NAME'])
    response = table.scan(
        FilterExpression=Attr('runner_name').eq(runner_name)
    )
    return response['Items']


def get_record(record_id):
    table = _get_database().Table(os.environ['DB_TABLE_NAME'])
    response = table.query(KeyConditionExpression=Key('id').eq(record_id))
    items = response['Items']
    return items[0] if items else None


def create_record(record):
    item = {
        'id': uuid.uuid4().hex,
        'sub': record['sub'],
        'race': record['race'],
        'runner_name': record['runner_name'],
        'team': record['team'],
        'result_time': record['result_time'],
        'section': record['section'],
        'description': record['description']
    }
    table = _get_database().Table(os.environ['DB_TABLE_NAME'])
    table.put_item(Item=item)
    return item


def update_record(record_id, changes):
    table = _get_database().Table(os.environ['DB_TABLE_NAME'])

    update_expression = []
    expression_attribute_values = {}
    for key in ['runner_name', 'race', 'team', 'time', 'result_time', 'section', 'description']:
        if key in changes:
            update_expression.append(f"{key} = :{key[0:2]}")
            expression_attribute_values[f":{key[0:2]}"] = changes[key]

    print(update_expression)
    print(expression_attribute_values)

    result = table.update_item(
        Key={
            'id': record_id,
        },
        UpdateExpression='set ' + ','.join(update_expression),
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues='ALL_NEW'
    )
    return result['Attributes']


def delete_record(record_id):
    table = _get_database().Table(os.environ['DB_TABLE_NAME'])

    result = table.delete_item(
        Key={
            'id': record_id,
        },
        ReturnValues='ALL_OLD'
    )
    return result['Attributes']
