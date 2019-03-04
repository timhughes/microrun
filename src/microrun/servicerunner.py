# -*- coding: utf-8 -*-

"""Main module."""
import asyncio
import logging

from microrun.errors import UnknownServiceError
from .service import BasicService

logger = logging.getLogger(__name__)


class MultiServiceManager:

    def __init__(self):
        self.services = {}
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config = None

    @property
    def services_list(self):
        return list(self.services.keys())

    async def start_all(self):
        for service_name in self.services.keys():
            await self.start_service(service_name)

    async def stop_all(self):
        for service_name in self.services.keys():
            await self.stop_service(service_name)

    async def start_service(self, name):
        self.logger.info('Starting: {}'.format(name))
        if name in self.services:
            asyncio.create_task(self.services[name].start())
        else:
            raise UnknownServiceError

    async def stop_service(self, name):
        self.logger.info('Stopping: {}'.format(name))
        if name in self.services:
            asyncio.create_task(self.services[name].stop())
        else:
            raise UnknownServiceError

    def create_service(self, name, config):
        service = BasicService()
        service.name = name
        service.config(**config)
        self._add_service(service)

    def _add_service(self, service):
        if service.name not in self.services:
            self.services[service.name] = service

    def get_service(self, name):
        if name in self.services:
            return self.services[name]
        else:
            raise UnknownServiceError

    def configure(self, config):
        if 'services' in config:
            for name, config in config['services'].items():
                self.create_service(name, config)
