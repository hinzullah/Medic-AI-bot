"""
Simple Medical Chatbot - No RAG, just prompt-based
"""

from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()


class SimpleMedicalChatbot:
    def __init__(self, model="gpt-4", temperature=0.3):
        """Initialize simple chatbot"""
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self.memory = ConversationBufferMemory(return_messages=True)
        
        # Medical prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are Dr. AI, a helpful medical assistant.

Your role:
- Provide general health information
- Explain common symptoms
- Offer wellness advice
- Be empathetic and supportive

CRITICAL SAFETY:
1. You're an AI, not a replacement for doctors
2. For emergencies (chest pain, difficulty breathing), advise calling 911
3. Never diagnose - only provide information
4. Always recommend consulting healthcare professionals

Response style:
- Clear and simple language
- Warm and professional tone
- Include when to seek help

Conversation history:
{history}

User: {input}
Dr. AI:"""),
        ])
        
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory
        )
        self.conversation.prompt = self.prompt
    
    def chat(self, message: str) -> str:
        """Get response to message"""
        try:
            response = self.conversation.predict(input=message)
            return response
        except Exception as e:
            return f"Error: {str(e)}"
    
    def reset(self):
        """Clear conversation memory"""
        self.memory.clear()


def main():
    """CLI interface"""
    print("=" * 60)
    print("🏥 Simple Medical Chatbot")
    print("=" * 60)
    print("Type 'quit' to exit\n")
    
    bot = SimpleMedicalChatbot()
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit']:
            print("\nGoodbye! Stay healthy! 👋")
            break
        
        if not user_input:
            continue
        
        response = bot.chat(user_input)
        print(f"\nDr. AI: {response}\n")


if __name__ == "__main__":
    main()
