
import pytest
import asyncio
from servicerunner.servicerunner import ServiceManager


@pytest.fixture(name='sm')
def servicemanager():

    return ServiceManager()


def test_servicemanager_can_create_services(sm):

    sm.create_service(
        'dummyservice',
        {
            'workingdir': '/dev/null',
            'displayname': 'Dummy Service',
            'command': 'true',
            'environment': {}
        }
    )
    assert len(sm.services) == 1


def test_servicemanager_list_services(sm):
    sm.create_service(
        'dummyservice',
        {
            'workingdir': '/',
            'displayname': 'Dummy Service',
            'command': 'true',
            'environment': {}
        }
    )
    services = sm.list_services()
    assert services == ['dummyservice']


@pytest.mark.asyncio
async def test_start_and_stop_a_service(sm):
    sm.create_service(
        'dummyservice',
        {
            'workingdir': '/',
            'displayname': 'Dummy Service',
            'command': ['sleep 5'],
            'environment': {}
        }
    )
    service = sm.get_service('dummyservice')
    assert service.status == 'stopped'
    sm.start_service('dummyservice')

    assert service.status == 'running'
    sm.stop_service('dummyservice')
    assert service.status == 'stopped'



def test_start_and_stop_multiple_services(sm):
    assert False
