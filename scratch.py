import asyncio
import logging
import os

import aiohttp_jinja2
import jinja2
from aiohttp import web

from openapi import spec

from openapi.spec import op, OpenApi, OpenApiSpec
from openapi.spec.path import ApiPath

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.StreamHandler()
logging.basicConfig(level=LOGLEVEL, format=FORMAT)

templates = {
    'index.html': "<html><body><h1>Welcome to {{ app['name'] }}</h1><p><a href='/pingers'>Pingers</a></p></body></html>",
    'pinger_list.html': '''<html>
    <body>
    <h1>{{ app['name'] }} - Pingers</h1>
    <ul>
    {% for pinger in pingers %}
    <li>{{ pinger }}</li>
    {% endfor %}
    </ul>
    </body>
    </html>''',
}


class Pinger:

    def __init__(self, address):
        self.address = address
        self.logger = logging.getLogger(self.__class__.__name__)
        self._process = None
        self._running = False

    async def start(self):
        self._process = await asyncio.create_subprocess_exec(
            'ping', self.address,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        self.logger.info('Started "ping {}" {}'.format(self.address, self._process.pid))

        await asyncio.gather(
            self.log(self._process.stdout),
            self.log(self._process.stderr, logging.ERROR)
        )
        await self._process.wait()
        self._running = False
        self.logger.info('Exited "ping {}" with errorcode: {}'.format(
            self.address, self._process.returncode))

    async def log(self, stream, level=logging.INFO):
        async for line in stream:
            self.logger.log(level, line.decode().strip())

    async def stop(self):
        try:
            await asyncio.wait_for(self._process.terminate(), timeout=1.0)
            self.logger.info('Exited "ping {}" with errorcode: {}'.format(
                self.address, self._process.returncode))
        except asyncio.TimeoutError as e:
            self.logger.info("Timeout Error: {}".format(e))

    @property
    def status(self):
        if self._running:
            msg = 'running'
        else:
            msg = 'stopped'
        return msg


class MultiPinger:

    def __init__(self, address_list):
        self.pingers = {}
        self.logger = logging.getLogger(self.__class__.__name__)

        for address in address_list:
            self.pingers[address] = Pinger(address)

    async def start_all(self):
        for address, pinger in self.pingers.items():
            self.logger.info('Starting: {}'.format(address))
            asyncio.create_task(pinger.start())

    async def stop_all(self):
        for address, pinger in self.pingers.items():
            self.logger.info('Stopping: {}'.format(address))
            asyncio.create_task(pinger.stop())

    @property
    def services_list(self):
        return self.pingers.keys()


class WebApplication:

    def __init__(self):
        self.app = web.Application()
        self.app['name'] = 'Sir Pingsalot'
        self.logger = logging.getLogger(self.__class__.__name__)
        self.app.add_routes([
            web.get('/', self.root),
            web.get('/upgrade', self.upgrade),
            web.get('/pingers', self.pingers),
        ])
        self._runner = None
        self.multiping = None

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

    async def upgrade(self, request):
        text = "Upgrade Page"
        self.logger.info(request.content_type)
        return web.Response(body=text, content_type='text/html')

    @aiohttp_jinja2.template('pinger_list.html')
    async def pingers(self, request):
        if request.method == 'GET':
            pingers = self.multiping.services_list
            return {'pingers': pingers}
        return {}


class OpenApiApplication:

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.app = web.Application()
        spec.setup_app(self.app)

        self.app.router.add_routes([
            web.view('/', ApiIndex)
        ])

        openapi=dict(
              title='A REST API',
        )

        self.app['spec'] = OpenApiSpec(
            OpenApi(**(openapi or {})),
            allowed_tags=['Index'],
            validate_docs=True
        )

    @op()
    async def thing(self):
        """
        ---
        summary: Get Index
        description: Returns the data for the index page
        responses:
            200:
                description: Index page
        """
        return {}

class ApiIndex(ApiPath):
    """
    ---
    summary: Index page data
    description: Index page description
    tags:
        - name: Index
          description: Simple description

    """

    @op()
    async def index(self):
        """
        ---
        summary: Get Index
        description: Returns the data for the index page
        responses:
            200:
                description: Index page
        """
        return {}


class PingMaster:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.multiping = None
        self.webapp = None

    def setup(self):
        self.multiping = MultiPinger(['127.1.1.1', '127.2.2.2'])
        self.webapp = WebApplication()
        self.webapp.multiping = self.multiping

        apiapp = OpenApiApplication()
        self.webapp.app.add_subapp('/api/v1', apiapp.app)

    async def run(self):
        await asyncio.gather(
            self.multiping.start_all(),
            self.webapp.start()
        )


def main():
    master = PingMaster()
    master.setup()
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(master.run())
    loop.run_forever()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
