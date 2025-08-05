"""
AIM2Ontology - Manager class for the AIM2 ontology.

This module provides the AIM2Ontology class which is responsible for loading,
managing, and saving the AIM2 ontology and its imported ontologies.
"""
import logging
import os
from pathlib import Path
from typing import Optional, Dict, List, Union

from owlready2 import get_ontology, sync_reasoner, default_world, World

from .schema import init_ontology, onto

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIM2Ontology:
    """
    Main class for managing the AIM2 ontology.
    
    This class handles the loading, integration, and saving of the AIM2 ontology
    and its imported ontologies.
    """
    
    def __init__(self, owl_path: Optional[Union[str, Path]] = None):
        """
        Initialize the AIM2 ontology manager.
        
        Args:
            owl_path: Path to save/load the ontology file. If None, a temporary
                     in-memory ontology will be used.
        """
        self.owl_path = Path(owl_path) if owl_path else None
        self.imported_ontologies: Dict[str, object] = {}
        self._initialized = False
        
        # Initialize the base ontology
        self.onto = onto or init_ontology()
        self.world = self.onto.world or default_world
        
        logger.info("AIM2Ontology initialized")
    
    def load(self, path: Optional[Union[str, Path]] = None) -> None:
        """
        Load the ontology from a file.
        
        Args:
            path: Path to the ontology file. If None, uses self.owl_path.
        """
        load_path = Path(path) if path else self.owl_path
        if not load_path:
            raise ValueError("No path provided and no default path set")
        
        if not load_path.exists():
            logger.warning(f"Ontology file not found at {load_path}. Creating a new one.")
            self._initialized = True
            return
        
        logger.info(f"Loading ontology from {load_path}")
        try:
            self.onto = get_ontology(str(load_path)).load()
            self._initialized = True
            logger.info("Ontology loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load ontology: {e}")
            raise
    
    def save(self, path: Optional[Union[str, Path]] = None) -> None:
        """
        Save the ontology to a file.
        
        Args:
            path: Path to save the ontology file. If None, uses self.owl_path.
        """
        if not self._initialized:
            raise RuntimeError("Ontology not initialized. Call load() or create() first.")
        
        save_path = Path(path) if path else self.owl_path
        if not save_path:
            raise ValueError("No path provided and no default path set")
        
        # Ensure the directory exists
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Saving ontology to {save_path}")
        try:
            self.onto.save(file=str(save_path), format="rdfxml")
            logger.info("Ontology saved successfully")
        except Exception as e:
            logger.error(f"Failed to save ontology: {e}")
            raise
    
    def reason(self) -> None:
        """
        Run the reasoner on the ontology.
        """
        if not self._initialized:
            raise RuntimeError("Ontology not initialized. Call load() or create() first.")
        
        logger.info("Running reasoner...")
        try:
            sync_reasoner()
            logger.info("Reasoning completed")
        except Exception as e:
            logger.error(f"Reasoning failed: {e}")
            raise
    
    def import_ontology(self, iri: str, prefix: str) -> None:
        """
        Import an external ontology.
        
        Args:
            iri: The IRI of the ontology to import.
            prefix: A prefix to use for the imported ontology.
        """
        if not self._initialized:
            raise RuntimeError("Ontology not initialized. Call load() or create() first.")
        
        if prefix in self.imported_ontologies:
            logger.warning(f"Ontology with prefix '{prefix}' already imported. Skipping.")
            return
        
        logger.info(f"Importing ontology: {iri}")
        try:
            imported_onto = get_ontology(iri).load()
            self.imported_ontologies[prefix] = imported_onto
            logger.info(f"Successfully imported ontology: {iri}")
        except Exception as e:
            logger.error(f"Failed to import ontology {iri}: {e}")
            raise

# Export the main class
__all__ = ['AIM2Ontology']
