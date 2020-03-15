from chalice import Chalice, Response
import boto3
from remote_sqlite import RemoteSqlite
app = Chalice(app_name='lambda-s3')

sts = boto3.client('sts')
s3 = boto3.client('s3')
account = sts.get_caller_identity()['Account']
bucket_name = f'{app.app_name}-{account}'
my_session = boto3.session.Session()
region_name = my_session.region_name

@app.route('/')
def index():
    return Response(status_code=200, headers={'Content-Type': 'text/plain'}, 
      body="""USAGE:\ncurl -X POST -H 'Content-Type: application/json' -d @data.json https://4a5znnfdz0.execute-api.us-west-2.amazonaws.com/api/insert/default.sqlite/test\n\ncurl -X POST -H 'Content-Type: application/json' -d @select.json https://4a5znnfdz0.execute-api.us-west-2.amazonaws.com/api/select/default.sqlite\n\ncurl -X POST -H 'Content-Type: application/json' -d @delete.json https://4a5znnfdz0.execute-api.us-west-2.amazonaws.com/api/execute/default.sqlite\n\ncurl -X POST -H 'Content-Type: application/json' -d @data.json https://4a5znnfdz0.execute-api.us-west-2.amazonaws.com/api/generate_create_table/default.sqlite/test\n\n""")

@app.route('/insert/{database}/{table}', methods=['POST'])
def insert(database, table):
    fspath = f's3://{bucket_name}/{database}'
    db = RemoteSqlite(f's3://{bucket_name}/{database}')
    db.insert(table, app.current_request.json_body)
    db.push(fspath)
    return {'success': True}

@app.route('/select/{database}', methods=['POST'])
def select(database):
    db = RemoteSqlite(f's3://{bucket_name}/{database}')
    return db.select(app.current_request.json_body['select_statement'])    

@app.route('/execute/{database}', methods=['POST'])
def execute(database):
    fspath = f's3://{bucket_name}/{database}'
    db = RemoteSqlite(fspath)
    db.con.cursor().execute(app.current_request.json_body['sql_statement'])
    db.con.commit()
    db.push(fspath)
    return {'success': True}

@app.route('/generate_create_table/{database}/{tbl_name}', methods=['POST'])
def generate_create_table(database, tbl_name):
    fspath = f's3://{bucket_name}/{database}'
    db = RemoteSqlite(fspath)
    return db.generate_create_table(tbl_name, app.current_request.json_body)


@app.route('/create_bucket')
def create_bucket():
    s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': region_name})
    return {'success': True}


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
