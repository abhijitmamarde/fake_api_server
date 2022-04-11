from flask import Flask, request, jsonify
from flask_cors import cross_origin
import json

app = Flask(__name__)


def get_display_name(col_name):
    """
    Utility function to get the display name for the given column

    - Changes to Title case
    - Replaces underscores to spaces etc
    """
    display_name = col_name.replace("_", " ")
    display_name = display_name.title()
    # Common word replacements
    if display_name == "Id":
        display_name = "ID"
    display_name = display_name.replace("Ip ", "IP ")
    return display_name


@app.route("/test")
def hello_world():
    return "<p>Hello, Server is <b>running!</b</p>"


@app.route("/api/<name>", methods=["GET", "POST"])
@cross_origin(origins=["*"])
def host_api(name):
    """
    Mock API handler, Supports CORS!

    In order to mimick the API, just need to have the <name>.json file in `api` folder.
    Sample jsons are created using - https://www.mockaroo.com/
    Can be added more as required!!!

    Supported/jsons available as of now:
        - /api/users
        - /api/customers

    Both GET and POST method is allowed

    For POST, following input params are supported:
        - offset (default: 0)
        - limit (default: 20)
        - sort_by (default: "id")
            - for reverse sort pass -<col_name>
    
    For GET method all records are fetched!
    """
    print(f"Inside trigger API for {name}")
    default_params = {
        "offset": 0,
        "limit": 20,
        "sort_by": "id",
    }
    p = {}
    try:
        p = request.get_json(force=True, silent=True)
        if p is None:
            p = {}
    except:
        print("No JSON passed, assuming the default!!!")
    
    for k, v in default_params.items():
        if k not in p:
            p[k] = v
        if not p[k]:
            p[k] = v

    data = json.load(open(f"api/{name}.json", encoding='utf8'))
    total_recs = len(data)
    columns = []
    display_columns = {}
    
    if data:
        columns = list(data[0].keys())
        display_columns = {x: get_display_name(x) for x in columns}

    if p["sort_by"]:
        rev_sort = False
        col_name = p["sort_by"]
        if col_name.startswith("-"):
            rev_sort = True
            col_name = col_name[1:]
        # for sorting, consider None value as ""
        data = sorted(data, key=lambda x: x[col_name] if x[col_name] else "", reverse=rev_sort)
    if request.method == "POST":
        data = data[p['offset']:p['offset'] + p['limit']]
    elif request.method == "GET":
        p['limit'] = total_recs

    # if any value is None, send in UI as ""
    for r in data:
        for k, v in r.items():
            if v is None:
                r[k] = ""
    
    if not data:
        p["err_msg"] = "No Records Exists!!!"

    
    return jsonify({
        **p,
        "total_recs": total_recs,
        "columns": columns,
        "display_columns": display_columns,
        "data": data,
    })
