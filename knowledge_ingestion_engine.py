#!/usr/bin/env python3
"""
Knowledge Ingestion Engine - Phase 2 of Memory Context Manager v2
Processes documentation, code comments, and builds semantic knowledge graphs
"""

import os
import re
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

@dataclass
class DocumentContext:
    """Context extracted from a document"""
    path: str
    title: str
    content: str
    content_type: str  # 'readme', 'api_doc', 'code_comment', 'config'
    extracted_concepts: List[str]
    relationships: List[Dict[str, str]]
    metadata: Dict[str, Any]
    processing_time: float

@dataclass
class KnowledgeNode:
    """A node in the knowledge graph"""
    id: str
    type: str  # 'concept', 'file', 'function', 'class', 'pattern'
    name: str
    description: str
    source: str
    confidence: float
    metadata: Dict[str, Any]
    created_at: float
    updated_at: float

@dataclass
class KnowledgeRelationship:
    """A relationship between knowledge nodes"""
    id: str
    source_id: str
    target_id: str
    relationship_type: str  # 'implements', 'depends_on', 'similar_to', 'references'
    strength: float
    metadata: Dict[str, Any]
    created_at: float

@dataclass
class KnowledgeGraph:
    """Complete knowledge graph structure"""
    nodes: Dict[str, KnowledgeNode]
    relationships: Dict[str, KnowledgeRelationship]
    concepts: Dict[str, List[str]]
    patterns: Dict[str, Any]
    metadata: Dict[str, Any]
    created_at: float
    updated_at: float

