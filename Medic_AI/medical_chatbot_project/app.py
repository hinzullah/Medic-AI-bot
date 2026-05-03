"""
Medical Chatbot App - Clean Version
"""

import os
import logging
import threading
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

bot = None
bot_lock = threading.Lock()
bot_error = None


def get_bot():
    """Load the chatbot on first use so Railway can bind to PORT quickly."""
    global bot, bot_error

    if bot:
        return bot

    with bot_lock:
        if bot:
            return bot

        logger.info("Loading chatbot...")
        try:
            from src.rag_chatbot import RAGMedicalChatbot
            logger.info("Initializing RAG Chatbot...")
            base_bot = RAGMedicalChatbot(knowledge_db_path=KNOWLEDGE_DB_PATH)
            bot = SafeChatbotWrapper(base_bot)
            bot_error = None
            logger.info("✅ RAG Chatbot loaded")
            return bot
        except Exception as e:
            logger.error(f"RAG Chatbot failed: {e}")

        try:
            from src.simple_chatbot import SimpleMedicalChatbot
            logger.info("Initializing Simple Chatbot...")
            base_bot = SimpleMedicalChatbot()
            bot = SafeChatbotWrapper(base_bot)
            bot_error = None
            logger.info("✅ Simple Chatbot loaded")
            return bot
        except Exception as e2:
            bot_error = str(e2)
            logger.error(f"Simple Chatbot failed: {e2}")
            return None

# Define response function
def respond(message, history):
    """Generate response"""
    try:
        chatbot = get_bot()
        if chatbot:
            return chatbot.chat(message)
        return f"Chatbot not initialized. Check Railway variables and logs. Last error: {bot_error}"
    except Exception as e:
        logger.error(f"Error: {e}")
        return f"Error: {str(e)}"


CSS = """
:root {
    --brand: #0f8f7f;
    --brand-dark: #0b615b;
    --ink: #17212b;
    --muted: #5f6f7a;
    --surface: #ffffff;
    --soft: #eef8f6;
    --warning: #fff4df;
    --warning-border: #f1c36d;
}

.gradio-container {
    background:
        radial-gradient(circle at 15% 0%, rgba(15, 143, 127, 0.12), transparent 30%),
        linear-gradient(180deg, #f7fbfa 0%, #edf5f3 100%);
    color: var(--ink);
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

#app-shell {
    max-width: 1060px;
    margin: 0 auto;
    padding: 28px 18px 18px;
}

#hero {
    padding: 24px 0 18px;
}

#hero h1 {
    margin: 0;
    color: var(--ink);
    font-size: clamp(2rem, 4vw, 3.5rem);
    line-height: 1;
    letter-spacing: 0;
}

#hero p {
    margin: 12px 0 0;
    max-width: 680px;
    color: var(--muted);
    font-size: 1.05rem;
    line-height: 1.55;
}

#status-row {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 18px;
}

.status-pill {
    border: 1px solid rgba(15, 143, 127, 0.18);
    background: rgba(255, 255, 255, 0.72);
    color: var(--brand-dark);
    border-radius: 999px;
    padding: 8px 12px;
    font-size: 0.88rem;
    font-weight: 650;
}

#safety-note {
    border: 1px solid var(--warning-border);
    background: var(--warning);
    border-radius: 8px;
    padding: 14px 16px;
    margin: 8px 0 18px;
    color: #5c4217;
    line-height: 1.45;
}

#safety-note strong {
    color: #3d2a0d;
}

#prompt-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 10px;
    margin: 0 0 18px;
}

.prompt-card {
    border: 1px solid rgba(15, 143, 127, 0.16);
    background: rgba(255, 255, 255, 0.78);
    border-radius: 8px;
    color: var(--brand-dark);
    font-size: 0.92rem;
    font-weight: 650;
    line-height: 1.35;
    padding: 12px 14px;
}

#chat-panel {
    border: 1px solid rgba(23, 33, 43, 0.08);
    border-radius: 8px;
    background: var(--surface);
    box-shadow: 0 18px 40px rgba(18, 45, 43, 0.10);
    overflow: hidden;
}

#chat-panel .wrap,
#chat-panel .contain {
    border-radius: 0;
}

#chatbot {
    min-height: 480px;
}

#chatbot .message {
    border-radius: 8px;
}

textarea {
    border-radius: 8px !important;
}

button.primary {
    background: var(--brand) !important;
    border-color: var(--brand) !important;
}

button.primary:hover {
    background: var(--brand-dark) !important;
    border-color: var(--brand-dark) !important;
}

#footer {
    margin-top: 16px;
    color: var(--muted);
    font-size: 0.9rem;
    text-align: center;
}

footer {
    display: none !important;
}

@media (max-width: 760px) {
    #prompt-grid {
        grid-template-columns: 1fr;
    }
}
"""

# Create interface
logger.info("Creating Gradio interface...")
theme = gr.themes.Soft(
    primary_hue="teal",
    secondary_hue="cyan",
    neutral_hue="slate",
    radius_size="sm",
    text_size="md",
).set(
    body_background_fill="#f7fbfa",
    block_background_fill="#ffffff",
    button_primary_background_fill="#0f8f7f",
    button_primary_background_fill_hover="#0b615b",
)

with gr.Blocks(title="Dr. AI Medical Assistant") as demo:
    with gr.Column(elem_id="app-shell"):
        gr.HTML(
            """
            <section id="hero">
                <h1>Dr. AI</h1>
                <p>Your focused medical information assistant for everyday health questions, symptom education, and safer next steps.</p>
                <div id="status-row">
                    <span class="status-pill">RAG knowledge base</span>
                    <span class="status-pill">Groq powered responses</span>
                    <span class="status-pill">Emergency-aware safety layer</span>
                </div>
            </section>
            <div id="safety-note">
                <strong>Important:</strong> This app provides general health information only. It is not a doctor, diagnosis, or treatment plan. For urgent symptoms or emergencies, contact local emergency services immediately.
            </div>
            <div id="prompt-grid">
                <div class="prompt-card">What are the symptoms of a common cold?</div>
                <div class="prompt-card">How can I improve my sleep quality?</div>
                <div class="prompt-card">What should I do for a headache?</div>
                <div class="prompt-card">How much water should I drink daily?</div>
                <div class="prompt-card">What are the benefits of regular exercise?</div>
                <div class="prompt-card">How do I know if I'm dehydrated?</div>
            </div>
            """
        )

        with gr.Column(elem_id="chat-panel"):
            chatbot = gr.ChatInterface(
                fn=respond,
                chatbot=gr.Chatbot(
                    label="Conversation",
                    height=520,
                    elem_id="chatbot",
                    avatar_images=(None, None),
                ),
                textbox=gr.Textbox(
                    placeholder="Ask about symptoms, wellness, sleep, hydration, headaches...",
                    label="Your question",
                    container=False,
                    scale=7
                ),
                title=None,
                description=None,
            )

        gr.HTML(
            """
            <div id="footer">
                Educational use only. Always consult a qualified healthcare professional for personal medical concerns.
            </div>
            """
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
    show_error=True,
    theme=theme,
    css=CSS
)
