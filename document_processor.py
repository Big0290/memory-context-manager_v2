"""
Document Processor for Enhanced Learning
Processes documents, websites, and content for intelligent summarization and storage
"""

import asyncio
import aiohttp
import logging
import re
import hashlib
from typing import Dict, Any, List, Optional, Tuple
from urllib.parse import urlparse, urljoin
from pathlib import Path
import mimetypes

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Advanced document processor for learning system"""
    
    def __init__(self):
        self.session = None
        self.max_content_length = 10 * 1024 * 1024  # 10MB limit
        self.supported_text_types = {
            'text/plain', 'text/markdown', 'text/html', 'text/css', 'text/javascript',
            'application/json', 'application/xml', 'text/xml', 'application/yaml'
        }
        self.supported_code_extensions = {
            '.py', '.js', '.ts', '.html', '.css', '.md', '.txt', '.json', '.yaml', '.yml',
            '.xml', '.sql', '.sh', '.bash', '.dockerfile', '.gitignore', '.env'
        }
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                'User-Agent': 'Brain-AI-Learning-System/1.0 (Document Processor)'
            }
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def process_content(self, source: str, content_type: str = "auto") -> Dict[str, Any]:
        """
        Process content from various sources (URL, file path, or raw text)
        
        Args:
            source: URL, file path, or raw content
            content_type: "url", "file", "text", or "auto" to detect
            
        Returns:
            Dict with processed content, metadata, and categorization
        """
        try:
            # Detect content type if auto
            if content_type == "auto":
                content_type = self._detect_content_type(source)
            
            # Extract content based on type
            if content_type == "url":
                content_data = await self._process_url(source)
            elif content_type == "file":
                content_data = await self._process_file(source)
            else:  # text
                content_data = await self._process_text(source)
            
            if not content_data or not content_data.get("content"):
                return {"success": False, "error": "No content extracted"}
            
            # Generate content hash for deduplication
            content_hash = hashlib.md5(content_data["content"].encode()).hexdigest()
            
            # Enhanced metadata
            metadata = {
                "source": source,
                "content_type": content_type,
                "content_hash": content_hash,
                "content_length": len(content_data["content"]),
                "extraction_method": content_data.get("method", "unknown"),
                "timestamp": content_data.get("timestamp"),
                "title": content_data.get("title", ""),
                "language": self._detect_language(content_data["content"]),
                "complexity": self._assess_complexity(content_data["content"])
            }
            
            # Intelligent categorization
            category = self._categorize_content(content_data["content"], metadata)
            
            return {
                "success": True,
                "content": content_data["content"],
                "metadata": metadata,
                "category": category,
                "ready_for_summarization": True
            }
            
        except Exception as e:
            logger.error(f"Content processing failed: {e}")
            return {"success": False, "error": str(e)}
    
    def _detect_content_type(self, source: str) -> str:
        """Detect if source is URL, file path, or raw text"""
        # Check if it's a URL
        if source.startswith(('http://', 'https://')):
            return "url"
        
        # Check if it's a file path
        if Path(source).exists() or any(source.endswith(ext) for ext in self.supported_code_extensions):
            return "file"
        
        # Default to text
        return "text"
    
    async def _process_url(self, url: str) -> Dict[str, Any]:
        """Extract and process content from URL"""
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            async with self.session.get(url) as response:
                if response.status != 200:
                    raise Exception(f"HTTP {response.status}: {await response.text()}")
                
                # Check content type
                content_type = response.headers.get('content-type', '').lower()
                content_length = int(response.headers.get('content-length', 0))
                
                if content_length > self.max_content_length:
                    raise Exception(f"Content too large: {content_length} bytes")
                
                # Read content
                content = await response.text()
                
                # Extract title and clean content based on type
                if 'text/html' in content_type:
                    title, clean_content = self._process_html(content)
                else:
                    title = urlparse(url).path.split('/')[-1] or url
                    clean_content = content
                
                return {
                    "content": clean_content,
                    "title": title,
                    "method": "web_extraction",
                    "timestamp": response.headers.get('date'),
                    "url": url,
                    "content_type": content_type
                }
                
        except Exception as e:
            logger.error(f"URL processing failed for {url}: {e}")
            raise
    
    async def _process_file(self, file_path: str) -> Dict[str, Any]:
        """Extract and process content from file"""
        try:
            path = Path(file_path)
            
            if not path.exists():
                raise Exception(f"File not found: {file_path}")
            
            if path.stat().st_size > self.max_content_length:
                raise Exception(f"File too large: {path.stat().st_size} bytes")
            
            # Detect MIME type
            mime_type, _ = mimetypes.guess_type(file_path)
            
            # Read content based on file type
            if mime_type and mime_type.startswith('text/') or path.suffix in self.supported_code_extensions:
                content = path.read_text(encoding='utf-8', errors='ignore')
            else:
                raise Exception(f"Unsupported file type: {mime_type}")
            
            return {
                "content": content,
                "title": path.name,
                "method": "file_extraction",
                "timestamp": path.stat().st_mtime,
                "file_path": str(path),
                "mime_type": mime_type
            }
            
        except Exception as e:
            logger.error(f"File processing failed for {file_path}: {e}")
            raise
    
    async def _process_text(self, text: str) -> Dict[str, Any]:
        """Process raw text content"""
        return {
            "content": text.strip(),
            "title": text[:50] + "..." if len(text) > 50 else text,
            "method": "direct_text",
            "timestamp": None
        }
    
    def _process_html(self, html_content: str) -> Tuple[str, str]:
        """Extract title and clean text from HTML"""
        # Extract title
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else "Webpage"
        
        # Remove scripts, styles, and comments
        clean_html = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)
        clean_html = re.sub(r'<style[^>]*>.*?</style>', '', clean_html, flags=re.DOTALL | re.IGNORECASE)
        clean_html = re.sub(r'<!--.*?-->', '', clean_html, flags=re.DOTALL)
        
        # Extract text content
        text_content = re.sub(r'<[^>]+>', ' ', clean_html)
        text_content = re.sub(r'\s+', ' ', text_content).strip()
        
        return title, text_content
    
    def _detect_language(self, content: str) -> str:
        """Detect content language (simple heuristic)"""
        # Simple language detection based on common patterns
        if re.search(r'(function|class|import|export|const|let|var)', content):
            return "javascript"
        elif re.search(r'(def |class |import |from )', content):
            return "python"  
        elif re.search(r'(<html|<div|<p>|</div>)', content, re.IGNORECASE):
            return "html"
        elif re.search(r'(SELECT|INSERT|UPDATE|DELETE)', content, re.IGNORECASE):
            return "sql"
        else:
            return "natural_language"
    
    def _assess_complexity(self, content: str) -> str:
        """Assess content complexity"""
        word_count = len(content.split())
        
        if word_count < 100:
            return "simple"
        elif word_count < 1000:
            return "moderate"  
        elif word_count < 5000:
            return "complex"
        else:
            return "very_complex"
    
    def _categorize_content(self, content: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Intelligently categorize content"""
        content_lower = content.lower()
        language = metadata.get("language", "")
        source = metadata.get("source", "")
        
        # Primary category
        primary_category = "general"
        confidence = 0.5
        
        # Technical content
        if language in ["python", "javascript", "html", "sql"]:
            primary_category = "technical"
            confidence = 0.9
        elif any(word in content_lower for word in ["code", "programming", "software", "development", "api"]):
            primary_category = "technical"
            confidence = 0.7
        
        # Documentation
        elif any(word in content_lower for word in ["documentation", "tutorial", "guide", "how to", "instructions"]):
            primary_category = "documentation"
            confidence = 0.8
        
        # Business/Professional
        elif any(word in content_lower for word in ["business", "strategy", "management", "project", "meeting"]):
            primary_category = "business"
            confidence = 0.7
        
        # Research/Academic  
        elif any(word in content_lower for word in ["research", "study", "analysis", "paper", "academic"]):
            primary_category = "research"
            confidence = 0.7
        
        # AI/ML specific
        elif any(word in content_lower for word in ["machine learning", "artificial intelligence", "neural network", "deep learning", "ai"]):
            primary_category = "ai_ml"
            confidence = 0.8
        
        # Secondary tags
        tags = []
        if "learning" in content_lower:
            tags.append("learning")
        if "memory" in content_lower:
            tags.append("memory")
        if "brain" in content_lower:
            tags.append("cognitive")
        if any(word in content_lower for word in ["important", "critical", "urgent"]):
            tags.append("high_priority")
        
        return {
            "primary": primary_category,
            "confidence": confidence,
            "tags": tags,
            "emotional_weight": "high" if "high_priority" in tags else "medium"
        }

