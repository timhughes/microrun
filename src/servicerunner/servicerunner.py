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

        for _, service in self.services.items():
            asyncio.create_task(service.start())

        # await asyncio.wait(tasks)

    async def killall(self) -> None:
        tasks = [service.stop() for _, service in self.services.items()]
        await asyncio.wait(tasks)

    def list_services(self) -> list:
        return list(self.services.keys())

    def get_service(self, name):
        if name in self.services:
            return self.services[name]
        else:
            raise UnknownServiceError

    def add_service(self, service):

        if service.name not in self.services:
            self.services[service.name] = service

    def create_service(self, name, config):
        service = BasicService()
        service.name = name
        service.workingdir = config['workingdir']
        service.displayname = config['displayname']
        service.command = config['command']
        service.environment = config['environment']
        self.add_service(service)

    async def start_service(self, name)-> bool:
        if name in self.services:
            yield self.services[name].start()
        else:
            raise UnknownServiceError

    def stop_service(self, name) -> bool:
        if name in self.services:
            self.services[name].stop()
        else:
            raise UnknownServiceError

    # def service_action(self, name, action):
    #    '''make services extensible with more than start stop status'''
    #    self.services[name].action



class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class UnknownServiceError(Error):
    """Exception raised for when we rey and get a service that doesn't exist.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
