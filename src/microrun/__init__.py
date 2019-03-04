# -*- coding: utf-8 -*-
"""Top-level package for microrun."""

import logging
from logging import NullHandler

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(NullHandler())


__author__ = """Tim Hughes"""
__email__ = 'thughes@thegoldfish.org'
__version__ = '0.1.0'





