#!/usr/bin/env python3
"""
Project Scanner - Phase 1 of Memory Context Manager v2
Comprehensive project scanning and indexing system
"""

import os
import json
import hashlib
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@dataclass
class FileMetadata:
    """Metadata for a single file"""
    path: str
    name: str
    size: int
    modified_time: float
    file_type: str
    language: Optional[str] = None
    framework: Optional[str] = None
    purpose: Optional[str] = None
    hash: Optional[str] = None
    dependencies: List[str] = None
    imports: List[str] = None
    exports: List[str] = None

@dataclass
class DirectoryInfo:
    """Information about a directory"""
    path: str
    name: str
    file_count: int
    subdir_count: int
    total_size: int
    languages: Set[str] = None
    frameworks: Set[str] = None
    purpose: Optional[str] = None  # Add purpose attribute

@dataclass
class DependencyInfo:
    """Information about project dependencies"""
    name: str
    version: str
    type: str  # 'package', 'module', 'framework'
    source: str  # 'package.json', 'requirements.txt', etc.
    path: str

@dataclass
class ProjectIndex:
    """Complete project index"""
    project_root: str
    scan_time: float
    total_files: int
    total_directories: int
    total_size: int
    files: Dict[str, FileMetadata]
    directories: Dict[str, DirectoryInfo]
    dependencies: Dict[str, DependencyInfo]
    patterns: Dict[str, Any]
    context: Dict[str, Any]
    history: List[Dict[str, Any]]

