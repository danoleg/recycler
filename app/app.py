import json
import ssl

from flask_restful import Api, Resource, reqparse
from flask import Flask, redirect, render_template, request, url_for
from flask_cors import CORS
from helpers.encoder import DateTimeEncoder
from helpers.iris import iris_connection
from importer import json_to_iris

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

app.config['iris_host'] = "iris"
app.config['iris_port'] = 1972
app.config['iris_namespace'] = "USER"
app.config['iris_username'] = "_SYSTEM"
app.config['iris_password'] = "demopass"


class ImportDataset(Resource):
    def post(self):
        global_name = "Items"
        with open('data/demodata.json') as f:
            data = json.load(f)
            try:
                kill_iris_global(global_name)
            except Exception:
                ...

            result, iris_data = json_to_iris(json.dumps(data), global_name)
        if result:
            data = {
                "status": True,
                "message": "Imported successfully",
            }
        else:
            data = {
                "status": False,
                "message": "Invalid json",
                "data": data
            }

        return data


class SetData(Resource):
    def get(self):
        data = {
            "iris_host": app.config['iris_host'],
            "iris_port": app.config['iris_port'],
            "iris_namespace": app.config['iris_namespace'],
            "iris_username": app.config['iris_username'],
            "iris_password": app.config['iris_password']
        }
        return data


class GetData(Resource):
    def post(self):
        post_parser = reqparse.RequestParser()
        args = post_parser.parse_args()
        global_name = "Items"
        items = []

        with iris_connection() as iris:
            i = 0
            while True:
                item = iris.get(global_name, 'items', i, 'title')
                if not item:
                    break

                if iris.get(global_name, 'items', i, 'deleted'):
                    i += 1
                    continue

                items.append({
                    "id": i,
                    "title": iris.get(global_name, 'items', i, 'title'),
                    "description": iris.get(global_name, 'items', i, 'description'),
                    "location": iris.get(global_name, 'items', i, 'location'),
                    "country": iris.get(global_name, 'items', i, 'country'),
                    "city": iris.get(global_name, 'items', i, 'city'),
                    "longitude": float(iris.get(global_name, 'items', i, 'longitude') or 0),
                    "latitude": float(iris.get(global_name, 'items', i, 'latitude') or 0),
                    "datetime": iris.get(global_name, 'items', i, 'datetime'),
                })
                i += 1

        data = {
            "status": True,
            "data": items[::-1]
        }
        return data


class UpdateData(Resource):
    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('title')
        post_parser.add_argument('description')
        post_parser.add_argument('location')
        post_parser.add_argument('country')
        post_parser.add_argument('city')
        post_parser.add_argument('longitude')
        post_parser.add_argument('latitude')
        post_parser.add_argument('datetime')
        post_parser.add_argument('number')
        args = post_parser.parse_args()
        global_name = "Items"

        with iris_connection() as iris:
            iris.set(args.title, global_name, 'items', args.number, 'title')
            iris.set(args.description, global_name, 'items', args.number, 'description')
            iris.set(args.location, global_name, 'items', args.number, 'location')
            iris.set(args.country, global_name, 'items', args.number, 'country')
            iris.set(args.city, global_name, 'items', args.number, 'city')
            iris.set(args.longitude, global_name, 'items', args.number, 'longitude')
            iris.set(args.latitude, global_name, 'items', args.number, 'latitude')
            iris.set(args.datetime, global_name, 'items', args.number, 'datetime')
        data = {
            "status": True
        }
        return data


class DeleteData(Resource):
    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('id')
        args = post_parser.parse_args()

        global_name = "Items"
        with iris_connection() as iris:
            iris.set(True, global_name, 'items', args.id, 'deleted')

        return {
            "status": True
        }


class CheckGlobal(Resource):
    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('name')
        post_parser.add_argument('node')
        args = post_parser.parse_args()
        with iris_connection() as iris:
            iris_root_nodes_count = iris.count_root_nodes(args.name)
        data = {
            "status": True,
            "data": iris_root_nodes_count
        }

        return data


class DeleteGlobal(Resource):
    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('name')
        args = post_parser.parse_args()
        result = kill_iris_global(args.name)
        if result:
            data = {
                "status": True,
                "message": f"{args.name} removed successfully",
            }
        else:
            data = {
                "status": False,
                "message": "Error"
            }

        return data


class Settings(Resource):
    def get(self):
        data = {
            "iris_host": app.config['iris_host'],
            "iris_port": app.config['iris_port'],
            "iris_namespace": app.config['iris_namespace'],
            "iris_username": app.config['iris_username'],
            "iris_password": app.config['iris_password']
        }
        return data


class IRISSettings(Resource):
    def post(self):
        post_parser = reqparse.RequestParser()
        post_parser.add_argument('iris_host')
        post_parser.add_argument('iris_port')
        post_parser.add_argument('iris_namespace')
        post_parser.add_argument('iris_username')
        post_parser.add_argument('iris_password')
        args = post_parser.parse_args()

        try:
            connection = args.iris_host, int(args.iris_port), args.iris_namespace, args.iris_username, args.iris_password
            with iris_connection(*connection) as iris:
                pass
        except Exception as e:
            data = {
                "result": "Error",
                "details": str(e)
            }
            return data

        app.config['iris_host'] = args.iris_host
        app.config['iris_port'] = int(args.iris_port)
        app.config['iris_namespace'] = args.iris_namespace
        app.config['iris_username'] = args.iris_username
        app.config['iris_password'] = args.iris_password

        data = {
            "result": "Success"
        }
        return data

api.add_resource(ImportDataset, '/import-dataset')
api.add_resource(GetData, '/data/getting')
api.add_resource(UpdateData, '/data/set')
api.add_resource(DeleteData, '/data/delete')
api.add_resource(DeleteGlobal, '/remove-global-from-iris')
api.add_resource(CheckGlobal, '/check-global-from-iris')
api.add_resource(IRISSettings, '/settings/iris')
api.add_resource(Settings, '/settings')


def kill_iris_global(root_item):
    with iris_connection() as iris:
        iris.kill(root_item)
    return 1

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8011)
