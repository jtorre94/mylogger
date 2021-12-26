import io
import unittest.mock as um
import unittest

from mylogger import Logger

# Mock yaml file
YAML_TEST = """
version: 1
formatters:
  simple:
    format: '%(name)s - %(levelname)s - %(message)s'
handlers:
  console:
    class: logging.StreamHandler
    level: DEBUG
    formatter: simple
    stream: ext://sys.stdout
  file:
    class: logging.FileHandler
    level: DEBUG
    formatter: simple
    filename: logs/__file__.log
  stringio:
    class: logging.StreamHandler
    level: ERROR
    formatter: simple
root:
  level: DEBUG
  handlers: [console, file, stringio]
"""

# Dictionary to avoid fetching from yml file in unit testing
YAML_TEST_DICT = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(name)s - %(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler', 'level': 'DEBUG', 'formatter': 'simple', 'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.FileHandler', 'level': 'DEBUG', 'formatter': 'simple', 'filename': 'logs/__file__.log'
        },
        'stringio': {
            'class': 'logging.StreamHandler', 'level': 'ERROR', 'formatter': 'simple'
        }
    },
    'root': {
        'level': 'DEBUG', 'handlers': ['console', 'file', 'stringio']
    }
}


class CreateLoggerFromYAMLConfig(unittest.TestCase):

    def test_yaml_loads_the_correct_dictionary(self):
        expected_config_dict = YAML_TEST_DICT
        with um.patch('builtins.open', um.mock_open(read_data=YAML_TEST)):
            actual_config_dict = Logger.load_yaml_config()
        self.assertEqual(expected_config_dict, actual_config_dict)

    def test_logger_correctly_created(self):
        actual_logger = Logger.create_logger(YAML_TEST_DICT)
        self.assertEqual('mylogger', actual_logger.name)
        self.assertEqual(len(actual_logger.parent.handlers), 3)


class AddBufferIOHandler(unittest.TestCase):
    @staticmethod
    def mock_handlers():
        """
        Creates a list of 3 mocked handlers for testing.

        Returns: list
            contains 3 mocked handlers.
        """
        handler_console = um.Mock(stream='console_stream')
        # The name attribute cannot be mocked during creation of the mock object, since it has special meaning:
        # https://stackoverflow.com/questions/62552148/how-to-mock-name-attribute-with-unittest-mock-magicmock-
        # or-mock-classes
        handler_console.name = 'console'

        file_console = um.Mock(stream='file_stream')
        file_console.name = 'file'

        stringio_console = um.Mock(stream='stringio_stream')
        stringio_console.name = 'stringio'

        return [handler_console, file_console, stringio_console]

    def test_stringio_stream_is_added_to_stringio_named_handler(self):
        # Create a mock logger instance and mock its handlers to a list whose elements just have
        # the name and stream properties.
        logger = um.Mock()
        logger.logger.parent.handlers = self.mock_handlers()
        # Mock the string_io for the stream as well.
        logger.string_io = io.StringIO()
        Logger.point_stringio_stream_to_stringio_variable(logger)
        # Check that the stringio handler stream was actually changed
        self.assertTrue(isinstance(logger.logger.parent.handlers[2].stream, io.StringIO))
        self.assertEqual('console_stream', logger.logger.parent.handlers[0].stream)


class CheckFlushingBuffer(unittest.TestCase):

    @staticmethod
    def log_value_errors(logger):
        try:
            raise ValueError
        except ValueError:
            for i in range(5):
                logger.error(f'ERROR {i}')

    @um.patch('mylogger.Logger.load_yaml_config')
    def test_logged_errors_are_correctly_passed_upon_flush_call(self, mock_load_yaml_config):
        # Mock the yaml config method to return the hardcoded test dictionary
        mock_load_yaml_config.return_value = YAML_TEST_DICT
        logger = Logger()
        # Generate the errors
        self.log_value_errors(logger.logger)
        expected_buffer_content = '\n'.join([f'mylogger - ERROR - ERROR {i}' for i in range(5)])
        actual_buffer_content = logger.flush_buffer()
        self.assertEqual(expected_buffer_content, actual_buffer_content)
