# Mylogger

Mylogger is a Python library for logging into stdout, file and buffer automatically.

The resulting logger is capable of displaying in console, file and memory.
* Console -> just prints the logs in sys.stdout
* File -> stores logs in the /logs folder in the package directory.
* Memory -> stores in memory the logs (exceptions/errors and above). Available for flushing at will.

VERY IMPORTANT: once the buffer is flushed, the logger is done and can't work anymore unless it is reinstantiated.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install mylogger.

```bash
pip install git+https://github.com/jtorre94/mylogger
```

## Usage

```python
from mylogger import Logger

# initialise to allow have the root_logger attribute and flush_log method.
mylog = Logger()
logger = mylog.logger

# log stuff.
logger.debug('DEBUG')
logger.info('INFO')
logger.warning('WARNING')
logger.error('ERROR')
try:
    raise ValueError
except ValueError:
    logger.exception('EXCEPTION')
logger.critical('CRITICAL')    

# retrieve the errors/exceptions/criticals raised throghout the script.
mylog.flush_buffer()

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
