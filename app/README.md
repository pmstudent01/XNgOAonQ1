# Vehicle Service App

A small Python application that implements the **Vehicle Service API** by wiring
together the Postman-generated SDK
(`vehicle_service_collection_sdk`, under
`postman/sdks/Collections SDKs/Vehicle Service Collection/python`).

It exposes all five operations from the **Vehicle Service Collection**:

| Operation       | HTTP                     | SDK method              | App method        |
| --------------- | ------------------------ | ----------------------- | ----------------- |
| List vehicles   | `GET /vehicles`          | `get_all_vehicles`      | `list_vehicles`   |
| Retrieve vehicle| `GET /vehicles/{id}`     | `retrieve_a_vehicle`    | `get_vehicle`     |
| Create vehicle  | `POST /vehicles`         | `create_a_vehicle`      | `create_vehicle`  |
| Update vehicle  | `PATCH /vehicles/{id}`   | `update_a_collection`   | `update_vehicle`  |
| Delete vehicle  | `DELETE /vehicles/{id}`  | `delete_a_vehicle`      | `delete_vehicle`  |

## Layout

```
app/
  __init__.py       # package marker
  config.py         # env-based settings (base URL, api key, timeout)
  client.py         # VehicleServiceClient facade over the generated SDK
  cli.py            # command-line entry point (python -m app.cli)
  requirements.txt  # installs the local SDK (editable) + python-dotenv
  .env.example      # sample configuration
```

## Setup

From the repository root:

```bash
python -m venv .venv
# Windows:  .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate

pip install -r app/requirements.txt
```

This installs the generated SDK from its local path in editable mode, so
`import vehicle_service_collection_sdk` resolves without publishing to PyPI.

## Configuration

Settings are read from environment variables (or a `.env` file in the working
directory). Copy the sample and edit as needed:

```bash
cp app/.env.example .env
```

| Variable                    | Default                 | Description                         |
| --------------------------- | ----------------------- | ----------------------------------- |
| `VEHICLE_SERVICE_BASE_URL`  | `http://localhost:4501` | API base URL (local mock by default)|
| `VEHICLE_SERVICE_API_KEY`   | _(empty)_               | Sent as `X-API-Key` when set        |
| `VEHICLE_SERVICE_TIMEOUT`   | `30`                    | Per-request timeout (seconds)       |

The default base URL matches the `Local - Agent Mode` Postman environment, which
points at the local **Vehicle Service Mock**.

## Usage

### CLI

```bash
python -m app.cli list
python -m app.cli get 1
python -m app.cli create --nick-name "The Lisa Marie" --vin 4M2DV11W4RDJ53329 \
    --make Mercury --model Villager --year 1994 --miles 159864
python -m app.cli update 1 --miles 160000
python -m app.cli delete 1
```

Override configuration inline with `--base-url` / `--api-key`.

### As a library

```python
from app.client import VehicleServiceClient

client = VehicleServiceClient()

vehicles = client.list_vehicles()
new = client.create_vehicle(nick_name="The Lisa Marie", vin="4M2DV11W4RDJ53329",
                            make="Mercury", model="Villager", year="1994", miles=159864)
one = client.get_vehicle(1)
client.update_vehicle(1, miles=160000)
client.delete_vehicle(1)
```
