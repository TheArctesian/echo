import os
import re
import yaml
from typing import Dict, Any, List
from langchain.schema import Document
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_obsidian_metadata(file_path: str) -> Dict[str, Any]:
    """Extract YAML frontmatter from Obsidian notes"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        
    # Look for YAML frontmatter between --- markers
    frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    
    metadata = {}
    if frontmatter_match:
        yaml_content = frontmatter_match.group(1)
        try:
            metadata = yaml.safe_load(yaml_content)
        except yaml.YAMLError:
            pass
            
    # Add filename and path to metadata
    metadata['source'] = file_path
    metadata['filename'] = os.path.basename(file_path)
    
    return metadata

def load_obsidian_docs(vault_path: str) -> List[Document]:
    """Load documents from Obsidian vault with metadata"""
    loader = DirectoryLoader(
        vault_path, 
        glob="**/*.md",
        show_progress=True
    )
    documents = loader.load()
    
    # Enhance documents with Obsidian-specific metadata
    enhanced_docs = []
    for doc in documents:
        metadata = extract_obsidian_metadata(doc.metadata['source'])
        doc.metadata.update(metadata)
        enhanced_docs.append(doc)
    
    return enhanced_docs

def split_docs(documents: List[Document]) -> List[Document]:
    """Split documents into chunks for embedding"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n## ", "\n### ", "\n#### ", "\n", " ", ""]
    )
    return text_splitter.split_documents(documents)