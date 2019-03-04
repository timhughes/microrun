import asyncio
import logging
from abc import ABC, abstractmethod
from datetime import datetime


class ServiceAbstract(ABC):

    def __init__(self, **kwargs):
        """Initialize"""
        self.name = None
        self._displayname = None
        self._workingdir = None
        self._environment = {}
        self._command = []


    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def status(self):
        pass

    def config(self, **kwargs):
        config = kwargs.copy()
        if 'command' in config:
            self._command = config['command']
        if 'displayname' in config:
            self._displayname = config['displayname']
        if 'workingdir' in config:
            self._workingdir = config['workingdir']
        if 'environment' in config:
            self._environment = config['environment']

    @property
    def command(self):
        return self._command


class BasicService(ServiceAbstract):

    def __init__(self, **kwargs):
        super(ServiceAbstract).__init__(**kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)
        self._process = None
        self._running = False

    async def start(self):
        self.logger = logging.getLogger("{}".format(self.name))
        extra_args = {'cwd': self._workingdir, 'env': self._environment}
        self.logger.info('Starting "{}" with environment of {}'.format(' '.join(self._command), extra_args))
        self._process = await asyncio.create_subprocess_shell(
            ' '.join(self._command),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            **extra_args,
        )
        self.logger.info('Started "{}" {}'.format(self._command, self._process.pid))
        self._running = True
        await asyncio.gather(
            self._log(self._process.stdout),
            self._log(self._process.stderr, logging.ERROR)
        )
        await self._process.wait()
        self._running = False
        self.logger.info('Exited "{}" with errorcode: {}'.format(
            self._command, self._process.returncode))

    async def stop(self):
        try:
            await asyncio.wait_for(self._process.terminate(), timeout=5.0)
            self.logger.info('Exited "{}" with errorcode: {}'.format(
                self._command, self._process.returncode))
        except asyncio.TimeoutError as e:
            self.logger.info("Timeout Error: {}".format(e))
            await asyncio.wait_for(self._process.kill(), timeout=5.0)

    @property
    def status(self):
        if self._running:
            msg = 'running'
        else:
            msg = 'stopped'
        return msg

    async def _log(self, stream, level=logging.INFO):
        async for line in stream:
            self.logger.log(level, line.decode().strip())

    def __repr__(self):
        r = {
            'status': self.status,
            'pid': self._process.pid,
            'command': self.command,
        }
        return r

