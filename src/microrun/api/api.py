import logging


from aiohttp import web
from openapi import spec
from openapi.spec import OpenApi, OpenApiSpec, op
import aiohttp_cors

from .views import Index, Services

# TODO hataeos    https://stackoverflow.com/a/682052
#  https://tbone.readthedocs.io/en/latest/source/resources.html#hateoas
#  https://flask-ripozo.readthedocs.io/en/latest/flask_tutorial.html


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
        cors = aiohttp_cors.setup(self.app, defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
        })
        for route in list(self.app.router.routes()):
            cors.add(route)

