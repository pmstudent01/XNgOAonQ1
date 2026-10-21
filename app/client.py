"""VehicleService client wrapper.

Wraps the Postman-generated ``vehicle_service_collection_sdk`` to expose a
small, ergonomic, domain-focused API for the rest of the app. All HTTP work,
serialization, and auth are delegated to the generated SDK.
"""

from __future__ import annotations

import logging
from typing import Any, Optional

from vehicle_service_collection_sdk import (
    VehicleServiceCollectionSdk,
    CreateAVehicleRequest,
)

from .config import Settings


class VehicleServiceClient:
    """High-level client for the Vehicle Service API.

    Thin facade over the generated SDK's five operations:
      * list_vehicles   -> GET    /vehicles
      * get_vehicle     -> GET    /vehicles/{id}
      * create_vehicle  -> POST   /vehicles
      * update_vehicle  -> PATCH  /vehicles/{id}
      * delete_vehicle  -> DELETE /vehicles/{id}
    """

    def __init__(self, settings: Optional[Settings] = None, *, logger: Optional[logging.Logger] = None) -> None:
        self.settings = settings or Settings.from_env()
        self._sdk = VehicleServiceCollectionSdk(
            api_key=self.settings.api_key,
            base_url=self.settings.base_url,
            timeout=self.settings.timeout,
            logger=logger,
        )

    @property
    def service(self):
        """Direct access to the underlying generated service, if needed."""
        return self._sdk.vehicle_service_collection_sdk

    # --- Operations -----------------------------------------------------

    def list_vehicles(self) -> Any:
        """Return all vehicles. (GET /vehicles)"""
        return self.service.get_all_vehicles()

    def get_vehicle(self, vehicle_id: int | str) -> Any:
        """Return a single vehicle by id. (GET /vehicles/{id})"""
        return self.service.retrieve_a_vehicle(str(vehicle_id))

    def create_vehicle(
        self,
        *,
        nick_name: Optional[str] = None,
        vin: Optional[str] = None,
        make: Optional[str] = None,
        model: Optional[str] = None,
        year: Optional[str] = None,
        miles: Optional[int] = None,
    ) -> Any:
        """Create a new vehicle. (POST /vehicles)"""
        body = CreateAVehicleRequest(
            nick_name=nick_name,
            vin=vin,
            make=make,
            model=model,
            year=year,
            miles=miles,
        )
        return self.service.create_a_vehicle(body)

    def update_vehicle(
        self,
        vehicle_id: int | str,
        *,
        nick_name: Optional[str] = None,
        vin: Optional[str] = None,
        make: Optional[str] = None,
        model: Optional[str] = None,
        year: Optional[str] = None,
        miles: Optional[int] = None,
    ) -> Any:
        """Update an existing vehicle. (PATCH /vehicles/{id})"""
        body = CreateAVehicleRequest(
            nick_name=nick_name,
            vin=vin,
            make=make,
            model=model,
            year=year,
            miles=miles,
        )
        # Generated signature is update_a_collection(request_body, id_).
        return self.service.update_a_collection(body, str(vehicle_id))

    def delete_vehicle(self, vehicle_id: int | str) -> Any:
        """Delete a vehicle by id. (DELETE /vehicles/{id})"""
        return self.service.delete_a_vehicle(str(vehicle_id))