class LLMSummarizer:
    """LLM-powered content summarization and analysis"""
    
    def __init__(self, llm_client):
        self.llm = llm_client
    
    async def summarize_and_analyze(self, content: str, metadata: Dict[str, Any], 
                                  category: Dict[str, Any]) -> Dict[str, Any]:
        """Generate intelligent summary and analysis of content"""
        try:
            # Create context-aware prompt
            prompt = self._create_summarization_prompt(content, metadata, category)
            
            # Generate summary using LLM
            summary_result = await self.llm.generate_response(
                prompt=prompt,
                system_prompt=self._get_summarization_system_prompt(),
                temperature=0.3,  # Lower temperature for consistent summaries
                max_tokens=800   # Longer for comprehensive summaries
            )
            
            if not summary_result.get("success"):
                return {"success": False, "error": "LLM summarization failed"}
            
            summary_text = summary_result["response"]
            
            # Parse structured summary if possible
            parsed_summary = self._parse_summary_response(summary_text)
            
            return {
                "success": True,
                "summary": parsed_summary.get("summary", summary_text),
                "key_points": parsed_summary.get("key_points", []),
                "relevance_score": parsed_summary.get("relevance", 0.7),
                "learning_value": parsed_summary.get("learning_value", "medium"),
                "recommended_tags": parsed_summary.get("tags", category.get("tags", [])),
                "emotional_weight": parsed_summary.get("emotional_weight", category.get("emotional_weight", "medium")),
                "full_analysis": summary_text
            }
            
        except Exception as e:
            logger.error(f"LLM summarization failed: {e}")
            return {"success": False, "error": str(e)}
    
    def _create_summarization_prompt(self, content: str, metadata: Dict[str, Any], 
                                   category: Dict[str, Any]) -> str:
        """Create intelligent summarization prompt"""
        content_preview = content[:2000] + "..." if len(content) > 2000 else content
        
        return f"""Analyze and summarize this content for a brain-inspired AI memory system:

**Content Metadata:**
- Source: {metadata.get('source', 'Unknown')}
- Type: {metadata.get('language', 'Unknown')}
- Category: {category.get('primary', 'general')} (confidence: {category.get('confidence', 0.5)})
- Complexity: {metadata.get('complexity', 'unknown')}
- Length: {metadata.get('content_length', 0)} characters

**Content to Analyze:**
{content_preview}

Please provide a structured analysis including:
1. **Summary**: Concise 2-3 sentence summary of main points
2. **Key Points**: 3-5 bullet points of most important information
3. **Relevance**: How relevant is this for future reference (0.1-1.0)
4. **Learning Value**: low/medium/high - educational value
5. **Emotional Weight**: low/medium/high/critical - importance level
6. **Tags**: 3-5 descriptive tags for categorization
7. **Application**: How might this knowledge be applied in future conversations

Focus on extracting actionable insights and knowledge that would be valuable for future reference."""

    def _get_summarization_system_prompt(self) -> str:
        """System prompt for summarization"""
        return """You are an intelligent content analyst for a brain-inspired AI system. Your role is to:

1. **Extract Core Knowledge**: Identify the most valuable information for future reference
2. **Categorize Intelligently**: Assign appropriate categories and emotional weights
3. **Summarize Concisely**: Create clear, actionable summaries
4. **Think Long-term**: Consider how this knowledge might be useful in future conversations
5. **Be Practical**: Focus on information that can be applied or referenced later

Respond in a structured format that can be easily parsed and stored in the memory system. Be concise but comprehensive."""
    
    def _parse_summary_response(self, response: str) -> Dict[str, Any]:
        """Parse structured summary response"""
        parsed = {}
        
        # Extract summary
        summary_match = re.search(r'(?:\*\*Summary\*\*|Summary):?\s*([^\n]+(?:\n[^\*\n]+)*)', response, re.IGNORECASE)
        if summary_match:
            parsed["summary"] = summary_match.group(1).strip()
        
        # Extract key points
        key_points_match = re.search(r'(?:\*\*Key Points\*\*|Key Points):?\s*\n?((?:[-•*]\s*[^\n]+\n?)+)', response, re.IGNORECASE)
        if key_points_match:
            points_text = key_points_match.group(1)
            parsed["key_points"] = [
                re.sub(r'^[-•*]\s*', '', point.strip()) 
                for point in points_text.split('\n') 
                if point.strip() and re.match(r'^[-•*]\s*', point.strip())
            ]
        
        # Extract relevance
        relevance_match = re.search(r'(?:\*\*Relevance\*\*|Relevance):?\s*([0-9.]+)', response, re.IGNORECASE)
        if relevance_match:
            parsed["relevance"] = float(relevance_match.group(1))
        
        # Extract learning value
        learning_match = re.search(r'(?:\*\*Learning Value\*\*|Learning Value):?\s*(\w+)', response, re.IGNORECASE)
        if learning_match:
            parsed["learning_value"] = learning_match.group(1).lower()
        
        # Extract emotional weight
        emotional_match = re.search(r'(?:\*\*Emotional Weight\*\*|Emotional Weight):?\s*(\w+)', response, re.IGNORECASE)
        if emotional_match:
            parsed["emotional_weight"] = emotional_match.group(1).lower()
        
        # Extract tags
        tags_match = re.search(r'(?:\*\*Tags\*\*|Tags):?\s*([^\n]+)', response, re.IGNORECASE)
        if tags_match:
            tags_text = tags_match.group(1)
            parsed["tags"] = [tag.strip().lower() for tag in re.split(r'[,;]', tags_text) if tag.strip()]
        
        return parsed

# Global instances
_document_processor = None
_llm_summarizer = None

async def get_document_processor() -> DocumentProcessor:
    """Get global document processor instance"""
    global _document_processor
    if _document_processor is None:
        _document_processor = DocumentProcessor()
    return _document_processor

async def get_llm_summarizer():
    """Get LLM summarizer instance"""
    global _llm_summarizer
    if _llm_summarizer is None:
        from llm_client import get_llm_client
        llm = await get_llm_client()
        _llm_summarizer = LLMSummarizer(llm.ollama)
    return _llm_summarizer