class DocumentationProcessor:
    """Processes various types of documentation and extracts knowledge"""
    
    def __init__(self):
        self.parsers = {
            'readme': self._parse_readme,
            'markdown': self._parse_markdown,
            'python_docstring': self._parse_python_docstring,
            'javascript_jsdoc': self._parse_javascript_jsdoc,
            'api_spec': self._parse_api_spec,
            'config_file': self._parse_config_file
        }
        
        # Concept extraction patterns
        self.concept_patterns = {
            'python': {
                'function': r'def\s+(\w+)\s*\([^)]*\)\s*:',
                'class': r'class\s+(\w+)',
                'import': r'(?:from|import)\s+(\w+)',
                'variable': r'(\w+)\s*=',
                'decorator': r'@(\w+)',
                'docstring': r'"""(.*?)"""',
                'comment': r'#\s*(.+)'
            },
            'javascript': {
                'function': r'(?:function\s+)?(\w+)\s*\([^)]*\)\s*{',
                'class': r'class\s+(\w+)',
                'import': r'(?:import|from)\s+(\w+)',
                'variable': r'(?:const|let|var)\s+(\w+)',
                'method': r'(\w+)\s*\([^)]*\)\s*{',
                'comment': r'//\s*(.+)|/\*([^*]+)\*/'
            },
            'markdown': {
                'heading': r'^#{1,6}\s+(.+)$',
                'link': r'\[([^\]]+)\]\(([^)]+)\)',
                'code_block': r'```(\w+)?\n(.*?)```',
                'inline_code': r'`([^`]+)`',
                'list_item': r'^[-*+]\s+(.+)$'
            }
        }
        
        # Relationship patterns
        self.relationship_patterns = {
            'implements': r'implements|implements|realizes',
            'depends_on': r'depends? on|requires|needs|uses',
            'similar_to': r'similar to|like|same as|equivalent to',
            'references': r'references?|see|check|look at',
            'extends': r'extends|inherits from|subclass of',
            'composes': r'contains|has|includes|consists of'
        }
    
    def process_document(self, doc_path: str, content: str = None) -> DocumentContext:
        """Process a document and extract knowledge"""
        start_time = time.time()
        
        try:
            file_path = Path(doc_path)
            file_type = self._detect_document_type(file_path)
            
            # Read content if not provided
            if content is None:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            
            # Parse based on document type
            if file_type in self.parsers:
                parser_result = self.parsers[file_type](content, file_path)
            else:
                parser_result = self._parse_generic(content, file_path)
            
            # Extract concepts
            concepts = self._extract_concepts(content, file_path)
            
            # Extract relationships
            relationships = self._extract_relationships(content, concepts)
            
            # Build metadata
            metadata = {
                'file_size': len(content),
                'lines': len(content.split('\n')),
                'language': self._detect_language(file_path),
                'last_modified': file_path.stat().st_mtime if file_path.exists() else None
            }
            
            processing_time = time.time() - start_time
            
            return DocumentContext(
                path=str(doc_path),
                title=parser_result.get('title', file_path.name),
                content=content,
                content_type=file_type,
                extracted_concepts=concepts,
                relationships=relationships,
                metadata=metadata,
                processing_time=processing_time
            )
            
        except Exception as e:
            logger.error(f"Failed to process document {doc_path}: {str(e)}")
            return DocumentContext(
                path=str(doc_path),
                title="Error",
                content="",
                content_type="error",
                extracted_concepts=[],
                relationships=[],
                metadata={'error': str(e)},
                processing_time=time.time() - start_time
            )
    
    def _detect_document_type(self, file_path: Path) -> str:
        """Detect the type of document for appropriate parsing"""
        name = file_path.name.lower()
        suffix = file_path.suffix.lower()
        
        if name in ['readme', 'readme.md', 'readme.txt']:
            return 'readme'
        elif suffix == '.md':
            return 'markdown'
        elif suffix == '.py':
            return 'python_docstring'
        elif suffix in ['.js', '.jsx', '.ts', '.tsx']:
            return 'javascript_jsdoc'
        elif suffix in ['.json', '.yaml', '.yml']:
            return 'api_spec'
        elif suffix in ['.toml', '.ini', '.cfg']:
            return 'config_file'
        else:
            return 'generic'
    
    def _detect_language(self, file_path: Path) -> str:
        """Detect the programming language of a file"""
        suffix = file_path.suffix.lower()
        
        language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.go': 'go',
            '.rs': 'rust',
            '.php': 'php',
            '.rb': 'ruby'
        }
        
        return language_map.get(suffix, 'unknown')
    
    def _parse_readme(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Parse README files for project information"""
        result = {
            'title': file_path.stem.title(),
            'description': '',
            'installation': '',
            'usage': '',
            'features': [],
            'dependencies': []
        }
        
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            # Detect sections
            if line.startswith('#'):
                current_section = line.lower().replace('#', '').strip()
                if 'description' in current_section or 'overview' in current_section:
                    current_section = 'description'
                elif 'install' in current_section:
                    current_section = 'installation'
                elif 'usage' in current_section or 'example' in current_section:
                    current_section = 'usage'
                elif 'feature' in current_section:
                    current_section = 'features'
                elif 'depend' in current_section or 'requirement' in current_section:
                    current_section = 'dependencies'
            
            # Extract content based on section
            elif current_section == 'description' and line:
                result['description'] += line + ' '
            elif current_section == 'installation' and line:
                result['installation'] += line + ' '
            elif current_section == 'usage' and line:
                result['usage'] += line + ' '
            elif current_section == 'features' and line.startswith('-'):
                result['features'].append(line[1:].strip())
            elif current_section == 'dependencies' and line.startswith('-'):
                result['dependencies'].append(line[1:].strip())
        
        # Clean up descriptions
        result['description'] = result['description'].strip()
        result['installation'] = result['installation'].strip()
        result['usage'] = result['usage'].strip()
        
        return result
    
    def _parse_markdown(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Parse general markdown files"""
        result = {
            'title': file_path.stem.title(),
            'headings': [],
            'links': [],
            'code_blocks': []
        }
        
        # Extract headings
        heading_matches = re.findall(r'^#{1,6}\s+(.+)$', content, re.MULTILINE)
        result['headings'] = [h.strip() for h in heading_matches]
        
        # Extract links
        link_matches = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        result['links'] = [{'text': text, 'url': url} for text, url in link_matches]
        
        # Extract code blocks
        code_matches = re.findall(r'```(\w+)?\n(.*?)```', content, re.DOTALL)
        result['code_blocks'] = [{'language': lang or 'text', 'code': code.strip()} for lang, code in code_matches]
        
        return result
    
    def _parse_python_docstring(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Parse Python files for docstrings and function/class definitions"""
        result = {
            'title': file_path.stem.title(),
            'functions': [],
            'classes': [],
            'docstrings': [],
            'imports': []
        }
        
        # Extract function definitions
        func_matches = re.findall(r'def\s+(\w+)\s*\([^)]*\)\s*:', content)
        for func_name in func_matches:
            result['functions'].append(func_name)
        
        # Extract class definitions
        class_matches = re.findall(r'class\s+(\w+)', content)
        for class_name in class_matches:
            result['classes'].append(class_name)
        
        # Extract docstrings
        docstring_matches = re.findall(r'"""(.*?)"""', content, re.DOTALL)
        result['docstrings'] = [ds.strip() for ds in docstring_matches]
        
        # Extract imports
        import_matches = re.findall(r'(?:from|import)\s+(\w+)', content)
        result['imports'] = list(set(import_matches))
        
        return result
    
    def _parse_javascript_jsdoc(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Parse JavaScript files for JSDoc comments and function definitions"""
        result = {
            'title': file_path.stem.title(),
            'functions': [],
            'classes': [],
            'jsdoc_comments': [],
            'imports': []
        }
        
        # Extract function definitions
        func_matches = re.findall(r'(?:function\s+)?(\w+)\s*\([^)]*\)\s*{', content)
        for func_name in func_matches:
            result['functions'].append(func_name)
        
        # Extract class definitions
        class_matches = re.findall(r'class\s+(\w+)', content)
        for class_name in class_matches:
            result['classes'].append(class_name)
        
        # Extract JSDoc comments
        jsdoc_matches = re.findall(r'/\*\*([^*]+)\*/', content, re.DOTALL)
        result['jsdoc_comments'] = [comment.strip() for comment in jsdoc_matches]
        
        # Extract imports
        import_matches = re.findall(r'(?:import|from)\s+(\w+)', content)
        result['imports'] = list(set(import_matches))
        
        return result
    
    def _parse_api_spec(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Parse API specification files (OpenAPI, etc.)"""
        result = {
            'title': file_path.stem.title(),
            'endpoints': [],
            'models': [],
            'schemas': []
        }
        
        try:
            if file_path.suffix == '.json':
                data = json.loads(content)
                
                # OpenAPI/Swagger format
                if 'openapi' in data or 'swagger' in data:
                    if 'paths' in data:
                        result['endpoints'] = list(data['paths'].keys())
                    if 'components' in data and 'schemas' in data['components']:
                        result['schemas'] = list(data['components']['schemas'].keys())
                    if 'definitions' in data:
                        result['schemas'] = list(data['definitions'].keys())
                
                # Generic JSON structure
                else:
                    result['schemas'] = list(data.keys())
            
            elif file_path.suffix in ['.yaml', '.yml']:
                # Basic YAML parsing (can be enhanced with PyYAML)
                lines = content.split('\n')
                for line in lines:
                    if ':' in line and not line.strip().startswith('#'):
                        key = line.split(':')[0].strip()
                        if key and not key.startswith('-'):
                            result['schemas'].append(key)
        
        except Exception as e:
            logger.warning(f"Failed to parse API spec {file_path}: {str(e)}")
        
        return result
    
    def _parse_config_file(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Parse configuration files"""
        result = {
            'title': file_path.stem.title(),
            'sections': [],
            'keys': [],
            'values': []
        }
        
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    result['keys'].append(key.strip())
                    result['values'].append(value.strip())
                elif ':' in line:
                    key, value = line.split(':', 1)
                    result['keys'].append(key.strip())
                    result['values'].append(value.strip())
                elif line.startswith('[') and line.endswith(']'):
                    section = line[1:-1]
                    result['sections'].append(section)
        
        return result
    
    def _parse_generic(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Parse generic files with basic text analysis"""
        result = {
            'title': file_path.stem.title(),
            'word_count': len(content.split()),
            'line_count': len(content.split('\n')),
            'char_count': len(content)
        }
        
        return result
    
    def _extract_concepts(self, content: str, file_path: Path) -> List[str]:
        """Extract concepts from document content"""
        concepts = set()
        
        # Detect language for appropriate pattern matching
        language = self._detect_language(file_path)
        
        if language in self.concept_patterns:
            patterns = self.concept_patterns[language]
            
            for concept_type, pattern in patterns.items():
                matches = re.findall(pattern, content, re.MULTILINE | re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        concepts.update([m.strip() for m in match if m.strip()])
                    else:
                        concepts.add(match.strip())
        
        # Add markdown concepts for all files
        markdown_patterns = self.concept_patterns['markdown']
        for concept_type, pattern in markdown_patterns.items():
            matches = re.findall(pattern, content, re.MULTILINE | re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    concepts.update([m.strip() for m in match if m.strip()])
                else:
                    concepts.add(match.strip())
        
        # Filter out common words and short concepts
        filtered_concepts = []
        for concept in concepts:
            if len(concept) > 2 and not concept.lower() in ['the', 'and', 'or', 'for', 'in', 'on', 'at', 'to', 'of', 'a', 'an']:
                filtered_concepts.append(concept)
        
        return filtered_concepts
    
    def _extract_relationships(self, content: str, concepts: List[str]) -> List[Dict[str, str]]:
        """Extract relationships between concepts"""
        relationships = []
        
        for rel_type, pattern in self.relationship_patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                # Find concepts that might be related
                for concept in concepts:
                    if concept.lower() in match.lower():
                        relationships.append({
                            'type': rel_type,
                            'source': concept,
                            'target': 'context',
                            'context': match
                        })
        
        return relationships

class KnowledgeGraphBuilder:
    """Builds and maintains the knowledge graph"""
    
    def __init__(self):
        self.nodes: Dict[str, KnowledgeNode] = {}
        self.relationships: Dict[str, KnowledgeRelationship] = {}
        self.concepts: Dict[str, List[str]] = defaultdict(list)
        self.patterns: Dict[str, Any] = {}
        self.node_counter = 0
        self.relationship_counter = 0
    
    def add_document_context(self, doc_context: DocumentContext) -> List[str]:
        """Add document context to the knowledge graph"""
        added_nodes = []
        
        # Create document node
        doc_node_id = f"doc_{self.node_counter}"
        self.node_counter += 1
        
        doc_node = KnowledgeNode(
            id=doc_node_id,
            type='document',
            name=doc_context.title,
            description=f"Document: {doc_context.path}",
            source=doc_context.path,
            confidence=0.9,
            metadata=doc_context.metadata,
            created_at=time.time(),
            updated_at=time.time()
        )
        
        self.nodes[doc_node_id] = doc_node
        added_nodes.append(doc_node_id)
        
        # Add concept nodes
        for concept in doc_context.extracted_concepts:
            concept_node_id = self._get_or_create_concept_node(concept, doc_context.path)
            if concept_node_id not in added_nodes:
                added_nodes.append(concept_node_id)
            
            # Create relationship between document and concept
            self._create_relationship(doc_node_id, concept_node_id, 'contains', 0.8)
        
        # Add relationship nodes
        for rel in doc_context.relationships:
            if rel['source'] in doc_context.extracted_concepts:
                source_id = self._get_concept_node_id(rel['source'])
                if source_id:
                    self._create_relationship(source_id, doc_node_id, rel['type'], 0.7)
        
        return added_nodes
    
    def _get_or_create_concept_node(self, concept: str, source: str) -> str:
        """Get existing concept node or create new one"""
        # Check if concept already exists
        for node_id, node in self.nodes.items():
            if node.type == 'concept' and node.name.lower() == concept.lower():
                # Update metadata
                node.updated_at = time.time()
                if source not in node.metadata.get('sources', []):
                    if 'sources' not in node.metadata:
                        node.metadata['sources'] = []
                    node.metadata['sources'].append(source)
                return node_id
        
        # Create new concept node
        concept_node_id = f"concept_{self.node_counter}"
        self.node_counter += 1
        
        concept_node = KnowledgeNode(
            id=concept_node_id,
            type='concept',
            name=concept,
            description=f"Concept: {concept}",
            source=source,
            confidence=0.8,
            metadata={'sources': [source]},
            created_at=time.time(),
            updated_at=time.time()
        )
        
        self.nodes[concept_node_id] = concept_node
        return concept_node_id
    
    def _get_concept_node_id(self, concept: str) -> Optional[str]:
        """Get the ID of an existing concept node"""
        for node_id, node in self.nodes.items():
            if node.type == 'concept' and node.name.lower() == concept.lower():
                return node_id
        return None
    
    def _create_relationship(self, source_id: str, target_id: str, rel_type: str, strength: float) -> str:
        """Create a relationship between two nodes"""
        rel_id = f"rel_{self.relationship_counter}"
        self.relationship_counter += 1
        
        relationship = KnowledgeRelationship(
            id=rel_id,
            source_id=source_id,
            target_id=target_id,
            relationship_type=rel_type,
            strength=strength,
            metadata={},
            created_at=time.time()
        )
        
        self.relationships[rel_id] = relationship
        return rel_id
    
    def build_knowledge_graph(self) -> KnowledgeGraph:
        """Build the complete knowledge graph"""
        # Analyze patterns
        self._analyze_patterns()
        
        # Build concept clusters
        self._build_concept_clusters()
        
        return KnowledgeGraph(
            nodes=self.nodes.copy(),
            relationships=self.relationships.copy(),
            concepts=dict(self.concepts),
            patterns=self.patterns.copy(),
            metadata={
                'total_nodes': len(self.nodes),
                'total_relationships': len(self.relationships),
                'total_concepts': len([n for n in self.nodes.values() if n.type == 'concept']),
                'created_at': time.time(),
                'updated_at': time.time()
            },
            created_at=time.time(),
            updated_at=time.time()
        )
    
    def _analyze_patterns(self):
        """Analyze patterns in the knowledge graph"""
        # Concept frequency analysis
        concept_counts = defaultdict(int)
        for node in self.nodes.values():
            if node.type == 'concept':
                concept_counts[node.name] += 1
        
        # Relationship type analysis
        rel_type_counts = defaultdict(int)
        for rel in self.relationships.values():
            rel_type_counts[rel.relationship_type] += 1
        
        # Source analysis
        source_counts = defaultdict(int)
        for node in self.nodes.values():
            source_counts[node.source] += 1
        
        self.patterns = {
            'concept_frequency': dict(concept_counts),
            'relationship_types': dict(rel_type_counts),
            'source_distribution': dict(source_counts),
            'node_types': self._count_node_types(),
            'connectivity': self._analyze_connectivity()
        }
    
    def _count_node_types(self) -> Dict[str, int]:
        """Count nodes by type"""
        type_counts = defaultdict(int)
        for node in self.nodes.values():
            type_counts[node.type] += 1
        return dict(type_counts)
    
    def _analyze_connectivity(self) -> Dict[str, Any]:
        """Analyze graph connectivity"""
        # Count connections per node
        connections = defaultdict(int)
        for rel in self.relationships.values():
            connections[rel.source_id] += 1
            connections[rel.target_id] += 1
        
        if connections:
            avg_connections = sum(connections.values()) / len(connections)
            max_connections = max(connections.values())
            min_connections = min(connections.values())
        else:
            avg_connections = max_connections = min_connections = 0
        
        return {
            'average_connections': avg_connections,
            'max_connections': max_connections,
            'min_connections': min_connections,
            'total_connections': len(self.relationships)
        }
    
    def _build_concept_clusters(self):
        """Build concept clusters based on relationships"""
        # Group concepts by source
        for node in self.nodes.values():
            if node.type == 'concept':
                source = node.metadata.get('sources', ['unknown'])[0]
                self.concepts[source].append(node.name)
    
    def export_graph(self, format: str = 'json') -> str:
        """Export the knowledge graph in various formats"""
        graph = self.build_knowledge_graph()
        
        if format == 'json':
            return json.dumps(asdict(graph), indent=2, default=str)
        elif format == 'summary':
            return self._generate_summary(graph)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _generate_summary(self, graph: KnowledgeGraph) -> str:
        """Generate a human-readable summary of the knowledge graph"""
        summary = f"""
# Knowledge Graph Summary

## 📊 Graph Statistics
- **Total Nodes**: {graph.metadata['total_nodes']}
- **Total Relationships**: {graph.metadata['total_relationships']}
- **Total Concepts**: {graph.metadata['total_concepts']}
- **Created**: {datetime.fromtimestamp(graph.created_at).strftime('%Y-%m-%d %H:%M:%S')}

## 🧠 Node Types
"""
        
        for node_type, count in graph.patterns.get('node_types', {}).items():
            summary += f"- **{node_type}**: {count}\n"
        
        summary += f"""
## 🔗 Relationship Types
"""
        
        for rel_type, count in graph.patterns.get('relationship_types', {}).items():
            summary += f"- **{rel_type}**: {count}\n"
        
        summary += f"""
## 📚 Top Concepts
"""
        
        concept_freq = graph.patterns.get('concept_frequency', {})
        top_concepts = sorted(concept_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        
        for concept, count in top_concepts:
            summary += f"- **{concept}**: {count} occurrences\n"
        
        summary += f"""
## 🔌 Connectivity
- **Average Connections**: {graph.patterns.get('connectivity', {}).get('average_connections', 0):.2f}
- **Max Connections**: {graph.patterns.get('connectivity', {}).get('max_connections', 0)}
- **Total Connections**: {graph.patterns.get('connectivity', {}).get('total_connections', 0)}
"""
        
        return summary

class KnowledgeIngestionEngine:
    """Main engine for knowledge ingestion and processing"""
    
    def __init__(self):
        self.doc_processor = DocumentationProcessor()
        self.graph_builder = KnowledgeGraphBuilder()
        self.processed_docs: List[DocumentContext] = []
        self.knowledge_graph: Optional[KnowledgeGraph] = None
    
    def ingest_project_documentation(self, project_root: str) -> KnowledgeGraph:
        """Ingest all documentation from a project"""
        logger.info(f"🔍 Starting knowledge ingestion for project: {project_root}")
        
        project_path = Path(project_root)
        
        # Find documentation files
        doc_files = self._find_documentation_files(project_path)
        logger.info(f"📚 Found {len(doc_files)} documentation files")
        
        # Process each document
        for doc_file in doc_files:
            try:
                logger.info(f"📖 Processing: {doc_file}")
                doc_context = self.doc_processor.process_document(str(doc_file))
                self.processed_docs.append(doc_context)
                
                # Add to knowledge graph
                added_nodes = self.graph_builder.add_document_context(doc_context)
                logger.info(f"✅ Added {len(added_nodes)} nodes from {doc_file.name}")
                
            except Exception as e:
                logger.error(f"❌ Failed to process {doc_file}: {str(e)}")
        
        # Build final knowledge graph
        logger.info("🏗️ Building knowledge graph...")
        self.knowledge_graph = self.graph_builder.build_knowledge_graph()
        
        logger.info(f"🎉 Knowledge ingestion complete!")
        logger.info(f"📊 Total nodes: {len(self.knowledge_graph.nodes)}")
        logger.info(f"🔗 Total relationships: {len(self.knowledge_graph.relationships)}")
        
        return self.knowledge_graph
    
    def _find_documentation_files(self, project_path: Path) -> List[Path]:
        """Find documentation files in the project"""
        doc_files = []
        
        # Common documentation file patterns
        doc_patterns = [
            'README*', '*.md', '*.rst', '*.txt',
            'docs/**/*', 'documentation/**/*',
            '*.py', '*.js', '*.jsx', '*.ts', '*.tsx',  # Source files with comments
            '*.json', '*.yaml', '*.yml', '*.toml'  # Config files
        ]
        
        for pattern in doc_patterns:
            if '**' in pattern:
                # Recursive pattern
                base_pattern = pattern.replace('/**/*', '')
                for file_path in project_path.rglob(base_pattern):
                    if self._is_documentation_file(file_path):
                        doc_files.append(file_path)
            else:
                # Simple pattern
                for file_path in project_path.glob(pattern):
                    if self._is_documentation_file(file_path):
                        doc_files.append(file_path)
        
        # Remove duplicates and sort
        doc_files = list(set(doc_files))
        doc_files.sort()
        
        return doc_files
    
    def _is_documentation_file(self, file_path: Path) -> bool:
        """Check if a file is a documentation file"""
        # Skip common non-documentation files
        skip_patterns = [
            'node_modules', '.git', '__pycache__', '.pytest_cache',
            'build', 'dist', 'target', 'out', 'bin', 'obj',
            '.venv', 'venv', 'env', '.env'
        ]
        
        for pattern in skip_patterns:
            if pattern in str(file_path):
                return False
        
        # Must be a file, not directory
        if not file_path.is_file():
            return False
        
        # Must be readable
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                f.read(1024)  # Read first 1KB to check readability
        except:
            return False
        
        return True
    
    def get_knowledge_graph(self) -> Optional[KnowledgeGraph]:
        """Get the current knowledge graph"""
        return self.knowledge_graph
    
    def export_knowledge(self, format: str = 'json') -> str:
        """Export the knowledge graph"""
        if not self.knowledge_graph:
            return "No knowledge graph available. Run ingest_project_documentation first."
        
        return self.graph_builder.export_graph(format)
    
    def search_concepts(self, query: str) -> List[Dict[str, Any]]:
        """Search for concepts in the knowledge graph"""
        if not self.knowledge_graph:
            return []
        
        results = []
        query_lower = query.lower()
        
        for node in self.knowledge_graph.nodes.values():
            if node.type == 'concept':
                if (query_lower in node.name.lower() or 
                    query_lower in node.description.lower()):
                    
                    # Find related nodes
                    related = []
                    for rel in self.knowledge_graph.relationships.values():
                        if rel.source_id == node.id:
                            target_node = self.knowledge_graph.nodes.get(rel.target_id)
                            if target_node:
                                related.append({
                                    'id': target_node.id,
                                    'name': target_node.name,
                                    'type': target_node.type,
                                    'relationship': rel.relationship_type
                                })
                    
                    results.append({
                        'concept': node.name,
                        'description': node.description,
                        'source': node.source,
                        'confidence': node.confidence,
                        'related': related
                    })
        
        return results

def main():
    """Main function for testing the knowledge ingestion engine"""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python knowledge_ingestion_engine.py <project_root>")
        sys.exit(1)
    
    project_root = sys.argv[1]
    
    if not os.path.exists(project_root):
        print(f"Error: Project root '{project_root}' does not exist")
        sys.exit(1)
    
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Create engine and ingest knowledge
    engine = KnowledgeIngestionEngine()
    
    try:
        print(f"🔍 Starting knowledge ingestion: {project_root}")
        knowledge_graph = engine.ingest_project_documentation(project_root)
        
        # Export results
        print("\n📊 Knowledge Graph Summary:")
        print(engine.export_knowledge('summary'))
        
        # Save detailed graph to file
        output_file = f"knowledge_graph_{int(time.time())}.json"
        with open(output_file, 'w') as f:
            f.write(engine.export_knowledge('json'))
        print(f"\n💾 Detailed knowledge graph saved to: {output_file}")
        
        # Demo search
        print("\n🔍 Demo Concept Search:")
        search_results = engine.search_concepts('function')
        print(f"Found {len(search_results)} concepts related to 'function'")
        for result in search_results[:3]:
            print(f"  - {result['concept']} (from {result['source']})")
        
    except Exception as e:
        print(f"❌ Error during knowledge ingestion: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
