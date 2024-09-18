"""DataUpdateCoordinator for eto_irrigation."""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, Any

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import (
    DPKTradingAuthenticationError,
    DPKTradingError,
    DPKTradingAPI,
)
from .const import DOMAIN, LOGGER

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import DPKTradingConfigEntry


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class DPKTradingDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: DPKTradingConfigEntry

    def __init__(
        self,
        eto_client: DPKTradingAPI,
        hass: HomeAssistant,
    ) -> None:
        """Initialize."""
        self._eto_client = eto_client

        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=10),
        )

    async def _async_update_data(self) -> Any:
        """Update data via library."""
        try:
            return await self._eto_client.async_get_data()
        except DPKTradingAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except DPKTradingError as exception:
            raise UpdateFailed(exception) from exception

    @property
    def eto_client(self) -> DPKTradingAPI:
        """Getter."""
        return self._eto_client
