"""
Tests for the AIM2 ontology schema.

This module contains unit tests for the core schema definitions in the AIM2 ontology.
"""
import unittest
from owlready2 import Thing, ObjectProperty, DataProperty, AnnotationProperty

class TestAIM2OntologySchema(unittest.TestCase):
    """Test cases for the AIM2 ontology schema."""
    
    @classmethod
    def setUpClass(cls):
        """Set up the test class by initializing the ontology."""
        from aim2.ontology.schema import init_ontology, onto
        cls.onto = onto or init_ontology()
    
    def test_annotation_class_exists(self):
        """Test that the base Annotation class exists and is a subclass of Thing."""
        self.assertTrue(hasattr(self.onto, 'Annotation'), 
                       "Ontology should have an 'Annotation' class")
        self.assertTrue(issubclass(self.onto.Annotation, Thing),
                      "Annotation should be a subclass of Thing")
    
    def test_structural_annotation_class_exists(self):
        """Test that the StructuralAnnotation class exists and is a subclass of Annotation."""
        self.assertTrue(hasattr(self.onto, 'StructuralAnnotation'),
                      "Ontology should have a 'StructuralAnnotation' class")
        self.assertTrue(issubclass(self.onto.StructuralAnnotation, self.onto.Annotation),
                      "StructuralAnnotation should be a subclass of Annotation")
    
    def test_source_annotation_class_exists(self):
        """Test that the SourceAnnotation class exists and is a subclass of Annotation."""
        self.assertTrue(hasattr(self.onto, 'SourceAnnotation'),
                      "Ontology should have a 'SourceAnnotation' class")
        self.assertTrue(issubclass(self.onto.SourceAnnotation, self.onto.Annotation),
                      "SourceAnnotation should be a subclass of Annotation")
    
    def test_functional_annotation_class_exists(self):
        """Test that the FunctionalAnnotation class exists and is a subclass of Annotation."""
        self.assertTrue(hasattr(self.onto, 'FunctionalAnnotation'),
                      "Ontology should have a 'FunctionalAnnotation' class")
        self.assertTrue(issubclass(self.onto.FunctionalAnnotation, self.onto.Annotation),
                      "FunctionalAnnotation should be a subclass of Annotation")
    
    def test_core_properties_exist(self):
        """Test that core properties exist and have the correct types."""
        # Test object properties
        self.assertTrue(hasattr(self.onto, 'is_a'), "Ontology should have 'is_a' property")
        # Check if is_a is an ObjectProperty by checking its class name
        self.assertTrue('ObjectProperty' in str(type(self.onto.is_a).__name__),
                     f"is_a should be an ObjectProperty, got {type(self.onto.is_a).__name__}")
        
        self.assertTrue(hasattr(self.onto, 'part_of'), "Ontology should have 'part_of' property")
        self.assertTrue('ObjectProperty' in str(type(self.onto.part_of).__name__),
                     f"part_of should be an ObjectProperty, got {type(self.onto.part_of).__name__}")
        
        self.assertTrue(hasattr(self.onto, 'has_part'), "Ontology should have 'has_part' property")
        self.assertTrue('ObjectProperty' in str(type(self.onto.has_part).__name__),
                     f"has_part should be an ObjectProperty, got {type(self.onto.has_part).__name__}")
    
    def test_annotation_properties_exist(self):
        """Test that annotation properties exist and have the correct types."""
        # Check if properties exist and have the right type names
        self.assertTrue(hasattr(self.onto, 'hasSource'), 
                       "Ontology should have 'hasSource' property")
        self.assertTrue('AnnotationProperty' in str(type(self.onto.hasSource).__name__),
                     f"hasSource should be an AnnotationProperty, got {type(self.onto.hasSource).__name__}")
        
        self.assertTrue(hasattr(self.onto, 'hasConfidence'),
                      "Ontology should have 'hasConfidence' property")
        self.assertTrue('DataProperty' in str(type(self.onto.hasConfidence).__name__),
                     f"hasConfidence should be a DataProperty, got {type(self.onto.hasConfidence).__name__}")

if __name__ == "__main__":
    unittest.main()
