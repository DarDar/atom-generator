#!/usr/bin/env python
from os.path import abspath, dirname, join
import sys

sys.path.append(abspath(dirname(__file__)))

from atom_generator import app as application

if not application.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(
        application.config.get('LOG_FILE', join(abspath(dirname(__file__)), 'atom-generator.log')),
        maxBytes=application.config.get('LOG_SIZE', 1024**2),
        backupCount=application.config.get('LOG_COUNT', 7)
    )
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    application.logger.addHandler(file_handler)
else:
    try:
        from flask_debugtoolbar import DebugToolbarExtension
        toolbar = DebugToolbarExtension(application)
    except ImportError:
        pass

if __name__ == '__main__':
    if application.debug:
        application.run(host='0.0.0.0')
    else:
        application.run()
