# fake_api_server

Flask based fake api server, serving API responses from json files

### Dependencies:

- Flask
- Flask-Cors

### Logic

Hosts json files available under `api` folder at route: `/api/<name_of_json>`

Example:

File named `api/users.json` is available at route: `/api/users`
