

# **A Strategic Development Plan for the AIM2 Project's Ontology and Information Extraction Backbone**

## **Foundational Ontology Development Framework**

This section details the architecture and implementation of a central Python module, aim2\_ontology, designed for the creation, management, and programmatic interaction with the AIM2 project's custom ontology. The foundational strategy is to leverage an "ontology-oriented programming" paradigm. This approach treats the ontology not as a static data file but as an active, class-based component of the Python application itself. This design is crucial for embedding the complex, domain-specific logic required to capture the nuances of plant metabolomics.

The selection of a suitable library is a pivotal architectural decision that dictates the entire development workflow. While libraries such as rdflib provide robust tools for manipulating Resource Description Framework (RDF) triples at a low level, they are less suited for the high-level conceptual modeling required by the AIM2 project.1 A more powerful and intuitive approach is offered by the

Owlready2 library, which enables developers to manipulate ontology classes, instances, and properties transparently, as if they were native Python objects.3 This paradigm shift is essential for defining and managing custom, hierarchical relationships (e.g.,

affects with sub-properties like upregulates) and for attaching methods directly to ontological concepts. For instance, this allows for the implementation of complex queries as simple Python method calls on an object (e.g., metabolite\_object.get\_accumulated\_tissues()), tightly integrating the semantic model with the application logic. This integration makes the entire system more coherent, maintainable, and powerful than would be possible with a simple RDF graph manipulation approach.6

### **Core Ontology Module (aim2\_ontology): An Object-Oriented Blueprint**

**Objective:** To establish a robust, extensible, and self-contained Python module that serves as the single source of truth for the AIM2 ontology, encapsulating all logic for its construction and management.

Implementation Details:  
The Owlready2 library will serve as the cornerstone of this module, chosen for its powerful ontology-oriented programming features that allow for a direct and intuitive mapping between OWL concepts and Python objects.6 The module will be structured to promote modularity and clarity of purpose.

* **Module Structure:**  
  * manager.py: This file will contain the main AIM2Ontology class. This class will act as the primary interface for the module, responsible for loading all necessary source ontologies, orchestrating the integration and trimming processes, and providing high-level methods for accessing and saving the final ontology.  
  * schema.py: This file will define the core class structure of the AIM2 ontology. It is here that the top-level categories specified in the project plan—StructuralAnnotation, SourceAnnotation, and FunctionalAnnotation—will be formally defined as subclasses of the universal OWL class, owl.Thing. This file will also contain the definitions for all custom relationship properties.  
  * importers/: This sub-package will contain a collection of dedicated Python modules, each responsible for handling a single external ontology (e.g., po\_importer.py for the Plant Ontology, go\_importer.py for the Gene Ontology). This design encapsulates the specific logic required for loading, filtering, and preparing each source, promoting maintainability.  
  * utils.py: A collection of helper functions for common tasks such as normalizing Internationalized Resource Identifiers (IRIs), cleaning labels, and other utility operations will be housed here.

An example of the basic class definitions within schema.py would be structured as follows, establishing the foundational hierarchy of the AIM2 ontology:

Python

from owlready2 import \*

\# This assumes 'onto' is an Ontology object created in manager.py,  
\# for example: onto \= get\_ontology("http://aim2.org/ontology.owl")

with onto:  
    class StructuralAnnotation(Thing): pass  
    class SourceAnnotation(Thing): pass  
    class FunctionalAnnotation(Thing): pass

### **Integrating and Refining Source Ontologies**

**Objective:** To programmatically fetch, filter, and merge terms from a diverse set of external ontologies into the unified AIM2 schema. This entire process must be designed to be reproducible, configurable, and automated.

Implementation Details:  
Each importer module within the importers/ sub-package will handle the complete lifecycle for a single source ontology.

* **Loading:** The get\_ontology(IRI).load() function from Owlready2 will be used to fetch the required OWL files from their respective sources.8 To optimize performance and reduce network dependency, the plan will leverage  
  Owlready2's built-in local caching mechanism by configuring the onto\_path global variable to point to a local directory where downloaded ontologies are stored.  
* **Trimming and Filtering:** A critical step for creating a "manageable and useful subset" is the programmatic trimming of large ontologies. For instance, the project requires reducing over 2,000 anatomical terms from the Plant Ontology to a focused set of 293\. The po\_importer.py module will implement this by maintaining a predefined allow-list of these 293 term IDs. The script will load the full Plant Ontology, iterate through all its classes using po\_onto.classes(), and selectively process only those classes whose identifiers are present in the allow-list. All other classes and their associated axioms will be programmatically ignored, effectively creating a tailored, project-specific subset of the ontology. This same strategy of allow-listing will be applied to other large sources like the Gene Ontology to ensure the final AIM2 ontology remains focused and relevant.  
* **Merging:** After filtering, the selected terms from the source ontologies will be integrated into the AIM2 schema by modifying their hierarchical relationships. This will be achieved by programmatically altering the is\_a property of the term's corresponding Owlready2 object. For example, a trimmed Gene Ontology term such as 'metabolic process' will be made a subclass of the FunctionalAnnotation class defined in the AIM2 schema.py. This re-parenting ensures that all imported concepts are correctly positioned within the new, unified hierarchy.

### **Defining Custom Hierarchies and Relationships**

**Objective:** To formally define the custom semantic relationships—such as is\_a, made\_via, accumulates\_in, and affects—that constitute the structural backbone of the AIM2 knowledge network.

Implementation Details:  
Owlready2 provides a highly intuitive and Pythonic syntax for creating custom properties by subclassing its ObjectProperty or DataProperty classes. This allows for the creation of rich, logical definitions that are machine-readable and can be leveraged by an OWL reasoner for logical inference.10

