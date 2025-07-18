from statsd import StatsClient
from app.core.config import settings

stats_client = StatsClient(host=settings.GRAPHITE_HOST, port=8125)
