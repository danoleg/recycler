import pymongo

from flask import current_app
from helpers.iris import iris_connection
from helpers.parser import parse_dict
from helpers.validator import validate_json


def json_to_iris(input_data: str, global_name: str) -> tuple:

    data, status = validate_json(input_data)
    if not status:
        return False, None
    else:
        with iris_connection() as iris:
            iris_comp_data = parse_dict(data)
            for item in iris_comp_data:
                path_list = item['path_list']
                iris.set(item['value'], global_name, *path_list)
            return True, iris_comp_data





