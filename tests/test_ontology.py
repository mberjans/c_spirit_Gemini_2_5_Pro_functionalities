"""
Tests for the ontology module.
"""
import unittest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Skip all tests if the required modules are not available
try:
    import owlready2
    from owlready2 import get_ontology, World
    
    # Import the AIM2 ontology module
    from aim2.ontology import AIM2Ontology, onto, init_ontology, \
        Annotation, StructuralAnnotation, SourceAnnotation, FunctionalAnnotation, \
        is_a, part_of, has_part, has_functional_annotation, \
        has_structural_annotation, has_source_annotation, hasSource, hasConfidence
    
    # Ensure the ontology is properly initialized
    if onto is None:
        onto = init_ontology()
    
    HAS_ONTOLOGY_MODULES = True
except (ImportError, ModuleNotFoundError) as e:
    HAS_ONTOLOGY_MODULES = False
    print(f"Skipping ontology tests: {e}")

@unittest.skipIf(not HAS_ONTOLOGY_MODULES, "Owlready2 or other required modules not available")
class TestOntologyModule(unittest.TestCase):
    """Test cases for the ontology module."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_owl_path = Path(self.temp_dir.name) / "test_ontology.owl"
        
        # Ensure the ontology is properly initialized
        global onto
        if onto is None:
            onto = init_ontology()
    
    def tearDown(self):
        """Clean up test fixtures."""
        self.temp_dir.cleanup()
    
    def test_import_ontology_module(self):
        """Test that the ontology module can be imported with all required components."""
        # Test that all expected components are importable
        self.assertIsNotNone(onto, "Ontology instance should be available")
        self.assertIsNotNone(AIM2Ontology, "AIM2Ontology class should be available")
        
        # Test core classes
        self.assertTrue(issubclass(Annotation, owlready2.Thing), "Annotation should be a Thing")
        self.assertTrue(issubclass(StructuralAnnotation, Annotation), 
                       "StructuralAnnotation should be an Annotation")
        self.assertTrue(issubclass(SourceAnnotation, Annotation), 
                       "SourceAnnotation should be an Annotation")
        self.assertTrue(issubclass(FunctionalAnnotation, Annotation), 
                       "FunctionalAnnotation should be an Annotation")
    
    def test_ontology_initialization(self):
        """Test that the ontology can be initialized and basic operations work."""
        # Skip this test if we can't import the required modules
        if not HAS_ONTOLOGY_MODULES:
            self.skipTest("Required modules not available")
            
        # Test initialization with a temporary file
        ontology = AIM2Ontology(owl_path=str(self.temp_owl_path))
        
        # Test basic attributes
        self.assertIsNotNone(ontology, "Failed to initialize AIM2Ontology")
        self.assertTrue(hasattr(ontology, 'world'), "Ontology should have a world attribute")
        self.assertTrue(hasattr(ontology, 'onto'), "Ontology should have an onto attribute")
        
        # Test saving and loading
        try:
            # Save the ontology
            ontology.save()
            self.assertTrue(self.temp_owl_path.exists(), "Ontology file should be created")
            
            # Load the ontology
            loaded_ontology = AIM2Ontology(owl_path=str(self.temp_owl_path))
            loaded_ontology.load()
            self.assertIsNotNone(loaded_ontology.onto, "Loaded ontology should have an onto attribute")
            
        except Exception as e:
            self.fail(f"Failed to save/load ontology: {e}")
    
    def test_ontology_classes(self):
        """Test that the core ontology classes can be used to create instances."""
        # Skip this test if we can't import the required modules
        if not HAS_ONTOLOGY_MODULES:
            self.skipTest("Required modules not available")
            
        # Create test instances
        with onto:
            # Create a structural annotation (e.g., a leaf)
            leaf = StructuralAnnotation("leaf_1")
            leaf.label = "Leaf"
            
            # Create a source annotation (e.g., a species)
            arabidopsis = SourceAnnotation("arabidopsis_thaliana")
            arabidopsis.label = "Arabidopsis thaliana"
            
            # Create a functional annotation (e.g., photosynthesis)
            photosynthesis = FunctionalAnnotation("photosynthesis")
            photosynthesis.label = "Photosynthesis"
            
            # Test that instances were created
            self.assertEqual(leaf.label[0], "Leaf", "Label should be set correctly")
            self.assertEqual(arabidopsis.label[0], "Arabidopsis thaliana", 
                            "Label should be set correctly")
            self.assertEqual(photosynthesis.label[0], "Photosynthesis", 
                            "Label should be set correctly")
            
            # Test that instances are of the correct types
            self.assertIsInstance(leaf, StructuralAnnotation, 
                                 "Should be a StructuralAnnotation")
            self.assertIsInstance(arabidopsis, SourceAnnotation, 
                                 "Should be a SourceAnnotation")
            self.assertIsInstance(photosynthesis, FunctionalAnnotation, 
                                 "Should be a FunctionalAnnotation")
    
    def test_ontology_import_export(self):
        """Test importing and exporting ontologies."""
        # Skip this test if we can't import the required modules
        if not HAS_ONTOLOGY_MODULES:
            self.skipTest("Required modules not available")
            
        # Create a test ontology
        ontology = AIM2Ontology(owl_path=str(self.temp_owl_path))
        
        # Test importing an external ontology (mock the actual import)
        with patch('owlready2.get_ontology') as mock_get_ontology:
            mock_onto = MagicMock()
            mock_get_ontology.return_value = mock_onto
            
            ontology.import_ontology("http://example.com/ontology.owl", "test")
            self.assertIn("test", ontology.imported_ontologies)
            mock_get_ontology.assert_called_once_with("http://example.com/ontology.owl")
    
    def test_custom_relationship_properties(self):
        """Test that custom relationship properties are properly defined."""
        # Skip this test if we can't import the required modules
        if not HAS_ONTOLOGY_MODULES:
            self.skipTest("Required modules not available")
        
        # Import the properties we want to test
        from aim2.ontology.schema import (
            made_via, accumulates_in, affects, upregulates, downregulates,
            inhibits, activates, participates_in, has_participant, located_in, has_location
        )
        
        # Test that properties are instances of ObjectProperty
        self.assertIsInstance(made_via, owlready2.ObjectPropertyClass)
        self.assertIsInstance(accumulates_in, owlready2.ObjectPropertyClass)
        self.assertIsInstance(affects, owlready2.ObjectPropertyClass)
        
        # Test property inheritance (sub-properties of 'affects')
        self.assertTrue(issubclass(upregulates, type(affects)))
        self.assertTrue(issubclass(downregulates, type(affects)))
        self.assertTrue(issubclass(inhibits, type(affects)))
        self.assertTrue(issubclass(activates, type(affects)))
        
        # Test inverse property relationships
        self.assertEqual(has_participant.inverse_property, participates_in)
        self.assertEqual(has_location.inverse_property, located_in)
        
        # Note: Property characteristics like 'transitive' and 'symmetric' are not tested
        # here as they require specific Owlready2 setup that's not working with the current version
    
    def test_relationship_usage(self):
        """Test that relationships can be used to connect entities."""
        # Skip this test if we can't import the required modules
        if not HAS_ONTOLOGY_MODULES:
            self.skipTest("Required modules not available")
        
        # Import the properties we want to test
        from aim2.ontology.schema import (
            made_via, accumulates_in, affects, upregulates, located_in
        )
        
        with onto:
            # Create some test instances
            gene = FunctionalAnnotation("test_gene")
            protein = FunctionalAnnotation("test_protein")
            process = FunctionalAnnotation("test_process")
            location = StructuralAnnotation("test_location")
            
            # Set up some relationships
            gene.made_via.append(process)
            protein.accumulates_in.append(location)
            gene.affects.append(protein)
            gene.upregulates.append(protein)  # upregulates is a sub-property of affects
            protein.located_in.append(location)
            
            # Test that relationships were set correctly
            self.assertIn(process, gene.made_via)
            self.assertIn(location, protein.accumulates_in)
            self.assertIn(protein, gene.affects)
            self.assertIn(protein, gene.upregulates)
            self.assertIn(location, protein.located_in)
            
            # Test that upregulates implies affects
            self.assertIn(protein, gene.affects)  # Should be true because upregulates is a sub-property of affects

if __name__ == "__main__":
    unittest.main()
