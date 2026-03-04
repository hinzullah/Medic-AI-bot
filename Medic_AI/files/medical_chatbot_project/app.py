"""
Main Gradio Web App - Production-ready medical chatbot
FIXED for Gradio 6.0
"""

import gradio as gr
from src.rag_chatbot import RAGMedicalChatbot
from src.safety_layer import SafeChatbotWrapper
from datetime import datetime
import os


class MedicalChatbotApp:
    def __init__(self):
        """Initialize the web app"""
        try:
            # Try to load RAG chatbot
            base_bot = RAGMedicalChatbot()
            self.bot = SafeChatbotWrapper(base_bot)
            self.has_rag = True
            print("✅ RAG chatbot loaded")
        except Exception as e:
            print(f"⚠️ Could not load RAG chatbot: {e}")
            print("Falling back to simple chatbot...")
            
            from src.simple_chatbot import SimpleMedicalChatbot
            base_bot = SimpleMedicalChatbot()
            self.bot = SafeChatbotWrapper(base_bot)
            self.has_rag = False
        
        self.conversation_log = []
    
    def respond(self, message, history):
        """Generate response for Gradio"""
        
        # Log conversation
        self.conversation_log.append({
            "timestamp": datetime.now().isoformat(),
            "user": message,
            "response": None
        })
        
        # Get response
        response = self.bot.chat(message)
        
        # Update log
        self.conversation_log[-1]["response"] = response
        
        return response
    
    def reset_conversation(self):
        """Reset the chat"""
        self.bot.reset()
        self.conversation_log = []
        return None


def create_interface():
    """Create Gradio interface"""
    
    app = MedicalChatbotApp()
    
    # Custom CSS
    css = """
    .message {
        font-size: 16px;
        padding: 10px;
    }
    """
    
    # Header HTML
    header = """
    <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 15px; margin-bottom: 20px;'>
        <h1 style='margin: 0; font-size: 2.5em;'>🏥 Dr. AI</h1>
        <p style='margin: 10px 0 0 0; font-size: 1.2em;'>Your 24/7 Medical Information Assistant</p>
    </div>

    <div style='padding: 20px; background-color: #000000; border-left: 5px solid #ffc107; border-radius: 8px; margin-bottom: 20px;'>
        <h3 style='margin-top: 0; color: #856404;'>⚠️ Important Medical Disclaimer</h3>
        <ul style='margin: 10px 0; color: #856404;'>
            <li><strong>This AI provides general health information only</strong></li>
            <li><strong>NOT a substitute for professional medical advice, diagnosis, or treatment</strong></li>
            <li><strong>For emergencies, call emergency services immediately (911, 999, 112)</strong></li>
            <li><strong>Always consult qualified healthcare professionals for medical concerns</strong></li>
            <li><strong>Never delay seeking medical care based on information from this chatbot</strong></li>
        </ul>
    </div>
    """
    
    # Create interface (Gradio 6.0 compatible)
    with gr.Blocks() as demo:
        gr.HTML(header)
        
        # ChatInterface (simplified for Gradio 6.0)
        chatbot = gr.ChatInterface(
            fn=app.respond,
            chatbot=gr.Chatbot(height=600),
            textbox=gr.Textbox(
                placeholder="Ask me about your health concerns...",
                container=False,
                scale=7
            ),
            title=None,  # Using custom header above
            description=None,
            examples=[
                "What are the symptoms of a common cold?",
                "How can I improve my sleep quality?",
                "What should I do for a headache?",
                "How much water should I drink daily?",
                "What are the benefits of regular exercise?",
                "How do I know if I'm dehydrated?",
            ]
        )
        
        # Footer
        footer_text = f"""
        <div style='text-align: center; padding: 20px; margin-top: 30px; border-top: 2px solid #e0e0e0;'>
            <p style='color: #666; font-size: 0.9em;'>
                Powered by LangChain + Groq | 
                <strong>For Educational Purposes Only</strong> | 
                This chatbot uses {"RAG with medical knowledge base" if app.has_rag else "AI language model"}
            </p>
            <p style='color: #999; font-size: 0.8em; margin-top: 10px;'>
                Remember: Always consult healthcare professionals for personalized medical advice
            </p>
        </div>
        """
        gr.HTML(footer_text)
    
    return demo, css


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🏥 Starting Dr. AI Medical Chatbot")
    print("="*60 + "\n")
    
    demo, css = create_interface()
    
    demo.launch(
        server_name="0.0.0.0",  # Allow external access
        server_port=7860,
        share=False,  # Set to True to get public URL
        show_error=True
    )