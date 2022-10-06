from datetime import timedelta

from graphene import List
from pydantic import BaseModel

from claude.components.graphene.node_base import NodeBase, NodeConfig
from claude.components.graphene.pydantic import object_type_from_pydantic
from claude.components.weather.idokep.parsers import get_days
from claude.components.weather.types import DayForecast


class DaysForecastNodeValidator(BaseModel):
    city: str


class DaysForecastWeatherNode(NodeBase[DaysForecastNodeValidator]):
    config = NodeConfig(
        result_type=List(object_type_from_pydantic(DayForecast)),
        input_validator=DaysForecastNodeValidator,
        cache_expiry_time=timedelta(hours=3),
    )

    async def resolve(self):
        return await get_days(self.args.city, self.request_context.config.idokep_parser.days)
