Of course. Here is a detailed checklist of granular tasks for each development ticket, designed for a software team to track progress. This checklist follows a test-driven development approach, where unit tests are created before the functionality is implemented.

### **Project Setup & Management (PROJ)**

#### **Ticket: PROJ-001 \- Initial Project Scaffolding and Dependency Management**

- [X] **PROJ-001-T01**: Create a test in tests/test\_project\_setup.py to verify the existence of the main package directory (aim2/) and all required sub-packages (ontology/, corpus/, extraction/, postprocessing/).  
- [X] **PROJ-001-T02**: Create the directory structure as specified in the project plan, including \_\_init\_\_.py files to make them recognizable as Python packages.  
- [X] **PROJ-001-T03**: Create the pyproject.toml file defining the project metadata (name, version, author).  
- [X] **PROJ-001-T04**: Create a requirements.txt file and add all specified libraries: Owlready2, Biopython, Selenium, undetected-chromedriver, PyMuPDF, LangChain, llm-ie, dedupe, pytest, Jinja2.  
- [X] **PROJ-001-T05**: Run the unit tests to confirm the project structure is correct.

#### **Ticket: PROJ-002 \- Implement Centralized Configuration System**

- [X] **PROJ-002-T01**: In tests/test\_config.py, write unit tests to check for: loading a sample YAML config file, correctly retrieving a value for a given key, and handling cases where a key is missing.  
- [X] **PROJ-002-T02**: Create a sample config.yml file in the root directory with placeholder values for file paths, API keys, and keywords.  
  - Note: The file exists in the config/ directory (better practice than root) with all required placeholders.
- [X] **PROJ-002-T03**: Create a module aim2/config.py to load the config.yml file and provide a global access point to its parameters.  
  - Note: The module is already implemented with comprehensive functionality.
- [X] **PROJ-002-T04**: Run all unit tests for the configuration system to ensure they pass.  
  - All tests in tests/test_config.py passed successfully.

#### **Ticket: PROJ-003 \- Set Up Testing Framework**

- [X] **PROJ-003-T01**: Add pytest to the requirements.txt file.  
  - Note: pytest>=8.4.1 is already listed in requirements.txt.
- [X] **PROJ-003-T02**: Create the tests/ directory at the project root.  
  - Note: The tests/ directory already exists and contains multiple test files.
- [X] **PROJ-003-T03**: Create placeholder test files for each core module (e.g., tests/ontology/test\_manager.py, tests/corpus/test\_builder.py).  
  - Created placeholder test files for all core modules: ontology, corpus, extraction, and postprocessing.
- [X] **PROJ-003-T04**: Add a simple assert True test in one of the placeholder files.  
  - Added a meaningful test in tests/ontology/test_manager.py that verifies ontology manager initialization.
- [X] **PROJ-003-T05**: Run pytest from the command line to confirm the framework is operational and the placeholder test passes.  
  - Verified test framework is operational with simple test cases in tests/ontology/test_manager.py

---

### **Ontology Development (ONT)**

#### **Ticket: ONT-001 \- Define Core AIM2 Ontology Schema and Manager**

- [X] **ONT-001-T01**: Write unit tests in tests/ontology/test\_schema.py to verify that the core classes (StructuralAnnotation, SourceAnnotation, FunctionalAnnotation) are created successfully within an Owlready2 ontology and are subclasses of owl.Thing.  
  - Created comprehensive tests verifying core classes and properties with proper inheritance and typing.
- [X] **ONT-001-T02**: Implement the class definitions in aim2/ontology/schema.py.  
  - Verified that all core classes, properties, and relationships are properly defined with appropriate inheritance and documentation.
- [X] **ONT-001-T03**: Write unit tests in tests/ontology/test\_manager.py to ensure the AIM2Ontology class can be instantiated and creates an empty ontology world.  
  - Implemented comprehensive tests for initialization, core classes, saving/loading, reasoning, and ontology imports.
- [X] **ONT-001-T04**: Implement the basic AIM2Ontology class structure in aim2/ontology/manager.py.  
  - Implemented with full functionality including loading, saving, reasoning, and ontology import capabilities.
- [X] **ONT-001-T05**: Run all unit tests for the core schema and manager to ensure they pass.  
  - All 21 tests passed successfully for the core schema and manager components.

#### **Ticket: ONT-002 \- Define Custom Relationship Properties**

