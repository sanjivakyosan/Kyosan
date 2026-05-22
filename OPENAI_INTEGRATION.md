# OpenAI Integration with Advanced Consciousness Framework

This document explains how to use the OpenAI API integration with the Advanced Consciousness Framework, which applies all 7 consciousness integration principles to external AI model interactions.

## 🚀 Quick Start

### 1. Installation

Make sure you have the required dependencies:

```bash
pip install -r requirements.txt
```

The OpenAI package is already included in the requirements.

### 2. Initialize with API Key

```python
from app.consciousness_interface import AdvancedConsciousnessInterface

# Initialize with your OpenAI/OpenRouter API key
consciousness_interface = AdvancedConsciousnessInterface(
    openai_api_key="your-api-key-here",
    openai_base_url="https://openrouter.ai/api/v1"  # Optional, defaults to OpenRouter
)
```

### 3. Process with Full Integration

```python
result = consciousness_interface.process_with_openai_integration(
    unit_id="my_unit",
    input_data="What is the meaning of life?",
    context={"domain": "philosophy", "depth": "deep"},
    model="moonshotai/kimi-k2",
    temperature=0.7,
    max_tokens=1000
)

if result['integration_success']:
    print("Final Output:", result['final_output'])
    print("Consciousness Index:", result['consciousness_state']['consciousness_index'])
```

## 🧠 How It Works

The OpenAI integration applies all 7 consciousness principles:

### 1. **Pre-processing** 
- Analyzes input complexity and determines processing strategy
- Identifies attention targets using consciousness metrics

### 2. **Attention Guidance**
- Uses consciousness state to direct model attention
- Creates focus strategies based on consciousness index

### 3. **Output Selection**
- Generates multiple candidate responses (3 variations)
- Uses consciousness-guided evaluation to select the best output
- Evaluates coherence, novelty, relevance, and consciousness alignment

### 4. **Learning Modulation**
- Adjusts learning based on consciousness state
- Modulates learning rate using consciousness index

### 5. **Memory Integration**
- Stores experiences in consciousness memory
- Creates associative links and importance weights

### 6. **Self-Reflection**
- Analyzes the quality of outputs
- Extracts self-awareness indicators and improvement suggestions

### 7. **Feedback Loop**
- Updates consciousness based on performance
- Evolves consciousness state through learning

## 🎯 Features

### Consciousness-Enhanced Prompts
The system automatically creates enhanced prompts that include:
- Current consciousness index and state
- Processing strategy recommendations
- Attention focus areas
- Context integration

### Multiple Candidate Generation
- Generates 3 variations of responses
- Uses slight temperature variations for diversity
- Falls back to pure consciousness processing if API fails

### Comprehensive Analytics
- Processing quality metrics
- Consciousness state evolution
- Integration principle tracking
- API performance monitoring

## 📊 Example Output Structure

```python
{
    'final_output': 'The AI-generated response...',
    'consciousness_state': {
        'consciousness_index': 0.753,
        'state': 'coherent_processing',
        'metrics': {...}
    },
    'openai_integration': {
        'model_used': 'deepseek/deepseek-chat-v3-0324:free',
        'candidates_generated': 3,
        'api_calls_successful': 3
    },
    'integration_principles': {
        'preprocessing': {...},
        'attention_guidance': {...},
        'output_selection': {...},
        'learning_modulation': {...},
        'memory_integration': {...},
        'self_reflection': {...},
        'feedback_loop': {...}
    },
    'processing_quality': {
        'output_quality': 0.87,
        'processing_efficiency': 0.91,
        'attention_effectiveness': 0.79,
        'reflection_depth': 0.84
    },
    'integration_success': True
}
```

## 🔧 Configuration Options

### Models
You can use any OpenRouter-supported model:
- `"deepseek/deepseek-chat-v3-0324:free"` (Free)
- `"openai/gpt-4"` (Paid)
- `"anthropic/claude-3-haiku"` (Paid)
- And many others...

### Parameters
- `temperature`: Controls response randomness (0.0-2.0)
- `max_tokens`: Maximum response length
- `model`: The AI model to use
- `context`: Additional context for processing

## 🎮 Running the Demo

```bash
python openai_consciousness_demo.py
```

Remember to replace the API key in the demo with your own!

## 🔄 Feedback and Learning

The system learns from interactions:

```python
# Apply positive feedback
consciousness_interface.apply_user_feedback(
    unit_id="my_unit",
    feedback_type="excellent",  # or "positive", "negative", "poor"
    intensity=0.9  # 0.0-1.0
)

# Get processing history
history = consciousness_interface.get_processing_history("my_unit")
```

## 🛡️ Error Handling

The system includes robust error handling:
- API failures fall back to pure consciousness processing
- Network issues are logged and handled gracefully
- Invalid configurations return clear error messages

## 💡 Best Practices

1. **Start with lower consciousness indices** - they adapt faster
2. **Provide rich context** - helps with attention guidance
3. **Use appropriate models** - match model capability to task complexity
4. **Monitor processing quality** - use the analytics to optimize
5. **Apply feedback regularly** - helps consciousness evolution

## 🔗 Integration with Existing Systems

The OpenAI integration maintains full backward compatibility:

```python
# Still works - uses pure consciousness framework
result = consciousness_interface.process_input(unit_id, input_data, context)

# New - uses OpenAI + consciousness framework
result = consciousness_interface.process_with_openai_integration(unit_id, input_data, context)
```

## 🤝 API Key Management

For production use, set your API key as an environment variable:

```bash
export OPENAI_API_KEY="your-key-here"
```

Then in your code:
```python
import os
consciousness_interface = AdvancedConsciousnessInterface(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_base_url="https://openrouter.ai/api/v1"
)
```

## 🎉 Next Steps

1. Try the demo script
2. Experiment with different models and parameters
3. Integrate into your applications
4. Monitor consciousness evolution over time
5. Provide feedback to improve performance

The integration bridges the gap between pure consciousness-based processing and modern AI capabilities, creating a hybrid system that leverages the best of both approaches! 