* **Property Creation:** The schema.py module will contain the definitions for all custom relationships. The domain and range of these properties will be explicitly defined to enforce the logical consistency of the ontology. For example, the accumulates\_in property will be defined to link an individual of the Metabolite class to an individual of the PlantPart class.  
* **Hierarchical Properties:** The system will also support hierarchical relationships by defining sub-properties. For instance, the specific relationships upregulates and downregulates will be defined as sub-properties of the more general affects property. This allows for querying at different levels of granularity.  
* **Code Structure Example (schema.py):**  
  Python  
  from owlready2 import \*  
  \#... (ontology and base classes defined)...  
  with onto:  
      \# Define entity classes  
      class Metabolite(StructuralAnnotation): pass  
      class PlantPart(SourceAnnotation): pass  
      class PlantTrait(FunctionalAnnotation): pass  
      class BiologicalProcess(FunctionalAnnotation): pass

      \# Define an Object Property with explicit domain and range  
      class accumulates\_in(ObjectProperty):  
          domain \= \[Metabolite\]  
          range  \= \[PlantPart\]

      \# Use the concise '\>\>' syntax for another property  
      class affects(Metabolite \>\> PlantTrait): pass

      \# Define sub-properties to create a relationship hierarchy  
      class upregulates(affects): pass  
      class downregulates(affects): pass

      \# Define a transitive property for partonomy reasoning  
      class is\_part\_of(PlantPart \>\> PlantPart, TransitiveProperty): pass

  This approach, well-documented in Owlready2's materials 4, creates a formal, logical structure that is far more powerful than a simple graph, enabling advanced querying and automated reasoning.

### **Ontology Persistence and Versioning**

**Objective:** To store the final, integrated ontology in standard, interoperable formats and to establish a robust system for managing its evolution over the project's lifecycle.

**Implementation Details:**

* **Serialization:** Once the integration process is complete, the final AIM2Ontology object will be serialized to a standard OWL file using the onto.save() method. The RDF/XML format will be used to ensure maximum compatibility with external ontology engineering tools like Protégé.8  
* **Accessibility:** To facilitate use by team members who may not be ontology experts, a utility script will be created to export the core components of the ontology—key terms, their definitions, synonyms, and relationships—into a set of human-readable CSV files. This script will programmatically iterate through the ontology's classes (onto.classes()) and their properties to generate the tables.  
* **Versioning:** The generated OWL and CSV files will be stored in a dedicated GitHub repository. This is a critical step that leverages the power of Git for version control, allowing the team to track all changes, manage official releases with tags, and collaborate on the ontology's development using standard software engineering practices like pull requests.

