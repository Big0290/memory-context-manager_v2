#!/usr/bin/env python3
"""
Phase 7A: Pattern Analysis Engine - Quick Start Implementation
Advanced code pattern recognition and analysis for Memory Context Manager v2
"""

import os
import json
import logging
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import ast
import re

logger = logging.getLogger(__name__)

@dataclass
class CodePattern:
    """Represents a detected coding pattern"""
    pattern_id: str
    pattern_type: str  # 'file_structure', 'code_style', 'architecture', 'dependency', 'workflow'
    pattern_name: str
    description: str
    confidence: float  # 0.0 to 1.0
    file_path: str
    line_numbers: List[int]
    pattern_data: Dict[str, Any]
    detected_at: datetime
    effectiveness_score: float = 0.0

@dataclass
class PatternAnalysis:
    """Complete pattern analysis result"""
    project_path: str
    analysis_timestamp: datetime
    total_patterns: int
    pattern_categories: Dict[str, int]
    patterns: List[CodePattern]
    summary: Dict[str, Any]
    analysis_duration: float

class CodeParser:
    """Parses code files to extract structural information"""
    
    def __init__(self):
        self.supported_languages = {
            '.py': self._parse_python,
            '.js': self._parse_javascript,
            '.ts': self._parse_typescript,
            '.jsx': self._parse_javascript,
            '.tsx': self._parse_typescript,
            '.java': self._parse_java,
            '.cpp': self._parse_cpp,
            '.c': self._parse_cpp,
            '.go': self._parse_go,
            '.rs': self._parse_rust
        }
    
    async def parse_file(self, file_path: str) -> Dict[str, Any]:
        """Parse a code file and extract structural information"""
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
                "content": content,
                "structure": parse_result,
                "file_size": len(content),
                "line_count": len(content.splitlines())
            }
            
        except Exception as e:
            logger.error(f"Error parsing file {file_path}: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _parse_python(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Parse Python code structure"""
        try:
            tree = ast.parse(content)
            
            # Extract classes, functions, imports
            classes = []
            functions = []
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    classes.append({
                        "name": node.name,
                        "line": node.lineno,
                        "bases": [base.id for base in node.bases if hasattr(base, 'id')],
                        "methods": [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    })
                elif isinstance(node, ast.FunctionDef):
                    functions.append({
                        "name": node.name,
                        "line": node.lineno,
                        "args": [arg.arg for arg in node.args.args],
                        "decorators": [d.id for d in node.decorator_list if hasattr(d, 'id')]
                    })
                elif isinstance(node, ast.Import):
                    imports.extend([alias.name for alias in node.names])
                elif isinstance(node, ast.ImportFrom):
                    imports.append(f"{node.module}.{', '.join([alias.name for alias in node.names])}")
            
            return {
                "classes": classes,
                "functions": functions,
                "imports": imports,
                "ast_tree": str(tree)
            }
            
        except Exception as e:
            logger.error(f"Error parsing Python code: {str(e)}")
            return {"error": str(e)}
    
    async def _parse_javascript(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Parse JavaScript/TypeScript code structure (basic implementation)"""
        # Basic regex-based parsing for demonstration
        classes = re.findall(r'class\s+(\w+)', content)
        functions = re.findall(r'(?:function\s+)?(\w+)\s*\([^)]*\)\s*{', content)
        imports = re.findall(r'import\s+.*?from\s+[\'"]([^\'"]+)[\'"]', content)
        
        return {
            "classes": [{"name": name, "line": 0} for name in classes],
            "functions": [{"name": name, "line": 0} for name in functions],
            "imports": imports,
            "parsing_method": "regex_basic"
        }
    
    async def _parse_typescript(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Parse TypeScript code structure"""
        return await self._parse_javascript(content, file_path)
    
    async def _parse_java(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Parse Java code structure (basic implementation)"""
        classes = re.findall(r'class\s+(\w+)', content)
        methods = re.findall(r'(?:public|private|protected)?\s*(?:static\s+)?(?:final\s+)?\w+\s+(\w+)\s*\([^)]*\)', content)
        
        return {
            "classes": [{"name": name, "line": 0} for name in classes],
            "methods": [{"name": name, "line": 0} for name in methods],
            "parsing_method": "regex_basic"
        }
    
    async def _parse_cpp(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Parse C++ code structure (basic implementation)"""
        classes = re.findall(r'class\s+(\w+)', content)
        functions = re.findall(r'\w+\s+(\w+)\s*\([^)]*\)\s*{', content)
        
        return {
            "classes": [{"name": name, "line": 0} for name in classes],
            "functions": [{"name": name, "line": 0} for name in functions],
            "parsing_method": "regex_basic"
        }
    
    async def _parse_go(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Parse Go code structure (basic implementation)"""
        functions = re.findall(r'func\s+(\w+)\s*\([^)]*\)', content)
        structs = re.findall(r'type\s+(\w+)\s+struct', content)
        
        return {
            "functions": [{"name": name, "line": 0} for name in functions],
            "structs": [{"name": name, "line": 0} for name in structs],
            "parsing_method": "regex_basic"
        }
    
    async def _parse_rust(self, content: str, file_path: Path) -> Dict[str, Any]:
        """Parse Rust code structure (basic implementation)"""
        functions = re.findall(r'fn\s+(\w+)\s*\([^)]*\)', content)
        structs = re.findall(r'struct\s+(\w+)', content)
        
        return {
            "functions": [{"name": name, "line": 0} for name in functions],
            "structs": [{"name": name, "line": 0} for name in structs],
            "parsing_method": "regex_basic"
        }

class StyleAnalyzer:
    """Analyzes code style and formatting patterns"""
    
    def __init__(self):
        self.style_patterns = {
            'naming_conventions': {
                'snake_case': r'[a-z][a-z0-9_]*',
                'camelCase': r'[a-z][a-zA-Z0-9]*',
                'PascalCase': r'[A-Z][a-zA-Z0-9]*',
                'UPPER_CASE': r'[A-Z][A-Z0-9_]*'
            },
            'indentation': {
                'spaces_2': r'^  ',
                'spaces_4': r'^    ',
                'tabs': r'^\t'
            },
            'line_length': {
                'short': 80,
                'medium': 120,
                'long': 200
            }
        }
    
    async def analyze_file_style(self, file_path: str, parsed_content: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the style patterns in a code file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.splitlines()
            
            # Analyze naming conventions
            naming_analysis = await self._analyze_naming_conventions(parsed_content, content)
            
            # Analyze indentation
            indentation_analysis = await self._analyze_indentation(lines)
            
            # Analyze line lengths
            line_length_analysis = await self._analyze_line_lengths(lines)
            
            # Analyze spacing and formatting
            formatting_analysis = await self._analyze_formatting(content)
            
            return {
                "success": True,
                "naming_conventions": naming_analysis,
                "indentation": indentation_analysis,
                "line_lengths": line_length_analysis,
                "formatting": formatting_analysis,
                "style_consistency_score": self._calculate_style_consistency(
                    naming_analysis, indentation_analysis, line_length_analysis, formatting_analysis
                )
            }
            
        except Exception as e:
            logger.error(f"Error analyzing file style: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _analyze_naming_conventions(self, parsed_content: Dict[str, Any], content: str) -> Dict[str, Any]:
        """Analyze naming convention usage"""
        naming_stats = {pattern: 0 for pattern in self.style_patterns['naming_conventions']}
        
        # Count function and class names
        if 'functions' in parsed_content:
            for func in parsed_content['functions']:
                name = func.get('name', '')
                for pattern_name, pattern in self.style_patterns['naming_conventions'].items():
                    if re.match(pattern, name):
                        naming_stats[pattern_name] += 1
                        break
        
        if 'classes' in parsed_content:
            for cls in parsed_content['classes']:
                name = cls.get('name', '')
                for pattern_name, pattern in self.style_patterns['naming_conventions'].items():
                    if re.match(pattern, name):
                        naming_stats[pattern_name] += 1
                        break
        
        return naming_stats
    
    async def _analyze_indentation(self, lines: List[str]) -> Dict[str, Any]:
        """Analyze indentation patterns"""
        indentation_stats = {pattern: 0 for pattern in self.style_patterns['indentation']}
        total_indented_lines = 0
        
        for line in lines:
            if line.strip():  # Non-empty line
                for pattern_name, pattern in self.style_patterns['indentation'].items():
                    if re.match(pattern, line):
                        indentation_stats[pattern_name] += 1
                        total_indented_lines += 1
                        break
        
        return {
            "patterns": indentation_stats,
            "total_indented_lines": total_indented_lines,
            "dominant_pattern": max(indentation_stats, key=indentation_stats.get) if total_indented_lines > 0 else "none"
        }
    
    async def _analyze_line_lengths(self, lines: List[str]) -> Dict[str, Any]:
        """Analyze line length patterns"""
        line_lengths = [len(line) for line in lines]
        avg_length = sum(line_lengths) / len(line_lengths) if line_lengths else 0
        
        length_categories = {category: 0 for category in self.style_patterns['line_length']}
        for length in line_lengths:
            if length <= self.style_patterns['line_length']['short']:
                length_categories['short'] += 1
            elif length <= self.style_patterns['line_length']['medium']:
                length_categories['medium'] += 1
            else:
                length_categories['long'] += 1
        
        return {
            "categories": length_categories,
            "average_length": avg_length,
            "max_length": max(line_lengths) if line_lengths else 0,
            "min_length": min(line_lengths) if line_lengths else 0
        }
    
    async def _analyze_formatting(self, content: str) -> Dict[str, Any]:
        """Analyze general formatting patterns"""
        return {
            "trailing_whitespace": len(re.findall(r'[ \t]+$', content, re.MULTILINE)),
            "consecutive_blank_lines": len(re.findall(r'\n\s*\n\s*\n', content)),
            "mixed_indentation": len(re.findall(r'^[ \t]+', content, re.MULTILINE)) > 0
        }
    
    def _calculate_style_consistency(self, naming: Dict, indentation: Dict, line_lengths: Dict, formatting: Dict) -> float:
        """Calculate overall style consistency score"""
        # Simple scoring algorithm - can be enhanced
        score = 0.0
        
        # Naming consistency (30% weight)
        if naming:
            dominant_naming = max(naming.values())
            total_naming = sum(naming.values())
            if total_naming > 0:
                score += 0.3 * (dominant_naming / total_naming)
        
        # Indentation consistency (40% weight)
        if indentation.get('total_indented_lines', 0) > 0:
            dominant_indent = indentation.get('dominant_pattern', 'none')
            if dominant_indent != 'none':
                dominant_count = indentation['patterns'].get(dominant_indent, 0)
                score += 0.4 * (dominant_count / indentation['total_indented_lines'])
        
        # Line length consistency (20% weight)
        if line_lengths.get('average_length', 0) > 0:
            if line_lengths['average_length'] <= self.style_patterns['line_length']['short']:
                score += 0.2
            elif line_lengths['average_length'] <= self.style_patterns['line_length']['medium']:
                score += 0.15
            else:
                score += 0.1
        
        # Formatting consistency (10% weight)
        if not formatting.get('mixed_indentation', False):
            score += 0.1
        
        return min(score, 1.0)

class PatternAnalyzer:
    """Advanced code pattern recognition and analysis"""
    
    def __init__(self):
        self.code_parser = CodeParser()
        self.style_analyzer = StyleAnalyzer()
        self.pattern_cache = {}
    
    async def analyze_project_patterns(self, project_path: str) -> Dict[str, Any]:
        """Comprehensive pattern analysis of entire project"""
        start_time = datetime.now()
        
        try:
            project_path = Path(project_path)
            if not project_path.exists():
                return {"success": False, "error": "Project path not found"}
            
            logger.info(f"🔍 Starting pattern analysis for: {project_path}")
            
            # 1. File structure analysis
            file_patterns = await self._analyze_file_structure(project_path)
            
            # 2. Code style analysis
            style_patterns = await self._analyze_code_style(project_path)
            
            # 3. Architecture patterns
            arch_patterns = await self._analyze_architecture(project_path)
            
            # 4. Dependency patterns
            dep_patterns = await self._analyze_dependencies(project_path)
            
            # 5. Workflow patterns
            workflow_patterns = await self._analyze_workflow(project_path)
            
            # Calculate analysis duration
            analysis_duration = (datetime.now() - start_time).total_seconds()
            
            # Generate comprehensive summary
            pattern_summary = self._generate_pattern_summary({
                "file": file_patterns,
                "style": style_patterns,
                "architecture": arch_patterns,
                "dependency": dep_patterns,
                "workflow": workflow_patterns
            })
            
            # Create analysis result
            analysis_result = PatternAnalysis(
                project_path=str(project_path),
                analysis_timestamp=datetime.now(),
                total_patterns=len(file_patterns.get('patterns', [])) + 
                              len(style_patterns.get('patterns', [])) + 
                              len(arch_patterns.get('patterns', [])) + 
                              len(dep_patterns.get('patterns', [])) + 
                              len(workflow_patterns.get('patterns', [])),
                pattern_categories={
                    "file_structure": len(file_patterns.get('patterns', [])),
                    "code_style": len(style_patterns.get('patterns', [])),
                    "architecture": len(arch_patterns.get('patterns', [])),
                    "dependency": len(dep_patterns.get('patterns', [])),
                    "workflow": len(workflow_patterns.get('patterns', []))
                },
                patterns=[],
                summary=pattern_summary,
                analysis_duration=analysis_duration
            )
            
            logger.info(f"✅ Pattern analysis completed in {analysis_duration:.2f}s")
            
            return {
                "success": True,
                "file_patterns": file_patterns,
                "style_patterns": style_patterns,
                "architecture_patterns": arch_patterns,
                "dependency_patterns": dep_patterns,
                "workflow_patterns": workflow_patterns,
                "pattern_summary": pattern_summary,
                "analysis_result": asdict(analysis_result)
            }
            
        except Exception as e:
            logger.error(f"❌ Pattern analysis failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    async def _analyze_file_structure(self, project_path: Path) -> Dict[str, Any]:
        """Analyze file organization and structure patterns"""
        try:
            patterns = []
            
            # Analyze directory structure
            dir_structure = await self._analyze_directory_structure(project_path)
            
            # Analyze file organization
            file_organization = await self._analyze_file_organization(project_path)
            
            # Analyze naming conventions
            naming_patterns = await self._analyze_file_naming(project_path)
            
            patterns.extend(dir_structure)
            patterns.extend(file_organization)
            patterns.extend(naming_patterns)
            
            return {
                "success": True,
                "patterns": patterns,
                "total_patterns": len(patterns),
                "directory_structure": dir_structure,
                "file_organization": file_organization,
                "naming_patterns": naming_patterns
            }
            
        except Exception as e:
            logger.error(f"Error analyzing file structure: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _analyze_code_style(self, project_path: Path) -> Dict[str, Any]:
        """Analyze coding style and formatting patterns"""
        try:
            patterns = []
            style_analysis = {}
            
            # Find all code files
            code_files = list(project_path.rglob("*"))
            code_files = [f for f in code_files if f.is_file() and f.suffix in self.code_parser.supported_languages]
            
            for code_file in code_files[:50]:  # Limit to first 50 files for performance
                try:
                    # Parse the file
                    parsed_content = await self.code_parser.parse_file(str(code_file))
                    if parsed_content.get("success"):
                        # Analyze style
                        style_result = await self.style_analyzer.analyze_file_style(str(code_file), parsed_content)
                        if style_result.get("success"):
                            style_analysis[str(code_file)] = style_result
                            
                            # Create style patterns
                            if style_result.get("style_consistency_score", 0) < 0.7:
                                patterns.append(CodePattern(
                                    pattern_id=f"style_{len(patterns)}",
                                    pattern_type="code_style",
                                    pattern_name="Low Style Consistency",
                                    description=f"File shows inconsistent coding style (score: {style_result.get('style_consistency_score', 0):.2f})",
                                    confidence=0.8,
                                    file_path=str(code_file),
                                    line_numbers=[],
                                    pattern_data=style_result,
                                    detected_at=datetime.now()
                                ))
                
                except Exception as e:
                    logger.warning(f"Could not analyze style for {code_file}: {str(e)}")
                    continue
            
            return {
                "success": True,
                "patterns": patterns,
                "total_patterns": len(patterns),
                "style_analysis": style_analysis,
                "files_analyzed": len(style_analysis)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing code style: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _analyze_architecture(self, project_path: Path) -> Dict[str, Any]:
        """Analyze architectural patterns and design decisions"""
        try:
            patterns = []
            
            # Look for common architectural patterns
            arch_patterns = await self._detect_architectural_patterns(project_path)
            patterns.extend(arch_patterns)
            
            return {
                "success": True,
                "patterns": patterns,
                "total_patterns": len(patterns),
                "architectural_insights": arch_patterns
            }
            
        except Exception as e:
            logger.error(f"Error analyzing architecture: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _analyze_dependencies(self, project_path: Path) -> Dict[str, Any]:
        """Analyze dependency management patterns"""
        try:
            patterns = []
            
            # Look for dependency files
            dep_files = [
                project_path / "requirements.txt",
                project_path / "pyproject.toml",
                project_path / "package.json",
                project_path / "Cargo.toml",
                project_path / "go.mod",
                project_path / "pom.xml"
            ]
            
            dependency_analysis = {}
            for dep_file in dep_files:
                if dep_file.exists():
                    dependency_analysis[str(dep_file)] = await self._analyze_dependency_file(dep_file)
            
            return {
                "success": True,
                "patterns": patterns,
                "total_patterns": len(patterns),
                "dependency_files": dependency_analysis
            }
            
        except Exception as e:
            logger.error(f"Error analyzing dependencies: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _analyze_workflow(self, project_path: Path) -> Dict[str, Any]:
        """Analyze development workflow patterns"""
        try:
            patterns = []
            
            # Look for workflow files
            workflow_files = [
                project_path / ".github",
                project_path / ".gitlab-ci.yml",
                project_path / "Jenkinsfile",
                project_path / "Makefile",
                project_path / "scripts"
            ]
            
            workflow_analysis = {}
            for workflow_path in workflow_files:
                if workflow_path.exists():
                    workflow_analysis[str(workflow_path)] = await self._analyze_workflow_path(workflow_path)
            
            return {
                "success": True,
                "patterns": patterns,
                "total_patterns": len(patterns),
                "workflow_files": workflow_analysis
            }
            
        except Exception as e:
            logger.error(f"Error analyzing workflow: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def _analyze_directory_structure(self, project_path: Path) -> List[CodePattern]:
        """Analyze directory structure patterns"""
        patterns = []
        
        # Look for common directory patterns
        dirs = [d for d in project_path.iterdir() if d.is_dir()]
        
        # Check for standard project structure
        standard_dirs = ['src', 'tests', 'docs', 'config', 'scripts']
        found_standard = [d.name for d in dirs if d.name in standard_dirs]
        
        if len(found_standard) >= 3:
            patterns.append(CodePattern(
                pattern_id="dir_standard_structure",
                pattern_type="file_structure",
                pattern_name="Standard Project Structure",
                description=f"Project follows standard directory structure: {', '.join(found_standard)}",
                confidence=0.9,
                file_path=str(project_path),
                line_numbers=[],
                pattern_data={"standard_dirs": found_standard},
                detected_at=datetime.now()
            ))
        
        return patterns
    
    async def _analyze_file_organization(self, project_path: Path) -> List[CodePattern]:
        """Analyze file organization patterns"""
        patterns = []
        
        # Count file types
        file_extensions = {}
        for file_path in project_path.rglob("*"):
            if file_path.is_file():
                ext = file_path.suffix.lower()
                file_extensions[ext] = file_extensions.get(ext, 0) + 1
        
        # Check for language diversity
        if len(file_extensions) > 5:
            patterns.append(CodePattern(
                pattern_id="file_multi_language",
                pattern_type="file_structure",
                pattern_name="Multi-Language Project",
                description=f"Project uses {len(file_extensions)} different file types",
                confidence=0.8,
                file_path=str(project_path),
                line_numbers=[],
                pattern_data={"file_types": file_extensions},
                detected_at=datetime.now()
            ))
        
        return patterns
    
    async def _analyze_file_naming(self, project_path: Path) -> List[CodePattern]:
        """Analyze file naming patterns"""
        patterns = []
        
        # Check for consistent naming
        files = [f for f in project_path.rglob("*") if f.is_file()]
        naming_patterns = {}
        
        for file_path in files:
            name = file_path.stem
            if name:
                # Simple pattern detection
                if re.match(r'^[a-z][a-z0-9_]*$', name):
                    naming_patterns['snake_case'] = naming_patterns.get('snake_case', 0) + 1
                elif re.match(r'^[a-z][a-zA-Z0-9]*$', name):
                    naming_patterns['camelCase'] = naming_patterns.get('camelCase', 0) + 1
                elif re.match(r'^[A-Z][a-zA-Z0-9]*$', name):
                    naming_patterns['PascalCase'] = naming_patterns.get('PascalCase', 0) + 1
        
        if naming_patterns:
            dominant_pattern = max(naming_patterns, key=naming_patterns.get)
            total_files = sum(naming_patterns.values())
            consistency = naming_patterns[dominant_pattern] / total_files
            
            if consistency > 0.8:
                patterns.append(CodePattern(
                    pattern_id="file_naming_consistent",
                    pattern_type="file_structure",
                    pattern_name="Consistent File Naming",
                    description=f"Project uses consistent {dominant_pattern} naming ({consistency:.1%})",
                    confidence=consistency,
                    file_path=str(project_path),
                    line_numbers=[],
                    pattern_data={"naming_patterns": naming_patterns, "dominant": dominant_pattern},
                    detected_at=datetime.now()
                ))
        
        return patterns
    
    async def _detect_architectural_patterns(self, project_path: Path) -> List[CodePattern]:
        """Detect common architectural patterns"""
        patterns = []
        
        # Look for MVC pattern
        if (project_path / "models").exists() and (project_path / "views").exists() and (project_path / "controllers").exists():
            patterns.append(CodePattern(
                pattern_id="arch_mvc",
                pattern_type="architecture",
                pattern_name="MVC Architecture",
                description="Project follows Model-View-Controller pattern",
                confidence=0.9,
                file_path=str(project_path),
                line_numbers=[],
                pattern_data={"pattern": "MVC"},
                detected_at=datetime.now()
            ))
        
        # Look for layered architecture
        if (project_path / "src").exists() and (project_path / "src" / "layers").exists():
            patterns.append(CodePattern(
                pattern_id="arch_layered",
                pattern_type="architecture",
                pattern_name="Layered Architecture",
                description="Project uses layered architecture pattern",
                confidence=0.8,
                file_path=str(project_path),
                line_numbers=[],
                pattern_data={"pattern": "Layered"},
                detected_at=datetime.now()
            ))
        
        return patterns
    
    async def _analyze_dependency_file(self, dep_file: Path) -> Dict[str, Any]:
        """Analyze a dependency file"""
        try:
            with open(dep_file, 'r') as f:
                content = f.read()
            
            return {
                "file_type": dep_file.suffix,
                "content_length": len(content),
                "line_count": len(content.splitlines()),
                "has_dependencies": len(content.strip()) > 0
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def _analyze_workflow_path(self, workflow_path: Path) -> Dict[str, Any]:
        """Analyze a workflow path"""
        try:
            if workflow_path.is_file():
                with open(workflow_path, 'r') as f:
                    content = f.read()
                return {
                    "type": "file",
                    "content_length": len(content),
                    "line_count": len(content.splitlines())
                }
            else:
                return {
                    "type": "directory",
                    "subdirectories": len([d for d in workflow_path.iterdir() if d.is_dir()]),
                    "files": len([f for f in workflow_path.iterdir() if f.is_file()])
                }
        except Exception as e:
            return {"error": str(e)}
    
    def _generate_pattern_summary(self, all_patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive pattern summary"""
        summary = {
            "total_patterns": 0,
            "pattern_distribution": {},
            "key_insights": [],
            "recommendations": []
        }
        
        # Count total patterns
        for category, data in all_patterns.items():
            if isinstance(data, dict) and data.get("success"):
                pattern_count = data.get("total_patterns", 0)
                summary["total_patterns"] += pattern_count
                summary["pattern_distribution"][category] = pattern_count
        
        # Generate insights
        if summary["total_patterns"] > 0:
            summary["key_insights"].append(f"Project shows {summary['total_patterns']} distinct patterns")
            
            if summary["pattern_distribution"].get("code_style", 0) > 0:
                summary["key_insights"].append("Code style patterns detected - consider style guide implementation")
            
            if summary["pattern_distribution"].get("architecture", 0) > 0:
                summary["key_insights"].append("Architectural patterns identified - good design practices")
        
        # Generate recommendations
        if summary["pattern_distribution"].get("code_style", 0) == 0:
            summary["recommendations"].append("Implement consistent coding style guidelines")
        
        if summary["pattern_distribution"].get("architecture", 0) == 0:
            summary["recommendations"].append("Consider documenting architectural decisions")
        
        return summary

# Example usage and testing
async def main():
    """Example usage of the PatternAnalyzer"""
    analyzer = PatternAnalyzer()
    
    # Analyze current project
    current_dir = Path.cwd()
    print(f"🔍 Analyzing patterns in: {current_dir}")
    
    result = await analyzer.analyze_project_patterns(str(current_dir))
    
    if result.get("success"):
        print("✅ Pattern analysis completed successfully!")
        print(f"📊 Total patterns found: {result.get('pattern_summary', {}).get('total_patterns', 0)}")
        print(f"📁 File structure patterns: {result.get('file_patterns', {}).get('total_patterns', 0)}")
        print(f"🎨 Code style patterns: {result.get('style_patterns', {}).get('total_patterns', 0)}")
        print(f"🏗️ Architecture patterns: {result.get('architecture_patterns', {}).get('total_patterns', 0)}")
        
        # Print key insights
        insights = result.get('pattern_summary', {}).get('key_insights', [])
        if insights:
            print("\n💡 Key Insights:")
            for insight in insights:
                print(f"  • {insight}")
        
        # Print recommendations
        recommendations = result.get('pattern_summary', {}).get('recommendations', [])
        if recommendations:
            print("\n🚀 Recommendations:")
            for rec in recommendations:
                print(f"  • {rec}")
    else:
        print(f"❌ Pattern analysis failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    asyncio.run(main())
