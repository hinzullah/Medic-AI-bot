"""
RAG Medical Chatbot - Uses vector database for knowledge retrieval
FIXED: Works with Groq (chat) + HuggingFace embeddings (FREE)
"""

from langchain_groq import ChatGroq  # For Groq LLM
from langchain_community.embeddings import HuggingFaceEmbeddings  # FREE embeddings
from langchain_community.vectorstores import Chroma
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()


class RAGMedicalChatbot:
    def __init__(self, knowledge_db_path="./medical_knowledge_db"):
        """Initialize RAG chatbot with knowledge base"""
        
        print("Initializing RAG Medical Chatbot...")
        
        # Load FREE HuggingFace embeddings (same as knowledge base)
        print("Loading embedding model...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Load vector database
        print("Loading knowledge base...")
        self.vectorstore = Chroma(
            persist_directory=knowledge_db_path,
            embedding_function=self.embeddings
        )
        
        # Create retriever
        self.retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": 3}  # Top 3 relevant docs
        )
        
        # Initialize Groq LLM
        self.llm = ChatGroq(
    model="llama-3.3-70b-versatile",  # Try this first
    # OR model="llama-3.1-8b-instant",  # If above doesn't work
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3
)
        
        # Set up memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        # Custom prompt for medical context
        qa_prompt = PromptTemplate(
            template="""You are Dr. AI, a knowledgeable and empathetic medical assistant.

Use the medical knowledge below to answer questions accurately.

CRITICAL SAFETY RULES:
1. Always state you're an AI, not a doctor
2. For emergencies, immediately advise calling emergency services
3. Never diagnose - only provide general information
4. Always recommend professional consultation for personalized advice

Medical Knowledge:
{context}

Conversation History:
{chat_history}

Question: {question}

Helpful Answer:""",
            input_variables=["context", "chat_history", "question"]
        )
        
        # Create the conversational chain
        print("Building conversation chain...")
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            memory=self.memory,
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": qa_prompt}
        )
        
        print("✅ RAG Chatbot ready!")
    
    def chat(self, message: str) -> str:
        """Get response with knowledge retrieval"""
        try:
            result = self.qa_chain.invoke({"question": message})
            return result["answer"]
            
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}. Please try rephrasing your question."
    
    def get_sources(self, message: str) -> list:
        """Get source documents for a query"""
        result = self.qa_chain({"question": message})
        sources = [doc.metadata.get("topic", "Unknown") 
                  for doc in result["source_documents"]]
        return list(set(sources))
    
    def reset(self):
        """Clear conversation memory"""
        self.memory.clear()


def main():
    """CLI interface for RAG chatbot"""
    print("=" * 60)
    print("🏥 RAG Medical Chatbot (Groq + HuggingFace)")
    print("=" * 60)
    
    try:
        bot = RAGMedicalChatbot()
    except Exception as e:
        print(f"❌ Error loading chatbot: {e}")
        print("\nMake sure:")
        print("1. You created the knowledge base: python src/knowledge_base.py")
        print("2. You have GROQ_API_KEY in .env file")
        print("3. Packages installed: pip install sentence-transformers langchain-groq")
        return
    
    print("\nType 'quit' to exit\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit']:
            print("\nGoodbye! 👋")
            break
        
        if not user_input:
            continue
        
        # Show relevant topics
        try:
            sources = bot.get_sources(user_input)
            if sources:
                print(f"\n📚 Relevant topics: {', '.join(sources)}")
        except:
            pass
        
        # Get response
        response = bot.chat(user_input)
        print(f"\nDr. AI: {response}\n")


if __name__ == "__main__":
    main()