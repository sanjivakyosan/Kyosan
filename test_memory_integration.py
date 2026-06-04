#!/usr/bin/env python3
# Copyright © Charles Roux 2026
"""
Test script to demonstrate the enhanced Memory Integration system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from consciousness_framework import SelfModelingUnit, MemorySystem, Memory
import time

def test_memory_integration():
    """Test the enhanced memory integration system"""
    print("🧠 Testing Enhanced Memory Integration System")
    print("=" * 60)
    
    # Create a test unit
    unit = SelfModelingUnit("memory_test_unit")
    
    # Test different types of inputs to build diverse memories
    test_inputs = [
        {
            "input": "What is consciousness and how does it relate to artificial intelligence?",
            "expected_tags": ["consciousness", "artificial", "intelligence", "philosophy"],
            "complexity": "high"
        },
        {
            "input": "I feel happy when learning new things about memory systems.",
            "expected_tags": ["learning", "memory", "happy", "emotion"],
            "complexity": "medium"
        },
        {
            "input": "The neural network processes information through multiple layers.",
            "expected_tags": ["neural", "network", "information", "technology"],
            "complexity": "medium"
        },
        {
            "input": "Memory consolidation happens during sleep and involves synaptic strengthening.",
            "expected_tags": ["memory", "consolidation", "sleep", "science"],
            "complexity": "high"
        },
        {
            "input": "I love exploring the mysteries of the human mind and consciousness.",
            "expected_tags": ["love", "exploring", "human", "mind", "consciousness"],
            "complexity": "medium"
        }
    ]
    
    print("📝 Processing diverse inputs to build memory associations...")
    
    for i, test_case in enumerate(test_inputs):
        print(f"\n--- Processing Input {i+1} ---")
        print(f"Input: {test_case['input']}")
        print(f"Expected tags: {test_case['expected_tags']}")
        
        # Process the input
        context = {"test_case": i, "complexity": test_case['complexity']}
        output = unit.process(test_case['input'], context)
        
        # Handle different output types
        if isinstance(output, str):
            output_str = output[:100] + "..." if len(output) > 100 else output
        else:
            output_str = str(output)[:100] + "..."
        
        print(f"Output: {output_str}")
        
        # Get memory integration score
        integration_score = unit.memory.get_memory_integration_score()
        print(f"Memory Integration Score: {integration_score:.3f}")
        
        # Show memory metrics
        metrics = unit.memory.integration_metrics
        print(f"Memory Metrics:")
        print(f"  - Total Associations: {metrics['total_associations']}")
        print(f"  - Avg Integration Strength: {metrics['avg_integration_strength']:.3f}")
        print(f"  - Semantic Clusters: {metrics['semantic_clusters']}")
        print(f"  - Temporal Links: {metrics['temporal_links']}")
        print(f"  - Emotional Connections: {metrics['emotional_connections']}")
        
        time.sleep(1)  # Small delay to see temporal effects
    
    print("\n" + "=" * 60)
    print("🔍 Analyzing Memory Integration Results")
    print("=" * 60)
    
    # Analyze the memory system
    all_memories = unit.memory.working_memory + unit.memory.episodic_memory[:10]
    
    print(f"Total Memories: {len(all_memories)}")
    print(f"Working Memory: {len(unit.memory.working_memory)}")
    print(f"Episodic Memory: {len(unit.memory.episodic_memory)}")
    
    # Show semantic clusters
    print(f"\n📚 Semantic Clusters ({len(unit.memory.semantic_index)}):")
    for tag, indices in unit.memory.semantic_index.items():
        print(f"  - {tag}: {len(indices)} memories")
    
    # Show emotional distribution
    print(f"\n😊 Emotional Distribution:")
    for emotion, indices in unit.memory.emotional_index.items():
        print(f"  - {emotion}: {len(indices)} memories")
    
    # Show association graph
    print(f"\n🔗 Association Graph:")
    total_links = sum(len(links) for links in unit.memory.association_graph.values())
    print(f"  - Total Memory Links: {total_links}")
    print(f"  - Connected Memories: {len(unit.memory.association_graph)}")
    
    # Show individual memory details
    print(f"\n📋 Individual Memory Details:")
    for i, memory in enumerate(all_memories[:3]):  # Show first 3 memories
        print(f"\nMemory {i+1}:")
        content_str = str(memory.content)
        print(f"  - Content: {content_str[:50]}...")
        print(f"  - Associations: {len(memory.associations)}")
        print(f"  - Semantic Tags: {memory.semantic_tags}")
        print(f"  - Emotional Valence: {memory.emotional_valence:.3f}")
        print(f"  - Complexity Score: {memory.complexity_score:.3f}")
        print(f"  - Integration Strength: {memory.integration_strength:.3f}")
        print(f"  - Related Memories: {len(memory.related_memories)}")
    
    # Final integration score
    final_score = unit.memory.get_memory_integration_score()
    print(f"\n🎯 Final Memory Integration Score: {final_score:.3f}")
    
    # Print score breakdown
    breakdown = unit.memory.integration_metrics.get('score_breakdown', {})
    if breakdown:
        print("\n🔬 Integration Score Breakdown:")
        for k, v in breakdown.items():
            print(f"  - {k}: {v:.3f}" if isinstance(v, float) else f"  - {k}: {v}")
    
    if final_score > 0.1:
        print("✅ Memory Integration System is WORKING!")
        print("   - Memories are being associated and connected")
        print("   - Semantic tags are being extracted")
        print("   - Emotional content is being analyzed")
        print("   - Temporal and contextual links are being created")
    else:
        print("❌ Memory Integration System needs more data")
        print("   - Try processing more diverse inputs")
        print("   - Allow more time for associations to form")
    
    # --- Mermaid Diagram Generation ---
    print("\n" + "=" * 60)
    print("🌐 Memory Network Visualization (Mermaid)")
    print("=" * 60)
    print("graph TD;")
    # Each memory is a node
    for i, memory in enumerate(all_memories):
        label = f"M{i+1}"
        tags = ','.join(memory.semantic_tags[:2])
        print(f"    {label}[\"{label}: {tags}\"]")
    # Edges for associations
    for i, memory in enumerate(all_memories):
        label = f"M{i+1}"
        for j in memory.related_memories:
            if j < len(all_memories):
                label2 = f"M{j+1}"
                print(f"    {label} -- assoc --> {label2}")
    print("\nCopy the above Mermaid code into a Mermaid live editor to view the network graph.")
    
    return final_score

def test_memory_retrieval():
    """Test memory retrieval with associations"""
    print("\n" + "=" * 60)
    print("🔍 Testing Memory Retrieval with Associations")
    print("=" * 60)
    
    unit = SelfModelingUnit("retrieval_test_unit")
    
    # Add some test memories
    test_memories = [
        "I learned about neural networks today",
        "Consciousness is a fascinating topic",
        "Memory systems are complex and interesting",
        "I feel excited about AI research",
        "The brain processes information in amazing ways"
    ]
    
    for memory_content in test_memories:
        context = {"source": "test", "topic": "ai_research"}
        unit.memory.add_to_working_memory(memory_content, importance=0.7, context=context)
    
    # Test retrieval
    query = "neural networks"
    retrieved = unit.memory.retrieve(query, num_results=3)
    
    print(f"Query: '{query}'")
    print(f"Retrieved {len(retrieved)} memories:")
    
    for i, memory in enumerate(retrieved):
        content_str = str(memory.content)
        print(f"  {i+1}. {content_str[:50]}...")
        print(f"     Associations: {len(memory.associations)}")
        print(f"     Integration Strength: {memory.integration_strength:.3f}")

if __name__ == "__main__":
    print("🧠 Enhanced Memory Integration System Test")
    print("=" * 60)
    
    # Test basic integration
    score = test_memory_integration()
    
    # Test retrieval
    test_memory_retrieval()
    
    print("\n" + "=" * 60)
    print("✅ Memory Integration Test Complete!")
    print(f"Final Integration Score: {score:.3f}")
    print("=" * 60) 