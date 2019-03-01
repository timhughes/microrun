import asyncio
import logging
from abc import ABC, abstractmethod



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
        self.name = None
        self.displayname = None
        self.workingdir = None
        self.environment = {}
        self.command = []
        self._process = None
        self.log = None

    async def start(self):
        self.log = logging.getLogger("{} {}".format(self.__class__.__name__, self.name))
        self.log.info(' '.join(self.command))

        kwargs = {'cwd': self.workingdir, 'env': self.environment}

        self._process = await asyncio.create_subprocess_shell(
            ' '.join(self.command),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            **kwargs
        )

        while True:
            if self._process.returncode:
                data = await self._process.stderr.readline()
                output = data.decode().strip()
                self.log.error(output)
                return
            else:
                data = await self._process.stdout.readline()
                output = data.decode().strip()
                if output:
                    self.log.info(output)

    def stop(self):
        self._process.terminate()

    def kill(self):
        self._process.kill()

    def status(self):
        # not implemented
        pass
