import asyncio
import logging

from microrun.api.api import OpenApiApplication
from microrun.servicerunner import MultiServiceManager
from microrun.web import WebApplication


class MicroRun:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.multiservicemanager = None
        self.webapp = None
        self.apiapp = None
        self.config = None

    def setup(self):
        """
        TODO: Rather than adding everything to everything we should everything to self and add self to everything

        """

        self.multiservicemanager = MultiServiceManager()
        self.multiservicemanager.configure(self.config)

        self.apiapp = OpenApiApplication()
        self.apiapp.msm = self.multiservicemanager
        self.apiapp.app['msm'] = self.multiservicemanager

        self.webapp = WebApplication()
        self.webapp.msm = self.multiservicemanager
        self.webapp.app['msm'] = self.multiservicemanager
        self.webapp.app.add_subapp('/api/v1', self.apiapp.app)

    async def run(self):
        await asyncio.gather(
            self.multiservicemanager.start_all(),
            self.webapp.start()
        )
