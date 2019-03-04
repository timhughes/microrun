import asyncio
import logging

from microrun.servicerunner import MultiServiceManager
from microrun.web import WebApplication


class MicroRun:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.multiservicemanager = None
        self.webapp = None
        self.config = None

    def setup(self):
        self.multiservicemanager = MultiServiceManager()
        self.multiservicemanager.configure(self.config)
        self.webapp = WebApplication()
        self.webapp.msm = self.multiservicemanager

    async def run(self):
        await asyncio.gather(
            self.multiservicemanager.start_all(),
            self.webapp.start()
        )
