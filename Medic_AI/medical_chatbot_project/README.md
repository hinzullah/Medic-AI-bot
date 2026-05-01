# 🏥 Medical AI Chatbot with LangChain

A production-ready medical information chatbot using LangChain, RAG (Retrieval-Augmented Generation), and OpenAI.

## ⚠️ Important Disclaimer

**This is for educational purposes only. NOT for diagnosing or treating medical conditions. Always consult qualified healthcare professionals for medical advice.**

---

## 🎯 Features

- ✅ **RAG-Powered**: Uses vector database for accurate medical information
- ✅ **Safety Layer**: Emergency detection, high-risk warnings, automatic disclaimers
- ✅ **Conversation Memory**: Remembers context within session
- ✅ **Beautiful UI**: Gradio web interface
- ✅ **Fallback System**: Works with or without knowledge base
- ✅ **Production-Ready**: Error handling, logging, safety checks

---

## 📁 Project Structure

```
medical-chatbot/
├── .env                        # API keys (create from .env.example)
├── requirements.txt            # Dependencies
├── README.md                   # This file
├── app.py                      # Main Gradio app (RUN THIS!)
│
├── src/
│   ├── simple_chatbot.py      # Basic prompt-based chatbot
│   ├── rag_chatbot.py         # RAG chatbot with knowledge base
│   ├── safety_layer.py        # Emergency detection & warnings
│   └── knowledge_base.py      # Create vector database
│
└── medical_knowledge_db/       # Vector database (auto-created)
```

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies

```bash
# Install packages
pip install -r requirements.txt
```

### Step 2: Set Up API Key

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your OpenAI API key
# Get key from: https://platform.openai.com/api-keys
```

Your `.env` file should look like:
```
OPENAI_API_KEY=sk-proj-...your-actual-key...
```

### Step 3: Create Knowledge Base (Optional but Recommended)

```bash
# Create the medical knowledge vector database
python src/knowledge_base.py
```

You should see:
```
Creating medical knowledge base...
Created 15 document chunks
✅ Knowledge base created at: ./medical_knowledge_db
```

### Step 4: Run the App!

```bash
# Start the web interface
python app.py
```

Open your browser to: **http://localhost:7860**

---

## 📖 Usage Examples

### Web Interface (Recommended)

1. Run `python app.py`
2. Open http://localhost:7860
3. Start chatting!

Example queries:
- "What are symptoms of a cold?"
- "How can I sleep better?"
- "What should I do for a headache?"
- "How much water should I drink?"

### Command Line Interface

**Simple Chatbot:**
```bash
python src/simple_chatbot.py
```

**RAG Chatbot (with knowledge base):**
```bash
python src/rag_chatbot.py
```

---

## 🔧 Configuration

### Using Different LLMs

Edit the chatbot files to use different models:

```python
# In simple_chatbot.py or rag_chatbot.py

# OpenAI GPT-4 (default)
llm = ChatOpenAI(model="gpt-4", temperature=0.3)

# OpenAI GPT-3.5 (cheaper)
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

# Anthropic Claude
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=0.3)
```

### Temperature Settings

- **0.2-0.3**: More factual, consistent (recommended for medical)
- **0.5-0.7**: Balanced
- **0.8-1.0**: More creative (NOT recommended for medical use)

---

## 🛡️ Safety Features

### Emergency Detection

Automatically detects emergency keywords:
- "chest pain"
- "difficulty breathing"  
- "severe bleeding"
- "heart attack"
- "suicide"

Response: **Immediate advice to call 911**

### High-Risk Warnings

Flags situations needing doctor consultation:
- Pregnancy-related
- Infant/baby concerns
- Severe pain
- High fever

### Medical Disclaimers

Every response includes:
- Statement that it's an AI
- Recommendation to consult professionals
- Emergency contact information

---

## 📚 Extending the Knowledge Base

Add your own medical information:

```python
# Edit src/knowledge_base.py

MEDICAL_KNOWLEDGE = [
    {
        "topic": "Your Topic",
        "content": """
        Your medical information here...
        """
    },
    # Add more topics...
]
```

Then recreate the database:
```bash
python src/knowledge_base.py
```

### Adding Documents (PDFs, Text Files)

```python
# In knowledge_base.py

from langchain.document_loaders import PyPDFLoader, TextLoader

# Load PDF
loader = PyPDFLoader("medical_guide.pdf")
documents = loader.load()

# Load text file
loader = TextLoader("symptoms.txt")
documents = loader.load()
```

---

## 🐛 Troubleshooting

### "No module named 'langchain'"
```bash
pip install -r requirements.txt
```

### "API key not found"
Make sure `.env` file exists and contains:
```
OPENAI_API_KEY=your_actual_key_here
```

### "Knowledge base not found"
Run this first:
```bash
python src/knowledge_base.py
```

### Port 7860 already in use
Change port in `app.py`:
```python
demo.launch(server_port=8000)  # Use different port
```

---

## 💰 Cost Estimates

Using OpenAI GPT-4:
- **Simple queries**: ~$0.01 per conversation
- **With RAG**: ~$0.02 per conversation (includes embedding costs)

Using GPT-3.5-Turbo:
- ~75% cheaper than GPT-4

Typical monthly costs for moderate use: **$5-20**

---

## 🔐 Security & Privacy

**IMPORTANT:**
- ✅ Never store real patient data
- ✅ Don't log sensitive health information
- ✅ Use HTTPS in production
- ✅ Comply with HIPAA (if handling real medical data)
- ✅ Add user authentication for production
- ✅ Rate limiting to prevent abuse

---

## 🚢 Deployment Options

### Local Development
```bash
python app.py
```

### Public Access (Temporary)
```python
# In app.py
demo.launch(share=True)  # Creates temporary public URL
```

### Cloud Deployment

**Hugging Face Spaces:**
1. Create account on huggingface.co
2. Create new Space (Gradio)
3. Upload files
4. Add OPENAI_API_KEY in settings

**AWS/GCP/Azure:**
1. Deploy as Docker container
2. Set environment variables
3. Configure firewall/load balancer

---

## 📝 Legal & Ethical Considerations

1. **Not for Medical Diagnosis**: Always include disclaimers
2. **Emergency Situations**: Direct to emergency services
3. **Data Privacy**: Don't store personal health information
4. **Regulatory Compliance**: Check local regulations
5. **Professional Review**: Have medical professionals review content
6. **Regular Updates**: Keep medical knowledge current

---

## 🎓 Learning Resources

- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Guide](https://platform.openai.com/docs)
- [Gradio Documentation](https://gradio.app/docs)
- [RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering/)

---

## 📧 Support

For issues or questions:
1. Check the troubleshooting section
2. Review example code
3. Test with simple queries first

---

## 📄 License

Educational use only. Not for commercial medical applications without proper licensing and medical oversight.

---

**Remember: This chatbot provides information, not medical advice. Always consult healthcare professionals for medical concerns!** 🏥