- [X] **ONT-002-T01**: Write unit tests in tests/ontology/test\_schema.py to check that custom properties (accumulates\_in, affects) are created as ObjectProperty subclasses.  
- [X] **ONT-002-T02**: Add tests to verify that the domain and range for each property are correctly assigned.  
- [X] **ONT-002-T03**: Add tests to verify that sub-properties (e.g., upregulates) correctly inherit from their parent property (affects).  
- [X] **ONT-002-T04**: Implement the property definitions in aim2/ontology/schema.py using Owlready2's class-based syntax.  
- [X] **ONT-002-T05**: Run all unit tests for custom properties to ensure they pass.

#### **Ticket: ONT-003 \- Implement Plant Ontology (PO) Importer**

- [ ] **ONT-003-T01**: Write unit tests in tests/ontology/importers/test\_po\_importer.py using a small, local test version of the PO. The tests should verify that the importer function correctly loads the ontology, filters classes based on a predefined allow-list, and ignores all other classes.  
- [ ] **ONT-003-T02**: Create the aim2/ontology/importers/po\_importer.py module.  
- [ ] **ONT-003-T03**: Implement the function to load the PO ontology, iterate through its classes using .classes(), and retain only those in the allow-list.  
- [ ] **ONT-003-T04**: Implement the logic to re-parent the filtered PO terms to become subclasses of the appropriate AIM2 class.  
- [ ] **ONT-003-T05**: Run all unit tests for the PO importer to ensure they pass.

#### **Ticket: ONT-004 \- Implement Gene Ontology (GO) Importer**

- [ ] **ONT-004-T01**: Write unit tests in tests/ontology/importers/test\_go\_importer.py using the go-basic.owl file. The tests should verify that the importer loads, filters to a relevant subset (e.g., based on a list of parent terms), and re-parents the terms correctly.  
- [ ] **ONT-004-T02**: Create the aim2/ontology/importers/go\_importer.py module.  
- [ ] **ONT-004-T03**: Implement the function to load the GO ontology and filter it to the desired subset.  
- [ ] **ONT-004-T04**: Run all unit tests for the GO importer to ensure they pass.

#### **Ticket: ONT-005 \- Implement NCBI Taxonomy Importer**

- [ ] **ONT-005-T01**: Write unit tests in tests/ontology/importers/test\_ncbi\_taxonomy.py. Use unittest.mock to patch Bio.Entrez calls to avoid actual network requests. Test that the function correctly formats the query and processes a mock XML response to return a TaxID.  
- [ ] **ONT-005-T02**: Create the aim2/ontology/importers/ncbi\_taxonomy.py module.  
- [ ] **ONT-005-T03**: Implement the function to query the NCBI Taxonomy database using Bio.Entrez.esearch and Bio.Entrez.efetch.  
- [ ] **ONT-005-T04**: Run all unit tests for the NCBI Taxonomy importer to ensure they pass.

#### **Ticket: ONT-006 \- Implement Importers for PECO, TO, and ChemFOnt**

- [ ] **ONT-006-T01**: Write unit tests for each importer (test\_peco\_importer.py, etc.) using local copies of their respective OWL files. Verify that each importer loads and integrates a sample of key terms.  
- [ ] **ONT-006-T02**: Create the importer modules: peco\_importer.py, to\_importer.py, chemfont\_importer.py.  
- [ ] **ONT-006-T03**: Implement the loading and integration logic for each ontology.  
- [ ] **ONT-006-T04**: Run all unit tests for these importers to ensure they pass.

#### **Ticket: ONT-007 \- Implement Importers for NP Classifier and PMN**

- [ ] **ONT-007-T01**: Write unit tests in tests/ontology/importers/test\_npc\_importer.py using a sample JSON file from the Natural Products Atlas download page. Verify that the parser creates the correct class hierarchy (Pathway, Superclass, Class).  
- [ ] **ONT-007-T02**: Write unit tests for the PMN importer using sample data files. Verify that pathway and compound information is correctly parsed and represented.  
- [ ] **ONT-007-T03**: Create npc\_importer.py and implement the JSON parsing logic to create Owlready2 classes.  
- [ ] **ONT-007-T04**: Create pmn\_importer.py and implement the logic to parse PMN data files.  
- [ ] **ONT-007-T05**: Run all unit tests for the NPC and PMN importers to ensure they pass.

#### **Ticket: ONT-008 \- Finalize Ontology Integration and Persistence**

