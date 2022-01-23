import os

from chalice import Chalice, NotFoundError, BadRequestError

from chalicelib import database

app = Chalice(app_name='chalice_demo')


@app.route('/')
def index():
    return {'hello': 'world'}

@app.route('/hello/{name}')
def hello_name(name):
   # '/hello/james' -> {"hello": "james"}
   return {'hello': name}

@app.route('/records', methods=['GET'], cors=True)
def get_all_records():
    print('*** get_all_records ***')
    return database.get_all_records()

@app.route('/records/query/{runner_name}', methods=['GET'], cors=True)
def query_records(runner_name):
    return database.query_records(runner_name)

@app.route('/records/{record_id}', methods=['GET'], cors=True)
def get_records(record_id):
    record = database.get_record(record_id)
    if record:
        return record
    else:
        raise NotFoundError('Record not found.')

@app.route('/records', methods=['POST'], cors=True)
def create_record():
    print('*** create_record ***')

    record = app.current_request.json_body
    # 必須項目をチェックする
    for key in ['runner_name','race','team','result_time','section']:
        if key not in record:
            raise BadRequestError(f"{key} is required.")

    sub = get_sub()
    record['sub'] = sub
    return database.create_record(record)

def get_sub():
    if os.environ.get('IS_LOCAL'):
        return 'LOCAL_USER'
    else:
        return 'AWS'
        # return app.current_request.context['authorizer']['claims']['sub']