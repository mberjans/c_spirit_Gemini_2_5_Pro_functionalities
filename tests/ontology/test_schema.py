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
    
    def test_custom_relationship_properties_exist(self):
        """Test that custom relationship properties exist and have the correct types."""
        # Test basic custom properties
        custom_props = [
            'made_via',
            'accumulates_in',
            'affects',
            'participates_in',
            'has_participant',
            'located_in',
            'has_location'
        ]
        
        for prop in custom_props:
            with self.subTest(property=prop):
                self.assertTrue(hasattr(self.onto, prop),
                             f"Ontology should have '{prop}' property")
                self.assertTrue('ObjectProperty' in str(type(getattr(self.onto, prop)).__name__),
                             f"{prop} should be an ObjectProperty, got {type(getattr(self.onto, prop)).__name__}")
    
    def test_affects_subproperties_exist(self):
        """Test that subproperties of 'affects' exist and have the correct inheritance."""
        # Test subproperties of 'affects'
        affects_subprops = [
            'upregulates',
            'downregulates',
            'inhibits',
            'activates'
        ]
        
        # First verify the base 'affects' property exists
        self.assertTrue(hasattr(self.onto, 'affects'),
                      "Ontology should have 'affects' property")
        
        # Then check each subproperty
        for subprop in affects_subprops:
            with self.subTest(subproperty=subprop):
                self.assertTrue(hasattr(self.onto, subprop),
                             f"Ontology should have '{subprop}' property")
                # In Owlready2, subproperties are tracked in the parent's .subclasses()
                subprop_obj = getattr(self.onto, subprop)
                self.assertIn(subprop_obj, self.onto.affects.subclasses(),
                           f"{subprop} should be a subproperty of 'affects'")
    
    def test_inverse_properties(self):
        """Test that inverse properties are correctly defined."""
        # Test participates_in / has_participant
        self.assertEqual(self.onto.participates_in.inverse_property, self.onto.has_participant,
                       "participates_in should have has_participant as inverse")
        self.assertEqual(self.onto.has_participant.inverse_property, self.onto.participates_in,
                       "has_participant should have participates_in as inverse")
        
        # Test located_in / has_location
        self.assertEqual(self.onto.located_in.inverse_property, self.onto.has_location,
                       "located_in should have has_location as inverse")
        self.assertEqual(self.onto.has_location.inverse_property, self.onto.located_in,
                       "has_location should have located_in as inverse")
    
    def test_property_domains_and_ranges(self):
        """Test that properties have the correct domain and range."""
        # In Owlready2, properties can have multiple domains and ranges
        # We need to check that Thing is included in both domain and range
        
        def assert_has_thing_domain(prop, prop_name):
            """Helper to check if Thing is in the property's domain."""
            domain_names = [d.name for d in prop.domain]
            self.assertIn('Thing', domain_names,
                        f"{prop_name} should have Thing in its domain")
        
        def assert_has_thing_range(prop, prop_name):
            """Helper to check if Thing is in the property's range."""
            range_names = [r.name for r in prop.range]
            self.assertIn('Thing', range_names,
                        f"{prop_name} should have Thing in its range")
        
        # Test made_via
        assert_has_thing_domain(self.onto.made_via, 'made_via')
        assert_has_thing_range(self.onto.made_via, 'made_via')
        
        # Test accumulates_in
        assert_has_thing_domain(self.onto.accumulates_in, 'accumulates_in')
        assert_has_thing_range(self.onto.accumulates_in, 'accumulates_in')
        
        # Test affects
        assert_has_thing_domain(self.onto.affects, 'affects')
        assert_has_thing_range(self.onto.affects, 'affects')

if __name__ == "__main__":
    unittest.main()
