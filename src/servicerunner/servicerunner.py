# -*- coding: utf-8 -*-

"""Main module."""
import asyncio
import logging

from .service import BasicService

logger = logging.getLogger(__name__)


class ServiceManager:

    def __init__(self):
        self.services = {}
        self.config = None
        self.loop = None

    async def serve(self) -> None:
        if not self.config:
            logger.error("No config provided")

        logger.debug('Serving')

        if 'services' in self.config:
            for name, config in self.config['services'].items():
                self.create_service(name, config)

        tasks = [service.start() for _, service in self.services.items()]
        await asyncio.wait(tasks)

    async def killall(self) -> None:
        tasks = [service.stop() for _, service in self.services.items()]
        await asyncio.wait(tasks)

    def list_services(self) -> None:
        return list(self.services.keys())

    def add_service(self, service):

        if service.name not in self.services:
            self.services[service.name] = service

    def create_service(self, name, config) -> None:
        service = BasicService()
        service.name = name
        service.workingdir = config['workingdir']
        service.displayname = config['displayname']
        service.command = config['command']
        service.environment = config['environment']
        self.add_service(service)

    def start_service(self, name) -> None:
        self.services[name].start()

    def stop_service(self, name) -> None:
        self.services[name].stop()

    # def service_action(self, name, action):
    #    '''make services extensible with more than start stop status'''
    #    self.services[name].action

