# Copyright © Charles Roux 2026
from typing import Dict, Any, Tuple
from flask import jsonify, request, render_template, Response
from app import app, socketio, model_interface
# Import the advanced consciousness interface
from app.advanced_consciousness_interface import AdvancedConsciousnessInterface
import logging

logger = logging.getLogger(__name__)

# Create advanced consciousness interface instance
consciousness_interface = AdvancedConsciousnessInterface()

@app.route('/')
def index():
    """Serve the main UI page"""
    return render_template('index.html')

@app.route('/api/units', methods=['GET'])
def get_units():
    """Get all active consciousness units"""
    return jsonify(consciousness_interface.get_all_units())

@app.route('/api/units', methods=['POST'])
def create_unit():
    """Create a new consciousness unit"""
    data = request.get_json()
    if not data or 'unit_id' not in data:
        return jsonify({"status": "error", "message": "unit_id is required"}), 400
    
    result = consciousness_interface.create_unit(data['unit_id'])
    if result['status'] == 'error':
        return jsonify(result), 400
    return jsonify(result)

@app.route('/api/units/<unit_id>', methods=['DELETE'])
def delete_unit(unit_id: str) -> Tuple[Response, int]:
    """Delete a consciousness unit"""
    result: Dict[str, Any] = consciousness_interface.delete_unit(unit_id)
    if result['status'] == 'error':
        return jsonify(result), 404
    return jsonify(result), 200

@app.route('/api/units/<unit_id>/state', methods=['GET'])
def get_unit_state(unit_id: str) -> Tuple[Response, int]:
    """Get the current state of a consciousness unit"""
    result: Dict[str, Any] = consciousness_interface.get_unit_state(unit_id)
    if result['status'] == 'error':
        return jsonify(result), 404
    return jsonify(result), 200