| Table 1: Source Ontologies and Integration Strategy |  |  |  |  |  |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Ontology Name** | **Abbreviation** | **Source URL (OWL Download)** | **Key Categories** | **Trimming/Filtering Strategy** | **Python Module Handler** |
| Chemont / ClassyFire | Chemont | Integrated within ChemFOnt | Structural | Extract chemical classes relevant to plant secondary metabolites. | importers/chemont\_importer.py |
| NP Classifier | NPC | Data available in JSON 13; ontology structure is implicit. | Structural | Extract Pathway, Superclass, and Class hierarchy. | importers/npc\_importer.py |
| Plant Metabolic Network | PMN | Data download available, but not as a single OWL file.14 | Structural | Extract pathway and compound class information. | importers/pmn\_importer.py |
| Plant Ontology | PO | [http://purl.obolibrary.org/obo/po.owl](http://purl.obolibrary.org/obo/po.owl) 16 | Source | Filter to a predefined list of \~293 relevant anatomical terms. | importers/po\_importer.py |
| NCBI Taxonomy | NCBITax | Accessed via E-utilities API.18 | Source | Focus on Viridiplantae; map species names to TaxIDs. | importers/ncbi\_taxonomy.py |
| Plant Experimental Condition Ontology | PECO | [http://purl.obolibrary.org/obo/peco.owl](http://purl.obolibrary.org/obo/peco.owl) 22 | Source | Select key terms related to abiotic/biotic stress conditions. | importers/peco\_importer.py |
| Gene Ontology | GO | [http://purl.obolibrary.org/obo/go-basic.owl](http://purl.obolibrary.org/obo/go-basic.owl) 23 | Functional | Filter to a subset of molecular function & biological process terms relevant to plant metabolism and resilience. | importers/go\_importer.py |
| Trait Ontology | TO | [http://purl.obolibrary.org/obo/to.owl](http://purl.obolibrary.org/obo/to.owl) 25 | Functional | Select traits related to plant growth, development, and stress response. | importers/to\_importer.py |
| Chemical Functional Ontology | ChemFOnt | Available from [https://www.chemfont.ca](https://www.chemfont.ca) 26 | Functional | Extract functional roles of chemicals, focusing on human health effects. | importers/chemfont\_importer.py |

## **Literature Corpus Construction and Preprocessing**

This section outlines the design of an automated pipeline for acquiring and preparing a comprehensive corpus of scientific literature for subsequent analysis by Large Language Models (LLMs). The architecture is designed for robustness and resilience, acknowledging the heterogeneous nature of scientific publishing and the significant technical challenges associated with programmatic access to full-text articles.

A successful corpus-building pipeline cannot be a simple, linear script; it must be a stateful, multi-stage process with built-in fallback mechanisms. The most efficient and reliable source of full-text scientific data is the PubMed Central (PMC) Open Access (OA) Subset, which provides articles in a structured XML format. In contrast, programmatically downloading PDF files directly from publisher websites is a fragile and high-effort task due to sophisticated anti-bot measures, such as JavaScript challenges, CAPTCHAs, and IP-based rate limiting.29 Therefore, the pipeline will be architected to prioritize structured, open-access sources (API queries leading to XML downloads) before resorting to unstructured, high-risk sources (PDF web scraping). This tiered approach maximizes the acquisition of high-quality, easily parsable data while isolating the more complex and error-prone scraping tasks to a smaller subset of articles.

### **Automated Literature Retrieval Module (corpus\_builder)**

**Objective:** To create a stand-alone, configurable Python script that systematically searches for and downloads scientific literature based on a defined set of keywords, managing different retrieval strategies based on data availability.

**Implementation Details:**

* **PubMed Search and ID Collection:** The script will begin by using the Bio.Entrez.esearch function from the well-established Biopython library. This function will query the PubMed database for articles matching a configurable list of keywords relevant to plant metabolites and resilience (e.g., "flavonoid AND drought", "terpenoid AND defense").32 The primary output of this step will be a comprehensive list of all matching PubMed Identifiers (PMIDs), which will serve as the master list for the retrieval process.  
* **Tier 1: PMC XML Retrieval:** For each PMID in the master list, the script will first attempt to retrieve the full-text article from the PMC OA subset. It will use Bio.Entrez.efetch or elink to check for the availability of a full-text XML version.21 If an XML version is available, it will be downloaded and stored locally. This represents the preferred data source due to its structured nature and permissive access.  
* **Tier 2: PDF Retrieval (Fallback Mechanism):** For PMIDs that do not have an available PMC XML file, the script will initiate a more complex fallback procedure to retrieve the PDF from the publisher's website.  
  * **DOI Resolution:** The script will first resolve the article's Digital Object Identifier (DOI) and use it to find the article's landing page.  
  * **Advanced Web Scraping:** To handle the challenges of modern, dynamic websites, the script will employ an advanced browser automation library. The recommended tool is Selenium coupled with the undetected-chromedriver package, which is specifically designed to modify the browser's properties to appear more human-like and evade common bot-detection scripts.35 To further mitigate the risk of being blocked, the system will be configured to route its requests through a rotating proxy service. This combination of tools is necessary to automate browser interactions, click on JavaScript-based download buttons, and handle other dynamic elements, while minimizing the risk of IP-based blocking.30 This tier of the retrieval process will be implemented with configurable delays between requests and robust error-handling logic to manage failed download attempts gracefully.

### **Document Ingestion and Text Extraction**

**Objective:** To create a unified parsing function that can accept a file path for either an XML or a PDF document and return its clean, plain text content, abstracting away the differences in the underlying file formats.

**Implementation Details:**

* **XML Parsing:** For .xml files downloaded from PMC, the pubmed\_parser library 37 or its successor  
  pubmedparser2 38 will be utilized. These libraries are purpose-built for the specific schema of PubMed and MEDLINE XML files. They can efficiently parse the document and extract distinct sections, such as the title, abstract, main body text, and references, into a structured Python dictionary, which simplifies the process of isolating the relevant textual content.39  
* **PDF Text Extraction:** For .pdf files, the PyMuPDF library (also known as fitz) is the recommended choice. Independent benchmarks have consistently shown that PyMuPDF is significantly faster and often more accurate for text extraction from digitally-born (non-scanned) PDFs compared to alternatives like PyPDF2 or pdfminer.40 The implementation will involve a script that opens the PDF, iterates through each page, and uses the  
  page.get\_text() method to extract the raw text content.

### **Text Normalization and Chunking Pipeline (text\_preprocessor)**

**Objective:** To prepare the raw extracted text for efficient and effective processing by LLMs through a systematic cleaning and chunking pipeline.

**Implementation Details:**

* **Cleaning and Normalization:** Before chunking, the raw text will undergo a cleaning process. This will be implemented using Python's built-in re module.44 A series of regular expressions will be applied to remove common artifacts found in scientific papers, such as repeating page headers and footers, figure captions that have been incorrectly merged with the main body text during extraction, and spurious line breaks or hyphenation at the end of lines. Additionally, Unicode normalization will be applied to ensure consistent character representation.  
* **Strategic Text Chunking:** The method used to split the document into smaller chunks is a critical factor influencing LLM performance. A naive fixed-size chunking approach can arbitrarily split sentences and separate related ideas, harming the model's ability to understand context. To avoid this, a more sophisticated strategy will be employed using the LangChain library's RecursiveCharacterTextSplitter.45 This tool attempts to split text along a prioritized list of separators, by default starting with paragraph breaks (  
  \\n\\n), then sentence breaks (\\n), and finally spaces. This hierarchical approach helps to keep semantically related sentences together within a single chunk, preserving local context for the LLM. The target chunk size and the amount of overlap between adjacent chunks will be defined as configurable parameters, allowing for empirical tuning to match the context window and optimal performance characteristics of the specific LLM being used.

## **LLM-Powered Information Extraction Engine**

This section details the design of the core Natural Language Processing (NLP) modules that will leverage Large Language Models (LLMs) to extract structured knowledge from the prepared literature corpus. The architecture will be deliberately modular, separating the task of Named Entity Recognition (NER) from the subsequent task of Relationship Extraction (RE). This two-stage design is not merely a software engineering choice but a crucial strategy to manage the cognitive load on the LLM and improve the accuracy and efficiency of the extraction process.

Asking an LLM to perform document-level relationship extraction in a single step has been shown to be inefficient. The model's attention becomes dispersed by the overwhelming number of entity pairs within a document that have no meaningful relationship, leading to a degradation in performance.46 A more effective and state-of-the-art pipeline first identifies all candidate entities of interest (the NER stage) and then, in a second, more focused stage, presents specific pairs of these entities to the LLM to classify the relationship between them. This approach transforms a broad, unfocused task into a series of smaller, well-defined classification problems. Modern information extraction libraries like

llm-ie are built around this modular philosophy, providing distinct components for entity extraction and relationship extraction, a design pattern that this project will adopt.48

### **Named Entity Recognition (NER) Module (entity\_extractor)**

**Objective:** To identify and classify all specified entity types (e.g., metabolites, species, plant traits) within the preprocessed text chunks, outputting them in a structured, machine-readable format.

**Implementation Details:**

* **Approach:** The module will implement an LLM-based, zero-shot or few-shot prompting approach. This strategy is chosen to avoid the significant time and resource investment required for collecting a large annotated dataset and fine-tuning a traditional NER model (such as a BERT-based model).  
* **Tooling:** To accelerate development and ensure robustness, the use of a specialized library is recommended. The llm-ie library is an excellent candidate, as it provides pre-built, well-tested components for LLM-based information extraction, including various prompting algorithms and support for multiple LLM backends.48 An alternative is  
  spacy-llm, which offers similar capabilities for integrating LLMs into a spaCy pipeline.51  
* **Schema and Output Format:** The prompt sent to the LLM will contain a clear definition of the entity schema (as detailed in Table 2 below) and will explicitly instruct the model to return its findings in a structured JSON format. This strict output formatting is essential for ensuring that the LLM's response can be reliably and automatically parsed by downstream components.  
* **Process:** The entity\_extractor module will be implemented as a script that iterates through the text chunks generated by the text\_preprocessor. For each chunk, it will construct and submit the NER prompt to the LLM, receive the JSON response, parse it to extract the identified entities, and aggregate these entities for the entire document. As part of this aggregation, the character offsets of each entity will be adjusted to be relative to the start of the original, un-chunked document, ensuring that their locations can be precisely tracked.

### **Relationship Extraction Module (relation\_extractor)**

**Objective:** To identify and classify the semantic relationships between the entities that were extracted in the NER step, adhering to the predefined relationship schema.

**Implementation Details:**

* **Candidate Pairing:** After the NER module has processed an entire document, the relation\_extractor will begin by generating candidate pairs of entities for relationship analysis. To manage the combinatorial explosion of potential pairs, a set of simple heuristics will be applied. For example, the system will be configured to only generate pairs of entities that appear within a certain proximity, such as within the same sentence or in adjacent sentences. This significantly reduces the number of queries that need to be sent to the LLM.  
* **Focused Prompting:** For each candidate pair, a new, highly focused prompt will be dynamically generated. This prompt will provide the LLM with crucial context, including the specific text snippet (e.g., the sentence) containing both entities, clear definitions of the two entities in question, and a direct request to classify the relationship between them according to the predefined schema (see Table 2). Recent research underscores the importance of such clear, structured, and context-rich prompts for achieving high accuracy in LLM-based relationship extraction.53  
* **Hierarchical Relationship Handling:** The project requires the extraction of hierarchical relationships (e.g., identifying upregulates as a specific type of affects). The prompt will be designed to handle this by using a chain-of-thought or multi-step approach. For example, the LLM could be asked to first identify if a general relationship like "affects" exists, and if so, to then classify it into a more specific sub-type from a provided list.

### **Prompt Engineering and LLM Integration Strategy**

**Objective:** To develop a centralized and flexible system for managing prompts and interfacing with various LLM providers, ensuring maintainability and adaptability.

**Implementation Details:**

* **Prompt Templates:** All prompts will be managed as external template files (e.g., using the Jinja2 templating engine) rather than being hardcoded as strings within the Python scripts. This separation of logic and content allows for easy editing, versioning, and experimentation with different prompt phrasings without modifying the core application code. The llm-ie library's PromptEditor provides an interactive command-line interface that can be used to collaboratively develop and refine these templates.48  
* **LLM Abstraction Layer:** To avoid vendor lock-in and to allow for easy comparison between different models, an abstraction layer will be implemented to handle all interactions with LLM APIs. This layer will provide a unified interface for sending requests and receiving responses. The engines module of the llm-ie library already provides this functionality for many popular backends (including OpenAI, Hugging Face, and local models via Ollama), and can be adopted directly to accelerate development.48  
* **Output Schema Enforcement:** To ensure the reliability of the LLM's output, the prompts will explicitly command the model to return data in a JSON format that conforms to a predefined schema. This schema can be formally defined using a library like Pydantic. The application can then use this Pydantic model to parse and validate the LLM's JSON response, automatically flagging or rejecting any outputs that do not adhere to the expected structure.

| Table 2: AIM2 Entity and Relation Schema for Extraction |  |  |  |
| :---- | :---- | :---- | :---- |
| **Category** | **Entity/Relation Type** | **Description** | **Attributes / Sub-types** |
| **Entities** |  |  |  |
| Structural | Chemical / Metabolite | A specific chemical compound or metabolite. | name, synonyms |
| Source | Species | A plant species. | ncbi\_tax\_id |
| Source | PlantAnatomy | A specific part or tissue of a plant. | name |
| Source | ExperimentalCondition | A condition applied during an experiment. | type (e.g., abiotic, biotic), value |
| Functional | Gene / Protein | A specific gene or protein. | symbol, id |
| Functional | MolecularTrait | A molecular-level trait or process. | go\_id |
| Functional | PlantTrait | A phenotypic trait of a plant. | trait\_ontology\_id |
| Functional | HumanTrait | A human health-related trait or effect. | name |
| **Relations** |  |  |  |
| General | is\_a | A subclass or instance relationship. | subclass\_of, instance\_of |
| Biosynthetic | made\_via | Indicates a biosynthetic pathway relationship. | precursor\_of, product\_of |
| Locational | accumulates\_in | Indicates where a metabolite is found. |  |
| Functional | affects | A general functional relationship. | upregulates, downregulates, inhibits, induces\_expression\_of, improves, worsens |

## **Post-Extraction Processing and Knowledge Integration**

This section details the critical final stages of the pipeline, which are designed to transform the raw, text-derived outputs from the LLM into a clean, validated, and ontology-grounded knowledge base. This post-processing is essential for ensuring the quality, consistency, and ultimate utility of the final AIM2 network. The process involves two sophisticated steps: entity normalization and fact consolidation.

The mapping of extracted textual entities to the formal AIM2 ontology is not a simple dictionary lookup; it is a complex disambiguation problem. An extracted string such as "RSV" could refer to the "Respiratory syncytial virus" or the "Rous-Sarcoma-Virus" depending on the document's context.56 Effective Named Entity Normalization (NEN) requires using the surrounding text as context to resolve this ambiguity, a principle central to the design of advanced biomedical NEN tools like Gilda.57 Similarly, the deduplication of extracted facts is not about finding identical strings but about identifying semantically equivalent statements. For example, the fact

(Metabolite\_A, affects, Trait\_B) may be semantically identical to (Trait\_B, is\_affected\_by, Metabolite\_A) if the relationships are defined as inverses. This requires fuzzy matching and machine learning techniques, as implemented in libraries like dedupe.58

### **Entity Normalization and Ontology Mapping (knowledge\_mapper)**

**Objective:** To accurately link the textual entities extracted by the LLM to their canonical identifiers within the AIM2 ontology, resolving both synonymy and ambiguity.

**Implementation Details:**

* **Grounding Dictionary Construction:** The module will begin by programmatically creating an in-memory "grounding dictionary." This will be done by loading the final AIM2 ontology using Owlready2 and iterating through all its entities. The dictionary will map all known names and synonyms for each entity to its unique, canonical IRI.  
* **Normalization Algorithm:** For each entity string extracted by the LLM, the module will execute a multi-step normalization algorithm:  
  1. **Exact Match:** First, it will perform a case-insensitive search for an exact match in the grounding dictionary.  
  2. **Fuzzy Match:** If no exact match is found, it will employ a fuzzy string matching algorithm (e.g., Levenshtein distance or a similar metric) to identify a list of potential candidate matches from the dictionary.  
  3. **Contextual Disambiguation:** If the previous steps result in multiple candidate matches (indicating ambiguity), a disambiguation step will be triggered. This can be implemented by generating a vector embedding of the context sentence from the source paper (where the entity was found) and comparing it to pre-computed embeddings of the definitions or descriptions associated with each candidate entity in the ontology. The candidate whose definition has the highest cosine similarity to the context sentence will be selected as the correct match.  
* **NCBI Taxonomy Integration:** For entities classified as Species, a specialized validation step will be performed. The ncbi-taxonomist Python package 60 or a custom script utilizing  
  Biopython's Bio.Entrez module will be used to query the NCBI Taxonomy database. This will validate the extracted species name and fetch its canonical NCBI Taxonomy ID, ensuring that all species information is robustly and correctly standardized.

### **Fact Consolidation and Deduplication (fact\_consolidator)**

**Objective:** To process the stream of normalized, extracted facts (represented as subject-predicate-object triples) and produce a clean, non-redundant set for inclusion in the final knowledge base.

**Implementation Details:**

* **Tooling:** The dedupe Python library is the ideal choice for this task. It is a mature, open-source library that uses active learning and statistical methods to perform fuzzy matching and entity resolution on structured data, which is precisely the challenge at hand.58  
* **Process:** The consolidation process will follow the standard workflow for the dedupe library:  
  1. **Define Fields:** The "records" to be deduplicated will be the extracted relationships (facts). The fields for comparison will be the canonical IRIs of the subject, predicate, and object of each fact. Additional fields, such as the source document's PMID, can also be included.  
  2. **Training Phase:** The dedupe library requires a small amount of manual labeling to train its model. The system will present a human expert with pairs of similar-looking facts and ask if they represent the same underlying piece of knowledge. This active learning process allows the model to learn the specific patterns of redundancy in the extracted data.  
  3. **Clustering:** Once the model is trained, it will be run over the entire set of extracted facts. The library will then partition the facts into clusters, where each cluster contains a set of records that the model has determined to be duplicates.  
  4. **Canonicalization:** From each identified cluster, a single canonical fact will be selected to be stored in the final knowledge base. The metadata for this canonical fact will be updated to include a list of all supporting evidence (e.g., the PMIDs of all source documents from which the fact was extracted), providing full traceability.

## **Implementation Roadmap and Best Practices**

This concluding section provides a high-level project structure, a consolidated technology stack, and a set of strategic recommendations designed to guide the development process and ensure the successful delivery of the AIM2 project's core software components. The plan emphasizes modular design, the use of best-in-class open-source libraries, and a rigorous, iterative evaluation framework.

### **Modular Program Structure and Dependencies**

**Objective:** To design a Python project structure that strictly adheres to the requirement for creating stand-alone yet importable programs, promoting code reuse, and simplifying maintenance.

Implementation Details:  
The project will be organized as a formal Python package. Each major functional component described in the preceding sections will be implemented as a sub-package. This modular design ensures a clear separation of concerns. Each module can be executed as a stand-alone script for specific tasks (e.g., running only the ontology build process) via a \_\_main\_\_.py entry point, or its classes and functions can be imported for use in larger, integrated workflows.

| Table 3: Proposed Python Project Structure |  |
| :---- | :---- |
| **Path** | **Description** |
| aim2/ | Main source directory for the Python package. |
| aim2/ontology/ | **Ontology Development Framework (Section 1\)** |
| manager.py | Contains the main AIM2Ontology class. |
| schema.py | Defines core ontology classes and properties. |
| importers/ | Contains modules for importing external ontologies. |
| aim2/corpus/ | **Literature Corpus Pipeline (Section 2\)** |
| builder.py | Script for searching and downloading literature. |
| parser.py | Functions for extracting text from XML and PDF files. |
| aim2/extraction/ | **LLM Information Extraction Engine (Section 3\)** |
| prompts/ | Directory for storing version-controlled prompt templates. |
| entity\_extractor.py | Module for Named Entity Recognition (NER). |
| relation\_extractor.py | Module for Relationship Extraction (RE). |
| aim2/postprocessing/ | **Post-Extraction Processing (Section 4\)** |
| mapper.py | Contains entity normalization and ontology mapping logic. |
| consolidator.py | Contains fact deduplication logic. |
| scripts/ | Top-level executable scripts that chain modules together for end-to-end workflows. |
| 1\_build\_ontology.py | Runs the full ontology development pipeline. |
| 2\_build\_corpus.py | Runs the full literature download and preprocessing pipeline. |
| 3\_run\_extraction.py | Runs the full information extraction and post-processing pipeline. |
| data/ | Directory for storing downloaded articles, source ontologies, and extracted data. |
| tests/ | Contains unit and integration tests for all modules. |

### **Recommended Python Libraries and Tooling**

**Objective:** To provide a clear, justified, and consolidated technology stack for the project, leveraging mature and well-supported open-source libraries to accelerate development and ensure robustness.

| Table 4: Recommended Python Libraries for Core Tasks |  |  |  |
| :---- | :---- | :---- | :---- |
| **Task** | **Primary Library** | **Rationale for Choice** | **Key Alternatives** |
| Ontology Management | Owlready2 | Enables the powerful "ontology-oriented programming" paradigm; provides a Pythonic interface for creating and manipulating OWL ontologies.3 | rdflib, nxontology |
| PubMed/NCBI API Access | Biopython (Bio.Entrez) | The de facto standard for interacting with NCBI E-utilities in Python; robust, well-maintained, and handles NCBI usage policies automatically.33 | entrezpy, custom requests calls |
| PubMed XML Parsing | pubmed\_parser / pubmedparser2 | Specifically designed for the structure of PubMed XMLs, greatly simplifying the extraction of structured data like abstracts and sections.38 | lxml, BeautifulSoup |
| PDF Text Extraction | PyMuPDF (fitz) | Demonstrates superior performance and accuracy for text extraction from scientific PDFs in multiple benchmarks.40 | pdfplumber, pypdf |
| Web Scraping & Automation | Selenium \+ undetected-chromedriver | Essential for handling JavaScript-heavy publisher websites and evading basic bot detection when downloading PDFs as a fallback.30 | Playwright, Scrapy |
| Text Preprocessing/Chunking | LangChain | Provides sophisticated, semantically-aware text splitters that are ideal for preparing text for LLM context windows.45 | NLTK, spaCy |
| LLM-based IE | llm-ie | A comprehensive toolkit specifically designed for NER and RE with LLMs, offering modularity, multiple backend support, and prompt engineering tools.48 | spacy-llm, custom prompting logic |
| Fact Deduplication | dedupe | A mature, machine learning-based library for fuzzy matching and entity resolution, perfectly suited for consolidating semantically redundant facts.58 | recordlinkage |

### **Strategic Recommendations for Development and Evaluation**

* **Iterative Development:** The project should be developed in a phased, iterative manner. The first phase should focus on building and validating the core ontology (Section 1). The second phase should develop the corpus acquisition and preprocessing pipeline (Section 2). Concurrently, prompt engineering and initial extraction tests can begin on a small set of documents (Section 3). The final phase will be to build the post-processing and knowledge integration pipeline (Section 4). This approach allows for early validation of each component.  
* **Gold Standard Corpus:** As specified in the project requirements, the creation of a gold standard test set of approximately 25 manually annotated papers is an essential and high-priority task. This corpus will be the bedrock for quantitatively evaluating the performance (precision, recall, F1-score) of the NER and RE modules. It will enable rigorous, data-driven comparisons between different LLMs, prompt strategies, and model parameters.  
* **Human-in-the-Loop Curation:** The system should be designed with the understanding that LLM outputs are high-quality drafts, not infallible truths. A simple script or process should be developed to present extracted facts to a human domain expert for rapid validation (e.g., accept, reject, or edit). This feedback is invaluable for identifying systematic errors in the extraction process and can be used to iteratively refine prompts or post-processing rules.  
* **Configuration-Driven Design:** To ensure flexibility and maintainability, all key parameters should be managed in external configuration files (e.g., using YAML or JSON format) rather than being hardcoded in the scripts. This includes the keyword list for literature searches, the allow-lists for ontology term trimming, the names of the LLM models to be used, paths to prompt templates, and chunking parameters. This design choice will make the entire pipeline highly configurable, reusable for different research questions, and easier to manage over the long term.

#### **Works cited**

1. RDFLib \- Wikipedia, accessed August 1, 2025, [https://en.wikipedia.org/wiki/RDFLib](https://en.wikipedia.org/wiki/RDFLib)  
2. RDFlib: Home, accessed August 1, 2025, [https://rdflib.dev/](https://rdflib.dev/)  
3. owlready2 \- conda-forge \- prefix.dev, accessed August 1, 2025, [https://prefix.dev/channels/conda-forge/packages/owlready2](https://prefix.dev/channels/conda-forge/packages/owlready2)  
4. owlready2/README.rst at master \- GitHub, accessed August 1, 2025, [https://github.com/pwin/owlready2/blob/master/README.rst](https://github.com/pwin/owlready2/blob/master/README.rst)  
5. owlready2 \- PyPI, accessed August 1, 2025, [https://pypi.org/project/owlready2/](https://pypi.org/project/owlready2/)  
6. (PDF) Owlready: Ontology-oriented programming in Python with automatic classification and high level constructs for biomedical ontologies \- ResearchGate, accessed August 1, 2025, [https://www.researchgate.net/publication/319126534\_Owlready\_Ontology-oriented\_programming\_in\_Python\_with\_automatic\_classification\_and\_high\_level\_constructs\_for\_biomedical\_ontologies](https://www.researchgate.net/publication/319126534_Owlready_Ontology-oriented_programming_in_Python_with_automatic_classification_and_high_level_constructs_for_biomedical_ontologies)  
7. Welcome to Owlready2's documentation\! — Owlready2 0.48 documentation, accessed August 1, 2025, [https://owlready2.readthedocs.io/](https://owlready2.readthedocs.io/)  
8. Managing ontologies — Owlready2 0.48 documentation, accessed August 1, 2025, [https://owlready2.readthedocs.io/en/latest/onto.html](https://owlready2.readthedocs.io/en/latest/onto.html)  
9. Introduction — Owlready2 0.48 documentation, accessed August 1, 2025, [https://owlready2.readthedocs.io/en/latest/intro.html](https://owlready2.readthedocs.io/en/latest/intro.html)  
10. Properties — Owlready2 0.48 documentation, accessed August 1, 2025, [https://owlready2.readthedocs.io/en/latest/properties.html](https://owlready2.readthedocs.io/en/latest/properties.html)  
11. Example — The flowers of evidence, accessed August 1, 2025, [http://www.lesfleursdunormal.fr/static/informatique/owlready/example\_en.html](http://www.lesfleursdunormal.fr/static/informatique/owlready/example_en.html)  
12. Managing ontologies — Owlready 0.2 documentation \- Pythonhosted.org, accessed August 1, 2025, [https://pythonhosted.org/Owlready/onto.html](https://pythonhosted.org/Owlready/onto.html)  
13. Downloads \- Natural Products Atlas, accessed August 1, 2025, [https://www.npatlas.org/download](https://www.npatlas.org/download)  
14. NBDC00914 \- Integbio Database Catalog, accessed August 1, 2025, [https://catalog.integbio.jp/dbcatalog/en/record/nbdc00914](https://catalog.integbio.jp/dbcatalog/en/record/nbdc00914)  
15. Submitting Data to PMN | Plant Metabolic Network, accessed August 1, 2025, [https://plantcyc.org/tutorials/submitting-data-tutorial](https://plantcyc.org/tutorials/submitting-data-tutorial)  
16. Plant ontology \- Wikipedia, accessed August 1, 2025, [https://en.wikipedia.org/wiki/Plant\_ontology](https://en.wikipedia.org/wiki/Plant_ontology)  
17. Plant Ontology \- OBO Foundry, accessed August 1, 2025, [http://obofoundry.org/ontology/po.html](http://obofoundry.org/ontology/po.html)  
18. NCBI Taxonomy \- Re3data.org, accessed August 1, 2025, [https://www.re3data.org/repository/r3d100010415](https://www.re3data.org/repository/r3d100010415)  
19. NCBI Taxonomy: a comprehensive update on curation, resources and tools | Database | Oxford Academic, accessed August 1, 2025, [https://academic.oup.com/database/article/doi/10.1093/database/baaa062/5881509](https://academic.oup.com/database/article/doi/10.1093/database/baaa062/5881509)  
20. APIs \- Develop \- NCBI, accessed August 1, 2025, [https://www.ncbi.nlm.nih.gov/home/develop/api/](https://www.ncbi.nlm.nih.gov/home/develop/api/)  
21. Bio.Entrez package — Biopython 1.76 documentation, accessed August 1, 2025, [https://biopython.org/docs/1.76/api/Bio.Entrez.html](https://biopython.org/docs/1.76/api/Bio.Entrez.html)  
22. logo Plant Experimental Conditions Ontology \- OBO Foundry, accessed August 1, 2025, [http://obofoundry.org/ontology/peco.html](http://obofoundry.org/ontology/peco.html)  
23. en.wikipedia.org, accessed August 1, 2025, [https://en.wikipedia.org/wiki/Gene\_Ontology](https://en.wikipedia.org/wiki/Gene_Ontology)  
24. Download ontology \- Gene Ontology, accessed August 1, 2025, [http://geneontology.org/docs/download-ontology/](http://geneontology.org/docs/download-ontology/)  
25. Plant Trait Ontology \- OBO Foundry, accessed August 1, 2025, [http://obofoundry.org/ontology/to.html](http://obofoundry.org/ontology/to.html)  
26. (PDF) ChemFOnt: the chemical functional ontology resource \- ResearchGate, accessed August 1, 2025, [https://www.researchgate.net/publication/364845548\_ChemFOnt\_the\_chemical\_functional\_ontology\_resource](https://www.researchgate.net/publication/364845548_ChemFOnt_the_chemical_functional_ontology_resource)  
27. ChemFOnt: the chemical functional ontology resource \- PubMed, accessed August 1, 2025, [https://pubmed.ncbi.nlm.nih.gov/36305829/](https://pubmed.ncbi.nlm.nih.gov/36305829/)  
28. ChemFOnt, accessed August 1, 2025, [https://chemfont.ca/](https://chemfont.ca/)  
29. 7 Best Python Web Scraping Libraries in 2025 \- ZenRows, accessed August 1, 2025, [https://www.zenrows.com/blog/python-web-scraping-library](https://www.zenrows.com/blog/python-web-scraping-library)  
30. How to Avoid Bot Detection With Selenium \- ZenRows, accessed August 1, 2025, [https://www.zenrows.com/blog/selenium-avoid-bot-detection](https://www.zenrows.com/blog/selenium-avoid-bot-detection)  
31. How To Make Selenium Undetectable \- ScrapeOps, accessed August 1, 2025, [https://scrapeops.io/selenium-web-scraping-playbook/python-selenium-make-selenium-undetectable/](https://scrapeops.io/selenium-web-scraping-playbook/python-selenium-make-selenium-undetectable/)  
32. Accessing NCBI's Entrez databases — test test documentation \- Biopython, accessed August 1, 2025, [https://biopython-tutorial.readthedocs.io/en/latest/notebooks/09%20-%20Accessing%20NCBIs%20Entrez%20databases.html](https://biopython-tutorial.readthedocs.io/en/latest/notebooks/09%20-%20Accessing%20NCBIs%20Entrez%20databases.html)  
33. Accessing NCBI's Entrez databases — Biopython 1.85 documentation, accessed August 1, 2025, [https://biopython.org/docs/latest/Tutorial/chapter\_entrez.html](https://biopython.org/docs/latest/Tutorial/chapter_entrez.html)  
34. Searching PubMed with Python \- Marco Bonzanini, accessed August 1, 2025, [https://marcobonzanini.com/2015/01/12/searching-pubmed-with-python/](https://marcobonzanini.com/2015/01/12/searching-pubmed-with-python/)  
35. Python Selenium: Bot Detection Prevention Techniques | by Abdul Wajid | Medium, accessed August 1, 2025, [https://medium.com/@abdul45.wajid/python-selenium-bot-detection-prevention-techniques-a387cbca7562](https://medium.com/@abdul45.wajid/python-selenium-bot-detection-prevention-techniques-a387cbca7562)  
36. how to avoid bot detection on websites using selenium python \- Stack Overflow, accessed August 1, 2025, [https://stackoverflow.com/questions/72406597/how-to-avoid-bot-detection-on-websites-using-selenium-python](https://stackoverflow.com/questions/72406597/how-to-avoid-bot-detection-on-websites-using-selenium-python)  
37. A Python Parser for PubMed Open-Access XML Subset and MEDLINE XML Dataset \- titipat achakulvisut, accessed August 1, 2025, [https://titipata.github.io/pubmed\_parser/](https://titipata.github.io/pubmed_parser/)  
38. pubmedparser2·PyPI, accessed August 1, 2025, [https://pypi.org/project/pubmedparser2/](https://pypi.org/project/pubmedparser2/)  
39. API Documentation — Pubmed Parser 0.5.2.dev12+g1559018 documentation, accessed August 1, 2025, [https://titipata.github.io/pubmed\_parser/api.html](https://titipata.github.io/pubmed_parser/api.html)  
40. A Guide to PDF Extraction Libraries in Python \- Metric Coders, accessed August 1, 2025, [https://www.metriccoders.com/post/a-guide-to-pdf-extraction-libraries-in-python](https://www.metriccoders.com/post/a-guide-to-pdf-extraction-libraries-in-python)  
41. Extract text from PDF File using Python \- GeeksforGeeks, accessed August 1, 2025, [https://www.geeksforgeeks.org/python/extract-text-from-pdf-file-using-python/](https://www.geeksforgeeks.org/python/extract-text-from-pdf-file-using-python/)  
42. Appendix 4: Performance Comparison Methodology \- PyMuPDF 1.26.3 documentation, accessed August 1, 2025, [https://pymupdf.readthedocs.io/en/latest/app4.html](https://pymupdf.readthedocs.io/en/latest/app4.html)  
43. Which is faster at extracting text from a PDF: PyMuPDF or PyPDF2? : r/learnpython \- Reddit, accessed August 1, 2025, [https://www.reddit.com/r/learnpython/comments/11ltkqz/which\_is\_faster\_at\_extracting\_text\_from\_a\_pdf/](https://www.reddit.com/r/learnpython/comments/11ltkqz/which_is_faster_at_extracting_text_from_a_pdf/)  
44. Removing Special Characters and Normalizing Text Using Python | CodeSignal Learn, accessed August 1, 2025, [https://codesignal.com/learn/courses/advanced-data-cleaning-handling-text-data-1/lessons/removing-special-characters-and-normalizing-text-using-python](https://codesignal.com/learn/courses/advanced-data-cleaning-handling-text-data-1/lessons/removing-special-characters-and-normalizing-text-using-python)  
45. Chunking Strategies for LLM Applications \- Pinecone, accessed August 1, 2025, [https://www.pinecone.io/learn/chunking-strategies/](https://www.pinecone.io/learn/chunking-strategies/)  
46. LLM with Relation Classifier for Document-Level Relation Extraction \- arXiv, accessed August 1, 2025, [https://arxiv.org/html/2408.13889v1](https://arxiv.org/html/2408.13889v1)  
47. A survey on cutting-edge relation extraction techniques based on language models \- arXiv, accessed August 1, 2025, [https://arxiv.org/html/2411.18157v1](https://arxiv.org/html/2411.18157v1)  
48. daviden1013/llm-ie: A comprehensive toolkit that provides ... \- GitHub, accessed August 1, 2025, [https://github.com/daviden1013/llm-ie](https://github.com/daviden1013/llm-ie)  
49. LLM-IE: a python package for biomedical generative information extraction with large language models \- Oxford Academic, accessed August 1, 2025, [https://academic.oup.com/jamiaopen/article-pdf/8/2/ooaf012/62387276/ooaf012.pdf](https://academic.oup.com/jamiaopen/article-pdf/8/2/ooaf012/62387276/ooaf012.pdf)  
50. LLM-IE: a python package for biomedical generative information extraction with large language models \- PMC, accessed August 1, 2025, [https://pmc.ncbi.nlm.nih.gov/articles/PMC11901043/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11901043/)  
51. spaCy · Industrial-strength Natural Language Processing in Python, accessed August 1, 2025, [https://spacy.io/](https://spacy.io/)  
52. Large Language Models · spaCy Usage Documentation, accessed August 1, 2025, [https://spacy.io/usage/large-language-models](https://spacy.io/usage/large-language-models)  
53. Prompting large language models to extract chemical‒disease relation precisely and comprehensively at the document level: an evaluation study \- PMC \- PubMed Central, accessed August 1, 2025, [https://pmc.ncbi.nlm.nih.gov/articles/PMC11978106/](https://pmc.ncbi.nlm.nih.gov/articles/PMC11978106/)  
54. Relation Extraction Prompts \- LLM Prompt Engineering Simplified \- LLMNanban, accessed August 1, 2025, [https://llmnanban.akmmusai.pro/Prompt-Gallery/Relation-Extraction-Prompts/](https://llmnanban.akmmusai.pro/Prompt-Gallery/Relation-Extraction-Prompts/)  
55. Relation Extraction with Fine-Tuned Large Language Models in Retrieval Augmented Generation Frameworks \- arXiv, accessed August 1, 2025, [https://arxiv.org/html/2406.14745v2](https://arxiv.org/html/2406.14745v2)  
56. HunFlair2 in a cross-corpus evaluation of biomedical named entity recognition and normalization tools | Bioinformatics | Oxford Academic, accessed August 1, 2025, [https://academic.oup.com/bioinformatics/article/40/10/btae564/7762634](https://academic.oup.com/bioinformatics/article/40/10/btae564/7762634)  
57. Gilda: biomedical entity text normalization with machine-learned disambiguation as a service | Bioinformatics Advances | Oxford Academic, accessed August 1, 2025, [https://academic.oup.com/bioinformaticsadvances/article/2/1/vbac034/6584365](https://academic.oup.com/bioinformaticsadvances/article/2/1/vbac034/6584365)  
58. dedupe \- PyPI, accessed August 1, 2025, [https://pypi.org/project/dedupe/](https://pypi.org/project/dedupe/)  
59. dedupeio/dedupe: :id: A python library for accurate and scalable fuzzy matching, record deduplication and entity-resolution. \- GitHub, accessed August 1, 2025, [https://github.com/dedupeio/dedupe](https://github.com/dedupeio/dedupe)  
60. Collecting and managing taxonomic data with NCBI-taxonomist \- PMC \- PubMed Central, accessed August 1, 2025, [https://pmc.ncbi.nlm.nih.gov/articles/PMC8016462/](https://pmc.ncbi.nlm.nih.gov/articles/PMC8016462/)  
61. Use Python dedupe library to return all matches against messy dataset \- Stack Overflow, accessed August 1, 2025, [https://stackoverflow.com/questions/47342980/use-python-dedupe-library-to-return-all-matches-against-messy-dataset](https://stackoverflow.com/questions/47342980/use-python-dedupe-library-to-return-all-matches-against-messy-dataset)  
62. dedupeio/dedupe-examples: :id: Examples for using the ... \- GitHub, accessed August 1, 2025, [https://github.com/dedupeio/dedupe-examples](https://github.com/dedupeio/dedupe-examples)  
63. Pubmed Parser \- Anaconda.org, accessed August 1, 2025, [https://anaconda.org/conda-forge/pubmed-parser](https://anaconda.org/conda-forge/pubmed-parser)