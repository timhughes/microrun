import logging
import os

import aiohttp_jinja2
import jinja2
from aiohttp import web

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.StreamHandler()
logging.basicConfig(level=LOGLEVEL, format=FORMAT)


root_html = '''
<!DOCTYPE html>
<html>
<head>
  <title>My first Vue app</title>
  <script src="https://unpkg.com/vue"></script>
</head>
<body>
  <div id="app">
    {{ message }}
  </div>

  <script>
    var app = new Vue({
      el: '#app',
      data: {
        message: 'Hello Vue!'
      }
    })
  </script>
</body>
</html>
'''


class WebApplication:

    def __init__(self):
        self.app = web.Application()
        self.app['name'] = 'MicroRun: Micro Service Runner'
        self.logger = logging.getLogger(self.__class__.__name__)

        self.app['static_root_url'] = '/static/'
        #self.app.router.add_static('/static/', path='static', name='static')
        self.app.add_routes([
            web.get('/', self.root, name='root'),
            web.get('/services', self.services, name='services'),
            web.get('/services/{name}/{action}', self.service_manage, name='service_manage'),

        ])
        self._runner = None
        self.msm = None

        aiohttp_jinja2.setup(
            self.app,
            # loader=jinja2.FileSystemLoader('/path/to/templates/folder')
            # loader=jinja2.DictLoader(templates),
            loader=jinja2.PackageLoader('microrun')
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

    async def service_manage(self, request):
        name = request.match_info['name']
        action = request.match_info['action']
        if action == 'stop':
            await self.msm.stop_service(name)
        elif action == 'start':
            await self.msm.start_service(name)

        location = request.app.router['services'].url_for()
        raise web.HTTPFound(location=location)


