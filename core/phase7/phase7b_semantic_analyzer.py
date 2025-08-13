#!/usr/bin/env python3
"""
Phase 7B.1: Semantic Analyzer - Deep Code Understanding
Advanced semantic analysis for understanding code intent, relationships, and business logic
"""

import logging
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from datetime import datetime
import ast
import re
import json
from collections import defaultdict, deque
import networkx as nx

logger = logging.getLogger(__name__)

@dataclass
class SemanticEntity:
    """Represents a semantic entity in code"""
    entity_id: str
    entity_type: str  # 'class', 'function', 'variable', 'module', 'interface'
    name: str
    full_path: str
    line_number: int
    semantic_type: str  # 'business_logic', 'infrastructure', 'utility', 'data_model'
    complexity_score: float  # 0.0 to 1.0
    relationships: List[str]  # IDs of related entities
    metadata: Dict[str, Any]
    created_at: datetime

@dataclass
class SemanticRelationship:
    """Represents a semantic relationship between entities"""
    relationship_id: str
    source_entity_id: str
    target_entity_id: str
    relationship_type: str  # 'inherits', 'implements', 'calls', 'uses', 'depends_on', 'composes'
    strength: float  # 0.0 to 1.0
    context: Dict[str, Any]
    created_at: datetime

@dataclass
class SemanticAnalysis:
    """Complete semantic analysis result"""
    entities: List[SemanticEntity]
    relationships: List[SemanticRelationship]
    relationship_graph: nx.DiGraph
    complexity_analysis: Dict[str, Any]
    architecture_patterns: List[Dict[str, Any]]
    business_logic_flow: List[Dict[str, Any]]
    technical_debt_indicators: List[Dict[str, Any]]
    analysis_timestamp: datetime
    analysis_duration: float

