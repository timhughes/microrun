import asyncio
import logging
from abc import ABC, abstractmethod
from datetime import datetime


class AbstractService(ABC):


    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def status(self):
        pass


class BasicService(AbstractService):

    def __init__(self):
        self.last_exitcode = None
        self.last_exittime = datetime.now()
        self.name = None
        self.displayname = None
        self.workingdir = None
        self.environment = {}
        self.command = []
        self._process = None
        self._running = False
        self.logger = logging.getLogger("{}".format(self.__class__.__name__))

    async def start(self):
        self.logger = logging.getLogger("{}".format(self.name))
        self.logger.info('Starting "{}":  {}'.format(self.name, ' '.join(self.command)))
        kwargs = {'cwd': self.workingdir, 'env': self.environment}
        self._process = await asyncio.create_subprocess_shell(
            ' '.join(self.command),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            **kwargs
        )
        self.logger.info('Started "{}": pid={}'.format(self.name, self._process.pid))
        self._running = True
        await asyncio.gather(
            self.log(self._process.stdout),
            self.log(self._process.stderr, logging.ERROR)
        )

        await self._process.wait()
        self._running = False
        self.last_exitcode = self._process.returncode
        self.last_exittime = datetime.now()
        self.log_exit()


    def log_exit(self):
        self.logger.info('Exited "{}": pid={}'.format(self.name, self._process.pid))

    async def stop(self):
        await self._process.terminate()

    async def kill(self):
        await self._process.kill()

    @property
    def status(self):
        if self._running:
            msg = 'running'
        else:
            msg = 'stopped'
        return msg

    async def log(self, stream, level=logging.INFO):
        async for line in stream:
            self.logger.log(level, line.decode().strip())
