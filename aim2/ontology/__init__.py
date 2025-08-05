"""
AIM2 Ontology Module

This module contains the core ontology definitions and management for the AIM2 system.
"""

# Import the main classes and functions
from .manager import AIM2Ontology

# Initialize the ontology and export commonly used classes and properties
from .schema import init_ontology, onto

# Initialize the ontology if not already done
if onto is None:
    onto = init_ontology()

# Export commonly used classes and properties
__all__ = [
    'AIM2Ontology',
    'onto',
    'init_ontology',
]
