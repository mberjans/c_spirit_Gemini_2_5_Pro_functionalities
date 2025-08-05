"""
Core schema definitions for the AIM2 ontology.

This module defines the main classes and properties for the AIM2 ontology using Owlready2.
It includes the core annotation classes and their relationships.
"""
from owlready2 import (
    get_ontology,
    Thing,
    ObjectProperty,
    DataProperty,
    FunctionalProperty,
    AnnotationProperty,
    default_world,
)

# Import the base ontology
base_iri = "http://purl.obolibrary.org/obo/aim2.owl"

# Create a function to initialize the ontology
def init_ontology():
    """Initialize the ontology and return the onto object."""
    # Get or create the ontology
    onto = get_ontology(base_iri)
    
    # Bind the ontology to the default world
    onto = onto.get_namespace(base_iri)
    
    # Define annotation properties
    with onto:
        class hasSource(AnnotationProperty):
            """Annotation property linking an entity to its source."""
            pass

        class hasConfidence(DataProperty, FunctionalProperty):
            """Data property for confidence scores (float between 0.0 and 1.0)."""
            pass

        # Define core classes
        class Annotation(Thing):
            """Base class for all annotation types in the AIM2 ontology."""
            pass

        class StructuralAnnotation(Annotation):
            """Represents structural annotations (e.g., anatomical parts, cellular components)."""
            pass

        class SourceAnnotation(Annotation):
            """Represents source annotations (e.g., species, tissues, cell types)."""
            pass

        class FunctionalAnnotation(Annotation):
            """Represents functional annotations (e.g., molecular functions, biological processes)."""
            pass

        # Define core object properties with domains and ranges
        class is_a(ObjectProperty):
            """Standard is-a relationship between classes."""
            domain = [Thing]
            range = [Thing]

        class part_of(ObjectProperty):
            """Part-whole relationship between entities."""
            domain = [Thing]
            range = [Thing]

        class has_part(ObjectProperty):
            """Inverse of part_of."""
            domain = [Thing]
            range = [Thing]
            inverse_property = part_of

        # Define annotation relationships
        class has_functional_annotation(ObjectProperty):
            """Links entities to their functional annotations."""
            domain = [Thing]
            range = [FunctionalAnnotation]

        class has_structural_annotation(ObjectProperty):
            """Links entities to their structural annotations."""
            domain = [Thing]
            range = [StructuralAnnotation]

        class has_source_annotation(ObjectProperty):
            """Links entities to their source annotations."""
            domain = [Thing]
            range = [SourceAnnotation]

        # Define custom relationship properties for AIM2
        class made_via(ObjectProperty):
            """Indicates the process or method by which something is made or modified."""
            domain = [Thing]
            range = [Thing]

        class accumulates_in(ObjectProperty):
            """Indicates where a substance or entity accumulates."""
            domain = [Thing]
            range = [Thing]

        class affects(ObjectProperty):
            """Generic relationship indicating that one entity affects another."""
            domain = [Thing]
            range = [Thing]

        # Define sub-properties of 'affects'
        class upregulates(affects):
            """Indicates that one entity upregulates another."""
            namespace = onto
            domain = [Thing]
            range = [Thing]

        class downregulates(affects):
            """Indicates that one entity downregulates another."""
            namespace = onto
            domain = [Thing]
            range = [Thing]

        class inhibits(affects):
            """Indicates that one entity inhibits another."""
            namespace = onto
            domain = [Thing]
            range = [Thing]

        class activates(affects):
            """Indicates that one entity activates another."""
            namespace = onto
            domain = [Thing]
            range = [Thing]

        # Define additional relationships for biological processes
        class participates_in(ObjectProperty):
            """Indicates participation of an entity in a process."""
            domain = [Thing]
            range = [Thing]

        class has_participant(ObjectProperty):
            """Inverse of participates_in."""
            domain = [Thing]
            range = [Thing]
            inverse_property = participates_in

        class located_in(ObjectProperty):
            """Indicates that an entity is located in another entity."""
            domain = [Thing]
            range = [Thing]

        class has_location(ObjectProperty):
            """Inverse of located_in."""
            domain = [Thing]
            range = [Thing]
            inverse_property = located_in

        # Set python names for properties for better string representation
        part_of.python_name = "part_of"
        has_part.python_name = "has_part"
        is_a.python_name = "is_a"
        
        # Note: Property characteristics like 'transitive' would be set here in a real implementation
        # but are causing issues with the current version of Owlready2
    
    return onto

# Initialize the ontology
onto = init_ontology()

# Export commonly used classes and properties
__all__ = [
    'onto',
    'init_ontology',
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
    # Custom relationship properties
    'made_via',
    'accumulates_in',
    'affects',
    'upregulates',
    'downregulates',
    'inhibits',
    'activates',
    'participates_in',
    'has_participant',
    'located_in',
    'has_location',
]
