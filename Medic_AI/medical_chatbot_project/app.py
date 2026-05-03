"""
Medical Chatbot App - Clean Version
"""

import sys
import os
import logging
from dotenv import load_dotenv
import gradio as gr
from src.safety_layer import SafeChatbotWrapper

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_DB_PATH = os.path.join(BASE_DIR, "medical_knowledge_db")

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logger.info("="*60)
logger.info("🏥 Starting Medical Chatbot")
logger.info("="*60)

# Load environment
load_dotenv()
logger.info("✅ Environment variables loaded")

# Get PORT
port = int(os.environ.get('PORT', 7860))
logger.info(f"PORT: {port}")

groq_key = os.environ.get('GROQ_API_KEY')
logger.info(f"GROQ_API_KEY found: {bool(groq_key)}")

# Load chatbot
logger.info("Loading chatbot...")
bot = None

try:
    from src.rag_chatbot import RAGMedicalChatbot
    logger.info("Initializing RAG Chatbot...")
    base_bot = RAGMedicalChatbot(knowledge_db_path=KNOWLEDGE_DB_PATH)
    bot = SafeChatbotWrapper(base_bot)
    logger.info("✅ RAG Chatbot loaded")
except Exception as e:
    logger.error(f"RAG Chatbot failed: {e}")
    try:
        from src.simple_chatbot import SimpleMedicalChatbot
        base_bot = SimpleMedicalChatbot()
        bot = SafeChatbotWrapper(base_bot)
        logger.info("✅ Simple Chatbot loaded")
    except Exception as e2:
        logger.error(f"Simple Chatbot failed: {e2}")

# Define response function
def respond(message, history):
    """Generate response"""
    try:
        if bot:
            return bot.chat(message)
        return "Chatbot not initialized"
    except Exception as e:
        logger.error(f"Error: {e}")
        return f"Error: {str(e)}"

# Create interface
logger.info("Creating Gradio interface...")
with gr.Blocks() as demo:
    gr.Markdown("# 🏥 Dr. AI Medical Chatbot")
    gr.Markdown("Ask me about your health concerns...")
    
    chatbot = gr.ChatInterface(
        fn=respond,
        chatbot=gr.Chatbot(height=400),
        textbox=gr.Textbox(
            placeholder="Ask about health...",
            container=False,
            scale=7
        ),
        title=None,
        description=None,
    )

logger.info("✅ Interface created")
logger.info("="*60)
logger.info(f"🚀 Launching on 0.0.0.0:{port}")
logger.info("="*60)

# Launch
demo.launch(
    server_name="0.0.0.0",
    server_port=port,
    share=False,
    show_error=True
)
