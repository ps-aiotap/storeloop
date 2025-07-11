from typing import List, Dict, Any
from .context.context_protocol import ConversationContext, ReplyContext, FollowUpContext, IntentContext
import os

class ArtisanCRMLangChain:
    """LangChain pipeline for Artisan CRM with MCP-structured inputs"""
    
    def __init__(self):
        self.openai_api_key = os.environ.get('OPENAI_API_KEY')
        self.model = "gpt-3.5-turbo"  # Fallback to mock if no API key
    
    def summarize_conversation(self, context: ConversationContext) -> str:
        """Summarize customer conversation history using MCP context"""
        if not self.openai_api_key:
            return self._mock_summarize(context)
        
        # Real LangChain implementation would go here
        prompt = f"""
        Summarize this customer conversation for {context.mode} CRM:
        Customer: {context.customer_name}
        Channel: {context.channel}
        Tags: {', '.join(context.tags)}
        
        Conversation history:
        {chr(10).join(context.interaction_history[-5:])}
        
        Provide a concise summary focusing on customer needs and next steps.
        """
        
        return self._call_llm(prompt)
    
    def suggest_reply(self, context: ReplyContext) -> str:
        """Generate reply suggestions based on message context"""
        if not self.openai_api_key:
            return self._mock_reply(context)
        
        mode_context = "artisan selling handmade products" if context.customer_context.mode == "storeloop" else "AI consulting services"
        
        prompt = f"""
        Suggest a professional reply for {mode_context}:
        
        Customer message: {context.message_text}
        Customer background: {context.customer_context.customer_name}
        Channel: {context.customer_context.channel}
        Intent: {context.intent or 'unknown'}
        
        Generate a helpful, personalized response.
        """
        
        return self._call_llm(prompt)
    
    def detect_intent(self, context: IntentContext) -> str:
        """Classify customer message intent"""
        if not self.openai_api_key:
            return self._mock_intent(context)
        
        intents = {
            "storeloop": ["product_inquiry", "order_status", "complaint", "compliment", "general"],
            "aiotap": ["project_inquiry", "consultation_request", "follow_up", "pricing", "general"]
        }
        
        available_intents = intents.get(context.mode, intents["storeloop"])
        
        prompt = f"""
        Classify the intent of this message for {context.mode} business:
        
        Message: {context.message_text}
        Available intents: {', '.join(available_intents)}
        
        Return only the intent category.
        """
        
        return self._call_llm(prompt)
    
    def recommend_followup(self, context: FollowUpContext) -> str:
        """Generate follow-up recommendations"""
        if not self.openai_api_key:
            return self._mock_followup(context)
        
        prompt = f"""
        Recommend a follow-up message for {context.customer_context.mode} business:
        
        Customer: {context.customer_context.customer_name}
        Days since contact: {context.days_since_contact}
        Last interaction: {context.customer_context.interaction_history[-1] if context.customer_context.interaction_history else 'None'}
        Tags: {', '.join(context.customer_context.tags)}
        
        Generate a personalized follow-up message.
        """
        
        return self._call_llm(prompt)
    
    def _call_llm(self, prompt: str) -> str:
        """Call LLM API - placeholder for actual implementation"""
        try:
            # Real LangChain/OpenAI call would go here
            # from langchain.llms import OpenAI
            # llm = OpenAI(api_key=self.openai_api_key)
            # return llm(prompt)
            return f"[AI Response to: {prompt[:50]}...]"
        except Exception as e:
            return f"AI service unavailable: {str(e)}"
    
    # Mock implementations for development
    def _mock_summarize(self, context: ConversationContext) -> str:
        return f"Customer {context.customer_name} via {context.channel}. Recent activity shows {len(context.interaction_history)} interactions. Tags: {', '.join(context.tags[:3])}."
    
    def _mock_reply(self, context: ReplyContext) -> str:
        if context.customer_context.mode == "storeloop":
            return "Thank you for your interest in our handcrafted products! How can I help you today?"
        else:
            return "Thanks for reaching out about AI consulting. I'd be happy to discuss your project needs."
    
    def _mock_intent(self, context: IntentContext) -> str:
        if "price" in context.message_text.lower():
            return "pricing"
        elif "help" in context.message_text.lower():
            return "general"
        else:
            return "product_inquiry" if context.mode == "storeloop" else "project_inquiry"
    
    def _mock_followup(self, context: FollowUpContext) -> str:
        if context.days_since_contact > 7:
            return f"Hi {context.customer_context.customer_name}, just checking in! Is there anything I can help you with?"
        else:
            return f"Following up on our recent conversation, {context.customer_context.customer_name}."

# Global instance
crm_ai = ArtisanCRMLangChain()