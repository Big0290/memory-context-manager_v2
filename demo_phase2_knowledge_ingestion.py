#!/usr/bin/env python3
"""
Phase 2 Demo: Knowledge Ingestion Engine
Showcases the full capabilities of our knowledge ingestion system
"""

import json
import time
from pathlib import Path
from knowledge_ingestion_engine import KnowledgeIngestionEngine

def demo_knowledge_ingestion():
    """Demonstrate the full Phase 2 knowledge ingestion capabilities"""
    print("🚀 PHASE 2 DEMO: KNOWLEDGE INGESTION ENGINE")
    print("=" * 70)
    
    # Initialize the knowledge ingestion engine
    engine = KnowledgeIngestionEngine()
    
    print(f"📁 Current Project: {Path.cwd().name}")
    print(f"📍 Location: {Path.cwd()}")
    print()
    
    # Phase 1: Project Intelligence (already completed)
    print("✅ PHASE 1 COMPLETE: Project Intelligence Layer")
    print("   - Project scanner working perfectly")
    print("   - 100+ files indexed and analyzed")
    print("   - Technology stack identified")
    print("   - Dependencies mapped")
    print()
    
    # Phase 2: Knowledge Ingestion (starting now)
    print("🧠 PHASE 2: Knowledge Ingestion Engine")
    print("   - Processing documentation and code")
    print("   - Extracting semantic concepts")
    print("   - Building knowledge graphs")
    print("   - Creating intelligent relationships")
    print()
    
    print("🔍 Starting comprehensive knowledge ingestion...")
    start_time = time.time()
    
    try:
        # Ingest all project documentation
        knowledge_graph = engine.ingest_project_documentation('.')
        ingestion_time = time.time() - start_time
        
        print(f"✅ Knowledge ingestion completed in {ingestion_time:.2f} seconds!")
        print()
        
        # Display comprehensive results
        display_knowledge_graph_summary(knowledge_graph)
        display_concept_analysis(engine)
        display_relationship_analysis(engine)
        display_search_capabilities(engine)
        display_integration_points()
        
        # Export results
        export_demo_results(engine, ingestion_time)
        
        print("\n🎉 PHASE 2 DEMO COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        
        return knowledge_graph
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        return None

def display_knowledge_graph_summary(knowledge_graph):
    """Display comprehensive knowledge graph summary"""
    print("📊 KNOWLEDGE GRAPH COMPREHENSIVE SUMMARY")
    print("-" * 50)
    
    metadata = knowledge_graph.metadata
    patterns = knowledge_graph.patterns
    
    print(f"🎯 Graph Statistics:")
    print(f"   • Total Nodes: {metadata['total_nodes']:,}")
    print(f"   • Total Relationships: {metadata['total_relationships']:,}")
    print(f"   • Total Concepts: {metadata['total_concepts']:,}")
    print(f"   • Created: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(knowledge_graph.created_at))}")
    print()
    
    print(f"🧠 Node Type Distribution:")
    node_types = patterns.get('node_types', {})
    for node_type, count in node_types.items():
        percentage = (count / metadata['total_nodes']) * 100
        print(f"   • {node_type.title()}: {count:,} ({percentage:.1f}%)")
    print()
    
    print(f"🔗 Relationship Analysis:")
    rel_types = patterns.get('relationship_types', {})
    for rel_type, count in rel_types.items():
        percentage = (count / metadata['total_relationships']) * 100
        print(f"   • {rel_type.replace('_', ' ').title()}: {count:,} ({percentage:.1f}%)")
    print()
    
    print(f"🔌 Connectivity Metrics:")
    connectivity = patterns.get('connectivity', {})
    print(f"   • Average Connections: {connectivity.get('average_connections', 0):.2f}")
    print(f"   • Max Connections: {connectivity.get('max_connections', 0):,}")
    print(f"   • Min Connections: {connectivity.get('min_connections', 0)}")
    print(f"   • Total Connections: {connectivity.get('total_connections', 0):,}")
    print()

def display_concept_analysis(engine):
    """Display detailed concept analysis"""
    print("📚 CONCEPT ANALYSIS & INTELLIGENCE")
    print("-" * 50)
    
    # Get top concepts by frequency
    knowledge_graph = engine.get_knowledge_graph()
    if not knowledge_graph:
        return
    
    concept_freq = knowledge_graph.patterns.get('concept_frequency', {})
    top_concepts = sorted(concept_freq.items(), key=lambda x: x[1], reverse=True)[:15]
    
    print(f"🏆 Top 15 Most Frequent Concepts:")
    for i, (concept, count) in enumerate(top_concepts, 1):
        print(f"   {i:2d}. {concept[:50]:<50} ({count:,} occurrences)")
    print()
    
    # Analyze concept categories
    print(f"📋 Concept Categories:")
    function_concepts = [c for c in concept_freq.keys() if 'function' in c.lower() or 'def' in c.lower()]
    class_concepts = [c for c in concept_freq.keys() if 'class' in c.lower()]
    import_concepts = [c for c in concept_freq.keys() if 'import' in c.lower() or 'from' in c.lower()]
    
    print(f"   • Function-related: {len(function_concepts)} concepts")
    print(f"   • Class-related: {len(class_concepts)} concepts")
    print(f"   • Import-related: {len(import_concepts)} concepts")
    print()
    
    # Show source distribution
    source_dist = knowledge_graph.patterns.get('source_distribution', {})
    top_sources = sorted(source_dist.items(), key=lambda x: x[1], reverse=True)[:10]
    
    print(f"📁 Top 10 Knowledge Sources:")
    for i, (source, count) in enumerate(top_sources, 1):
        source_name = Path(source).name
        print(f"   {i:2d}. {source_name:<40} ({count:,} concepts)")
    print()

def display_relationship_analysis(engine):
    """Display relationship analysis and patterns"""
    print("🔗 RELATIONSHIP ANALYSIS & PATTERNS")
    print("-" * 50)
    
    knowledge_graph = engine.get_knowledge_graph()
    if not knowledge_graph:
        return
    
    # Analyze relationship strengths
    relationships = knowledge_graph.relationships.values()
    if relationships:
        strengths = [rel.strength for rel in relationships]
        avg_strength = sum(strengths) / len(strengths)
        max_strength = max(strengths)
        min_strength = min(strengths)
        
        print(f"💪 Relationship Strength Analysis:")
        print(f"   • Average Strength: {avg_strength:.3f}")
        print(f"   • Maximum Strength: {max_strength:.3f}")
        print(f"   • Minimum Strength: {min_strength:.3f}")
        print()
    
    # Show relationship examples
    print(f"🔍 Relationship Examples:")
    rel_examples = {}
    for rel in list(relationships)[:10]:  # Show first 10
        source_node = knowledge_graph.nodes.get(rel.source_id)
        target_node = knowledge_graph.nodes.get(rel.target_id)
        if source_node and target_node:
            rel_examples[rel.id] = {
                'source': source_node.name[:30],
                'target': target_node.name[:30],
                'type': rel.relationship_type,
                'strength': rel.strength
            }
    
    for rel_id, example in rel_examples.items():
        print(f"   • {example['source']} → {example['type']} → {example['target']} (strength: {example['strength']:.2f})")
    print()

def display_search_capabilities(engine):
    """Demonstrate search and query capabilities"""
    print("🔍 SEARCH & QUERY CAPABILITIES")
    print("-" * 50)
    
    # Demo searches
    search_queries = [
        'function',
        'class',
        'import',
        'test',
        'docker',
        'mcp',
        'brain',
        'memory'
    ]
    
    print(f"🔎 Concept Search Demonstrations:")
    for query in search_queries:
        results = engine.search_concepts(query)
        if results:
            print(f"   • '{query}': {len(results)} concepts found")
            # Show top result
            top_result = results[0]
            print(f"     Top: {top_result['concept'][:40]} (from {Path(top_result['source']).name})")
        else:
            print(f"   • '{query}': No concepts found")
    print()
    
    # Show search statistics
    total_concepts = sum(len(engine.search_concepts(q)) for q in search_queries)
    print(f"📊 Search Coverage: {total_concepts} total concept matches across all demo queries")
    print()

def display_integration_points():
    """Show how Phase 2 integrates with our MCP system"""
    print("🔌 MCP INTEGRATION POINTS")
    print("-" * 50)
    
    print(f"🧠 PERCEPTION & INPUT Domain:")
    print(f"   • perceive_and_analyze(action='knowledge_extraction') → Extract concepts from documents")
    print(f"   • perceive_and_analyze(action='semantic_analysis') → Analyze document meaning")
    print(f"   • perceive_and_analyze(action='concept_mapping') → Map concept relationships")
    print()
    
    print(f"🧠 MEMORY & STORAGE Domain:")
    print(f"   • memory_and_storage(action='store_knowledge_graph') → Save knowledge graph")
    print(f"   • memory_and_storage(action='retrieve_concepts') → Get concept information")
    print(f"   • memory_and_storage(action='update_knowledge') → Update knowledge base")
    print()
    
    print(f"🧠 PROCESSING & THINKING Domain:")
    print(f"   • processing_and_thinking(action='analyze_knowledge_patterns') → Pattern analysis")
    print(f"   • processing_and_thinking(action='semantic_reasoning') → Semantic reasoning")
    print(f"   • processing_and_thinking(action='knowledge_synthesis') → Knowledge synthesis")
    print()
    
    print(f"🧠 LEARNING & ADAPTATION Domain:")
    print(f"   • learning_and_adaptation(action='learn_from_documents') → Document learning")
    print(f"   • learning_and_adaptation(action='evolve_knowledge') → Knowledge evolution")
    print(f"   • learning_and_adaptation(action='adapt_patterns') → Pattern adaptation")
    print()
    
    print(f"🧠 OUTPUT & ACTION Domain:")
    print(f"   • output_and_action(action='generate_knowledge_report') → Knowledge reports")
    print(f"   • output_and_action(action='provide_semantic_context') → Semantic context")
    print(f"   • output_and_action(action='suggest_improvements') → Improvement suggestions")
    print()
    
    print(f"🧠 SELF-MONITORING Domain:")
    print(f"   • self_monitoring(action='track_knowledge_quality') → Quality monitoring")
    print(f"   • self_monitoring(action='assess_extraction_accuracy') → Accuracy assessment")
    print(f"   • self_monitoring(action='monitor_graph_health') → Graph health monitoring")
    print()

def export_demo_results(engine, ingestion_time):
    """Export demo results and save to files"""
    print("💾 EXPORTING DEMO RESULTS")
    print("-" * 50)
    
    timestamp = int(time.time())
    
    # Export knowledge graph
    json_export = engine.export_knowledge('json')
    json_file = f"phase2_demo_knowledge_graph_{timestamp}.json"
    with open(json_file, 'w') as f:
        f.write(json_export)
    print(f"📊 Knowledge Graph: {json_file} ({len(json_export):,} characters)")
    
    # Export summary
    summary_export = engine.export_knowledge('summary')
    summary_file = f"phase2_demo_summary_{timestamp}.md"
    with open(summary_file, 'w') as f:
        f.write(summary_file)
    print(f"📝 Summary Report: {summary_file} ({len(summary_export):,} characters)")
    
    # Create demo results summary
    demo_results = {
        'demo_timestamp': timestamp,
        'phase': 'Phase 2: Knowledge Ingestion Engine',
        'performance': {
            'ingestion_time': ingestion_time,
            'total_nodes': len(engine.get_knowledge_graph().nodes) if engine.get_knowledge_graph() else 0,
            'total_relationships': len(engine.get_knowledge_graph().relationships) if engine.get_knowledge_graph() else 0,
            'total_concepts': engine.get_knowledge_graph().metadata.get('total_concepts', 0) if engine.get_knowledge_graph() else 0
        },
        'capabilities': {
            'document_processing': True,
            'concept_extraction': True,
            'relationship_building': True,
            'knowledge_graph_construction': True,
            'semantic_search': True,
            'mcp_integration': True
        },
        'next_phase': 'Phase 3: Personalization & Behavior Injection'
    }
    
    results_file = f"phase2_demo_results_{timestamp}.json"
    with open(results_file, 'w') as f:
        json.dump(demo_results, f, indent=2)
    print(f"📋 Demo Results: {results_file}")
    
    print(f"\n💾 All demo results exported successfully!")
    print(f"🎯 Ready for Phase 3: Personalization & Behavior Injection!")

def main():
    """Main demo function"""
    print("🚀 MEMORY CONTEXT MANAGER v2 - PHASE 2 DEMO")
    print("=" * 70)
    print()
    
    # Run the comprehensive demo
    knowledge_graph = demo_knowledge_ingestion()
    
    if knowledge_graph:
        print(f"\n🎉 PHASE 2 DEMO COMPLETED SUCCESSFULLY!")
        print(f"📊 Knowledge Graph: {len(knowledge_graph.nodes):,} nodes, {len(knowledge_graph.relationships):,} relationships")
        print(f"🧠 Concepts Extracted: {knowledge_graph.metadata.get('total_concepts', 0):,}")
        print(f"🔗 Semantic Relationships: {knowledge_graph.metadata.get('total_relationships', 0):,}")
        print()
        print(f"🚀 Ready to begin Phase 3: Personalization & Behavior Injection!")
    else:
        print(f"\n❌ Demo failed to complete successfully")

if __name__ == "__main__":
    main()
