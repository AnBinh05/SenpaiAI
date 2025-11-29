#!/usr/bin/env python3
"""
Script to populate the database and vector store with sample Japanese learning data.
Run this script after setting up the database to initialize with sample data.
"""

import asyncio
import sys
import os
from sqlalchemy.orm import Session

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.core.database import SessionLocal, engine, Base
from app.models.database import Document, GrammarRule, Vocabulary
from app.services.vector_db import chroma_service
from app.utils.sample_corpus import ALL_DOCUMENTS

def create_sample_grammar_rules():
    """Create sample grammar rules."""
    return [
        GrammarRule(
            rule_name="Particle は (wa)",
            japanese_pattern="は",
            meaning="Topic marker particle",
            usage_notes="Marks the topic of the sentence. Pronounced 'wa' not 'ha'.",
            examples=[
                {"japanese": "わたしは学生です", "english": "I am a student"},
                {"japanese": "これは本です", "english": "This is a book"}
            ],
            jlpt_level="N5",
            difficulty_score=2.0
        ),
        GrammarRule(
            rule_name="Particle を (wo/o)",
            japanese_pattern="を",
            meaning="Direct object marker",
            usage_notes="Marks the direct object of a verb. Pronounced 'o' not 'wo'.",
            examples=[
                {"japanese": "本を読みます", "english": "I read a book"},
                {"japanese": "コーヒーを飲みます", "english": "I drink coffee"}
            ],
            jlpt_level="N5",
            difficulty_score=2.0
        ),
        GrammarRule(
            rule_name="Te-form",
            japanese_pattern="て/で",
            meaning="Connecting form of verbs",
            usage_notes="Used to connect verbs and express various meanings like progressive tense, requests, etc.",
            examples=[
                {"japanese": "本を読んでいます", "english": "I am reading a book"},
                {"japanese": "手を洗ってください", "english": "Please wash your hands"}
            ],
            jlpt_level="N4",
            difficulty_score=4.0
        )
    ]

def create_sample_vocabulary():
    """Create sample vocabulary entries."""
    return [
        Vocabulary(
            japanese_word="学生",
            reading="がくせい",
            meaning="student",
            part_of_speech="noun",
            jlpt_level="N5",
            example_sentences=[
                {"japanese": "私は学生です", "english": "I am a student"},
                {"japanese": "学生の時は忙しかった", "english": "I was busy when I was a student"}
            ]
        ),
        Vocabulary(
            japanese_word="本",
            reading="ほん",
            meaning="book",
            part_of_speech="noun",
            jlpt_level="N5",
            example_sentences=[
                {"japanese": "この本は面白いです", "english": "This book is interesting"},
                {"japanese": "本を読むのが好きです", "english": "I like reading books"}
            ]
        ),
        Vocabulary(
            japanese_word="読む",
            reading="よむ",
            meaning="to read",
            part_of_speech="verb",
            jlpt_level="N5",
            example_sentences=[
                {"japanese": "毎日新聞を読みます", "english": "I read the newspaper every day"},
                {"japanese": "この本を読んでください", "english": "Please read this book"}
            ]
        )
    ]

async def populate_database():
    """Populate the database with sample data."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Clear existing documents to avoid duplicates
        print("Clearing existing documents...")
        db.query(Document).delete()
        db.commit()
        
        print("Adding documents to database...")
        
        # Add documents
        for doc_data in ALL_DOCUMENTS:
            document = Document(
                title=doc_data["title"],
                content=doc_data["content"],
                document_type=doc_data["document_type"],
                jlpt_level=doc_data["jlpt_level"],
                tags=doc_data["tags"],
                source_url=doc_data["source_url"]
            )
            db.add(document)
        
        # Add grammar rules
        print("Adding grammar rules...")
        grammar_rules = create_sample_grammar_rules()
        for rule in grammar_rules:
            db.add(rule)
        
        # Add vocabulary
        print("Adding vocabulary...")
        vocabulary = create_sample_vocabulary()
        for vocab in vocabulary:
            db.add(vocab)
        
        db.commit()
        print("Database populated successfully!")
        
    except Exception as e:
        print(f"Error populating database: {e}")
        db.rollback()
    finally:
        db.close()

async def populate_vector_store():
    """Populate the vector store with embeddings."""
    print("Clearing existing vector store...")
    try:
        # Clear existing collection
        chroma_service.client.delete_collection(name=chroma_service.collection_name)
        # Recreate collection
        chroma_service.collection = chroma_service.client.get_or_create_collection(
            name=chroma_service.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        print("Vector store cleared successfully.")
    except Exception as e:
        print(f"Note: Could not clear vector store (may not exist yet): {e}")
    
    print("Adding documents to vector store...")
    
    try:
        # Get documents from database
        db = SessionLocal()
        documents = db.query(Document).all()
        db.close()
        
        # Convert to format expected by ChromaDB
        doc_data = []
        for doc in documents:
            doc_data.append({
                "id": str(doc.id),
                "title": doc.title,
                "content": doc.content,
                "document_type": doc.document_type,
                "jlpt_level": doc.jlpt_level,
                "tags": doc.tags,
                "source_url": doc.source_url
            })
        
        # Add to ChromaDB
        doc_ids = chroma_service.add_documents(doc_data)
        print(f"Added {len(doc_ids)} document chunks to vector store")
        
        # Print stats
        stats = chroma_service.get_collection_stats()
        print(f"Vector store stats: {stats}")
        
    except Exception as e:
        print(f"Error populating vector store: {e}")

async def main():
    """Main function to populate both database and vector store."""
    print("Starting SenpaiAI data population...")
    
    await populate_database()
    await populate_vector_store()
    
    print("Data population completed successfully!")
    print("\nYou can now start the SenpaiAI application.")

if __name__ == "__main__":
    asyncio.run(main())


