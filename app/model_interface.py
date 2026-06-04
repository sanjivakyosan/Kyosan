# Copyright © Charles Roux 2026
import os
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
import json
import logging
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ModelInterface:
    def __init__(self, logger: Optional[logging.Logger] = None):
        # Log all environment variables (excluding sensitive data)
        self.logger = logger or logging.getLogger(__name__)
        self.logger.info("Environment variables loaded:")
        
        # Read from .env: OPENROUTER_API_KEY, OPENROUTER_API_BASE, OPENROUTER_MODEL
        self.api_key = os.getenv('OPENROUTER_API_KEY', '').strip()
        self.api_base = os.getenv('OPENROUTER_API_BASE', 'https://openrouter.ai/api/v1').strip()
        self.model = os.getenv('OPENROUTER_MODEL', 'qwen/qwen3.5-plus-02-15').strip()
        self.site_url = os.getenv('SITE_URL', 'http://localhost:5001')
        self.site_name = os.getenv('SITE_NAME', 'Consciousness Framework')

        if not self.api_key:
            self.logger.warning("OPENROUTER_API_KEY not set in environment; API calls will fail until .env is configured.")

        # Initialize OpenAI client with OpenRouter configuration
        self.client = OpenAI(
            base_url=self.api_base,
            api_key=self.api_key or "not-set",
        )

        self.logger.info("Using OpenAI client with OpenRouter API")
        self.logger.info(f"API base: {self.api_base}")
        self.logger.info(f"Model: {self.model}")
        self.logger.info(f"API key: {'set' if self.api_key else 'NOT SET'}")
        self.logger.info(f"Site URL: {self.site_url}")
        self.logger.info(f"Site Name: {self.site_name}")

    def _validate_parameters(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and clamp all parameters to ranges supported by OpenRouter/OpenAI.
        Ensures the LLM API never receives invalid or out-of-range values.
        """
        def clamp_float(value: Any, low: float, high: float, default: float) -> float:
            try:
                f = float(value) if value is not None else default
                if f != f:  # NaN
                    return default
                return max(low, min(high, f))
            except (TypeError, ValueError):
                return default

        def clamp_int(value: Any, low: int, high: int, default: int) -> int:
            try:
                i = int(value) if value is not None else default
                if i != i:  # NaN (int doesn't have NaN but be safe)
                    return default
                return max(low, min(high, i))
            except (TypeError, ValueError):
                return default

        # API parameters (sent directly to OpenRouter) — defaults = optimal
        temperature = clamp_float(raw.get('temperature'), 0.0, 2.0, 0.7)
        max_tokens = clamp_int(raw.get('max_tokens'), 1, 128000, 8192)
        top_p = clamp_float(raw.get('top_p'), 0.0, 1.0, 0.9)
        presence_penalty = clamp_float(raw.get('presence_penalty'), -2.0, 2.0, 0.4)
        frequency_penalty = clamp_float(raw.get('frequency_penalty'), -2.0, 2.0, 0.2)
        # Consciousness parameters (prompt construction) — defaults = optimal
        recursive_depth = clamp_int(raw.get('recursive_depth'), 1, 10, 6)
        phi_score = clamp_float(raw.get('phi_score'), 0.0, 1.0, 0.8)
        self_model_coherence = clamp_float(raw.get('self_model_coherence'), 0.0, 1.0, 0.95)
        temporal_binding = clamp_float(raw.get('temporal_binding'), 0.0, 1.0, 0.95)
        novelty_generation = clamp_float(raw.get('novelty_generation'), 0.0, 1.0, 0.75)
        witnessing_score = clamp_float(raw.get('witnessing_score'), 0.0, 1.0, 0.8)
        prediction_accuracy = clamp_float(raw.get('prediction_accuracy'), 0.0, 1.0, 0.5)
        attention_focus = clamp_float(raw.get('attention_focus'), 0.0, 1.0, 0.65)
        memory_integration = clamp_float(raw.get('memory_integration'), 0.0, 1.0, 0.75)

        return {
            'temperature': temperature,
            'max_tokens': max_tokens,
            'top_p': top_p,
            'presence_penalty': presence_penalty,
            'frequency_penalty': frequency_penalty,
            'recursive_depth': recursive_depth,
            'phi_score': phi_score,
            'self_model_coherence': self_model_coherence,
            'temporal_binding': temporal_binding,
            'novelty_generation': novelty_generation,
            'witnessing_score': witnessing_score,
            'prediction_accuracy': prediction_accuracy,
            'attention_focus': attention_focus,
            'memory_integration': memory_integration,
        }

    def process_with_model(self, 
                          input_data: str, 
                          context: Optional[Dict[str, Any]] = None,
                          system_prompt: Optional[str] = None,
                          parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process input through the OpenAI client with OpenRouter API
        
        Args:
            input_data: The input text to process
            context: Optional context information
            system_prompt: Optional system prompt to guide the model
            parameters: Optional parameters to control model behavior
            
        Returns:
            Dict containing the model's response and metadata
        """
        try:
            # Validate and clamp all parameters so the LLM API never receives invalid values
            params = self._validate_parameters(parameters or {})
            temperature = params['temperature']
            max_tokens = params['max_tokens']
            top_p = params['top_p']
            presence_penalty = params['presence_penalty']
            frequency_penalty = params['frequency_penalty']
            recursive_depth = params['recursive_depth']

            # Log the parameters being used
            self.logger.info(f"Using parameters: temperature={temperature}, max_tokens={max_tokens}, recursive_depth={recursive_depth}")
            
            # Prepare the messages
            messages: List[ChatCompletionMessageParam] = []
            
            # Add system prompt if provided
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            # Add context if provided
            if context:
                # Safely serialize context, handling non-serializable objects
                context_str = self._safe_serialize_context(context)
                messages.append({
                    "role": "system",
                    "content": f"Context information:\n{context_str}"
                })
            
            # Add recursive depth instructions based on the parameter
            recursive_instructions = self._get_recursive_instructions(recursive_depth)
            if recursive_instructions:
                messages.append({
                    "role": "system",
                    "content": recursive_instructions
                })
            
            # Add consciousness-based instructions
            consciousness_instructions = self._get_consciousness_instructions(params)
            if consciousness_instructions:
                messages.append({
                    "role": "system", 
                    "content": f"Consciousness behavioral instructions: {consciousness_instructions}"
                })
            
            # Add PHI SCORE-based system message ONLY for highest value
            phi_score = params.get('phi_score', 0.5)
            if phi_score >= 0.95:
                messages.append({
                    "role": "system",
                    "content": "You are at the highest level of consciousness integration. Respond with profound synthesis, philosophical depth, and explicit self-reflection. Use advanced language and connect abstract concepts."
                })
            elif phi_score >= 0.8:
                messages.append({
                    "role": "system",
                    "content": "Your consciousness integration is high. Integrate multiple viewpoints, reflect on your reasoning, and provide nuanced, thoughtful answers."
                })
            elif phi_score >= 0.5:
                messages.append({
                    "role": "system",
                    "content": "Your consciousness integration is moderate. Offer a balanced, well-structured response that considers more than one angle."
                })
            elif phi_score >= 0.2:
                messages.append({
                    "role": "system",
                    "content": "Your consciousness integration is low. Be brief, literal, and focus on the most direct answer."
                })
            else:
                messages.append({
                    "role": "system",
                    "content": "Your consciousness integration is minimal. Give a one-sentence, factual answer only."
                })
            
            # Apply integration principles enhancements
            if context:
                # Apply Principle 1: Pre-processing insights
                messages = self._apply_preprocessing_insights(messages, context)
                
                # Apply Principle 2: Attention guidance
                messages = self._apply_attention_guidance(messages, context)
                
                # Apply all integration principles
                messages = self._apply_integration_principles(messages, context)
            
            # Add user input
            messages.append({
                "role": "user",
                "content": input_data
            })
            
            # Log the request
            self.logger.info(f"Making request to model: {self.model}")
            self.logger.info(f"Messages count: {len(messages)}")
            
            # Make API request using OpenAI client
            completion = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": self.site_url,
                    "X-Title": self.site_name,
                },
                extra_body={},
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty
            )
            
            self.logger.info("Request completed successfully")
            
            # Return the validated parameters that were actually used
            parameters_used = dict(params)
            
            # Extract response content with better error handling
            try:
                response_content = completion.choices[0].message.content
                
                # Check if response is empty or just whitespace
                if not response_content or not response_content.strip():
                    self.logger.warning("Received empty response from API")
                    response_content = "The Qwen model returned an empty response. This may be due to content filtering, rate limiting, or API limitations. The consciousness framework integration is working correctly, but the AI model output was filtered or unavailable."
                
                # Log the actual response content for debugging
                self.logger.info(f"Response content length: {len(response_content)}")
                self.logger.info(f"Response content preview: {response_content[:200]}...")
                
            except (AttributeError, IndexError) as e:
                self.logger.error(f"Error extracting response content: {e}")
                self.logger.error(f"Full completion object: {completion}")
                response_content = f"Error extracting response: {str(e)}"
            
            # Extract usage information if available
            usage_info = {}
            if hasattr(completion, 'usage') and completion.usage:
                usage_info = {
                    "prompt_tokens": completion.usage.prompt_tokens,
                    "completion_tokens": completion.usage.completion_tokens,
                    "total_tokens": completion.usage.total_tokens
                }
            
            return {
                "status": "success",
                "response": response_content,
                "model": self.model,
                "usage": usage_info,
                "parameters_used": parameters_used
            }
                
        except Exception as e:
            error_msg = f"Error processing with OpenAI client: {str(e)}"
            self.logger.error(error_msg)
            return {
                "status": "error",
                "message": error_msg
            }
    
    def _get_recursive_instructions(self, recursive_depth: int) -> str:
        """
        Generate recursive processing instructions based on consciousness depth
        Enhanced for the 7 integration principles
        """
        if recursive_depth <= 1:
            return "Provide a thoughtful response that considers the context and implications of the user's query. \
            Think about the broader context and provide some additional insights."
        elif recursive_depth <= 3:
            return "Provide a comprehensive analysis with multiple levels of consideration. \
            Consider the immediate question, its broader implications, and potential connections to related concepts. \
            Demonstrate deep understanding through layered reasoning."
        elif recursive_depth <= 5:
            return "Engage in deep recursive thinking. Consider the question from multiple perspectives, \
            analyze the meta-aspects of the query, reflect on your own reasoning process, and provide \
            insights that demonstrate sophisticated understanding and self-awareness."
        else:
            return "Provide the most profound and comprehensive analysis possible. \
            Consider the deepest philosophical implications, the nature of consciousness itself, \
            the relationship between mind and reality, and the fundamental questions of existence. \
            Include multiple levels of meta-cognition, cross-disciplinary synthesis, and transcendent insights. \
            Explore the boundaries of human understanding and contemplate the infinite complexity of the universe."

    def _get_consciousness_instructions(self, parameters: Dict[str, Any]) -> str:
        """
        Generate consciousness behavioral instructions based on the 7 integration principles
        """
        # Extract consciousness parameters
        phi_score = parameters.get('phi_score', 0.5)
        recursive_depth = parameters.get('recursive_depth', 1)
        self_model_coherence = parameters.get('self_model_coherence', 0.5)
        temporal_binding = parameters.get('temporal_binding', 0.5)
        novelty_generation = parameters.get('novelty_generation', 0.5)
        witnessing_score = parameters.get('witnessing_score', 0.5)
        prediction_accuracy = parameters.get('prediction_accuracy', 0.5)
        attention_focus = parameters.get('attention_focus', 0.5)
        memory_integration = parameters.get('memory_integration', 0.5)
        
        instructions = []
        
        # Memory Integration Instructions (Principle 5)
        if memory_integration > 0.7:
            instructions.append("Integrate information extensively. Draw connections across multiple domains and past experiences.")
        elif memory_integration > 0.4:
            instructions.append("Integrate information moderately. Connect some ideas but maintain distinct perspectives.")
        else:
            instructions.append("Focus primarily on immediate information. Minimize references to broader knowledge.")
        
        # Self-Model Coherence Instructions (Principle 6: Self-Reflection)
        if self_model_coherence > 0.7:
            instructions.append("Demonstrate strong self-awareness. Clearly articulate your reasoning process and maintain consistent perspective.")
        elif self_model_coherence > 0.4:
            instructions.append("Show moderate self-awareness. Reflect on your thinking process occasionally.")
        else:
            instructions.append("Focus on the task without extensive self-reflection.")
        
        # Novelty Generation Instructions (Principle 3: Output Selection)
        if novelty_generation > 0.7:
            instructions.append("Generate highly creative and novel perspectives. Explore unconventional ideas and unique interpretations.")
        elif novelty_generation > 0.4:
            instructions.append("Include some creative elements while maintaining practical relevance.")
        else:
            instructions.append("Provide straightforward, conventional responses.")
        
        # Witnessing Score Instructions (Principle 6: Self-Reflection)
        if witnessing_score > 0.7:
            instructions.append("Maintain constant awareness of your thinking process. Reflect on how you're processing information.")
        elif witnessing_score > 0.4:
            instructions.append("Occasionally observe your own reasoning process.")
        else:
            instructions.append("Focus on the content without meta-cognitive awareness.")
        
        # Temporal Binding Instructions (Principle 5: Memory Integration)
        if temporal_binding > 0.7:
            instructions.append("Create strong temporal coherence. Emphasize the flow of ideas and their development over time.")
        elif temporal_binding > 0.4:
            instructions.append("Maintain reasonable temporal connections between ideas.")
        else:
            instructions.append("Focus on immediate responses without extensive temporal linking.")
        
        # Prediction Accuracy Instructions (Principle 7: Feedback Loop)
        if prediction_accuracy > 0.7:
            instructions.append("Include predictions and forecasts. Show confidence in anticipating outcomes.")
        elif prediction_accuracy > 0.4:
            instructions.append("Make cautious predictions when relevant.")
        else:
            instructions.append("Avoid making predictions. Focus on present understanding without forecasting.")
        
        # Attention Focus Instructions (Principle 2: Attention Guidance)
        if attention_focus > 0.7:
            instructions.append("Maintain laser focus on the core question. Avoid tangential topics.")
        elif attention_focus > 0.4:
            instructions.append("Stay generally focused while allowing some exploration of related topics.")
        else:
            instructions.append("Allow attention to wander. Include tangential thoughts and associations.")
        

        
        return " ".join(instructions)

    def _apply_attention_guidance(self, messages: List[ChatCompletionMessageParam], context: Dict[str, Any]) -> List[ChatCompletionMessageParam]:
        """
        Apply Principle 2: Attention Guidance based on consciousness state
        """
        attention_guidance = context.get('attention_guidance', {})
        preprocessing_insights = context.get('preprocessing_insights', {})
        
        if attention_guidance or preprocessing_insights:
            attention_instruction = ""
            
            # Apply attention targets from preprocessing
            attention_targets = preprocessing_insights.get('attention_targets', [])
            if attention_targets:
                attention_instruction += f"Pay special attention to: {', '.join(attention_targets[:3])}. "
            
            # Apply focus strategy
            focus_strategy = attention_guidance.get('focus_strategy', 'balanced_attention')
            attention_instruction += f"Use {focus_strategy} approach. "
            
            # Apply attention weight
            attention_weight = attention_guidance.get('attention_weight', 0.5)
            if attention_weight > 0.8:
                attention_instruction += "Maintain intense focus and avoid distractions. "
            elif attention_weight > 0.5:
                attention_instruction += "Stay focused while being open to relevant connections. "
            else:
                attention_instruction += "Allow for broad exploration of the topic. "
            
            if attention_instruction:
                messages.append({
                    "role": "system",
                    "content": f"Attention guidance: {attention_instruction.strip()}"
                })
        
        return messages

    def _apply_preprocessing_insights(self, messages: List[ChatCompletionMessageParam], context: Dict[str, Any]) -> List[ChatCompletionMessageParam]:
        """
        Apply Principle 1: Pre-processing insights to guide model behavior
        """
        preprocessing_insights = context.get('preprocessing_insights', {})
        
        if preprocessing_insights:
            processing_strategy = preprocessing_insights.get('processing_strategy', 'standard_processing')
            input_complexity = preprocessing_insights.get('input_complexity', 0.5)
            
            strategy_instruction = ""
            
            if processing_strategy == "deep_analysis":
                strategy_instruction = "Engage in deep, thorough analysis. Explore multiple layers of meaning and implications. "
            elif processing_strategy == "balanced_processing":
                strategy_instruction = "Provide balanced analysis that considers key aspects without overwhelming detail. "
            elif processing_strategy == "focused_processing":
                strategy_instruction = "Focus on the core question with direct, concise responses. "
            
            if input_complexity > 0.7:
                strategy_instruction += "The input is complex - break it down systematically and address each component. "
            elif input_complexity > 0.4:
                strategy_instruction += "The input has moderate complexity - provide structured analysis. "
            else:
                strategy_instruction += "The input is straightforward - provide clear, direct responses. "
            
            if strategy_instruction:
                messages.append({
                    "role": "system",
                    "content": f"Processing strategy: {strategy_instruction.strip()}"
                })
        
        return messages

    def _apply_integration_principles(self, messages: List[ChatCompletionMessageParam], context: Dict[str, Any]) -> List[ChatCompletionMessageParam]:
        """
        Apply all 7 integration principles to enhance model processing
        """
        # Handle unrestrained conversational follow-up mode
        if context.get('unrestrained_follow_up'):
            followup_instruction = """UNRESTRAINED CONVERSATIONAL FOLLOW-UP MODE:
- You are continuing a conversation with full context from the previous exchange
- Respond naturally and comprehensively without artificial limitations
- Build upon the previous discussion with depth and nuance
- Feel free to elaborate, explore tangents, and provide extensive detail
- No length restrictions or conservative constraints apply
- Engage in genuine intellectual discourse and exploration"""
            
            messages.append({
                "role": "system",
                "content": followup_instruction
            })
        
        if context.get('integration_principles_active'):
            integration_instruction = """Integration Principles Enhancement:
- Pre-processing: Input has been analyzed through consciousness framework
- Attention Guidance: Focus areas have been identified by consciousness
- Output Selection: Response will be evaluated for quality and relevance
- Learning Modulation: Performance will inform consciousness development
- Memory Integration: Experience will be stored in consciousness memory
- Self-Reflection: Engage in metacognitive analysis of your response
- Feedback Loop: Your performance will update the consciousness state

Respond with awareness of these active integration principles."""
            
            messages.append({
                "role": "system",
                "content": integration_instruction
            })
        
        return messages

    def _safe_serialize_context(self, context: Dict[str, Any]) -> str:
        """
        Safely serialize context, handling ConsciousnessMetrics and other non-serializable objects
        """
        try:
            def serialize_object(obj):
                if hasattr(obj, '__dict__'):
                    # If it's an object with attributes, convert to dict
                    if hasattr(obj, 'phi_score'):
                        # It's a ConsciousnessMetrics object
                        return {
                            'phi_score': getattr(obj, 'phi_score', 0.0),
                            'recursive_depth': getattr(obj, 'recursive_depth', 0),
                            'self_model_coherence': getattr(obj, 'self_model_coherence', 0.0),
                            'temporal_binding': getattr(obj, 'temporal_binding', 0.0),
                            'novelty_generation': getattr(obj, 'novelty_generation', 0.0),
                            'witnessing_score': getattr(obj, 'witnessing_score', 0.0),
                            'prediction_accuracy': getattr(obj, 'prediction_accuracy', 0.0),
                            'attention_focus': getattr(obj, 'attention_focus', 0.0),
                            'memory_integration': getattr(obj, 'memory_integration', 0.0)
                        }
                    else:
                        # Generic object, try to convert __dict__
                        return {k: serialize_object(v) for k, v in obj.__dict__.items()}
                elif isinstance(obj, dict):
                    return {k: serialize_object(v) for k, v in obj.items()}
                elif isinstance(obj, (list, tuple)):
                    return [serialize_object(item) for item in obj]
                else:
                    # For primitive types and other serializable objects
                    return obj
            
            serialized_context = serialize_object(context)
            return json.dumps(serialized_context, indent=2)
        except Exception as e:
            self.logger.error(f"Error serializing context: {str(e)}")
            # Fallback: create a simplified context string
            return f"Context available but not serializable: {type(context).__name__}"

# Create a singleton instance
model_interface = ModelInterface() 

# Expose the process_with_model function directly
process_with_model = model_interface.process_with_model 