- [ ] **ONT-008-T01**: Write an integration test in tests/ontology/test\_manager.py that calls the main build method of the AIM2Ontology class. Mock the individual importers to return small, controlled ontology objects. Verify that the final merged ontology contains elements from all mocked sources.  
- [ ] **ONT-008-T02**: Write a test to check the save() method. The test should save the ontology to a temporary file and verify the file's existence and basic integrity.  
- [ ] **ONT-008-T03**: In manager.py, implement the main orchestration method that calls all the importer functions and merges their results into the main ontology.  
- [ ] **ONT-008-T04**: Implement the save() method using onto.save() and the utility to export to CSV.  
- [ ] **ONT-008-T05**: Run all integration tests for the ontology build process to ensure they pass.

---

### **Literature Corpus & Preprocessing (COR)**

#### **Ticket: COR-001 \- Implement PubMed Search and PMID Collection**

- [ ] **COR-001-T01**: Write unit tests in tests/corpus/test\_builder.py that mock Bio.Entrez.esearch. Verify that the function constructs the correct search term and processes the mock XML response to return a list of PMIDs.  
- [ ] **COR-001-T02**: In aim2/corpus/builder.py, implement the function to perform the PubMed search using Bio.Entrez.esearch.  
- [ ] **COR-001-T03**: Run all unit tests for the PubMed search to ensure they pass.

#### **Ticket: COR-002 \- Implement Tier 1 Literature Retrieval (PMC XML)**

- [ ] **COR-002-T01**: Write unit tests that mock Bio.Entrez.efetch. The test should provide a list of PMIDs and verify that the function attempts a download for each and correctly handles the mock response.  
- [ ] **COR-002-T02**: Implement the XML retrieval logic in aim2/corpus/builder.py using Bio.Entrez.efetch. The function should save the returned content to a local file named with the PMID.  
- [ ] **COR-002-T03**: Run all unit tests for XML retrieval to ensure they pass.

#### **Ticket: COR-003 \- Implement Tier 2 Literature Retrieval (PDF Scraping)**

- [ ] **COR-003-T01**: Write unit tests that mock the selenium.webdriver object. Test the logic that resolves DOIs and constructs URLs. Verify that the function correctly configures the undetected-chromedriver with proxies and anti-detection options.  
- [ ] **COR-003-T02**: Implement the PDF retrieval function in aim2/corpus/builder.py using Selenium and undetected-chromedriver. Include robust error handling for TimeoutException and other common Selenium errors.  
- [ ] **COR-003-T03**: Run all unit tests for the PDF scraping logic to ensure they pass.

#### **Ticket: COR-004 \- Implement Unified Document Parser**

- [ ] **COR-004-T01**: Write unit tests in tests/corpus/test\_parser.py with sample XML and PDF files. Verify that the function correctly identifies the file type and returns the expected text content for each.  
- [ ] **COR-004-T02**: In aim2/corpus/parser.py, implement a function that takes a file path, checks the extension, and calls either pubmedparser2 for XML or PyMuPDF for PDF. Benchmarks show PyMuPDF is a high-performance choice.  
- [ ] **COR-004-T03**: Run all unit tests for the document parser to ensure they pass.

#### **Ticket: COR-005 \- Implement Text Cleaning and Chunking Pipeline**

- [ ] **COR-005-T01**: Write unit tests in tests/corpus/test\_preprocessor.py. Test the cleaning function with sample text containing common artifacts (e.g., "Fig. 1", page numbers, repeated headers) and assert they are removed.  
- [ ] **COR-005-T02**: Write tests for the chunking function. Provide a long text and verify that it is split into chunks that respect the specified size and semantic boundaries (paragraphs, sentences).  
- [ ] **COR-005-T03**: In aim2/corpus/preprocessor.py, implement the text cleaning function using the re module.  
- [ ] **COR-005-T04**: Implement the chunking function using LangChain's RecursiveCharacterTextSplitter.  
- [ ] **COR-005-T05**: Run all unit tests for the preprocessing pipeline to ensure they pass.

---

### **Information Extraction (EXT)**

#### **Ticket: EXT-001 \- Set Up LLM Abstraction Layer and Prompt Management**

