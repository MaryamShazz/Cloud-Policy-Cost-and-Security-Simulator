from __future__ import annotations
import logging

logger = logging.getLogger(__name__)
class MetricsStreamer:

    def start(self):
        logger.info('[metrics_streamer] Legacy streamer disabled; real DES metrics via control_plane.')
    def stop(self):
        pass
metrics_streamer = MetricsStreamer()
