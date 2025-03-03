import os
import glob
import markdown
import json
import ollama
from bs4 import BeautifulSoup
from typing import List, Dict

class ObsidianKnowledgeBase:
    def __init__(self, base_path: str):
        self.base_path = base_path
        self.markdown_files = []
        self.processed_content = []
        
    def get_all_markdown_files(self) -> List[str]:
        """Recursively get all markdown files from the knowledge base"""
        markdown_files = []
        for root, dirs, files in os.walk(self.base_path):
            for file in files:
                if file.endswith(('.md', '.markdown')):
                    markdown_files.append(os.path.join(root, file))
        return markdown_files
    
    def process_markdown_file(self, file_path: str) -> Dict:
        """Process a single markdown file and extract relevant information"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Convert markdown to HTML for easier processing
        html = markdown.markdown(content)
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract text content
        text = soup.get_text()
        
        # Get relative path for context
        rel_path = os.path.relpath(file_path, self.base_path)
        
        return {
            'path': rel_path,
            'content': text,
            'tags': self._extract_tags(content)
        }
    
    def _extract_tags(self, content: str) -> List[str]:
        """Extract Obsidian tags from content"""
        tags = []
        for line in content.split('\n'):
            if line.startswith('#'):
                tags.extend([tag.strip() for tag in line.split('#')[1:]])
        return tags
    
    def process_all_files(self):
        """Process all markdown files in the knowledge base"""
        self.markdown_files = self.get_all_markdown_files()
        for file_path in self.markdown_files:
            processed = self.process_markdown_file(file_path)
            self.processed_content.append(processed)
            
    def generate_training_data(self) -> List[Dict]:
        """Generate training data in a format suitable for Ollama"""
        training_data = []
        
        for content in self.processed_content:
            # Create context from file path
            context = f"From: {content['path']}\n"
            if content['tags']:
                context += f"Tags: {', '.join(content['tags'])}\n"
                
            # Split content into chunks for training
            chunks = self._chunk_content(content['content'])
            
            for chunk in chunks:
                training_data.append({
                    'prompt': f"{context}\nPlease explain or discuss this content:\n{chunk}",
                    'response': chunk
                })
                
        return training_data

    def _chunk_content(self, content: str, chunk_size: int = 512) -> List[str]:
        """Split content into manageable chunks"""
        words = content.split()
        chunks = []
        current_chunk = []
        
        for word in words:
            current_chunk.append(word)
            if len(' '.join(current_chunk)) >= chunk_size:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
            
        return chunks

class PersonalizedOllamaBot:
    def __init__(self, model_name: str = "llama2"):
        self.model_name = model_name
        
    def train(self, training_data: List[Dict]):
        """Train the Ollama model with the provided data"""
        try:
            # Create a new Ollama model based on the base model
            modelfile = self._generate_modelfile(training_data)
            ollama.create(name=f"personal-{self.model_name}", modelfile=modelfile)
            
            # Train the model with the data
            for item in training_data:
                ollama.train(
                    model=f"personal-{self.model_name}",
                    prompt=item['prompt'],
                    response=item['response']
                )
                
        except Exception as e:
            print(f"Error during training: {str(e)}")
    
    def _generate_modelfile(self, training_data: List[Dict]) -> str:
        """Generate Modelfile content for Ollama"""
        return f"""
FROM {self.model_name}
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER num_ctx 4096

# System prompt to maintain personality
SYSTEM """You are an AI assistant trained on my personal knowledge base. 
Respond in a way that reflects my writing style and knowledge structure.
Always provide context about where the information comes from in my notes when relevant."""
"""
    
    def chat(self, message: str) -> str:
        """Generate a response using the trained model"""
        try:
            response = ollama.chat(
                model=f"personal-{self.model_name}", 
                messages=[{'role': 'user', 'content': message}]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error generating response: {str(e)}"

def main():
    # Initialize knowledge base processor
    kb = ObsidianKnowledgeBase("~/D/Second Brain")
    print("Processing Obsidian knowledge base...")
    kb.process_all_files()
    
    # Generate training data
    training_data = kb.generate_training_data()
    print(f"Generated {len(training_data)} training examples")
    
    # Initialize and train the bot
    bot = PersonalizedOllamaBot()
    print("Training bot...")
    bot.train(training_data)
    
    # Interactive chat loop
    print("\nChat with your personalized bot (type 'quit' to exit)")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == 'quit':
            break
        
        response = bot.chat(user_input)
        print("Bot:", response)

if __name__ == "__main__":
    main()