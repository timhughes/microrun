
import pytest
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
            'command': 'false',
            'environment': {}
        }
    )
    assert len(sm.services) == 1


def test_sm_list_services(sm):
    sm.create_service(
        'dummyservice',
        {
            'workingdir': '/dev/null',
            'displayname': 'Dummy Service',
            'command': 'false',
            'environment': {}
        }
    )
    services = sm.list_services()
    assert services == ['dummyservice']
