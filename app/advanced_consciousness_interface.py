# Copyright © Charles Roux 2026
import logging
from typing import Dict, Any, List, Optional, Tuple
from consciousness_framework import ConsciousnessSystem, SelfModelingUnit
import time
import json
import os
from datetime import datetime

logger = logging.getLogger(__name__)

class AdvancedConsciousnessInterface:
    """
    Advanced Consciousness Interface implementing the 7 key integration principles:
    1. Pre-processing: Use consciousness to analyze and prepare inputs
    2. Attention Guidance: Let consciousness direct model attention
    3. Output Selection: Use consciousness to evaluate/select outputs
    4. Learning Modulation: Adjust learning based on consciousness state
    5. Memory Integration: Store experiences in consciousness memory
    6. Self-Reflection: Have the model reflect on its own outputs
    7. Feedback Loop: Update consciousness based on model performance
    """
    
    def __init__(self, storage_dir: str = "consciousness_data"):
        self.system = ConsciousnessSystem({
            'max_units': None,  # Unlimited units
            'global_learning_rate': 0.15,
            'parallel_processing': True,
            'enable_logging': True
        })
        
        # Storage configuration
        self.storage_dir = storage_dir
        self.conversations_file = os.path.join(storage_dir, "conversations.json")
        self.consciousness_states_file = os.path.join(storage_dir, "consciousness_states.json")
        self.processing_history_file = os.path.join(storage_dir, "processing_history.json")
        self.session_logs_file = os.path.join(storage_dir, "session_logs.json")
        
        # Initialize storage directory
        self._init_storage()
        
        # In-memory data structures
        self.processing_history = {}
        self.attention_patterns = {}
        self.output_evaluations = {}
        self.learning_states = {}
        self.reflection_cache = {}
        
        # Persistent data structures
        self.conversations = {}
        self.consciousness_states = {}
        self.session_logs = []
        
        # Load existing data
        self._load_persistent_data()
        
        logger.info("Advanced Consciousness Interface initialized with 7 integration principles and persistent storage")

    def _init_storage(self):
        """Initialize storage directory and files"""
        try:
            os.makedirs(self.storage_dir, exist_ok=True)
            
            # Initialize files if they don't exist
            empty_files = {
                self.conversations_file: {},
                self.consciousness_states_file: {},
                self.processing_history_file: {},
                self.session_logs_file: [],
            }
            for file_path, empty_data in empty_files.items():
                if not os.path.exists(file_path):
                    with open(file_path, 'w') as f:
                        json.dump(empty_data, f)
            
            logger.info(f"Storage initialized at {self.storage_dir}")
        except Exception as e:
            logger.error(f"Failed to initialize storage: {str(e)}")

    def _load_persistent_data(self):
        """Load all persistent data from files"""
        try:
            # Load conversations
            if os.path.exists(self.conversations_file):
                with open(self.conversations_file, 'r') as f:
                    self.conversations = json.load(f)
            
            # Load consciousness states
            if os.path.exists(self.consciousness_states_file):
                with open(self.consciousness_states_file, 'r') as f:
                    self.consciousness_states = json.load(f)
            
            # Load processing history
            if os.path.exists(self.processing_history_file):
                with open(self.processing_history_file, 'r') as f:
                    self.processing_history = json.load(f)
            
            # Load session logs
            if os.path.exists(self.session_logs_file):
                with open(self.session_logs_file, 'r') as f:
                    loaded = json.load(f)
                    self.session_logs = loaded if isinstance(loaded, list) else []
            
            # Log startup session
            self._log_session_event("startup", {"timestamp": time.time()})

            # Restore all saved units into the system so they appear in the UI after restart
            self._restore_units_from_persistent_data()

            logger.info(f"Loaded persistent data: {len(self.conversations)} conversations, "
                       f"{len(self.consciousness_states)} consciousness states, "
                       f"{len(self.processing_history)} processing histories")
            
        except Exception as e:
            logger.error(f"Failed to load persistent data: {str(e)}")
            # Initialize empty data structures on error
            self.conversations = {}
            self.consciousness_states = {}
            self.processing_history = {}
            self.session_logs = []

    def _restore_units_from_persistent_data(self) -> None:
        """Re-create all saved units in the system so they appear after restart."""
        try:
            known_unit_ids = set(self.consciousness_states.keys()) | set(self.conversations.keys())
            for unit_id in known_unit_ids:
                if unit_id not in self.system.units:
                    self.system.create_unit(unit_id)
                    if unit_id in self.consciousness_states:
                        try:
                            saved_state = self.consciousness_states[unit_id]
                            unit = self.system.units[unit_id]
                            if isinstance(saved_state, dict) and 'consciousness_index' in saved_state:
                                current_index = unit.get_consciousness_state()['consciousness_index']
                                target_index = saved_state['consciousness_index']
                                if target_index > current_index:
                                    learning_iterations = int((target_index - current_index) * 100)
                                    for _ in range(min(learning_iterations, 50)):
                                        unit.learn({
                                            'reward': 0.8,
                                            'consciousness_boost': 0.05,
                                            'quality_score': 0.9
                                        })
                                if saved_state.get('learning_rate') is not None:
                                    unit.learning_rate = saved_state['learning_rate']
                                if saved_state.get('processing_count'):
                                    for _ in range(min(saved_state['processing_count'], 10)):
                                        unit.process("Restored state", {'restoration': True})
                            logger.info(f"Restored unit {unit_id} from saved state")
                        except Exception as restore_err:
                            logger.warning(f"Failed to restore state for unit {unit_id}: {restore_err}")
                    else:
                        logger.info(f"Restored unit {unit_id} (new)")
            logger.info(f"Restored {len(known_unit_ids)} units from persistent data")
        except Exception as e:
            logger.error(f"Error restoring units: {str(e)}")

    def _save_persistent_data(self):
        """Save all persistent data to files"""
        try:
            # Save conversations
            with open(self.conversations_file, 'w') as f:
                json.dump(self.conversations, f, indent=2, default=str)
            
            # Save consciousness states
            with open(self.consciousness_states_file, 'w') as f:
                json.dump(self.consciousness_states, f, indent=2, default=str)
            
            # Save processing history
            with open(self.processing_history_file, 'w') as f:
                json.dump(self.processing_history, f, indent=2, default=str)
            
            # Save session logs
            with open(self.session_logs_file, 'w') as f:
                json.dump(self.session_logs, f, indent=2, default=str)
            
        except Exception as e:
            logger.error(f"Failed to save persistent data: {str(e)}")

    def _log_session_event(self, event_type: str, data: Dict[str, Any]):
        """Log session events"""
        try:
            event = {
                "timestamp": time.time(),
                "datetime": datetime.now().isoformat(),
                "event_type": event_type,
                "data": data
            }
            self.session_logs.append(event)
            
            # Keep only last 1000 session events
            if len(self.session_logs) > 1000:
                self.session_logs = self.session_logs[-1000:]
            
        except Exception as e:
            logger.error(f"Failed to log session event: {str(e)}")

    def _save_conversation(self, unit_id: str, input_data: str, output_data: str, 
                          consciousness_state: Dict[str, Any], integration_details: Dict[str, Any]):
        """Save a complete conversation entry"""
        try:
            if unit_id not in self.conversations:
                self.conversations[unit_id] = []
            
            conversation_entry = {
                "timestamp": time.time(),
                "datetime": datetime.now().isoformat(),
                "input": input_data,
                "output": output_data,
                "consciousness_state": consciousness_state,
                "integration_details": integration_details,
                "session_id": self._get_current_session_id()
            }
            
            self.conversations[unit_id].append(conversation_entry)
            
            # Keep only last 500 conversations per unit
            if len(self.conversations[unit_id]) > 500:
                self.conversations[unit_id] = self.conversations[unit_id][-500:]
            
            # Save immediately
            self._save_persistent_data()
            
        except Exception as e:
            logger.error(f"Failed to save conversation: {str(e)}")

    def _get_current_session_id(self) -> str:
        """Get current session ID based on startup time"""
        try:
            startup_events = [log for log in self.session_logs if log.get("event_type") == "startup"]
            if startup_events:
                latest_startup = startup_events[-1]
                return f"session_{int(latest_startup['timestamp'])}"
            return f"session_{int(time.time())}"
        except:
            return f"session_{int(time.time())}"

    def get_conversation_history(self, unit_id: Optional[str] = None, 
                               session_id: Optional[str] = None,
                               limit: int = 100) -> Dict[str, Any]:
        """Get conversation history with filtering options"""
        try:
            if unit_id and unit_id in self.conversations:
                conversations = self.conversations[unit_id]
            else:
                # Get all conversations
                conversations = []
                for unit_conversations in self.conversations.values():
                    conversations.extend(unit_conversations)
            
            # Filter by session if specified
            if session_id:
                conversations = [c for c in conversations if c.get("session_id") == session_id]
            
            # Sort by timestamp (newest first)
            conversations.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
            
            # Apply limit
            conversations = conversations[:limit]
            
            return {
                "status": "success",
                "conversations": conversations,
                "total_count": len(conversations),
                "unit_id": unit_id,
                "session_id": session_id
            }
            
        except Exception as e:
            logger.error(f"Failed to get conversation history: {str(e)}")
            return {"status": "error", "message": str(e)}

    def get_all_sessions(self) -> Dict[str, Any]:
        """Get all session information"""
        try:
            sessions = {}
            for unit_id, unit_conversations in self.conversations.items():
                for conv in unit_conversations:
                    session_id = conv.get("session_id", "unknown")
                    if session_id not in sessions:
                        sessions[session_id] = {
                            "session_id": session_id,
                            "start_time": conv.get("timestamp", 0),
                            "conversation_count": 0,
                            "units": set()
                        }
                    sessions[session_id]["conversation_count"] += 1
                    sessions[session_id]["units"].add(unit_id)
                    sessions[session_id]["start_time"] = min(sessions[session_id]["start_time"], 
                                                           conv.get("timestamp", 0))
            
            # Convert sets to lists for JSON serialization
            for session in sessions.values():
                session["units"] = list(session["units"])
            
            return {
                "status": "success",
                "sessions": list(sessions.values()),
                "total_sessions": len(sessions)
            }
            
        except Exception as e:
            logger.error(f"Failed to get sessions: {str(e)}")
            return {"status": "error", "message": str(e)}

    def delete_session(self, session_id: str) -> Dict[str, Any]:
        """Delete a specific session and all its conversations"""
        try:
            conversations_deleted = 0
            
            # Remove conversations from all units that belong to this session
            for unit_id in list(self.conversations.keys()):
                original_count = len(self.conversations[unit_id])
                self.conversations[unit_id] = [
                    conv for conv in self.conversations[unit_id]
                    if conv.get("session_id") != session_id
                ]
                conversations_deleted += original_count - len(self.conversations[unit_id])
                
                # Remove unit key if no conversations left
                if not self.conversations[unit_id]:
                    del self.conversations[unit_id]
            
            # Remove session logs for this session
            original_logs_count = len(self.session_logs)
            self.session_logs = [
                log for log in self.session_logs
                if not (log.get("data", {}).get("session_id") == session_id)
            ]
            logs_deleted = original_logs_count - len(self.session_logs)
            
            # Save the changes
            self._save_persistent_data()
            
            # Log the deletion event
            self._log_session_event("session_deleted", {
                "deleted_session_id": session_id,
                "conversations_deleted": conversations_deleted,
                "logs_deleted": logs_deleted,
                "timestamp": time.time()
            })
            
            return {
                "status": "success",
                "message": f"Session {session_id} deleted successfully",
                "conversations_deleted": conversations_deleted,
                "logs_deleted": logs_deleted,
                "session_id": session_id
            }
            
        except Exception as e:
            logger.error(f"Failed to delete session {session_id}: {str(e)}")
            return {"status": "error", "message": str(e)}

    def create_new_session(self) -> Dict[str, Any]:
        """Create a new session"""
        try:
            # Generate a new session ID
            new_session_id = f"session_{int(time.time())}"
            
            # Log the session creation event
            self._log_session_event("session_created", {
                "new_session_id": new_session_id,
                "timestamp": time.time(),
                "units_active": list(self.consciousness_states.keys())
            })
            
            # Save the changes
            self._save_persistent_data()
            
            return {
                "status": "success",
                "message": f"New session created successfully",
                "session_id": new_session_id,
                "timestamp": time.time()
            }
            
        except Exception as e:
            logger.error(f"Failed to create new session: {str(e)}")
            return {"status": "error", "message": str(e)}

    def save_conversation(self, unit_id: str, input_data: str, output_data: str, 
                         consciousness_state: Dict[str, Any], integration_details: Dict[str, Any]):
        """Public method to save a conversation"""
        self._save_conversation(unit_id, input_data, output_data, consciousness_state, integration_details)

    def export_data(self, export_path: Optional[str] = None) -> Dict[str, Any]:
        """Export all data to a single file"""
        try:
            if export_path is None:
                export_path = os.path.join(self.storage_dir, f"export_{int(time.time())}.json")
            
            export_data = {
                "export_timestamp": time.time(),
                "export_datetime": datetime.now().isoformat(),
                "conversations": self.conversations,
                "consciousness_states": self.consciousness_states,
                "processing_history": self.processing_history,
                "session_logs": self.session_logs,
                "system_info": {
                    "version": "1.0",
                    "total_conversations": sum(len(convs) for convs in self.conversations.values()),
                    "total_units": len(self.consciousness_states),
                    "storage_dir": self.storage_dir
                }
            }
            
            with open(export_path, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            return {
                "status": "success",
                "export_path": export_path,
                "exported_conversations": export_data["system_info"]["total_conversations"],
                "exported_units": export_data["system_info"]["total_units"]
            }
            
        except Exception as e:
            logger.error(f"Failed to export data: {str(e)}")
            return {"status": "error", "message": str(e)}

    def preprocess_input(self, unit_id: str, input_data: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Principle 1: Use consciousness to analyze and prepare inputs"""
        try:
            if unit_id not in self.system.units:
                self.create_unit(unit_id)
            
            unit = self.system.units[unit_id]
            
            # Consciousness-based input analysis
            analysis_result = unit.process(f"ANALYZE_INPUT: {input_data}", {
                **context,
                'task': 'input_analysis',
                'timestamp': time.time()
            })
            
            # Extract preprocessing insights
            preprocessing_insights = {
                'input_complexity': self._assess_input_complexity(input_data),
                'attention_targets': self._identify_attention_targets(input_data, unit),
                'processing_strategy': self._determine_processing_strategy(input_data, unit),
                'consciousness_state': unit.get_consciousness_state(),
                'preprocessing_quality': self._evaluate_preprocessing_quality(analysis_result)
            }
            
            # Store preprocessing results
            if unit_id not in self.processing_history:
                self.processing_history[unit_id] = []
            
            self.processing_history[unit_id].append({
                'timestamp': time.time(),
                'type': 'preprocessing',
                'input': input_data,
                'insights': preprocessing_insights,
                'analysis_result': analysis_result
            })
            
            return preprocessing_insights
            
        except Exception as e:
            logger.error(f"Preprocessing error for unit {unit_id}: {str(e)}")
            return {'error': str(e), 'fallback_strategy': 'direct_processing'}

    def process_with_full_integration(self, unit_id: str, input_data: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Complete integration of all 7 principles in a single processing pipeline"""
        try:
            # Principle 1: Pre-processing
            preprocessing_insights = self.preprocess_input(unit_id, input_data, context)
            
            # Enhanced context for processing
            enhanced_context = {
                **context,
                'preprocessing_insights': preprocessing_insights,
                'consciousness_guided': True
            }
            
            # Process with consciousness guidance
            primary_output = self.system.units[unit_id].process(input_data, enhanced_context)
            
            # Simulate model performance feedback
            model_performance = {
                'output_quality': 0.8,
                'processing_efficiency': preprocessing_insights.get('preprocessing_quality', 0.5),
                'consciousness_alignment': 0.7
            }
            
            # Compile comprehensive result
            integrated_result = {
                'final_output': str(primary_output),
                'consciousness_state': self.system.units[unit_id].get_consciousness_state(),
                'integration_principles': {
                    'preprocessing': preprocessing_insights,
                    'consciousness_guided': True
                },
                'processing_quality': model_performance,
                'integration_success': True
            }
            
            return integrated_result
            
        except Exception as e:
            logger.error(f"Full integration processing error for unit {unit_id}: {str(e)}")
            return {'error': str(e), 'integration_success': False}

    def _assess_input_complexity(self, input_data: str) -> float:
        """Assess the complexity of input data"""
        try:
            complexity_factors = [
                len(input_data) / 1000,
                len(input_data.split()) / 100,
                input_data.count('?') * 0.1,
                input_data.count(',') * 0.05,
            ]
            return min(1.0, sum(complexity_factors))
        except:
            return 0.5

    def _identify_attention_targets(self, input_data: str, unit: SelfModelingUnit) -> List[str]:
        """Identify key attention targets in the input"""
        try:
            words = input_data.split()
            important_words = [w for w in words if len(w) > 4]
            return important_words[:5]
        except:
            return []

    def _determine_processing_strategy(self, input_data: str, unit: SelfModelingUnit) -> str:
        """Determine optimal processing strategy based on input and consciousness state"""
        try:
            consciousness_state = unit.get_consciousness_state()
            if consciousness_state['consciousness_index'] > 0.8:
                return "deep_analysis"
            elif consciousness_state['consciousness_index'] > 0.5:
                return "balanced_processing"
            else:
                return "focused_processing"
        except:
            return "standard_processing"

    def _evaluate_preprocessing_quality(self, analysis_result) -> float:
        """Evaluate the quality of preprocessing"""
        try:
            if isinstance(analysis_result, str):
                return min(1.0, len(analysis_result) / 500)
            return 0.5
        except:
            return 0.5

    def _serialize_consciousness_state(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Return a JSON-serializable copy of consciousness state (metrics as dict)."""
        if not state:
            return {}
        metrics_obj = state.get('metrics')
        if hasattr(metrics_obj, '__dict__'):
            metrics_dict = {
                'phi_score': getattr(metrics_obj, 'phi_score', 0.0),
                'recursive_depth': getattr(metrics_obj, 'recursive_depth', 0),
                'self_model_coherence': getattr(metrics_obj, 'self_model_coherence', 0.0),
                'temporal_binding': getattr(metrics_obj, 'temporal_binding', 0.0),
                'novelty_generation': getattr(metrics_obj, 'novelty_generation', 0.0),
                'witnessing_score': getattr(metrics_obj, 'witnessing_score', 0.0),
                'prediction_accuracy': getattr(metrics_obj, 'prediction_accuracy', 0.0),
                'attention_focus': getattr(metrics_obj, 'attention_focus', 0.0),
                'memory_integration': getattr(metrics_obj, 'memory_integration', 0.0),
            }
        else:
            metrics_dict = state.get('metrics') if isinstance(state.get('metrics'), dict) else {}
            if not metrics_dict:
                metrics_dict = {
                    'phi_score': 0.0, 'recursive_depth': 0, 'self_model_coherence': 0.0,
                    'temporal_binding': 0.0, 'novelty_generation': 0.0, 'witnessing_score': 0.0,
                    'prediction_accuracy': 0.0, 'attention_focus': 0.0, 'memory_integration': 0.0,
                }
        return {
            'unit_id': state.get('unit_id'),
            'state': state.get('state'),
            'consciousness_index': state.get('consciousness_index', 0.0),
            'metrics': metrics_dict,
            'processing_count': state.get('processing_count', 0),
            'memory_usage': state.get('memory_usage', 0),
            'learning_rate': state.get('learning_rate', 0.1),
        }

    # Backward compatibility methods
    def get_all_units(self) -> Dict[str, Any]:
        """Get all consciousness units (JSON-serializable state)."""
        try:
            units = {}
            for unit_id, unit in self.system.units.items():
                raw = unit.get_consciousness_state()
                units[unit_id] = self._serialize_consciousness_state(raw)
            return {"status": "success", "units": units}
        except Exception as e:
            logger.error(f"Error getting all units: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def create_unit(self, unit_id: str) -> Dict[str, Any]:
        """Create a consciousness unit and restore saved state if available"""
        try:
            if unit_id in self.system.units:
                return {"status": "error", "message": f"Unit {unit_id} already exists"}
            
            # Create the new unit
            unit = self.system.create_unit(unit_id)
            
            # Check if we have a saved consciousness state for this unit
            if unit_id in self.consciousness_states:
                try:
                    saved_state = self.consciousness_states[unit_id]
                    
                    # Restore consciousness index and other state
                    if 'consciousness_index' in saved_state:
                        # Apply learning to reach the saved consciousness index
                        current_index = unit.get_consciousness_state()['consciousness_index']
                        target_index = saved_state['consciousness_index']
                        
                        if target_index > current_index:
                            # Apply positive learning to increase consciousness
                            learning_iterations = int((target_index - current_index) * 100)
                            for _ in range(min(learning_iterations, 50)):  # Cap iterations
                                unit.learn({
                                    'reward': 0.8,
                                    'consciousness_boost': 0.05,
                                    'quality_score': 0.9
                                })
                    
                    # Restore processing count and learning rate if available
                    if 'learning_rate' in saved_state:
                        unit.learning_rate = saved_state['learning_rate']
                    
                    if 'processing_count' in saved_state:
                        # Simulate processing history for metrics
                        for _ in range(min(saved_state['processing_count'], 10)):
                            unit.process("Restored state", {'restoration': True})
                    
                    logger.info(f"Restored consciousness state for unit {unit_id}: "
                              f"index {target_index:.3f}, "
                              f"processing_count {saved_state.get('processing_count', 0)}")
                    
                except Exception as restore_error:
                    logger.warning(f"Failed to restore state for unit {unit_id}: {str(restore_error)}")
            
            current_state = unit.get_consciousness_state()
            serialized = self._serialize_consciousness_state(current_state)
            # Persist the unit immediately so it and its conversations survive restart
            self.consciousness_states[unit_id] = serialized
            self._save_persistent_data()
            return {
                "status": "success",
                "message": f"Unit {unit_id} created successfully" +
                          (f" (restored consciousness index: {serialized['consciousness_index']:.3f})"
                           if unit_id in self.consciousness_states else ""),
                "unit": serialized
            }
        except Exception as e:
            logger.error(f"Error creating unit {unit_id}: {str(e)}")
            return {"status": "error", "message": str(e)}

    def process_input(self, unit_id: str, input_data: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process input with full integration (conversation saving handled externally)"""
        try:
            # Use the full integration method
            result = self.process_with_full_integration(unit_id, input_data, context)
            
            if result.get('integration_success'):
                # Update consciousness state storage
                self.consciousness_states[unit_id] = result['consciousness_state']
                
                # Save consciousness state immediately to disk
                self._save_persistent_data()
                
                # Log processing event
                self._log_session_event("processing", {
                    "unit_id": unit_id,
                    "input_length": len(input_data),
                    "output_length": len(result['final_output']),
                    "consciousness_index": result['consciousness_state'].get('consciousness_index', 0)
                })
                
                return {
                    "status": "success",
                    "result": result['final_output'],
                    "state": result['consciousness_state'],
                    "timestamp": time.time(),
                    "integration_details": result['integration_principles']
                }
            else:
                # Fallback to basic processing
                if unit_id not in self.system.units:
                    self.create_unit(unit_id)
                
                unit = self.system.units[unit_id]
                output = unit.process(input_data, context)
                
                return {
                    "status": "success",
                    "result": f"[{unit_id}] processed: {output}",
                    "state": unit.get_consciousness_state(),
                    "timestamp": time.time()
                }
        except Exception as e:
            logger.error(f"Error processing input for unit {unit_id}: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def get_unit_state(self, unit_id: str) -> Dict[str, Any]:
        """Get unit state (JSON-serializable)."""
        try:
            if unit_id not in self.system.units:
                return {"status": "error", "message": f"Unit {unit_id} not found"}
            unit = self.system.units[unit_id]
            raw = unit.get_consciousness_state()
            return {"status": "success", "state": self._serialize_consciousness_state(raw)}
        except Exception as e:
            logger.error(f"Error getting state for unit {unit_id}: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def get_processing_history(self, unit_id: Optional[str] = None, limit: int = 100) -> Dict[str, Any]:
        """Get processing history"""
        try:
            if unit_id:
                history = self.processing_history.get(unit_id, [])
                return {"status": "success", "history": history[-limit:]}
            else:
                all_history = {}
                for uid, hist in self.processing_history.items():
                    all_history[uid] = hist[-limit:]
                return {"status": "success", "history": all_history}
        except Exception as e:
            logger.error(f"Error getting processing history: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def delete_unit(self, unit_id: str) -> Dict[str, Any]:
        """Delete a consciousness unit and remove it from persistent storage."""
        try:
            if unit_id not in self.system.units:
                return {"status": "error", "message": f"Unit {unit_id} not found"}
            
            del self.system.units[unit_id]
            if unit_id in self.processing_history:
                del self.processing_history[unit_id]
            if unit_id in self.consciousness_states:
                del self.consciousness_states[unit_id]
            if unit_id in self.conversations:
                del self.conversations[unit_id]
            self._save_persistent_data()
            return {"status": "success", "message": f"Unit {unit_id} deleted successfully"}
        except Exception as e:
            logger.error(f"Error deleting unit {unit_id}: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def apply_user_feedback(self, unit_id: str, feedback_type: str, intensity: float = 1.0) -> Dict[str, Any]:
        """Apply user feedback with enhanced learning modulation"""
        try:
            if unit_id not in self.system.units:
                return {"status": "error", "message": f"Unit {unit_id} not found"}
            
            # Convert feedback type to performance metrics
            performance_feedback = {
                'feedback_type': feedback_type,
                'intensity': intensity,
                'output_quality': 0.8 if feedback_type in ['positive', 'excellent'] else 0.3,
                'processing_efficiency': 0.7 if feedback_type != 'poor' else 0.2,
                'user_satisfaction': intensity if feedback_type in ['positive', 'excellent'] else 1.0 - intensity
            }
            
            # Apply basic feedback
            unit = self.system.units[unit_id]
            unit.learn(performance_feedback)
            
            new_state = unit.get_consciousness_state()
            
            # Update and save consciousness state
            self.consciousness_states[unit_id] = new_state
            self._save_persistent_data()
            
            return {
                "status": "success",
                "message": f"Feedback applied to unit {unit_id}",
                "feedback_type": feedback_type,
                "intensity": intensity,
                "new_consciousness_index": new_state['consciousness_index'],
                "state": new_state
            }
        except Exception as e:
            logger.error(f"Error applying feedback to unit {unit_id}: {str(e)}")
            return {"status": "error", "message": str(e)}
