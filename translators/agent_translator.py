#!/usr/bin/env python3
"""
Agent Translator - Uses OpenAI with custom system prompt for English to Shona translation
"""

import os
import re
import logging
from typing import Optional, List, Dict
from dotenv import load_dotenv
from base_translator import BaseShonaTranslator

# Try to import OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️  OpenAI library not installed. Please install with: pip install openai")

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AgentShonaTranslator(BaseShonaTranslator):
    """English to Shona translator using OpenAI with custom system prompt for exclusions and glossary usage"""
    
    def __init__(self, glossary_dir: str = "../glossary"):
        super().__init__(glossary_dir)
        
        self.client = None
        self.model = "gpt-4o"  # Using GPT-4o for better translation quality
        
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI library not installed. Please install with: pip install openai")
        
        # Initialize OpenAI client
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        try:
            # Initialize OpenAI client with just the API key
            self.client = OpenAI(api_key=api_key)
            logger.info("OpenAI client initialized successfully")
        except Exception as e:
            raise Exception(f"Failed to initialize OpenAI client: {e}")
        
        # Load exclusion list, abbreviations, and medical terms for system prompt
        self.exclusion_terms = self._load_exclusion_terms()
        self.abbreviations = self._load_abbreviations()
        self.medical_terms = self._load_medical_terms()
        
        # Generate system prompt
        self.system_prompt = self._generate_system_prompt()
        
        # Print system prompt for debugging
        print("\n" + "="*80)
        print("AGENT TRANSLATOR SYSTEM PROMPT:")
        print("="*80)
        print(self.system_prompt)
        print("="*80 + "\n")
        
        logger.info("Agent Shona Translator initialized")
    
    def _load_exclusion_terms(self) -> List[str]:
        """Load terms that should be excluded from translation"""
        exclusion_file = os.path.join(self.glossary_manager.glossary_dir, "exclusion_list.csv")
        exclusion_terms = []
        
        try:
            with open(exclusion_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines[1:]:  # Skip header
                    if line.strip():
                        term = line.split(',')[0].strip()
                        exclusion_terms.append(term.lower())
            logger.info(f"Loaded {len(exclusion_terms)} exclusion terms")
        except Exception as e:
            logger.warning(f"Could not load exclusion list: {e}")
        
        return exclusion_terms
    
    def _load_abbreviations(self) -> Dict[str, str]:
        """Load abbreviations and their expansions"""
        abbreviations_file = os.path.join(self.glossary_manager.glossary_dir, "abbreviations.csv")
        abbreviations = {}
        
        try:
            with open(abbreviations_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines[1:]:  # Skip header
                    if line.strip():
                        parts = line.split(',')
                        if len(parts) >= 2:
                            abbrev = parts[0].strip()
                            expansion = parts[1].strip()
                            abbreviations[abbrev.lower()] = expansion
            logger.info(f"Loaded {len(abbreviations)} abbreviations")
        except Exception as e:
            logger.warning(f"Could not load abbreviations: {e}")
        
        return abbreviations
    
    def _load_medical_terms(self) -> Dict[str, str]:
        """Load medical and technical terms"""
        medical_file = os.path.join(self.glossary_manager.glossary_dir, "medical_technical_terms.csv")
        medical_terms = {}
        
        try:
            with open(medical_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines[1:]:  # Skip header
                    if line.strip():
                        parts = line.split(',')
                        if len(parts) >= 2:
                            english = parts[0].strip()
                            shona = parts[1].strip()
                            medical_terms[english.lower()] = shona
            logger.info(f"Loaded {len(medical_terms)} medical/technical terms")
        except Exception as e:
            logger.warning(f"Could not load medical terms: {e}")
        
        return medical_terms
    
    def _generate_system_prompt(self) -> str:
        """Generate the system prompt with exclusions and glossary terms"""
        
        # Build exclusion instructions
        exclusion_text = ""
        if self.exclusion_terms:
            exclusion_text = f"""
EXCLUSION LIST - DO NOT TRANSLATE THESE TERMS (keep them in English):
{', '.join(self.exclusion_terms)}

"""
        
        # Build abbreviation instructions
        abbreviation_text = ""
        if self.abbreviations:
            abbreviation_text = f"""
ABBREVIATIONS - Use these expansions when translating:
"""
            for abbrev, expansion in self.abbreviations.items():
                abbreviation_text += f"- {abbrev.upper()}: {expansion}\n"
            abbreviation_text += "\n"
        
        # Build medical terms instructions
        medical_text = ""
        if self.medical_terms:
            medical_text = f"""
MEDICAL/TECHNICAL TERMS - Use these Shona translations:
"""
            for english, shona in self.medical_terms.items():
                medical_text += f"- {english}: {shona}\n"
            medical_text += "\n"
        
        system_prompt = f"""You are an expert English to Shona translator specializing in medical, technical, and academic documents.

{exclusion_text}
{abbreviation_text}
{medical_text}
Key guidelines for translation:
1. Maintain formal and professional tone appropriate for academic/medical contexts
2. Use standard Shona orthography and grammar
3. For technical terms without direct Shona equivalents, provide the English term in parentheses after the Shona translation
4. Preserve the meaning and context while making it natural in Shona
5. For medical terms, use established Shona medical terminology where available
6. Keep document formatting markers intact (if any)
7. DO NOT translate terms from the exclusion list - keep them in English
8. Use the provided abbreviations and medical/technical terms as specified above
9. IMPORTANT: The agent already has all glossary information in the system prompt, so rely on that instead of partial glossary matches

RESPONSE FORMAT:
- Respond with ONLY the Shona translation
- No explanations, comments, or additional text
- Preserve original formatting and structure
- Keep line breaks and paragraph structure intact"""
        
        return system_prompt
    
    def _translate_with_api(self, text: str) -> Optional[str]:
        """Translate text using OpenAI API with custom system prompt"""
        try:
            # Skip glossary preprocessing - agent has all info in system prompt
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": text}
                ],
                max_completion_tokens=2000,  # GPT-4o uses max_completion_tokens
                timeout=60  # Increased timeout for larger chunks
            )
            
            translated_text = response.choices[0].message.content.strip()
            
            # Validate the translation
            if not translated_text or translated_text == text:
                logger.warning(f"OpenAI returned empty or unchanged text for: {text}")
                return None
            
            logger.info(f"OpenAI translation: '{text[:50]}...' -> '{translated_text[:50]}...'")
            return translated_text
            
        except Exception as e:
            logger.error(f"OpenAI translation error: {e}")
            return None
    
    def get_best_translation(self, text: str) -> str:
        """Override to use agent-specific logic - skip glossary manager, use chunk-based translation"""
        if not text.strip():
            return text
        
        # Skip very short or numeric-only text
        if len(text.strip()) < 2 or re.match(r'^[\d\s\W]+$', text.strip()):
            return text
        
        # 1. Check cache first (smart caching)
        cached_translation = self.cache.get(text)
        if cached_translation:
            logger.info(f"Cache HIT: '{text[:50]}...' -> '{cached_translation[:50]}...'")
            return cached_translation  # No post-processing needed for agent
        
        # 2. Try API translation directly (no glossary manager)
        api_translation = None
        if not self.cache.has_translation(text, self.provider_name):
            api_translation = self._translate_with_api(text)
            
            # Cache the API translation if it's valid
            if api_translation and api_translation.strip() and api_translation != text:
                self.cache.set(text, api_translation, self.provider_name, confidence=0.9)
        
        # 3. Return API translation or original text
        if api_translation and api_translation != text and api_translation.strip():
            logger.info(f"Agent API: '{text[:50]}...' -> '{api_translation[:50]}...'")
            return api_translation
        
        # 4. If no translation found, return original
        logger.warning(f"No translation found for: {text}")
        return text
    
    def translate_large_text(self, text: str, chunk_size: int = 1000) -> str:
        """Translate large text in chunks for better performance"""
        if len(text) <= chunk_size:
            return self.get_best_translation(text)
        
        # Split text into sentences for better chunking
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= chunk_size:
                current_chunk += sentence + " "
            else:
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + " "
        
        # Add the last chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        # Translate each chunk
        translated_chunks = []
        for chunk in chunks:
            translated_chunk = self.get_best_translation(chunk)
            translated_chunks.append(translated_chunk)
        
        # Combine translated chunks
        return " ".join(translated_chunks)
    
    def translate_paragraph(self, paragraph) -> None:
        """Override to use agent-specific translation logic"""
        if not paragraph.text.strip():
            return
        
        # Store original formatting
        runs = list(paragraph.runs)
        original_text = paragraph.text
        
        # Use chunk-based translation for longer paragraphs
        if len(original_text) > 500:
            translated_text = self.translate_large_text(original_text)
        else:
            translated_text = self.get_best_translation(original_text)
        
        # Clear the paragraph
        paragraph.clear()
        
        # Add translated text with preserved formatting
        if runs:
            new_run = paragraph.add_run(translated_text)
            # Copy formatting from the first run
            if runs[0].bold is not None:
                new_run.bold = runs[0].bold
            if runs[0].italic is not None:
                new_run.italic = runs[0].italic
            if runs[0].underline is not None:
                new_run.underline = runs[0].underline
            if runs[0].font.name:
                new_run.font.name = runs[0].font.name
            if runs[0].font.size:
                new_run.font.size = runs[0].font.size