class AdvancedCodeParser:
    """Advanced code parsing with semantic understanding"""
    
    def __init__(self):
        self.supported_languages = {
            '.py': self._parse_python_semantic,
            '.js': self._parse_javascript_semantic,
            '.ts': self._parse_typescript_semantic,
            '.java': self._parse_java_semantic,
            '.cpp': self._parse_cpp_semantic,
            '.go': self._parse_go_semantic,
            '.rs': self._parse_rust_semantic
        }
        self.semantic_patterns = self._initialize_semantic_patterns()
    
    def _initialize_semantic_patterns(self) -> Dict[str, Any]:
        """Initialize semantic pattern recognition"""
        return {
            'business_logic_indicators': [
                'process', 'validate', 'calculate', 'compute', 'analyze',
                'transform', 'convert', 'format', 'parse', 'generate'
            ],
            'infrastructure_indicators': [
                'connect', 'send', 'receive', 'store', 'retrieve',
                'cache', 'queue', 'lock', 'unlock', 'sync'
            ],
            'utility_indicators': [
                'helper', 'util', 'common', 'shared', 'base',
                'abstract', 'interface', 'trait', 'mixin'
            ],
            'data_model_indicators': [
                'model', 'entity', 'dto', 'vo', 'pojo',
                'schema', 'table', 'collection', 'array'
            ]
        }
    
    async def parse_semantic(self, file_path: str) -> Dict[str, Any]:
        """Parse file for semantic understanding"""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {"success": False, "error": "File not found"}
            
            file_extension = file_path.suffix.lower()
            if file_extension not in self.supported_languages:
                return {"success": False, "error": f"Unsupported language: {file_extension}"}
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse based on language
            parser_func = self.supported_languages[file_extension]
            parse_result = await parser_func(content, file_path)
            
            return {
                "success": True,
                "file_path": str(file_path),
                "language": file_extension,
                "semantic_analysis": parse_result,
                "file_size": len(content),
                "line_count": len(content.splitlines())
            }
            
        except Exception as e:
            logger.error(f"Error parsing file {file_path}: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _parse_python_semantic(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Parse Python code for semantic understanding"""
        try:
            tree = ast.parse(content)
            
            entities = []
            relationships = []
            
            # Extract semantic entities
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    entity = await self._analyze_python_class(node, file_path)
                    entities.append(entity)
                    
                elif isinstance(node, ast.FunctionDef):
                    entity = await self._analyze_python_function(node, file_path)
                    entities.append(entity)
                    
                elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                    entity = await self._analyze_python_import(node, file_path)
                    entities.append(entity)
            
            # Analyze semantic relationships
            relationships = await self._analyze_python_relationships(tree, entities)
            
            return {
                "entities": entities,
                "relationships": relationships,
                "ast_tree": str(tree)
            }
            
        except Exception as e:
            logger.error(f"Error parsing Python code: {str(e)}")
            return {"error": str(e)}
    
    async def _analyze_python_class(self, node: ast.ClassDef, file_path: Path) -> Dict[str, Any]:
        """Analyze Python class for semantic understanding"""
        try:
            # Determine semantic type
            semantic_type = self._determine_semantic_type(node.name, node.bases, node.body)
            
            # Calculate complexity
            complexity_score = self._calculate_class_complexity(node)
            
            # Extract methods and their purposes
            methods = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    method_purpose = self._analyze_method_purpose(item)
                    methods.append({
                        "name": item.name,
                        "purpose": method_purpose,
                        "line": item.lineno
                    })
            
            return {
                "entity_id": f"class_{node.name}_{file_path.stem}",
                "entity_type": "class",
                "name": node.name,
                "full_path": f"{file_path.stem}.{node.name}",
                "line_number": node.lineno,
                "semantic_type": semantic_type,
                "complexity_score": complexity_score,
                "relationships": [],
                "metadata": {
                    "bases": [self._get_base_name(base) for base in node.bases],
                    "methods": methods,
                    "decorators": [d.id for d in node.decorator_list if hasattr(d, 'id')],
                    "docstring": ast.get_docstring(node)
                },
                "created_at": datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing Python class: {str(e)}")
            return {}
    
    async def _analyze_python_function(self, node: ast.FunctionDef, file_path: Path) -> Dict[str, Any]:
        """Analyze Python function for semantic understanding"""
        try:
            # Determine semantic type
            semantic_type = self._determine_semantic_type(node.name, [], node.body)
            
            # Calculate complexity
            complexity_score = self._calculate_function_complexity(node)
            
            # Analyze function purpose
            purpose = self._analyze_function_purpose(node)
            
            return {
                "entity_id": f"func_{node.name}_{file_path.stem}",
                "entity_type": "function",
                "name": node.name,
                "full_path": f"{file_path.stem}.{node.name}",
                "line_number": node.lineno,
                "semantic_type": semantic_type,
                "complexity_score": complexity_score,
                "relationships": [],
                "metadata": {
                    "args": [arg.arg for arg in node.args.args],
                    "purpose": purpose,
                    "decorators": [d.id for d in node.decorator_list if hasattr(d, 'id')],
                    "docstring": ast.get_docstring(node),
                    "returns": self._analyze_return_type(node)
                },
                "created_at": datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing Python function: {str(e)}")
            return {}
    
    def _determine_semantic_type(self, name: str, bases: List[Any], body: List[Any]) -> str:
        """Determine semantic type based on name, bases, and body"""
        name_lower = name.lower()
        
        # Check for business logic indicators
        if any(indicator in name_lower for indicator in self.semantic_patterns['business_logic_indicators']):
            return 'business_logic'
        
        # Check for infrastructure indicators
        if any(indicator in name_lower for indicator in self.semantic_patterns['infrastructure_indicators']):
            return 'infrastructure'
        
        # Check for data model indicators
        if any(indicator in name_lower for indicator in self.semantic_patterns['data_model_indicators']):
            return 'data_model'
        
        # Check for utility indicators
        if any(indicator in name_lower for indicator in self.semantic_patterns['utility_indicators']):
            return 'utility'
        
        # Default to business logic if uncertain
        return 'business_logic'
    
    def _calculate_class_complexity(self, node: ast.ClassDef) -> float:
        """Calculate complexity score for a class"""
        try:
            complexity = 0.0
            
            # Method count complexity
            method_count = len([item for item in node.body if isinstance(item, ast.FunctionDef)])
            complexity += min(method_count * 0.1, 0.3)  # Max 0.3 for methods
            
            # Inheritance complexity
            inheritance_depth = len(node.bases)
            complexity += min(inheritance_depth * 0.1, 0.2)  # Max 0.2 for inheritance
            
            # Decorator complexity
            decorator_count = len(node.decorator_list)
            complexity += min(decorator_count * 0.05, 0.1)  # Max 0.1 for decorators
            
            # Body complexity
            body_complexity = self._calculate_body_complexity(node.body)
            complexity += body_complexity * 0.4  # 40% weight for body complexity
            
            return min(complexity, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating class complexity: {str(e)}")
            return 0.5
    
    def _calculate_function_complexity(self, node: ast.FunctionDef) -> float:
        """Calculate complexity score for a function"""
        try:
            complexity = 0.0
            
            # Argument complexity
            arg_count = len(node.args.args)
            complexity += min(arg_count * 0.05, 0.2)  # Max 0.2 for arguments
            
            # Body complexity
            body_complexity = self._calculate_body_complexity(node.body)
            complexity += body_complexity * 0.8  # 80% weight for body complexity
            
            return min(complexity, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating function complexity: {str(e)}")
            return 0.5
    
    def _calculate_body_complexity(self, body: List[Any]) -> float:
        """Calculate complexity of a code body"""
        try:
            complexity = 0.0
            
            for item in body:
                if isinstance(item, ast.If):
                    complexity += 0.1
                elif isinstance(item, ast.For):
                    complexity += 0.1
                elif isinstance(item, ast.While):
                    complexity += 0.1
                elif isinstance(item, ast.Try):
                    complexity += 0.15
                elif isinstance(item, ast.With):
                    complexity += 0.05
                elif isinstance(item, ast.Return):
                    complexity += 0.02
                elif isinstance(item, ast.Assign):
                    complexity += 0.01
                elif isinstance(item, ast.Expr):
                    complexity += 0.01
            
            return min(complexity, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating body complexity: {str(e)}")
            return 0.5
    
    def _analyze_method_purpose(self, node: ast.FunctionDef) -> str:
        """Analyze the purpose of a method"""
        name_lower = node.name.lower()
        
        if name_lower.startswith('get_'):
            return 'getter'
        elif name_lower.startswith('set_'):
            return 'setter'
        elif name_lower.startswith('is_') or name_lower.startswith('has_'):
            return 'validator'
        elif name_lower.startswith('on_'):
            return 'event_handler'
        elif name_lower.startswith('handle_'):
            return 'event_handler'
        elif name_lower.startswith('process_'):
            return 'processor'
        elif name_lower.startswith('validate_'):
            return 'validator'
        elif name_lower.startswith('transform_'):
            return 'transformer'
        else:
            return 'business_logic'
    
    def _analyze_function_purpose(self, node: ast.FunctionDef) -> str:
        """Analyze the purpose of a function"""
        return self._analyze_method_purpose(node)
    
    def _analyze_return_type(self, node: ast.FunctionDef) -> str:
        """Analyze the return type of a function"""
        # Simple return type analysis - can be enhanced
        for item in node.body:
            if isinstance(item, ast.Return):
                if item.value is None:
                    return 'None'
                elif isinstance(item.value, ast.Constant):
                    return type(item.value.value).__name__
                elif isinstance(item.value, ast.Name):
                    return 'variable'
                elif isinstance(item.value, ast.Call):
                    return 'function_call'
        
        return 'unknown'
    
    def _get_base_name(self, base: Any) -> str:
        """Get the name of a base class"""
        if hasattr(base, 'id'):
            return base.id
        elif hasattr(base, 'attr'):
            return base.attr
        else:
            return 'unknown'
    
    async def _analyze_python_import(self, node: ast.Import, file_path: Path) -> Dict[str, Any]:
        """Analyze Python import for semantic understanding"""
        try:
            return {
                "entity_id": f"import_{file_path.stem}",
                "entity_type": "module",
                "name": "imports",
                "full_path": str(file_path.stem),
                "line_number": node.lineno,
                "semantic_type": "infrastructure",
                "complexity_score": 0.1,
                "relationships": [],
                "metadata": {
                    "imports": [alias.name for alias in node.names],
                    "type": "import"
                },
                "created_at": datetime.now()
            }
        except Exception as e:
            logger.error(f"Error analyzing Python import: {str(e)}")
            return {}
    
    async def _analyze_python_relationships(self, tree: ast.AST, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze relationships between Python entities"""
        try:
            relationships = []
            
            # Build entity lookup
            entity_lookup = {entity['name']: entity for entity in entities if 'name' in entity}
            
            # Analyze class inheritance
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    for base in node.bases:
                        base_name = self._get_base_name(base)
                        if base_name in entity_lookup:
                            relationships.append({
                                "relationship_id": f"inherits_{node.name}_{base_name}",
                                "source_entity_id": f"class_{node.name}_{tree}",
                                "target_entity_id": f"class_{base_name}_{tree}",
                                "relationship_type": "inherits",
                                "strength": 0.9,
                                "context": {"line": node.lineno},
                                "created_at": datetime.now()
                            })
            
            return relationships
            
        except Exception as e:
            logger.error(f"Error analyzing Python relationships: {str(e)}")
            return []
    
    # Placeholder methods for other languages
    async def _parse_javascript_semantic(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Parse JavaScript code for semantic understanding"""
        return {"entities": [], "relationships": [], "language": "javascript"}
    
    async def _parse_typescript_semantic(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Parse TypeScript code for semantic understanding"""
        return {"entities": [], "relationships": [], "language": "typescript"}
    
    async def _parse_java_semantic(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Parse Java code for semantic understanding"""
        return {"entities": [], "relationships": [], "language": "java"}
    
    async def _parse_cpp_semantic(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Parse C++ code for semantic understanding"""
        return {"entities": [], "relationships": [], "language": "cpp"}
    
    async def _parse_go_semantic(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Parse Go code for semantic understanding"""
        return {"entities": [], "relationships": [], "language": "go"}
    
    async def _parse_rust_semantic(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Parse Rust code for semantic understanding"""
        return {"entities": [], "relationships": [], "language": "rust"}

class RelationshipMapper:
    """Maps relationships between semantic entities"""
    
    def __init__(self):
        self.relationship_patterns = {
            'inheritance': ['extends', 'implements', 'inherits'],
            'composition': ['contains', 'has_a', 'composed_of'],
            'dependency': ['depends_on', 'uses', 'imports'],
            'association': ['calls', 'invokes', 'triggers']
        }
    
    async def build_relationship_graph(self, entities: List[Dict[str, Any]], relationships: List[Dict[str, Any]]) -> nx.DiGraph:
        """Build a directed graph of entity relationships"""
        try:
            G = nx.DiGraph()
            
            # Add entities as nodes
            for entity in entities:
                G.add_node(entity['entity_id'], **entity)
            
            # Add relationships as edges
            for relationship in relationships:
                G.add_edge(
                    relationship['source_entity_id'],
                    relationship['target_entity_id'],
                    **relationship
                )
            
            return G
            
        except Exception as e:
            logger.error(f"Error building relationship graph: {str(e)}")
            return nx.DiGraph()
    
    async def analyze_relationship_patterns(self, graph: nx.DiGraph) -> Dict[str, Any]:
        """Analyze patterns in entity relationships"""
        try:
            patterns = {
                'centrality': {},
                'clustering': {},
                'connectivity': {},
                'cycles': []
            }
            
            # Calculate centrality measures
            if len(graph.nodes()) > 0:
                patterns['centrality'] = {
                    'degree': nx.degree_centrality(graph),
                    'betweenness': nx.betweenness_centrality(graph),
                    'closeness': nx.closeness_centrality(graph)
                }
                
                # Calculate clustering coefficient
                patterns['clustering'] = nx.clustering(graph)
                
                # Check for cycles
                try:
                    cycles = list(nx.simple_cycles(graph))
                    patterns['cycles'] = cycles
                except:
                    patterns['cycles'] = []
            
            return patterns
            
        except Exception as e:
            logger.error(f"Error analyzing relationship patterns: {str(e)}")
            return {}

class IntentAnalyzer:
    """Analyzes code intent and purpose"""
    
    def __init__(self):
        self.intent_patterns = {
            'data_processing': ['process', 'transform', 'convert', 'parse'],
            'validation': ['validate', 'check', 'verify', 'ensure'],
            'business_logic': ['calculate', 'compute', 'analyze', 'determine'],
            'infrastructure': ['connect', 'send', 'receive', 'store'],
            'utility': ['helper', 'util', 'format', 'normalize']
        }
    
    async def analyze_code_intent(self, code_content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the intent and purpose of code"""
        try:
            intent_analysis = {
                'primary_intent': 'unknown',
                'confidence': 0.0,
                'intent_indicators': [],
                'business_context': {},
                'technical_context': {}
            }
            
            # Analyze code content for intent indicators
            content_lower = code_content.lower()
            
            # Find intent indicators
            found_intents = []
            for intent_type, indicators in self.intent_patterns.items():
                for indicator in indicators:
                    if indicator in content_lower:
                        found_intents.append(intent_type)
                        intent_analysis['intent_indicators'].append({
                            'type': intent_type,
                            'indicator': indicator
                        })
            
            # Determine primary intent
            if found_intents:
                # Count occurrences of each intent type
                intent_counts = {}
                for intent in found_intents:
                    intent_counts[intent] = intent_counts.get(intent, 0) + 1
                
                # Select most common intent
                primary_intent = max(intent_counts, key=intent_counts.get)
                intent_analysis['primary_intent'] = primary_intent
                intent_analysis['confidence'] = min(len(found_intents) * 0.2, 1.0)
            
            # Analyze business context
            intent_analysis['business_context'] = await self._analyze_business_context(code_content, context)
            
            # Analyze technical context
            intent_analysis['technical_context'] = await self._analyze_technical_context(code_content, context)
            
            return intent_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing code intent: {str(e)}")
            return {'primary_intent': 'unknown', 'confidence': 0.0}
    
    async def _analyze_business_context(self, code_content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze business context of code"""
        try:
            business_context = {
                'domain': 'unknown',
                'business_rules': [],
                'data_entities': [],
                'workflow_steps': []
            }
            
            # Simple domain detection based on common terms
            content_lower = code_content.lower()
            
            if any(term in content_lower for term in ['user', 'customer', 'account']):
                business_context['domain'] = 'user_management'
            elif any(term in content_lower for term in ['order', 'payment', 'transaction']):
                business_context['domain'] = 'ecommerce'
            elif any(term in content_lower for term in ['report', 'analytics', 'metrics']):
                business_context['domain'] = 'reporting'
            elif any(term in content_lower for term in ['config', 'settings', 'preferences']):
                business_context['domain'] = 'configuration'
            
            return business_context
            
        except Exception as e:
            logger.error(f"Error analyzing business context: {str(e)}")
            return {'domain': 'unknown'}
    
    async def _analyze_technical_context(self, code_content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze technical context of code"""
        try:
            technical_context = {
                'framework': 'unknown',
                'design_patterns': [],
                'architectural_layers': [],
                'performance_characteristics': {}
            }
            
            # Simple framework detection
            content_lower = code_content.lower()
            
            if 'django' in content_lower:
                technical_context['framework'] = 'django'
            elif 'flask' in content_lower:
                technical_context['framework'] = 'flask'
            elif 'fastapi' in content_lower:
                technical_context['framework'] = 'fastapi'
            elif 'react' in content_lower:
                technical_context['framework'] = 'react'
            
            return technical_context
            
        except Exception as e:
            logger.error(f"Error analyzing technical context: {str(e)}")
            return {'framework': 'unknown'}

class DomainAnalyzer:
    """Analyzes domain-specific knowledge and patterns"""
    
    def __init__(self):
        self.domain_patterns = {
            'web_development': ['http', 'request', 'response', 'api', 'endpoint'],
            'data_science': ['pandas', 'numpy', 'matplotlib', 'scikit-learn'],
            'devops': ['docker', 'kubernetes', 'ci/cd', 'deployment'],
            'mobile_development': ['ios', 'android', 'react_native', 'flutter'],
            'game_development': ['unity', 'unreal', 'game_loop', 'physics']
        }
    
    async def analyze_domain_context(self, code_content: str, project_context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze domain context of code"""
        try:
            domain_analysis = {
                'primary_domain': 'unknown',
                'domain_confidence': 0.0,
                'domain_patterns': [],
                'technology_stack': [],
                'best_practices': []
            }
            
            # Analyze code content for domain indicators
            content_lower = code_content.lower()
            
            # Find domain patterns
            found_domains = []
            for domain, patterns in self.domain_patterns.items():
                for pattern in patterns:
                    if pattern in content_lower:
                        found_domains.append(domain)
                        domain_analysis['domain_patterns'].append({
                            'domain': domain,
                            'pattern': pattern
                        })
            
            # Determine primary domain
            if found_domains:
                domain_counts = {}
                for domain in found_domains:
                    domain_counts[domain] = domain_counts.get(domain, 0) + 1
                
                primary_domain = max(domain_counts, key=domain_counts.get)
                domain_analysis['primary_domain'] = primary_domain
                domain_analysis['domain_confidence'] = min(len(found_domains) * 0.2, 1.0)
            
            # Analyze technology stack
            domain_analysis['technology_stack'] = await self._analyze_technology_stack(code_content)
            
            # Suggest best practices
            domain_analysis['best_practices'] = await self._suggest_best_practices(
                domain_analysis['primary_domain']
            )
            
            return domain_analysis
            
        except Exception as e:
            logger.error(f"Error analyzing domain context: {str(e)}")
            return {'primary_domain': 'unknown', 'domain_confidence': 0.0}
    
    async def _analyze_technology_stack(self, code_content: str) -> List[str]:
        """Analyze technology stack from code content"""
        try:
            technologies = []
            content_lower = code_content.lower()
            
            # Common technology indicators
            tech_indicators = {
                'python': ['import pandas', 'import numpy', 'import django', 'import flask'],
                'javascript': ['import react', 'import vue', 'import angular', 'const express'],
                'java': ['import java', 'public class', 'spring boot', 'maven'],
                'go': ['package main', 'import fmt', 'func main', 'go mod'],
                'rust': ['use std', 'fn main', 'cargo', 'struct']
            }
            
            for tech, indicators in tech_indicators.items():
                for indicator in indicators:
                    if indicator in content_lower:
                        technologies.append(tech)
                        break
            
            return list(set(technologies))  # Remove duplicates
            
        except Exception as e:
            logger.error(f"Error analyzing technology stack: {str(e)}")
            return []
    
    async def _suggest_best_practices(self, domain: str) -> List[str]:
        """Suggest best practices for a domain"""
        try:
            best_practices = {
                'web_development': [
                    'Use HTTPS for all communications',
                    'Implement proper error handling',
                    'Follow RESTful API design principles',
                    'Use input validation and sanitization'
                ],
                'data_science': [
                    'Document data preprocessing steps',
                    'Use version control for data',
                    'Implement reproducible workflows',
                    'Validate data quality and integrity'
                ],
                'devops': [
                    'Automate deployment processes',
                    'Use infrastructure as code',
                    'Implement monitoring and alerting',
                    'Follow security best practices'
                ],
                'mobile_development': [
                    'Optimize for performance',
                    'Handle offline scenarios',
                    'Implement proper error handling',
                    'Follow platform design guidelines'
                ]
            }
            
            return best_practices.get(domain, ['Follow general software development best practices'])
            
        except Exception as e:
            logger.error(f"Error suggesting best practices: {str(e)}")
            return ['Follow general software development best practices']

class SemanticAnalyzer:
    """Deep semantic understanding of code and context"""
    
    def __init__(self):
        self.code_parser = AdvancedCodeParser()
        self.relationship_mapper = RelationshipMapper()
        self.intent_analyzer = IntentAnalyzer()
        self.domain_analyzer = DomainAnalyzer()
    
    async def analyze_code_semantics(self, code_content: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze code for deep semantic understanding"""
        try:
            # Analyze code intent
            intent_analysis = await self.intent_analyzer.analyze_code_intent(code_content, context)
            
            # Analyze domain context
            domain_analysis = await self.domain_analyzer.analyze_domain_context(code_content, context)
            
            return {
                "success": True,
                "intent_analysis": intent_analysis,
                "domain_analysis": domain_analysis,
                "semantic_score": (intent_analysis.get('confidence', 0) + domain_analysis.get('domain_confidence', 0)) / 2
            }
            
        except Exception as e:
            logger.error(f"Error analyzing code semantics: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def map_entity_relationships(self, codebase: Dict[str, Any]) -> Dict[str, Any]:
        """Map relationships between code entities"""
        try:
            # Extract entities and relationships from codebase
            entities = codebase.get('entities', [])
            relationships = codebase.get('relationships', [])
            
            # Build relationship graph
            graph = await self.relationship_mapper.build_relationship_graph(entities, relationships)
            
            # Analyze relationship patterns
            patterns = await self.relationship_mapper.analyze_relationship_patterns(graph)
            
            return {
                "success": True,
                "graph": graph,
                "patterns": patterns,
                "entity_count": len(entities),
                "relationship_count": len(relationships)
            }
            
        except Exception as e:
            logger.error(f"Error mapping entity relationships: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def understand_business_logic(self, code_content: str) -> Dict[str, Any]:
        """Comprehend business logic and application purpose"""
        try:
            # Analyze business context
            business_context = await self.intent_analyzer._analyze_business_context(code_content, {})
            
            # Analyze domain context
            domain_context = await self.domain_analyzer.analyze_domain_context(code_content, {})
            
            return {
                "success": True,
                "business_context": business_context,
                "domain_context": domain_context,
                "business_logic_score": business_context.get('domain', 'unknown') != 'unknown'
            }
            
        except Exception as e:
            logger.error(f"Error understanding business logic: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def analyze_project_semantics(self, project_path: str) -> SemanticAnalysis:
        """Perform comprehensive semantic analysis of a project"""
        start_time = datetime.now()
        
        try:
            project_path = Path(project_path)
            if not project_path.exists():
                raise ValueError("Project path not found")
            
            logger.info(f"🔍 Starting semantic analysis for: {project_path}")
            
            # Find all code files
            code_files = []
            for ext in self.code_parser.supported_languages:
                code_files.extend(project_path.rglob(f"*{ext}"))
            
            # Parse each file for semantic understanding
            all_entities = []
            all_relationships = []
            
            for code_file in code_files[:50]:  # Limit to first 50 files for performance
                try:
                    parse_result = await self.code_parser.parse_semantic(str(code_file))
                    if parse_result.get("success"):
                        semantic_data = parse_result.get("semantic_analysis", {})
                        entities = semantic_data.get("entities", [])
                        relationships = semantic_data.get("relationships", [])
                        
                        all_entities.extend(entities)
                        all_relationships.extend(relationships)
                        
                except Exception as e:
                    logger.warning(f"Could not analyze {code_file}: {str(e)}")
                    continue
            
            # Build relationship graph
            graph = await self.relationship_mapper.build_relationship_graph(all_entities, all_relationships)
            
            # Analyze patterns
            patterns = await self.relationship_mapper.analyze_relationship_patterns(graph)
            
            # Calculate analysis duration
            analysis_duration = (datetime.now() - start_time).total_seconds()
            
            # Create semantic analysis result
            analysis_result = SemanticAnalysis(
                entities=all_entities,
                relationships=all_relationships,
                relationship_graph=graph,
                complexity_analysis=patterns,
                architecture_patterns=[],  # TODO: Implement architecture pattern detection
                business_logic_flow=[],    # TODO: Implement business logic flow analysis
                technical_debt_indicators=[],  # TODO: Implement technical debt detection
                analysis_timestamp=datetime.now(),
                analysis_duration=analysis_duration
            )
            
            logger.info(f"✅ Semantic analysis completed in {analysis_duration:.2f}s")
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"❌ Semantic analysis failed: {str(e)}")
            raise

# Example usage and testing
async def main():
    """Example usage of the SemanticAnalyzer"""
    analyzer = SemanticAnalyzer()
    
    # Test semantic analysis
    print("🔍 Testing Semantic Analyzer (Phase 7B.1)")
    
    # Test code intent analysis
    print("\n💭 Testing code intent analysis...")
    test_code = """
def process_user_data(user_input):
    # Validate input
    if not user_input:
        raise ValueError("User input cannot be empty")
    
    # Transform data
    processed_data = user_input.strip().lower()
    
    # Return result
    return processed_data
"""
    
    intent_result = await analyzer.analyze_code_semantics(test_code, {})
    if intent_result.get("success"):
        print(f"  ✅ Intent: {intent_result['intent_analysis']['primary_intent']}")
        print(f"  📊 Confidence: {intent_result['intent_analysis']['confidence']:.2f}")
        print(f"  🏢 Domain: {intent_result['domain_analysis']['primary_domain']}")
    else:
        print(f"  ❌ Intent analysis failed: {intent_result.get('error')}")
    
    # Test business logic understanding
    print("\n🏢 Testing business logic understanding...")
    business_result = await analyzer.understand_business_logic(test_code)
    if business_result.get("success"):
        print(f"  ✅ Business logic score: {business_result['business_logic_score']}")
        print(f"  🎯 Domain: {business_result['business_context']['domain']}")
    else:
        print(f"  ❌ Business logic analysis failed: {business_result.get('error')}")
    
    # Test project semantic analysis
    print("\n📁 Testing project semantic analysis...")
    current_dir = str(Path.cwd())
    print(f"  Analyzing semantics in: {current_dir}")
    
    try:
        project_result = await analyzer.analyze_project_semantics(current_dir)
        print(f"  ✅ Project semantic analysis completed!")
        print(f"  📊 Entities found: {len(project_result.entities)}")
        print(f"  🔗 Relationships found: {len(project_result.relationships)}")
        print(f"  ⏱️ Analysis time: {project_result.analysis_duration:.2f}s")
        
        # Show some entity examples
        if project_result.entities:
            print(f"\n  📋 Entity examples:")
            for entity in project_result.entities[:3]:
                print(f"    • {entity.get('name', 'Unknown')} ({entity.get('entity_type', 'Unknown')})")
                print(f"      Type: {entity.get('semantic_type', 'Unknown')}, Complexity: {entity.get('complexity_score', 0):.2f}")
        
    except Exception as e:
        print(f"  ❌ Project analysis failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
