"""Command-line interface for the Vehicle Service app.

Usage examples::

    python -m app.cli list
    python -m app.cli get 1
    python -m app.cli create --nick-name "The Lisa Marie" --vin 4M2DV11W4RDJ53329 \
        --make Mercury --model Villager --year 1994 --miles 159864
    python -m app.cli update 1 --miles 160000
    python -m app.cli delete 1
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from .client import VehicleServiceClient
from .config import Settings


def _print(result: Any) -> None:
    try:
        # Pydantic models from the SDK expose model_dump(); fall back to str.
        if hasattr(result, "model_dump"):
            result = result.model_dump()
    except Exception:
        pass
    if result is None or result == "":
        print("(no content)")
        return
    try:
        print(json.dumps(result, indent=2, default=str))
    except (TypeError, ValueError):
        print(result)


def _add_vehicle_fields(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--nick-name", dest="nick_name")
    parser.add_argument("--vin")
    parser.add_argument("--make")
    parser.add_argument("--model")
    parser.add_argument("--year")
    parser.add_argument("--miles", type=int)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="vehicle-service",
        description="Vehicle Service app (built on the generated Postman SDK).",
    )
    parser.add_argument("--base-url", help="Override the API base URL.")
    parser.add_argument("--api-key", help="Override the API key.")

    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list", help="List all vehicles (GET /vehicles).")

    p_get = sub.add_parser("get", help="Retrieve a vehicle (GET /vehicles/{id}).")
    p_get.add_argument("id")

    p_create = sub.add_parser("create", help="Create a vehicle (POST /vehicles).")
    _add_vehicle_fields(p_create)

    p_update = sub.add_parser("update", help="Update a vehicle (PATCH /vehicles/{id}).")
    p_update.add_argument("id")
    _add_vehicle_fields(p_update)

    p_delete = sub.add_parser("delete", help="Delete a vehicle (DELETE /vehicles/{id}).")
    p_delete.add_argument("id")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    base = Settings.from_env()
    settings = Settings(
        base_url=args.base_url or base.base_url,
        api_key=args.api_key or base.api_key,
        timeout=base.timeout,
    )
    client = VehicleServiceClient(settings)

    try:
        if args.command == "list":
            _print(client.list_vehicles())
        elif args.command == "get":
            _print(client.get_vehicle(args.id))
        elif args.command == "create":
            _print(
                client.create_vehicle(
                    nick_name=args.nick_name,
                    vin=args.vin,
                    make=args.make,
                    model=args.model,
                    year=args.year,
                    miles=args.miles,
                )
            )
        elif args.command == "update":
            _print(
                client.update_vehicle(
                    args.id,
                    nick_name=args.nick_name,
                    vin=args.vin,
                    make=args.make,
                    model=args.model,
                    year=args.year,
                    miles=args.miles,
                )
            )
        elif args.command == "delete":
            client.delete_vehicle(args.id)
            print(f"Deleted vehicle {args.id}.")
        else:  # pragma: no cover - argparse enforces valid commands
            return 2
    except Exception as exc:  # surface SDK/HTTP errors cleanly
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
