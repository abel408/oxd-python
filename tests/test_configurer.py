import uuid
import os.path
from nose.tools import assert_true, assert_equal, assert_is_none, assert_false

from oxdpython.configurer import Configurer

this_dir = os.path.dirname(os.path.realpath(__file__))
location = os.path.join(this_dir, 'data', 'initial.cfg')


def test_oxdconfig_looks_for_config_file_while_initialization():
    config = Configurer(location)
    assert_true(os.path.isfile(config.config_file))


def test_get_function_returns_value_for_set_config_value():
    config = Configurer(location)
    # for a set value it should be the set value
    assert_equal(config.get('oxd', 'port'), '8099')
    assert_equal(config.get('oxd', 'host'), 'localhost')

    # for an unset value it should be none
    assert_is_none(config.get('oxd', 'message'))
    assert_is_none(config.get('two', 'coffee'))


def test_set_function_saves_the_configuratio_to_file():
    config = Configurer(location)
    test_id = str(uuid.uuid4())
    # only allowed sections for a set function are oxd and client
    assert_true(config.set('oxd', 'id', test_id))
    assert_true(config.set('client', 'name', 'Test Client'))
    assert_false(config.set('test', 'key', 'value'))

    # Ensure things have been written to the file
    config2 = Configurer(location)
    assert_equal(config2.get('oxd', 'id'), test_id)
    assert_equal(config2.get('client', 'name'), 'Test Client')