- [ ] **EXT-001-T01**: Write unit tests in tests/extraction/test\_llm\_interface.py. Test the prompt loader to ensure it can read a Jinja2 template and render it with variables. Mock an LLM API call and verify the abstraction layer formats the request and parses the response correctly.  
- [ ] **EXT-001-T02**: Create the aim2/extraction/prompts/ directory and add an initial NER prompt template file.  
- [ ] **EXT-001-T03**: In aim2/extraction/llm\_interface.py, implement the prompt loading logic and the LLM abstraction layer, using the engines module from llm-ie as a backend.  
- [ ] **EXT-001-T04**: Run all unit tests for the LLM interface to ensure they pass.

#### **Ticket: EXT-002 \- Implement Named Entity Recognition (NER) Module**

- [ ] **EXT-002-T01**: Write unit tests in tests/extraction/test\_entity\_extractor.py. Use a sample text chunk and a mock LLM JSON response. Verify that the extractor function correctly calls the LLM interface and parses the mock response into structured entity objects.  
- [ ] **EXT-002-T02**: In aim2/extraction/entity\_extractor.py, implement the main script that iterates through text chunks, constructs the prompt using the template from EXT-001, sends it to the LLM via the abstraction layer, and parses the output. The llm-ie library provides a framework for this.  
- [ ] **EXT-002-T03**: Run all unit tests for the NER module to ensure they pass.

#### **Ticket: EXT-003 \- Implement Relationship Extraction (RE) Module**

- [ ] **EXT-003-T01**: Write unit tests in tests/extraction/test\_relation\_extractor.py. Provide a list of extracted entities and test the candidate pairing logic. For a given pair, mock the LLM response and verify that the extractor correctly parses the relationship type.  
- [ ] **EXT-003-T02**: In aim2/extraction/relation\_extractor.py, implement the logic to generate candidate entity pairs based on proximity.  
- [ ] **EXT-003-T03**: Implement the function to generate a focused prompt for each pair and call the LLM to classify the relationship, a core feature of libraries like llm-ie.  
- [ ] **EXT-003-T04**: Run all unit tests for the RE module to ensure they pass.

---

### **Post-Extraction Processing (POST)**

#### **Ticket: POST-001 \- Implement Entity Normalization and Ontology Mapping**

- [ ] **POST-001-T01**: Write unit tests in tests/postprocessing/test\_mapper.py. Use a mock Owlready2 ontology to test the creation of the grounding dictionary.  
- [ ] **POST-001-T02**: Write separate tests for the normalization algorithm: one for exact matches, one for fuzzy string matching, and one that mocks contextual disambiguation logic.  
- [ ] **POST-001-T03**: In aim2/postprocessing/mapper.py, implement the function to build the grounding dictionary (mapping synonyms to canonical IRIs) from the AIM2 ontology.  
- [ ] **POST-001-T04**: Implement the multi-step normalization function that links extracted text strings to ontology identifiers, a process also known as Named Entity Normalization (NEN).  
- [ ] **POST-001-T05**: Run all unit tests for the entity normalization module to ensure they pass.

#### **Ticket: POST-002 \- Implement NCBI Taxonomy Validation for Species**

- [ ] **POST-002-T01**: Write unit tests that mock the API call to the NCBI Taxonomy service. Verify that for an entity of type Species, the function is called and correctly processes the mock response to attach a TaxID.  
- [ ] **POST-002-T02**: In aim2/postprocessing/mapper.py, enhance the normalization logic to include a specific step for Species entities, using a library like ncbi-taxonomist or Biopython to validate and retrieve the official TaxID.  
- [ ] **POST-002-T03**: Run all unit tests for the species validation feature to ensure they pass.

#### **Ticket: POST-003 \- Implement Fact Consolidation and Deduplication**

- [ ] **POST-003-T01**: Write unit tests in tests/postprocessing/test\_consolidator.py. Create a sample list of extracted facts (triples), including clear duplicates.  
- [ ] **POST-003-T02**: Write a test to ensure the data is correctly formatted for the dedupe library's input requirements.  
- [ ] **POST-003-T03**: Mock the output of dedupe.match() to return predefined clusters. Write a test to verify that the consolidation logic correctly processes these clusters and selects a single canonical fact from each.  
- [ ] **POST-003-T04**: In aim2/postprocessing/consolidator.py, implement the data preparation step for the dedupe library.  
- [ ] **POST-003-T05**: Implement the logic to handle the training/labeling phase and the final clustering process as described in the dedupe examples.  
- [ ] **POST-003-T06**: Run all unit tests for the fact consolidation module to ensure they pass.