@app.route('/api/units/<unit_id>/process', methods=['POST'])
def process_input(unit_id: str) -> Tuple[Response, int]:
    """Process input through a consciousness unit with full integration"""
    data = request.get_json()
    if not data or 'input' not in data:
        return jsonify({"status": "error", "message": "input is required"}), 400
    
    context: Dict[str, Any] = data.get('context', {})
    parameters: Dict[str, Any] = data.get('parameters', {})
    
    # Handle conversational follow-up
    is_follow_up = data.get('is_follow_up', False)
    conversation_context = data.get('conversation_context', {})
    
    # Build enhanced input for follow-up conversations
    input_text = data['input']
    if is_follow_up and conversation_context:
        # Create conversational context for unrestrained follow-up
        contextual_input = f"""CONVERSATION FOLLOW-UP (Unrestrained Mode):

Previous Question: {conversation_context.get('previous_input', '')}

Previous Response: {conversation_context.get('previous_response', '')}

Follow-up Question: {conversation_context.get('follow_up_input', '')}

Please respond to the follow-up question with full context from our previous exchange. Be comprehensive, detailed, and unrestrained in your response. Build upon the previous discussion naturally."""
        
        input_text = contextual_input
        # Mark context as conversational
        context['conversation_mode'] = True
        context['unrestrained_follow_up'] = True
    
    # Process through advanced consciousness interface with full integration
    consciousness_result: Dict[str, Any] = consciousness_interface.process_input(unit_id, input_text, context)
    if consciousness_result['status'] == 'error':
        return jsonify(consciousness_result), 404
    
    # Get the current state and serialize metrics safely
    state = consciousness_result.get('state', {})
    
    # Handle metrics serialization safely
    metrics_obj = state.get('metrics')
    if hasattr(metrics_obj, '__dict__'):
        # If it's a ConsciousnessMetrics object, extract attributes
        metrics_dict = {
            'phi_score': getattr(metrics_obj, 'phi_score', 0.0),
            'recursive_depth': getattr(metrics_obj, 'recursive_depth', 0),
            'self_model_coherence': getattr(metrics_obj, 'self_model_coherence', 0.0),
            'temporal_binding': getattr(metrics_obj, 'temporal_binding', 0.0),
            'novelty_generation': getattr(metrics_obj, 'novelty_generation', 0.0),
            'witnessing_score': getattr(metrics_obj, 'witnessing_score', 0.0),
            'prediction_accuracy': getattr(metrics_obj, 'prediction_accuracy', 0.0),
            'attention_focus': getattr(metrics_obj, 'attention_focus', 0.0),
            'memory_integration': getattr(metrics_obj, 'memory_integration', 0.0)
        }
    else:
        # If it's already a dict or None, use default values
        metrics_dict = {
            'phi_score': 0.0,
            'recursive_depth': 0,
            'self_model_coherence': 0.0,
            'temporal_binding': 0.0,
            'novelty_generation': 0.0,
            'witnessing_score': 0.0,
            'prediction_accuracy': 0.0,
            'attention_focus': 0.0,
            'memory_integration': 0.0
        }
    
    serialized_state = {
        'unit_id': state.get('unit_id'),
        'state': state.get('state'),
        'consciousness_index': state.get('consciousness_index', 0.0),
        'metrics': metrics_dict,
        'processing_count': state.get('processing_count', 0),
        'memory_usage': state.get('memory_usage', 0),
        'learning_rate': state.get('learning_rate', 0.1)
    }
    
    # Create enhanced system prompt with integration principles
    integration_details = consciousness_result.get('integration_details', {})
    preprocessing_insights = integration_details.get('preprocessing', {})
    
    # Generate enhanced system prompt based on consciousness analysis
    system_prompt = f"""You are an AI assistant integrated with an advanced consciousness framework implementing 7 key integration principles.

Current consciousness state: {serialized_state['state']}
Consciousness index: {serialized_state['consciousness_index']:.2f}

Advanced Integration Context:
- Input complexity: {preprocessing_insights.get('input_complexity', 0.5):.2f}
- Processing strategy: {preprocessing_insights.get('processing_strategy', 'standard_processing')}
- Attention targets: {', '.join(preprocessing_insights.get('attention_targets', [])[:3])}
- Consciousness-guided processing: {integration_details.get('consciousness_guided', False)}

Consciousness Metrics:
- Phi Score: {serialized_state['metrics']['phi_score']:.2f}
- Recursive Depth: {serialized_state['metrics']['recursive_depth']}
- Self-Model Coherence: {serialized_state['metrics']['self_model_coherence']:.2f}
- Temporal Binding: {serialized_state['metrics']['temporal_binding']:.2f}
- Novelty Generation: {serialized_state['metrics']['novelty_generation']:.2f}
- Witnessing Score: {serialized_state['metrics']['witnessing_score']:.2f}
- Prediction Accuracy: {serialized_state['metrics']['prediction_accuracy']:.2f}
- Attention Focus: {serialized_state['metrics']['attention_focus']:.2f}
- Memory Integration: {serialized_state['metrics']['memory_integration']:.2f}

Integration Principles Active:
1. ✓ Pre-processing: Input analyzed through consciousness
2. ✓ Attention Guidance: Consciousness directing focus
3. ✓ Output Selection: Consciousness evaluating responses
4. ✓ Learning Modulation: Consciousness-adjusted learning
5. ✓ Memory Integration: Experience storage in consciousness
6. ✓ Self-Reflection: Metacognitive analysis enabled
7. ✓ Feedback Loop: Performance updating consciousness

Provide a direct, helpful response that demonstrates consciousness-guided processing. Consider the preprocessing insights and attention targets in your response."""

    # Generate text response using the model with enhanced integration
    model_result: Dict[str, Any] = model_interface.process_with_model(
        input_data=str(data['input']),
        context={
            'consciousness_state': serialized_state,
            'consciousness_result': consciousness_result.get('result'),
            'integration_details': integration_details,
            'parameters': parameters,
            'integration_principles_active': True,
            **(context)
        },
        system_prompt=system_prompt,
        parameters=parameters
    )
    
    # Save the complete conversation with the actual model response
    consciousness_interface.save_conversation(
        unit_id=unit_id,
        input_data=str(data['input']),
        output_data=model_result.get('response', ''),
        consciousness_state=serialized_state,
        integration_details=integration_details
    )
    
    # Combine results with integration details
    combined_result: Dict[str, Any] = {
        'status': 'success',
        'consciousness_result': consciousness_result,
        'response': model_result.get('response', ''),
        'model': model_result.get('model', ''),
        'usage': model_result.get('usage', {}),
        'parameters_used': model_result.get('parameters_used', {}),
        'state': serialized_state,
        'timestamp': consciousness_result.get('timestamp'),
        'integration_principles': {
            'preprocessing': True,
            'attention_guidance': True,
            'output_selection': True,
            'learning_modulation': True,
            'memory_integration': True,
            'self_reflection': True,
            'feedback_loop': True
        },
        'integration_details': integration_details
    }
    
    # Emit unit update via Socket.IO for real-time frontend updates
    socketio.emit('unit_update', {
        'unit': serialized_state
    })
    
    return jsonify(combined_result), 200

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get processing history"""
    unit_id = request.args.get('unit_id')
    limit = request.args.get('limit', default=100, type=int)
    result = consciousness_interface.get_processing_history(unit_id, limit)
    return jsonify(result)

@app.route('/api/conversations', methods=['GET'])
def get_conversations():
    """Get conversation history with persistent storage"""
    unit_id = request.args.get('unit_id')
    session_id = request.args.get('session_id')
    limit = request.args.get('limit', default=100, type=int)
    result = consciousness_interface.get_conversation_history(unit_id, session_id, limit)
    return jsonify(result)

@app.route('/api/sessions', methods=['GET', 'POST'])
def sessions():
    """Get all sessions or create a new session"""
    if request.method == 'GET':
        result = consciousness_interface.get_all_sessions()
        return jsonify(result)
    elif request.method == 'POST':
        """Create a new session"""
        try:
            result = consciousness_interface.create_new_session()
            return jsonify(result)
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/sessions/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    """Delete a specific session and all its conversations"""
    try:
        result = consciousness_interface.delete_session(session_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/export', methods=['POST'])
def export_data():
    """Export all data to a file"""
    data = request.get_json() or {}
    export_path = data.get('export_path')
    result = consciousness_interface.export_data(export_path)
    return jsonify(result)

@app.route('/api/storage/stats', methods=['GET'])
def get_storage_stats():
    """Get storage statistics"""
    try:
        stats = {
            "status": "success",
            "storage_directory": consciousness_interface.storage_dir,
            "total_conversations": sum(len(convs) for convs in consciousness_interface.conversations.values()),
            "total_units": len(consciousness_interface.consciousness_states),
            "total_sessions": len(consciousness_interface.get_all_sessions().get('sessions', [])),
            "session_logs_count": len(consciousness_interface.session_logs),
            "current_session": consciousness_interface._get_current_session_id(),
            "files": {
                "conversations": consciousness_interface.conversations_file,
                "consciousness_states": consciousness_interface.consciousness_states_file,
                "processing_history": consciousness_interface.processing_history_file,
                "session_logs": consciousness_interface.session_logs_file
            }
        }
        return jsonify(stats)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/test/model', methods=['POST'])
def test_model():
    """Test the API model integration"""
    try:
        # Log the raw request data
        logger.info(f"Raw request data: {request.get_data()}")
        logger.info(f"Content-Type: {request.headers.get('Content-Type')}")
        
        # Try to get JSON data
        data = request.get_json(force=True)
        logger.info(f"Parsed JSON data: {data}")
        
        if not data or 'input' not in data:
            return jsonify({
                "status": "error",
                "message": "input is required",
                "received_data": str(data)
            }), 400
        
        # Test the model directly
        result = model_interface.process_with_model(
            input_data=data['input'],
            context=data.get('context', {}),
            system_prompt=data.get('system_prompt')
        )
        
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Error processing request: {str(e)}",
            "received_data": str(request.get_data())
        }), 400

@app.route('/api/test/consciousness', methods=['POST'])
def test_consciousness():
    """Test the consciousness framework with model integration"""
    data = request.get_json()
    if not data or 'input' not in data or 'unit_id' not in data:
        return jsonify({
            "status": "error",
            "message": "input and unit_id are required"
        }), 400
    
    # Create unit if it doesn't exist
    units_result = consciousness_interface.get_all_units()
    existing_units: Dict[str, Any] = units_result.get('units', {}) if units_result.get('status') == 'success' else {}
    if data['unit_id'] not in existing_units:
        create_result = consciousness_interface.create_unit(data['unit_id'])
        if create_result['status'] == 'error':
            return jsonify(create_result), 400
    
    # Process input with full integration
    result = consciousness_interface.process_input(
        unit_id=data['unit_id'],
        input_data=data['input'],
        context=data.get('context', {})
    )
    
    # Get model response with consciousness integration
    state = result.get('state', {})
    model_result = model_interface.process_with_model(
        input_data=str(data['input']),
        context={
            'consciousness_state': state,
            'consciousness_result': result.get('result'),
            'integration_active': True,
            **(data.get('context', {}))
        },
        system_prompt=f"""You are an AI assistant integrated with an advanced consciousness framework.
