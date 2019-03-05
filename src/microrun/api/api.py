import logging


from aiohttp import web
from openapi import spec
from openapi.spec import OpenApi, OpenApiSpec, op

from .views import Index, Services


class OpenApiApplication:

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.app = web.Application()
        spec.setup_app(self.app)

        self.app.router.add_routes([
            web.view('/', Index),
            web.view('/services', Services, name='services'),
        ])

        openapi=dict(
            title='A REST API',
        )

        self.app['spec'] = OpenApiSpec(
            OpenApi(**(openapi or {})),
            allowed_tags=['Index'],
            validate_docs=True
        )
