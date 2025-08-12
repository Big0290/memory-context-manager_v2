#!/usr/bin/env python3
"""
Demo: Project Scanner Integration with MCP System
Shows how the project scanner works and integrates with our consolidated tools
"""

import json
import time
from pathlib import Path
from project_scanner import ProjectScanner

def demo_project_scanning():
    """Demonstrate the project scanner capabilities"""
    print("🚀 PROJECT SCANNER DEMO - Phase 1 Implementation")
    print("=" * 60)
    
    # Initialize scanner for current project
    current_dir = Path.cwd()
    scanner = ProjectScanner(str(current_dir))
    
    print(f"📁 Project: {current_dir.name}")
    print(f"📍 Location: {current_dir}")
    print()
    
    # Perform comprehensive scan
    print("🔍 Starting comprehensive project scan...")
    start_time = time.time()
    
    try:
        project_index = scanner.scan_project()
        scan_duration = time.time() - start_time
        
        print(f"✅ Scan completed in {scan_duration:.2f} seconds")
        print()
        
        # Display summary
        print("📊 PROJECT INDEX SUMMARY")
        print("-" * 40)
        print(f"📁 Total Files: {project_index.total_files}")
        print(f"📂 Total Directories: {project_index.total_directories}")
        print(f"💾 Total Size: {project_index.total_size:,} bytes")
        print(f"🔗 Dependencies: {len(project_index.dependencies)}")
        print()
        
        # Language breakdown
        print("🗣️ LANGUAGE BREAKDOWN")
        print("-" * 40)
        languages = project_index.patterns.get('languages', {})
        for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / project_index.total_files) * 100
            print(f"  {lang:12} : {count:3d} files ({percentage:5.1f}%)")
        print()
        
        # Framework detection
        print("🏗️ FRAMEWORK DETECTION")
        print("-" * 40)
        frameworks = project_index.patterns.get('frameworks', {})
        if frameworks:
            for framework, count in sorted(frameworks.items(), key=lambda x: x[1], reverse=True):
                print(f"  {framework:15} : {count:3d} files")
        else:
            print("  No frameworks detected")
        print()
        
        # File type analysis
        print("📄 FILE TYPE ANALYSIS")
        print("-" * 40)
        file_types = project_index.patterns.get('file_types', {})
        for file_type, count in sorted(file_types.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / project_index.total_files) * 100
            print(f"  {file_type:15} : {count:3d} files ({percentage:5.1f}%)")
        print()
        
        # Project structure
        print("🎯 PROJECT STRUCTURE")
        print("-" * 40)
        structure = project_index.context.get('project_structure', {})
        print(f"  Depth: {structure.get('depth', 0)} levels")
        print(f"  Source Directories: {len(structure.get('source_directories', []))}")
        print(f"  Test Directories: {len(structure.get('test_directories', []))}")
        print(f"  Documentation: {len(structure.get('documentation_directories', []))}")
        print()
        
        # Technology stack
        print("🔧 TECHNOLOGY STACK")
        print("-" * 40)
        tech_stack = project_index.context.get('technology_stack', {})
        print(f"  Languages: {', '.join(tech_stack.get('languages', []))}")
        print(f"  Frameworks: {', '.join(tech_stack.get('frameworks', []))}")
        print(f"  Package Managers: {', '.join(tech_stack.get('package_managers', []))}")
        print(f"  Build Tools: {', '.join(tech_stack.get('build_tools', []))}")
        print()
        
        # Sample files by category
        print("📋 SAMPLE FILES BY CATEGORY")
        print("-" * 40)
        
        # Python files
        python_files = [f for f in project_index.files.values() if f.language == 'python']
        if python_files:
            print(f"🐍 Python Files (showing first 5):")
            for file in python_files[:5]:
                print(f"    {file.path}")
            if len(python_files) > 5:
                print(f"    ... and {len(python_files) - 5} more")
            print()
        
        # Documentation files
        doc_files = [f for f in project_index.files.values() if f.file_type == 'documentation']
        if doc_files:
            print(f"📚 Documentation Files (showing first 5):")
            for file in doc_files[:5]:
                print(f"    {file.path}")
            if len(doc_files) > 5:
                print(f"    ... and {len(doc_files) - 5} more")
            print()
        
        # Configuration files
        config_files = [f for f in project_index.files.values() if f.file_type == 'configuration']
        if config_files:
            print(f"⚙️ Configuration Files:")
            for file in config_files:
                print(f"    {file.path}")
            print()
        
        # Change detection demo
        print("🔄 CHANGE DETECTION DEMO")
        print("-" * 40)
        print("Scanning for changes since last scan...")
        changes = scanner.detect_changes()
        if changes:
            print(f"Found {len(changes)} changes:")
            for change in changes[:3]:  # Show first 3 changes
                print(f"  {change['type']}: {change['path']}")
            if len(changes) > 3:
                print(f"  ... and {len(changes) - 3} more changes")
        else:
            print("No changes detected")
        print()
        
        # Export capabilities
        print("💾 EXPORT CAPABILITIES")
        print("-" * 40)
        
        # JSON export
        json_export = scanner.export_index('json')
        print(f"JSON Export: {len(json_export):,} characters")
        
        # Summary export
        summary_export = scanner.export_index('summary')
        print(f"Summary Export: {len(summary_export):,} characters")
        print()
        
        # Performance metrics
        print("📈 PERFORMANCE METRICS")
        print("-" * 40)
        print(f"Scan Speed: {project_index.total_files / scan_duration:.1f} files/second")
        print(f"Memory Efficiency: {len(json_export) / project_index.total_files:.1f} chars/file")
        print(f"Index Size: {len(json_export):,} characters")
        print()
        
        # Integration points
        print("🔌 INTEGRATION POINTS")
        print("-" * 40)
        print("✅ Ready for MCP tool integration")
        print("✅ Ready for context injection")
        print("✅ Ready for dependency analysis")
        print("✅ Ready for pattern learning")
        print("✅ Ready for change tracking")
        print()
        
        print("🎉 PROJECT SCANNER DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
        return project_index
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        return None

def demo_mcp_integration():
    """Show how this integrates with our MCP system"""
    print("\n🔗 MCP INTEGRATION DEMO")
    print("=" * 40)
    
    print("This project scanner is designed to integrate with our consolidated MCP tools:")
    print()
    
    print("🧠 PERCEPTION & INPUT Domain:")
    print("  - perceive_and_analyze(action='project_scan')")
    print("  - perceive_and_analyze(action='dependency_analysis')")
    print("  - perceive_and_analyze(action='pattern_recognition')")
    print()
    
    print("🧠 MEMORY & STORAGE Domain:")
    print("  - memory_and_storage(action='store_project_context')")
    print("  - memory_and_storage(action='retrieve_project_info')")
    print("  - memory_and_storage(action='update_project_index')")
    print()
    
    print("🧠 PROCESSING & THINKING Domain:")
    print("  - processing_and_thinking(action='analyze_code_patterns')")
    print("  - processing_and_thinking(action='detect_architectural_patterns')")
    print("  - processing_and_thinking(action='identify_improvements')")
    print()
    
    print("🧠 LEARNING & ADAPTATION Domain:")
    print("  - learning_and_adaptation(action='learn_from_project_structure')")
    print("  - learning_and_adaptation(action='adapt_to_coding_patterns')")
    print("  - learning_and_adaptation(action='evolve_understanding')")
    print()
    
    print("🧠 OUTPUT & ACTION Domain:")
    print("  - output_and_action(action='generate_project_report')")
    print("  - output_and_action(action='suggest_improvements')")
    print("  - output_and_action(action='provide_context')")
    print()
    
    print("🧠 SELF-MONITORING Domain:")
    print("  - self_monitoring(action='track_scan_performance')")
    print("  - self_monitoring(action='monitor_index_quality')")
    print("  - self_monitoring(action='assess_scan_accuracy')")
    print()

def main():
    """Main demo function"""
    print("🚀 MEMORY CONTEXT MANAGER v2 - PROJECT SCANNER DEMO")
    print("=" * 70)
    print()
    
    # Run project scanning demo
    project_index = demo_project_scanning()
    
    if project_index:
        # Show MCP integration
        demo_mcp_integration()
        
        # Save demo results
        demo_file = f"demo_results_{int(time.time())}.json"
        with open(demo_file, 'w') as f:
            json.dump({
                'demo_timestamp': time.time(),
                'project_summary': {
                    'name': project_index.context.get('project_name'),
                    'files': project_index.total_files,
                    'directories': project_index.total_directories,
                    'size': project_index.total_size,
                    'languages': project_index.patterns.get('languages', {}),
                    'frameworks': project_index.patterns.get('frameworks', {}),
                    'scan_duration': project_index.scan_time
                }
            }, f, indent=2)
        
        print(f"\n💾 Demo results saved to: {demo_file}")
        print("\n🎯 Ready for Phase 2: Knowledge Ingestion Engine!")

if __name__ == "__main__":
    main()
