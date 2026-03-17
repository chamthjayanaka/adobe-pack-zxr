"""
Adobe Acrobat Toolkit - Python automation and utilities

A comprehensive toolkit for working with Adobe Acrobat files and automation.
"""
from .client import AdobeAcrobatClient
from .processor import AdobeAcrobatProcessor
from .metadata import AdobeAcrobatMetadataReader
from .batch import BatchProcessor
from .exporter import DataExporter

__version__ = "0.1.0"
__author__ = "Open Source Community"

__all__ = [
    "AdobeAcrobatClient",
    "AdobeAcrobatProcessor",
    "AdobeAcrobatMetadataReader",
    "BatchProcessor",
    "DataExporter",
]
