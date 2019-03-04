
import logging
import os

import aiohttp_jinja2
import jinja2
from aiohttp import web

from microrun.servicerunner import MultiServiceManager

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.StreamHandler()
logging.basicConfig(level=LOGLEVEL, format=FORMAT)


templates = {
    'index.html': "<html><body><h1>Welcome to {{ app['name'] }}</h1><p><a href='/services'>Services</a></p></body></html>",
    'service_list.html': '''<html>
    <body>
    <h1>{{ app['name'] }} - Services</h1>
    <ul>
    {% for service, data in services.items() %}
    <li>{{ service }} - {% if data['status'] == 'running' %}<a href='/services/{{ service }}/stop'>Stop</a>{% else %}<a href='/services/{{ service }}/start'>Start</a>{% endif %}</li>
        <ul>
        {% for k, v in data.items() %}
            <li>{{ k }}:{{ v }}</li>
        {% endfor %}
        </ul>
    {% endfor %}
    </ul>
    </body>
    </html>''',
}


class WebApplication:

    def __init__(self):
        self.app = web.Application()
        self.app['name'] = 'MicroRun: Micro Service Runner'
        self.logger = logging.getLogger(self.__class__.__name__)
        self.app.add_routes([
            web.get('/', self.root, name='root'),
            web.get('/services', self.services, name='services'),
            web.get('/services/{name}/{action}', self.service_manage, name='service_manage'),


        ])
        self._runner = None
        self.msm: MultiServiceManager = None

        aiohttp_jinja2.setup(
            self.app,
            # loader=jinja2.FileSystemLoader('/path/to/templates/folder')
            loader=jinja2.DictLoader(templates),
        )

    async def start(self):
        self._runner = web.AppRunner(self.app)
        await self._runner.setup()
        site = web.TCPSite(self._runner, 'localhost', 8080)
        await site.start()

    async def stop(self):
        await self._runner.cleanup()

    # Move these to a views module

    @aiohttp_jinja2.template('index.html')
    async def root(self, request):
        if request.method == 'GET':
            return {}

    @aiohttp_jinja2.template('service_list.html')
    async def services(self, request):
        if request.method == 'GET':
            services = {}
            service_names = self.msm.services_list
            for name in service_names:
                service = self.msm.get_service(name)
                services[name] = service.__repr__()
            return {'services': services}
        return {}

    async def service_manage(self, request):
        name = request.match_info['name']
        action = request.match_info['action']
        if action == 'stop':
            await self.msm.stop_service(name)
        elif action == 'start':
            await self.msm.start_service(name)

        location = request.app.router['services'].url_for()
        raise web.HTTPFound(location=location)