class ProjectScanner:
    """Comprehensive project scanning and indexing system"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root).resolve()
        self.file_index: Dict[str, FileMetadata] = {}
        self.directory_index: Dict[str, DirectoryInfo] = {}
        self.dependency_index: Dict[str, DependencyInfo] = {}
        self.pattern_index: Dict[str, Any] = {}
        self.context_index: Dict[str, Any] = {}
        self.history_index: List[Dict[str, Any]] = []
        
        # Language and framework detection patterns
        self.language_patterns = {
            'python': ['.py', '.pyw', '.pyx', '.pyi'],
            'javascript': ['.js', '.jsx', '.mjs', '.cjs'],
            'typescript': ['.ts', '.tsx'],
            'java': ['.java', '.class'],
            'cpp': ['.cpp', '.cc', '.cxx', '.hpp', '.h'],
            'c': ['.c', '.h'],
            'go': ['.go'],
            'rust': ['.rs'],
            'php': ['.php'],
            'ruby': ['.rb'],
            'swift': ['.swift'],
            'kotlin': ['.kt', '.kts'],
            'scala': ['.scala'],
            'r': ['.r', '.R'],
            'matlab': ['.m', '.mat'],
            'shell': ['.sh', '.bash', '.zsh', '.fish'],
            'html': ['.html', '.htm'],
            'css': ['.css', '.scss', '.sass', '.less'],
            'sql': ['.sql'],
            'yaml': ['.yml', '.yaml'],
            'json': ['.json'],
            'xml': ['.xml'],
            'markdown': ['.md', '.markdown'],
            'docker': ['.dockerfile', 'Dockerfile'],
            'make': ['Makefile', 'makefile'],
            'cmake': ['CMakeLists.txt', '.cmake'],
            'gradle': ['build.gradle', 'build.gradle.kts'],
            'maven': ['pom.xml'],
            'npm': ['package.json', 'package-lock.json'],
            'pip': ['requirements.txt', 'pyproject.toml', 'setup.py'],
            'cargo': ['Cargo.toml', 'Cargo.lock'],
            'go_mod': ['go.mod', 'go.sum'],
            'composer': ['composer.json', 'composer.lock'],
            'gemfile': ['Gemfile', 'Gemfile.lock'],
            'podfile': ['Podfile', 'Podfile.lock'],
            'gradle_wrapper': ['gradlew', 'gradlew.bat'],
            'git': ['.gitignore', '.gitattributes', '.gitmodules'],
            'editor': ['.vscode', '.idea', '.vimrc', '.emacs'],
            'config': ['.env', '.env.local', '.env.production', 'config.json', 'config.yml'],
            'test': ['test', 'tests', 'spec', 'specs', '__tests__', '.test.', '.spec.'],
            'docs': ['docs', 'documentation', 'README', 'CHANGELOG', 'LICENSE']
        }
        
        # Framework detection patterns
        self.framework_patterns = {
            'python': {
                'django': ['django', 'manage.py', 'wsgi.py', 'urls.py'],
                'flask': ['flask', 'app.py', 'application.py'],
                'fastapi': ['fastapi', 'uvicorn', 'main.py'],
                'numpy': ['numpy', 'np.'],
                'pandas': ['pandas', 'pd.'],
                'tensorflow': ['tensorflow', 'tf.'],
                'pytorch': ['torch', 'pytorch'],
                'scikit-learn': ['sklearn', 'sklearn.'],
                'pytest': ['pytest', 'test_', 'conftest.py']
            },
            'javascript': {
                'react': ['react', 'jsx', 'tsx', 'create-react-app'],
                'vue': ['vue', 'vuex', 'nuxt'],
                'angular': ['angular', '@angular'],
                'express': ['express', 'app.use', 'router.'],
                'next': ['next', 'pages/', 'components/'],
                'gatsby': ['gatsby', 'gatsby-config.js'],
                'jest': ['jest', 'test', 'spec'],
                'webpack': ['webpack', 'webpack.config.js'],
                'babel': ['babel', 'babel.config.js', '.babelrc']
            },
            'java': {
                'spring': ['spring', '@SpringBootApplication', 'application.properties'],
                'hibernate': ['hibernate', '@Entity', '@Table'],
                'maven': ['maven', 'pom.xml'],
                'gradle': ['gradle', 'build.gradle'],
                'junit': ['junit', '@Test', 'test/']
            }
        }
        
        # Purpose detection patterns
        self.purpose_patterns = {
            'configuration': ['config', 'conf', 'settings', '.env', '.ini', '.cfg'],
            'documentation': ['readme', 'docs', 'documentation', 'changelog', 'license'],
            'testing': ['test', 'tests', 'spec', 'specs', '__tests__', '.test.', '.spec.'],
            'build': ['build', 'dist', 'target', 'out', 'bin', 'obj'],
            'source': ['src', 'source', 'lib', 'app', 'main'],
            'assets': ['assets', 'static', 'public', 'resources', 'media'],
            'scripts': ['scripts', 'tools', 'utils', 'bin'],
            'data': ['data', 'datasets', 'db', 'database', 'migrations']
        }
    
    def scan_project(self) -> ProjectIndex:
        """Comprehensive project scanning and indexing"""
        logger.info(f"🔍 Starting project scan: {self.project_root}")
        start_time = time.time()
        
        try:
            # Clear previous index
            self.file_index.clear()
            self.directory_index.clear()
            self.dependency_index.clear()
            self.pattern_index.clear()
            self.context_index.clear()
            
            # Scan file system
            self._scan_file_system()
            
            # Detect dependencies
            self._detect_dependencies()
            
            # Analyze patterns
            self._analyze_patterns()
            
            # Build context
            self._build_context()
            
            # Record scan history
            scan_duration = time.time() - start_time
            self._record_scan_history(scan_duration)
            
            # Create and return project index
            project_index = ProjectIndex(
                project_root=str(self.project_root),
                scan_time=start_time,
                total_files=len(self.file_index),
                total_directories=len(self.directory_index),
                total_size=sum(f.size for f in self.file_index.values()),
                files=self.file_index.copy(),
                directories=self.directory_index.copy(),
                dependencies=self.dependency_index.copy(),
                patterns=self.pattern_index.copy(),
                context=self.context_index.copy(),
                history=self.history_index.copy()
            )
            
            logger.info(f"✅ Project scan completed in {scan_duration:.2f}s")
            logger.info(f"📊 Indexed {len(self.file_index)} files, {len(self.directory_index)} directories")
            
            return project_index
            
        except Exception as e:
            logger.error(f"❌ Project scan failed: {str(e)}")
            raise
    
    def _scan_file_system(self):
        """Scan the file system and build file and directory indexes"""
        logger.info("📁 Scanning file system...")
        
        for root, dirs, files in os.walk(self.project_root):
            root_path = Path(root)
            relative_root = root_path.relative_to(self.project_root)
            
            # Skip common directories that don't need indexing
            dirs[:] = [d for d in dirs if not self._should_skip_directory(d)]
            
            # Process directories
            if str(relative_root) != '.':
                self._process_directory(root_path, relative_root)
            
            # Process files
            for file in files:
                if not self._should_skip_file(file):
                    file_path = root_path / file
                    relative_path = file_path.relative_to(self.project_root)
                    self._process_file(file_path, relative_path)
    
    def _should_skip_directory(self, dir_name: str) -> bool:
        """Determine if a directory should be skipped during scanning"""
        skip_patterns = {
            '.git', '.svn', '.hg',  # Version control
            '__pycache__', '.pytest_cache', '.mypy_cache',  # Python cache
            'node_modules', '.next', '.nuxt',  # Node.js
            'target', 'build', 'dist', 'out',  # Build outputs
            '.idea', '.vscode', '.vs',  # IDE files
            '.venv', 'venv', 'env', '.env',  # Virtual environments
            'tmp', 'temp', 'cache', '.cache',  # Temporary files
            'coverage', '.nyc_output',  # Test coverage
            'logs', '.logs'  # Log files
        }
        return dir_name in skip_patterns or dir_name.startswith('.')
    
    def _should_skip_file(self, file_name: str) -> bool:
        """Determine if a file should be skipped during scanning"""
        skip_patterns = {
            '.DS_Store', 'Thumbs.db',  # OS files
            '.pyc', '.pyo', '.pyd',  # Python compiled
            '.class', '.jar', '.war',  # Java compiled
            '.o', '.so', '.dll', '.dylib',  # Compiled libraries
            '.log', '.tmp', '.temp',  # Temporary files
            '.cache', '.bak', '.backup',  # Backup files
            '.swp', '.swo', '.swn',  # Vim swap files
            '.lock', '.pid'  # Lock files
        }
        return any(file_name.endswith(pattern) for pattern in skip_patterns)
    
    def _process_directory(self, dir_path: Path, relative_path: Path):
        """Process and index a directory"""
        try:
            dir_info = DirectoryInfo(
                path=str(relative_path),
                name=dir_path.name,
                file_count=0,
                subdir_count=0,
                total_size=0,
                languages=set(),
                frameworks=set(),
                purpose=None # Initialize purpose to None
            )
            
            # Count files and subdirectories
            for item in dir_path.iterdir():
                if item.is_file():
                    dir_info.file_count += 1
                    dir_info.total_size += item.stat().st_size
                elif item.is_dir():
                    dir_info.subdir_count += 1
            
            # Detect purpose
            dir_info.purpose = self._detect_purpose(dir_path)
            
            self.directory_index[str(relative_path)] = dir_info
            
        except Exception as e:
            logger.warning(f"⚠️ Failed to process directory {dir_path}: {str(e)}")
    
    def _process_file(self, file_path: Path, relative_path: Path):
        """Process and index a file"""
        try:
            stat = file_path.stat()
            
            # Detect file type and language
            file_type = self._detect_file_type(file_path)
            language = self._detect_language(file_path)
            framework = self._detect_framework(file_path, language)
            purpose = self._detect_purpose(file_path)
            
            # Calculate file hash for change detection
            file_hash = self._calculate_file_hash(file_path)
            
            # Extract dependencies and imports (basic implementation)
            dependencies = self._extract_dependencies(file_path, language)
            imports = self._extract_imports(file_path, language)
            exports = self._extract_exports(file_path, language)
            
            # Create file metadata
            file_metadata = FileMetadata(
                path=str(relative_path),
                name=file_path.name,
                size=stat.st_size,
                modified_time=stat.st_mtime,
                file_type=file_type,
                language=language,
                framework=framework,
                purpose=purpose,
                hash=file_hash,
                dependencies=dependencies or [],
                imports=imports or [],
                exports=exports or []
            )
            
            self.file_index[str(relative_path)] = file_metadata
            
            # Update directory language and framework sets
            if language:
                parent_dir = str(relative_path.parent)
                if parent_dir in self.directory_index:
                    self.directory_index[parent_dir].languages.add(language)
                if framework:
                    self.directory_index[parent_dir].frameworks.add(framework)
            
        except Exception as e:
            logger.warning(f"⚠️ Failed to process file {file_path}: {str(e)}")
    
    def _detect_file_type(self, file_path: Path) -> str:
        """Detect the type of a file"""
        suffix = file_path.suffix.lower()
        name = file_path.name.lower()
        
        # Check for special files first
        if name in ['dockerfile', 'makefile', 'readme', 'license', 'changelog']:
            return name
        
        # Check for common file types
        if suffix in ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs', '.php', '.rb']:
            return 'source_code'
        elif suffix in ['.json', '.xml', '.yaml', '.yml', '.toml', '.ini', '.cfg']:
            return 'configuration'
        elif suffix in ['.md', '.txt', '.rst', '.adoc']:
            return 'documentation'
        elif suffix in ['.html', '.css', '.scss', '.sass']:
            return 'web'
        elif suffix in ['.sql', '.db', '.sqlite']:
            return 'database'
        elif suffix in ['.sh', '.bash', '.zsh', '.fish']:
            return 'script'
        elif suffix in ['.png', '.jpg', '.jpeg', '.gif', '.svg']:
            return 'image'
        elif suffix in ['.mp4', '.avi', '.mov', '.wmv']:
            return 'video'
        elif suffix in ['.mp3', '.wav', '.flac', '.aac']:
            return 'audio'
        else:
            return 'unknown'
    
    def _detect_language(self, file_path: Path) -> Optional[str]:
        """Detect the programming language of a file"""
        suffix = file_path.suffix.lower()
        name = file_path.name.lower()
        
        for language, patterns in self.language_patterns.items():
            if suffix in patterns or name in patterns:
                return language
        
        return None
    
    def _detect_framework(self, file_path: Path, language: Optional[str]) -> Optional[str]:
        """Detect the framework being used"""
        if not language or language not in self.framework_patterns:
            return None
        
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            content_lower = content.lower()
            
            for framework, patterns in self.framework_patterns[language].items():
                for pattern in patterns:
                    if pattern.lower() in content_lower:
                        return framework
            
        except Exception:
            pass
        
        return None
    
    def _detect_purpose(self, item_path: Path) -> Optional[str]:
        """Detect the purpose of a file or directory"""
        path_str = str(item_path).lower()
        name = item_path.name.lower()
        
        for purpose, patterns in self.purpose_patterns.items():
            for pattern in patterns:
                if pattern in path_str or pattern in name:
                    return purpose
        
        return None
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate a hash of the file content for change detection"""
        try:
            hasher = hashlib.md5()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception:
            return ""
    
    def _extract_dependencies(self, file_path: Path, language: Optional[str]) -> List[str]:
        """Extract dependencies from a file (basic implementation)"""
        # This is a basic implementation - can be enhanced later
        return []
    
    def _extract_imports(self, file_path: Path, language: Optional[str]) -> List[str]:
        """Extract imports from a file (basic implementation)"""
        # This is a basic implementation - can be enhanced later
        return []
    
    def _extract_exports(self, file_path: Path, language: Optional[str]) -> List[str]:
        """Extract exports from a file (basic implementation)"""
        # This is a basic implementation - can be enhanced later
        return []
    
    def _detect_dependencies(self):
        """Detect project dependencies from package manager files"""
        logger.info("📦 Detecting dependencies...")
        
        dependency_files = [
            ('package.json', 'npm'),
            ('package-lock.json', 'npm'),
            ('requirements.txt', 'pip'),
            ('pyproject.toml', 'pip'),
            ('setup.py', 'pip'),
            ('Cargo.toml', 'cargo'),
            ('go.mod', 'go'),
            ('composer.json', 'composer'),
            ('Gemfile', 'gem'),
            ('Podfile', 'cocoapods'),
            ('build.gradle', 'gradle'),
            ('pom.xml', 'maven')
        ]
        
        for filename, package_manager in dependency_files:
            file_path = self.project_root / filename
            if file_path.exists():
                self._parse_dependency_file(file_path, package_manager)
    
    def _parse_dependency_file(self, file_path: Path, package_manager: str):
        """Parse a dependency file and extract dependency information"""
        try:
            if package_manager == 'npm':
                self._parse_npm_dependencies(file_path)
            elif package_manager == 'pip':
                self._parse_pip_dependencies(file_path)
            elif package_manager == 'cargo':
                self._parse_cargo_dependencies(file_path)
            elif package_manager == 'go':
                self._parse_go_dependencies(file_path)
            # Add more package managers as needed
            
        except Exception as e:
            logger.warning(f"⚠️ Failed to parse {file_path}: {str(e)}")
    
    def _parse_npm_dependencies(self, file_path: Path):
        """Parse npm package.json file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Parse dependencies
            for dep_type in ['dependencies', 'devDependencies', 'peerDependencies']:
                if dep_type in data:
                    for name, version in data[dep_type].items():
                        dep_info = DependencyInfo(
                            name=name,
                            version=str(version),
                            type='package',
                            source='package.json',
                            path=str(file_path)
                        )
                        self.dependency_index[f"{name}@{version}"] = dep_info
                        
        except Exception as e:
            logger.warning(f"⚠️ Failed to parse npm dependencies: {str(e)}")
    
    def _parse_pip_dependencies(self, file_path: Path):
        """Parse pip requirements.txt or pyproject.toml file"""
        try:
            if file_path.name == 'requirements.txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            # Parse requirement line (basic implementation)
                            if '==' in line:
                                name, version = line.split('==', 1)
                            elif '>=' in line:
                                name, version = line.split('>=', 1)
                            else:
                                name, version = line, 'unknown'
                            
                            dep_info = DependencyInfo(
                                name=name.strip(),
                                version=version.strip(),
                                type='package',
                                source='requirements.txt',
                                path=str(file_path)
                            )
                            self.dependency_index[f"{name}@{version}"] = dep_info
            
            elif file_path.name == 'pyproject.toml':
                # Basic TOML parsing (can be enhanced with proper TOML library)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Simple regex-based parsing for now
                    import re
                    deps_match = re.search(r'\[project\.dependencies\]\s*\n(.*?)(?=\n\[|\n$)', content, re.DOTALL)
                    if deps_match:
                        deps_content = deps_match.group(1)
                        for line in deps_content.split('\n'):
                            line = line.strip()
                            if '=' in line and not line.startswith('#'):
                                name, version = line.split('=', 1)
                                dep_info = DependencyInfo(
                                    name=name.strip().strip('"'),
                                    version=version.strip().strip('"'),
                                    type='package',
                                    source='pyproject.toml',
                                    path=str(file_path)
                                )
                                self.dependency_index[f"{name}@{version}"] = dep_info
                                
        except Exception as e:
            logger.warning(f"⚠️ Failed to parse pip dependencies: {str(e)}")
    
    def _parse_cargo_dependencies(self, file_path: Path):
        """Parse Cargo.toml file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic TOML parsing for dependencies
            import re
            deps_match = re.search(r'\[dependencies\]\s*\n(.*?)(?=\n\[|\n$)', content, re.DOTALL)
            if deps_match:
                deps_content = deps_match.group(1)
                for line in deps_content.split('\n'):
                    line = line.strip()
                    if '=' in line and not line.startswith('#'):
                        name, version = line.split('=', 1)
                        dep_info = DependencyInfo(
                            name=name.strip(),
                            version=version.strip().strip('"'),
                            type='package',
                            source='Cargo.toml',
                            path=str(file_path)
                        )
                        self.dependency_index[f"{name}@{version}"] = dep_info
                        
        except Exception as e:
            logger.warning(f"⚠️ Failed to parse cargo dependencies: {str(e)}")
    
    def _parse_go_dependencies(self, file_path: Path):
        """Parse go.mod file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('require '):
                        # Parse require line
                        parts = line.split()
                        if len(parts) >= 3:
                            name = parts[1]
                            version = parts[2]
                            
                            dep_info = DependencyInfo(
                                name=name,
                                version=version,
                                type='package',
                                source='go.mod',
                                path=str(file_path)
                            )
                            self.dependency_index[f"{name}@{version}"] = dep_info
                            
        except Exception as e:
            logger.warning(f"⚠️ Failed to parse go dependencies: {str(e)}")
    
    def _analyze_patterns(self):
        """Analyze code patterns and project structure"""
        logger.info("🔍 Analyzing patterns...")
        
        # Language distribution
        language_counts = {}
        for file_meta in self.file_index.values():
            if file_meta.language:
                language_counts[file_meta.language] = language_counts.get(file_meta.language, 0) + 1
        
        # Framework distribution
        framework_counts = {}
        for file_meta in self.file_index.values():
            if file_meta.framework:
                framework_counts[file_meta.framework] = framework_counts.get(file_meta.framework, 0) + 1
        
        # File type distribution
        file_type_counts = {}
        for file_meta in self.file_index.values():
            file_type_counts[file_meta.file_type] = file_type_counts.get(file_meta.file_type, 0) + 1
        
        # Purpose distribution
        purpose_counts = {}
        for file_meta in self.file_index.values():
            if file_meta.purpose:
                purpose_counts[file_meta.purpose] = purpose_counts.get(file_meta.purpose, 0) + 1
        
        self.pattern_index = {
            'languages': language_counts,
            'frameworks': framework_counts,
            'file_types': file_type_counts,
            'purposes': purpose_counts,
            'total_files': len(self.file_index),
            'total_directories': len(self.directory_index),
            'total_dependencies': len(self.dependency_index)
        }
    
    def _build_context(self):
        """Build project context and metadata"""
        logger.info("🏗️ Building project context...")
        
        # Project metadata
        self.context_index = {
            'project_name': self.project_root.name,
            'project_root': str(self.project_root),
            'scan_timestamp': datetime.now().isoformat(),
            'technology_stack': self._identify_technology_stack(),
            'project_structure': self._analyze_project_structure(),
            'development_environment': self._detect_development_environment(),
            'build_system': self._detect_build_system(),
            'version_control': self._detect_version_control()
        }
    
    def _identify_technology_stack(self) -> Dict[str, Any]:
        """Identify the technology stack being used"""
        stack = {
            'languages': list(self.pattern_index.get('languages', {}).keys()),
            'frameworks': list(self.pattern_index.get('frameworks', {}).keys()),
            'package_managers': list(set(dep.source for dep in self.dependency_index.values())),
            'databases': [],
            'deployment': [],
            'testing': [],
            'build_tools': []
        }
        
        # Detect databases
        for file_meta in self.file_index.values():
            if file_meta.purpose == 'database':
                stack['databases'].append(file_meta.language or 'unknown')
        
        # Detect testing frameworks
        for file_meta in self.file_index.values():
            if file_meta.purpose == 'testing':
                stack['testing'].append(file_meta.language or 'unknown')
        
        # Detect build tools
        for file_meta in self.file_index.values():
            if file_meta.file_type in ['make', 'cmake', 'gradle', 'maven']:
                stack['build_tools'].append(file_meta.file_type)
        
        return stack
    
    def _analyze_project_structure(self) -> Dict[str, Any]:
        """Analyze the overall project structure"""
        structure = {
            'depth': 0,
            'main_directories': [],
            'source_directories': [],
            'test_directories': [],
            'documentation_directories': [],
            'configuration_files': []
        }
        
        # Calculate max depth
        max_depth = 0
        for file_path in self.file_index.keys():
            depth = len(Path(file_path).parts)
            max_depth = max(max_depth, depth)
        structure['depth'] = max_depth
        
        # Categorize directories
        for dir_path, dir_info in self.directory_index.items():
            if dir_info.purpose == 'source':
                structure['source_directories'].append(dir_path)
            elif dir_info.purpose == 'testing':
                structure['test_directories'].append(dir_path)
            elif dir_info.purpose == 'documentation':
                structure['documentation_directories'].append(dir_path)
            elif dir_info.purpose == 'configuration':
                structure['configuration_files'].append(dir_path)
        
        return structure
    
    def _detect_development_environment(self) -> Dict[str, Any]:
        """Detect the development environment and tools"""
        env = {
            'ide_files': [],
            'editor_configs': [],
            'linters': [],
            'formatters': []
        }
        
        # Detect IDE and editor files
        for file_meta in self.file_index.values():
            if file_meta.file_type == 'editor':
                env['ide_files'].append(file_meta.path)
            elif file_meta.name in ['.editorconfig', '.prettierrc', '.eslintrc']:
                env['editor_configs'].append(file_meta.path)
        
        return env
    
    def _detect_build_system(self) -> Dict[str, Any]:
        """Detect the build system and tools"""
        build = {
            'build_files': [],
            'scripts': [],
            'output_directories': []
        }
        
        # Detect build files
        for file_meta in self.file_index.values():
            if file_meta.file_type in ['make', 'cmake', 'gradle', 'maven']:
                build['build_files'].append(file_meta.path)
            elif file_meta.purpose == 'build':
                build['output_directories'].append(file_meta.path)
        
        return build
    
    def _detect_version_control(self) -> Dict[str, Any]:
        """Detect version control system and configuration"""
        vcs = {
            'system': 'unknown',
            'config_files': [],
            'ignore_files': []
        }
        
        # Check for Git
        git_dir = self.project_root / '.git'
        if git_dir.exists():
            vcs['system'] = 'git'
            vcs['config_files'].append('.git/config')
            
            # Check for .gitignore
            gitignore = self.project_root / '.gitignore'
            if gitignore.exists():
                vcs['ignore_files'].append('.gitignore')
        
        return vcs
    
    def _record_scan_history(self, scan_duration: float):
        """Record scan history for tracking and analysis"""
        scan_record = {
            'timestamp': datetime.now().isoformat(),
            'duration': scan_duration,
            'files_scanned': len(self.file_index),
            'directories_scanned': len(self.directory_index),
            'dependencies_found': len(self.dependency_index),
            'patterns_analyzed': len(self.pattern_index),
            'context_built': len(self.context_index)
        }
        
        self.history_index.append(scan_record)
        
        # Keep only last 10 scans
        if len(self.history_index) > 10:
            self.history_index = self.history_index[-10:]
    
    def detect_changes(self) -> List[Dict[str, Any]]:
        """Detect changes in the project since last scan"""
        logger.info("🔄 Detecting changes...")
        
        changes = []
        
        for file_path, file_meta in self.file_index.items():
            full_path = self.project_root / file_path
            
            if full_path.exists():
                # Check if file has changed
                current_hash = self._calculate_file_hash(full_path)
                if current_hash != file_meta.hash:
                    changes.append({
                        'type': 'modified',
                        'path': file_path,
                        'old_hash': file_meta.hash,
                        'new_hash': current_hash,
                        'timestamp': datetime.now().isoformat()
                    })
            else:
                # File was deleted
                changes.append({
                    'type': 'deleted',
                    'path': file_path,
                    'timestamp': datetime.now().isoformat()
                })
        
        return changes
    
    def build_dependency_graph(self) -> Dict[str, Any]:
        """Build a dependency graph showing relationships"""
        logger.info("🔗 Building dependency graph...")
        
        graph = {
            'nodes': [],
            'edges': [],
            'packages': {},
            'relationships': {}
        }
        
        # Add dependency nodes
        for dep_id, dep_info in self.dependency_index.items():
            graph['nodes'].append({
                'id': dep_id,
                'name': dep_info.name,
                'version': dep_info.version,
                'type': dep_info.type,
                'source': dep_info.source
            })
            
            graph['packages'][dep_id] = {
                'name': dep_info.name,
                'version': dep_info.version,
                'type': dep_info.type,
                'source': dep_info.source
            }
        
        # Add file nodes
        for file_path, file_meta in self.file_index.items():
            if file_meta.language:
                graph['nodes'].append({
                    'id': f"file:{file_path}",
                    'name': file_meta.name,
                    'type': 'file',
                    'language': file_meta.language,
                    'framework': file_meta.framework
                })
        
        return graph
    
    def export_index(self, format: str = 'json') -> str:
        """Export the project index in various formats"""
        if format == 'json':
            # Convert sets to lists for JSON serialization
            index_data = asdict(self.get_current_index())
            self._convert_sets_to_lists(index_data)
            return json.dumps(index_data, indent=2)
        elif format == 'summary':
            return self._generate_summary()
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _convert_sets_to_lists(self, obj):
        """Recursively convert sets to lists for JSON serialization"""
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, set):
                    obj[key] = list(value)
                elif isinstance(value, (dict, list)):
                    self._convert_sets_to_lists(value)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                if isinstance(item, set):
                    obj[i] = list(item)
                elif isinstance(item, (dict, list)):
                    self._convert_sets_to_lists(item)
    
    def _generate_summary(self) -> str:
        """Generate a human-readable summary of the project"""
        index = self.get_current_index()
        
        summary = f"""
