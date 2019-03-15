
import pytest
import asyncio
from microrun.servicerunner import MultiServiceManager


@pytest.fixture(name='sm')
def servicemanager():
    return MultiServiceManager()


def test_servicemanager_can_create_services(sm):

    sm.create_service(
        'dummyservice',
        {
            'workingdir': '/tmp/',
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
            'workingdir': '/tmp/',
            'displayname': 'Dummy Service',
            'command': 'true',
            'environment': {}
        }
    )
    services = sm.services_list
    assert services == ['dummyservice']


@pytest.mark.asyncio
async def test_start_and_stop_a_service(sm):
    sm.create_service(
        'dummyservice',
        {
            'workingdir': '/',
            'displayname': 'Dummy Service',
            'command': ['sleep 10'],
            'environment': {}
        }
    )
    service = sm.get_service('dummyservice')
    assert service.status == 'stopped'
    sm.start_service('dummyservice')

    assert service.status == 'running'
    sm.stop_service('dummyservice')
    assert service.status == 'stopped'
