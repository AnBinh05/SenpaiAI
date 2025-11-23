#!/usr/bin/env python3
"""
Script to check available Ollama models and install if needed.
"""
import ollama
import sys

def check_ollama_connection():
    """Check if Ollama is running."""
    try:
        ollama.list()
        return True
    except Exception as e:
        print(f"❌ Ollama is not running or not accessible: {e}")
        print("\n💡 To start Ollama:")
        print("   1. Open a new terminal")
        print("   2. Run: ollama serve")
        print("   3. Or install Ollama from: https://ollama.ai/download")
        return False

def list_available_models():
    """List all available Ollama models."""
    try:
        response = ollama.list()
        if 'models' in response and response['models']:
            models = [model['name'] for model in response['models']]
            print(f"\n✅ Found {len(models)} model(s):")
            for model in models:
                print(f"   - {model}")
            return models
        else:
            print("\n⚠️  No models found. You need to install a model first.")
            return []
    except Exception as e:
        print(f"❌ Error listing models: {e}")
        return []

def install_model(model_name: str):
    """Install an Ollama model."""
    print(f"\n📥 Installing model: {model_name}")
    print("   This may take a few minutes depending on your internet connection...")
    try:
        ollama.pull(model_name)
        print(f"✅ Successfully installed: {model_name}")
        return True
    except Exception as e:
        print(f"❌ Error installing {model_name}: {e}")
        return False

def main():
    print("🔍 Checking Ollama connection...")
    
    if not check_ollama_connection():
        sys.exit(1)
    
    print("✅ Ollama is running!")
    
    available_models = list_available_models()
    
    # Check for recommended models
    recommended_models = [
        "gemma:2b",      # Small, fast
        "llama2:7b",     # Medium, good quality
        "mistral:7b",    # Medium, good quality
        "nomic-embed-text"  # For embeddings
    ]
    
    print("\n📋 Recommended models for SenpaiAI:")
    for model in recommended_models:
        if model in available_models:
            print(f"   ✅ {model} (installed)")
        else:
            print(f"   ❌ {model} (not installed)")
    
    # Check if default model is available
    default_model = "gemma:2b"
    if default_model not in available_models:
        print(f"\n⚠️  Default model '{default_model}' is not installed.")
        response = input(f"Would you like to install '{default_model}' now? (y/n): ")
        if response.lower() == 'y':
            install_model(default_model)
        else:
            print("\n💡 To install manually, run:")
            print(f"   ollama pull {default_model}")
            print("\n💡 Or update OLLAMA_MODEL in backend/.env to use an installed model.")
    
    # Check for embedding model
    embedding_model = "nomic-embed-text"
    if embedding_model not in available_models:
        print(f"\n⚠️  Embedding model '{embedding_model}' is not installed (needed for RAG).")
        response = input(f"Would you like to install '{embedding_model}' now? (y/n): ")
        if response.lower() == 'y':
            install_model(embedding_model)

if __name__ == "__main__":
    main()