# Project Index Summary

## 📁 Project Overview
- **Name**: {index.context.get('project_name', 'Unknown')}
- **Root**: {index.project_root}
- **Scan Time**: {datetime.fromtimestamp(index.scan_time).strftime('%Y-%m-%d %H:%M:%S')}

## 📊 Statistics
- **Total Files**: {index.total_files}
- **Total Directories**: {index.total_directories}
- **Total Size**: {index.total_size:,} bytes
- **Dependencies**: {len(index.dependencies)}

## 🗣️ Languages
{self._format_language_summary()}

## 🏗️ Frameworks
{self._format_framework_summary()}

## 📦 Dependencies
{self._format_dependency_summary()}

## 🎯 Project Structure
{self._format_structure_summary()}
"""
        return summary
    
    def _format_language_summary(self) -> str:
        """Format language summary for display"""
        languages = self.pattern_index.get('languages', {})
        if not languages:
            return "- No programming languages detected"
        
        lines = []
        for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / self.pattern_index['total_files']) * 100
            lines.append(f"- **{lang}**: {count} files ({percentage:.1f}%)")
        
        return '\n'.join(lines)
    
    def _format_framework_summary(self) -> str:
        """Format framework summary for display"""
        frameworks = self.pattern_index.get('frameworks', {})
        if not frameworks:
            return "- No frameworks detected"
        
        lines = []
        for framework, count in sorted(frameworks.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"- **{framework}**: {count} files")
        
        return '\n'.join(lines)
    
    def _format_dependency_summary(self) -> str:
        """Format dependency summary for display"""
        if not self.dependency_index:
            return "- No dependencies detected"
        
        # Group by source
        by_source = {}
        for dep in self.dependency_index.values():
            if dep.source not in by_source:
                by_source[dep.source] = []
            by_source[dep.source].append(dep)
        
        lines = []
        for source, deps in by_source.items():
            lines.append(f"- **{source}**: {len(deps)} dependencies")
            for dep in deps[:5]:  # Show first 5
                lines.append(f"  - {dep.name}@{dep.version}")
            if len(deps) > 5:
                lines.append(f"  - ... and {len(deps) - 5} more")
        
        return '\n'.join(lines)
    
    def _format_structure_summary(self) -> str:
        """Format project structure summary for display"""
        structure = self.context_index.get('project_structure', {})
        
        lines = []
        lines.append(f"- **Depth**: {structure.get('depth', 0)} levels")
        lines.append(f"- **Source Directories**: {len(structure.get('source_directories', []))}")
        lines.append(f"- **Test Directories**: {len(structure.get('test_directories', []))}")
        lines.append(f"- **Documentation**: {len(structure.get('documentation_directories', []))}")
        
        return '\n'.join(lines)
    
    def get_current_index(self) -> ProjectIndex:
        """Get the current project index"""
        return ProjectIndex(
            project_root=str(self.project_root),
            scan_time=time.time(),
            total_files=len(self.file_index),
            total_directories=len(self.directory_index),
            total_size=sum(f.size for f in self.file_index.values()),
            files=self.file_index.copy(),
            directories=self.directory_index.copy(),
            dependencies=self.dependency_index.copy(),
            patterns=self.pattern_index.copy(),
            context=self.context_index.copy(),
            history=self.history_index.copy()
        )


def main():
    """Main function for testing the project scanner"""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python project_scanner.py <project_root>")
        sys.exit(1)
    
    project_root = sys.argv[1]
    
    if not os.path.exists(project_root):
        print(f"Error: Project root '{project_root}' does not exist")
        sys.exit(1)
    
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Create scanner and scan project
    scanner = ProjectScanner(project_root)
    
    try:
        print(f"🔍 Scanning project: {project_root}")
        project_index = scanner.scan_project()
        
        # Export results
        print("\n📊 Project Index Summary:")
        print(scanner._generate_summary())
        
        # Save detailed index to file
        output_file = f"project_index_{int(time.time())}.json"
        with open(output_file, 'w') as f:
            f.write(scanner.export_index('json'))
        print(f"\n💾 Detailed index saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error scanning project: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
