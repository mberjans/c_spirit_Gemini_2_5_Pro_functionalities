"""
AIM2 Ontology Module

This module contains the core ontology definitions and management for the AIM2 system.
"""

# Import the main classes and functions
from .manager import AIM2Ontology
from .schema import (
    onto,
    Annotation,
    StructuralAnnotation,
    SourceAnnotation,
    FunctionalAnnotation,
    is_a,
    part_of,
    has_part,
    has_functional_annotation,
    has_structural_annotation,
    has_source_annotation,
    hasSource,
    hasConfidence,
)

__all__ = [
    'AIM2Ontology',
    'onto',
    'Annotation',
    'StructuralAnnotation',
    'SourceAnnotation',
    'FunctionalAnnotation',
    'is_a',
    'part_of',
    'has_part',
    'has_functional_annotation',
    'has_structural_annotation',
    'has_source_annotation',
    'hasSource',
    'hasConfidence',
]
