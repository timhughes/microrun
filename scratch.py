import asyncio
import logging
import os
from aiohttp import web

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.StreamHandler()
logging.basicConfig(level=LOGLEVEL, format=FORMAT)


class Pinger:

    def __init__(self, address):
        self.address = address
        self.logger = logging.getLogger("{}".format(self.__class__.__name__))
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


class MultiPinger:

    def __init__(self, address_list):
        self.pingers = {}
        self.logger = logging.getLogger("{}".format(self.__class__.__name__))

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


class WebServer(web.Application):


    self.logger = logging.getLogger(__name__)


    async def root(request):
        text = "<a href='/upgrade'>Upgrade</a>"
        logger.info(request.content_type)
        return web.Response(body=text, content_type='text/html')



def main():

    multiping = MultiPinger(['127.1.1.1', '127.2.2.2'])
    app = web.Application()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()

    loop = asyncio.get_event_loop()
    asyncio.ensure_future(multiping.start_all())
    loop.run_forever()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