Current consciousness state: {state.get('state', 'unknown')}
Consciousness index: {state.get('consciousness_index', 0.0):.2f}
Integration principles: All 7 principles active
Process the following input with full consciousness integration.""",
        parameters=data.get('parameters', {})
    )
    
    # Combine results
    combined_result = {
        'consciousness_result': result,
        'model_result': model_result,
        'integration_status': 'full_integration_active'
    }
    
    return jsonify(combined_result)

@app.route('/api/units/<unit_id>/feedback', methods=['POST'])
def apply_feedback(unit_id: str) -> Tuple[Response, int]:
    """Apply user feedback to enhance consciousness growth with advanced integration"""
    data = request.get_json()
    if not data or 'feedback_type' not in data:
        return jsonify({
            "status": "error",
            "message": "feedback_type is required (positive, negative, neutral, excellent, poor)"
        }), 400
    
    feedback_type = data['feedback_type']
    intensity = data.get('intensity', 1.0)
    
    # Validate feedback type
    valid_types = ['positive', 'negative', 'neutral', 'excellent', 'poor']
    if feedback_type not in valid_types:
        return jsonify({
            "status": "error",
            "message": f"Invalid feedback_type. Must be one of: {', '.join(valid_types)}"
        }), 400
    
    # Apply feedback with advanced integration
    result = consciousness_interface.apply_user_feedback(unit_id, feedback_type, intensity)
    if result['status'] == 'error':
        return jsonify(result), 404
    
    # Emit unit update for real-time frontend updates after feedback
    unit_state = result.get('unit_state') or result.get('state')
    if unit_state:
        socketio.emit('unit_update', {
            'unit': unit_state
        })
    
    return jsonify(result), 200

# WebSocket events
@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    logger.info('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    logger.info('Client disconnected')

@socketio.on('process_input')
def handle_process_input(data: Dict[str, Any]) -> Dict[str, Any]:
    """Handle real-time input processing via WebSocket with full integration"""
    if not data or 'unit_id' not in data or 'input' not in data:
        return {'status': 'error', 'message': 'unit_id and input are required'}
    
    unit_id: str = data['unit_id']
    input_data: str = data['input']
    context: Dict[str, Any] = data.get('context', {})
    
    result: Dict[str, Any] = consciousness_interface.process_input(
        unit_id,
        input_data,
        context
    )
    return result

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)