"""
Knowledge Base Builder - Create vector database from medical texts
FIXED: Using HuggingFace embeddings (FREE) since Groq doesn't provide embeddings
"""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings  # ADDED
import os
from dotenv import load_dotenv

load_dotenv()


# Medical knowledge content
MEDICAL_KNOWLEDGE = [
    {
        "topic": "Common Cold",
        "content": """
Common Cold - Symptoms and Treatment

SYMPTOMS:
- Runny or stuffy nose
- Sore throat
- Cough and sneezing
- Mild headache
- Low-grade fever (sometimes)
- Fatigue

DURATION: Usually 7-10 days

HOME TREATMENT:
- Rest and sleep well
- Drink plenty of fluids (water, tea, soup)
- Use over-the-counter pain relievers
- Gargle with salt water for sore throat
- Use humidifier for congestion

WHEN TO SEE A DOCTOR:
- Symptoms last more than 10 days
- High fever (above 101.3°F/38.5°C)
- Severe headache or sinus pain
- Difficulty breathing
- Symptoms worsen after improvement
"""
    },
    {
        "topic": "Headaches",
        "content": """
Headache Types and Management

TENSION HEADACHES (Most Common):
- Feels like tight band around head
- Mild to moderate pain
- Both sides of head
- Treatment: Rest, hydration, OTC pain relievers

MIGRAINES:
- Throbbing pain, usually one side
- Moderate to severe intensity
- Nausea, light/sound sensitivity
- Treatment: Dark room, medications, avoid triggers

EMERGENCY SIGNS - Call 911:
- Sudden severe headache ("worst ever")
- Headache with fever and stiff neck
- After head injury
- With vision changes or weakness
- New headache after age 50
"""
    },
    {
        "topic": "Healthy Sleep",
        "content": """
Healthy Sleep Habits

RECOMMENDED SLEEP:
- Adults: 7-9 hours per night
- Teenagers: 8-10 hours
- Children: 9-12 hours

GOOD SLEEP HABITS:
- Consistent sleep schedule (same time daily)
- Dark, quiet, cool bedroom
- Avoid screens 1 hour before bed
- No caffeine after 2 PM
- Regular exercise (but not before bed)
- Relaxing bedtime routine

SIGNS OF SLEEP PROBLEMS:
- Difficulty falling asleep
- Waking frequently
- Not feeling rested
- Daytime sleepiness
- Snoring or breathing pauses

If sleep problems persist, consult a doctor.
"""
    },
    {
        "topic": "Hydration",
        "content": """
Staying Hydrated

DAILY WATER NEEDS:
- Men: About 15.5 cups (3.7 liters)
- Women: About 11.5 cups (2.7 liters)
- Adjust for activity level and climate

SIGNS OF DEHYDRATION:
- Thirst
- Dry mouth
- Dark urine
- Fatigue
- Dizziness
- Headache

HYDRATION TIPS:
- Drink water throughout the day
- Have water with every meal
- Eat water-rich foods (fruits, vegetables)
- Drink before, during, after exercise
- Limit alcohol and caffeine

SEVERE DEHYDRATION (Emergency):
- Extreme thirst
- No urination
- Rapid heartbeat
- Confusion
- Seek immediate medical care
"""
    },
    {
        "topic": "Exercise Benefits",
        "content": """
Physical Activity and Health

RECOMMENDED EXERCISE:
- 150 minutes moderate activity per week
- OR 75 minutes vigorous activity
- Plus strength training 2x/week

HEALTH BENEFITS:
- Reduces risk of heart disease, diabetes
- Helps maintain healthy weight
- Improves mental health and mood
- Strengthens bones and muscles
- Increases energy levels
- Better sleep quality

GETTING STARTED:
- Start slow and gradually increase
- Choose activities you enjoy
- Walk 10 minutes, increase over time
- Take stairs instead of elevator
- Park farther away
- Exercise with friends

BEFORE STARTING NEW EXERCISE:
- Consult doctor if over 50 or health conditions
- Start gradually
- Listen to your body
- Stop if you feel pain

EMERGENCY SIGNS DURING EXERCISE:
- Chest pain or pressure
- Severe shortness of breath
- Dizziness or fainting
- Stop immediately and seek help
"""
    }
]


def create_knowledge_base(persist_directory="./medical_knowledge_db"):
    """Create vector database from medical knowledge"""
    
    print("Creating medical knowledge base...")
    
    # Convert to documents
    documents = [
        Document(
            page_content=item["content"],
            metadata={"topic": item["topic"]}
        )
        for item in MEDICAL_KNOWLEDGE
    ]
    
    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    
    splits = text_splitter.split_documents(documents)
    print(f"Created {len(splits)} document chunks")
    
    # Create embeddings - FIXED: Using HuggingFace (FREE)
    print("Loading embedding model (first time may take a moment)...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    # Create vector store
    print("Building vector database...")
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    
    print(f"✅ Knowledge base created at: {persist_directory}")
    return vectorstore


def load_knowledge_base(persist_directory="./medical_knowledge_db"):
    """Load existing knowledge base"""

    # FIXED: Using HuggingFace embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )
    
    return vectorstore


if __name__ == "__main__":
    # Create the knowledge base
    create_knowledge_base()
    
    # Test retrieval
    print("\nTesting knowledge retrieval...")
    vectorstore = load_knowledge_base()
    
    test_query = "What are symptoms of a cold?"
    docs = vectorstore.similarity_search(test_query, k=2)
    
    print(f"\nQuery: {test_query}")
    print(f"Found {len(docs)} relevant documents:")
    for i, doc in enumerate(docs, 1):
        print(f"\n{i}. Topic: {doc.metadata['topic']}")
        print(f"Content preview: {doc.page_content[:200]}...")