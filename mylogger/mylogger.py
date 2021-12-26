import io
import logging
import logging.config

import yaml


class Logger:
    YAML_PATH = r'config/mylogger_config.yml'
    string_io = io.StringIO()

    def __init__(self) -> None:
        """
        1. Create the logger based on the configuration provided if applicable.
        2. Point stream from string_io handler to a io.StringIO() object.
        """
        config = self.load_yaml_config()

        # Create the logger as per the configuration says.
        self.logger = self.create_logger(config)

        # Manualy make the stringio handler stream to a stringIO() object.
        self.point_stringio_stream_to_stringio_variable()

    @staticmethod
    def load_yaml_config(file: str = YAML_PATH) -> dict:
        """
        Load the config based on the arguments provided.

        Returns: dict
            dictionary which will be used for configuring the logger, handlers, etc.
        """

        with open(file, 'r') as config_yaml:
            return yaml.safe_load(config_yaml.read())

    @staticmethod
    def create_logger(config: dict) -> logging.getLogger():
        """
        Create the log based on a config dictionary

        Returns: logging.getLogger()
            logger object to be used like logger.error, logger.info etc.
        """

        logging.config.dictConfig(config)
        return logging.getLogger(__name__)

    def point_stringio_stream_to_stringio_variable(self):
        """
        io.StringIO() stream seems to be not directly configurable in the yml file itself, so the handler
        stringio must be configured ad-hoc for the stream to point to an io.StringIO() object.

        Returns: None
            just adds the handler.
        """
        for h in self.logger.parent.handlers:
            if h.name == 'stringio':
                h.stream = self.string_io

    def flush_buffer(self):
        """
        Return the errors/exceptions logged in memory throughout the execution.

        Returns: str
            buffer contents (log errors/exceptions) stored in the io.StringIO() object.
        """
        with self.string_io:
            return self.string_io.getvalue().strip()


if __name__ == '__main__':
    pass
