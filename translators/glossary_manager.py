#!/usr/bin/env python3
"""
Glossary Manager - Shared component for deterministic terms and abbreviations
"""

import os
import re
import csv
import logging
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

class GlossaryManager:
    """Manages deterministic translations and abbreviations from CSV files"""
    
    def __init__(self, glossary_dir: str = "../glossary"):
        self.glossary_dir = glossary_dir
        self.medical_technical_glossary: Dict[str, str] = {}
        self.phrase_translations: Dict[str, str] = {}
        self.abbreviations: Dict[str, str] = {}
        self.post_processing_corrections: Dict[str, str] = {}
        self.exclusion_list: set = set()
        
        # Load all glossary data
        self._load_glossary_data()
        
        logger.info(f"GlossaryManager initialized with {len(self.medical_technical_glossary)} terms, "
                   f"{len(self.phrase_translations)} phrases, {len(self.abbreviations)} abbreviations, "
                   f"{len(self.exclusion_list)} exclusions")
    
    def _load_glossary_data(self):
        """Load all glossary data from CSV files"""
        # Create glossary directory if it doesn't exist
        os.makedirs(self.glossary_dir, exist_ok=True)
        
        # Load different types of glossary data
        self._load_medical_technical_glossary()
        self._load_phrase_translations()
        self._load_abbreviations()
        self._load_post_processing_corrections()
        self._load_exclusion_list()
    
    def _load_medical_technical_glossary(self):
        """Load medical/technical terms from CSV"""
        csv_file = os.path.join(self.glossary_dir, "medical_technical_terms.csv")
        
        if not os.path.exists(csv_file):
            # Create default file with common terms
            self._create_default_medical_technical_csv(csv_file)
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    english = row.get('english', '').strip().lower()
                    shona = row.get('shona', '').strip()
                    if english and shona:
                        self.medical_technical_glossary[english] = shona
            logger.info(f"Loaded {len(self.medical_technical_glossary)} medical/technical terms")
        except Exception as e:
            logger.error(f"Error loading medical/technical glossary: {e}")
    
    def _load_phrase_translations(self):
        """Load phrase translations from CSV"""
        csv_file = os.path.join(self.glossary_dir, "phrase_translations.csv")
        
        if not os.path.exists(csv_file):
            # Create default file with common phrases
            self._create_default_phrase_csv(csv_file)
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    english = row.get('english', '').strip().lower()
                    shona = row.get('shona', '').strip()
                    if english and shona:
                        self.phrase_translations[english] = shona
            logger.info(f"Loaded {len(self.phrase_translations)} phrase translations")
        except Exception as e:
            logger.error(f"Error loading phrase translations: {e}")
    
    def _load_abbreviations(self):
        """Load abbreviations from CSV"""
        csv_file = os.path.join(self.glossary_dir, "abbreviations.csv")
        
        if not os.path.exists(csv_file):
            # Create default file with common abbreviations
            self._create_default_abbreviations_csv(csv_file)
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    abbrev = row.get('abbreviation', '').strip()
                    expansion = row.get('expansion', '').strip()
                    if abbrev and expansion:
                        self.abbreviations[abbrev] = expansion
            logger.info(f"Loaded {len(self.abbreviations)} abbreviations")
        except Exception as e:
            logger.error(f"Error loading abbreviations: {e}")
    
    def _load_post_processing_corrections(self):
        """Load post-processing corrections from CSV"""
        csv_file = os.path.join(self.glossary_dir, "post_processing_corrections.csv")
        
        if not os.path.exists(csv_file):
            # Create default file with common corrections
            self._create_default_corrections_csv(csv_file)
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    pattern = row.get('pattern', '').strip()
                    replacement = row.get('replacement', '').strip()
                    if pattern and replacement:
                        self.post_processing_corrections[pattern] = replacement
            logger.info(f"Loaded {len(self.post_processing_corrections)} post-processing corrections")
        except Exception as e:
            logger.error(f"Error loading post-processing corrections: {e}")
    
    def _load_exclusion_list(self):
        """Load exclusion list from CSV"""
        csv_file = os.path.join(self.glossary_dir, "exclusion_list.csv")
        
        if not os.path.exists(csv_file):
            # Create default file with common exclusions
            self._create_default_exclusion_list_csv(csv_file)
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    term = row.get('term', '').strip().lower()
                    if term:
                        self.exclusion_list.add(term)
            logger.info(f"Loaded {len(self.exclusion_list)} terms from exclusion list")
        except Exception as e:
            logger.error(f"Error loading exclusion list: {e}")
    
    def _create_default_medical_technical_csv(self, csv_file: str):
        """Create default medical/technical terms CSV"""
        default_terms = [
            # Document terms
            {'english': 'version', 'shona': 'shanduko', 'category': 'document'},
            {'english': 'objective', 'shona': 'chinangwa', 'category': 'document'},
            {'english': 'methodology', 'shona': 'maitiro', 'category': 'document'},
            {'english': 'duration', 'shona': 'nguva', 'category': 'document'},
            {'english': 'participants', 'shona': 'vatori vechikamu', 'category': 'document'},
            {'english': 'sites', 'shona': 'nzvimbo', 'category': 'document'},
            {'english': 'introduction', 'shona': 'nhanganyaya', 'category': 'document'},
            {'english': 'discussion', 'shona': 'nhaurirano', 'category': 'document'},
            {'english': 'interview', 'shona': 'bvunzurudzo', 'category': 'document'},
            {'english': 'guide', 'shona': 'gwara', 'category': 'document'},
            {'english': 'questionnaire', 'shona': 'mubvunzo', 'category': 'document'},
            {'english': 'focus group', 'shona': 'boka rekutarisa', 'category': 'document'},
            
            # Medical terms
            {'english': 'healthcare', 'shona': 'hutano', 'category': 'medical'},
            {'english': 'healthcare workers', 'shona': 'vashandi vehutano', 'category': 'medical'},
            {'english': 'hospital', 'shona': 'chipatara', 'category': 'medical'},
            {'english': 'patient', 'shona': 'murwere', 'category': 'medical'},
            {'english': 'clinical', 'shona': 'kiriniki', 'category': 'medical'},
            {'english': 'diagnosis', 'shona': 'kuongororwa', 'category': 'medical'},
            {'english': 'treatment', 'shona': 'kurapwa', 'category': 'medical'},
            {'english': 'medicine', 'shona': 'mushonga', 'category': 'medical'},
            {'english': 'doctor', 'shona': 'chiremba', 'category': 'medical'},
            {'english': 'nurse', 'shona': 'mukoti', 'category': 'medical'},
            {'english': 'midwife', 'shona': 'nyamukuta', 'category': 'medical'},
            {'english': 'newborn', 'shona': 'mwana achangoberekwa', 'category': 'medical'},
            {'english': 'baby', 'shona': 'mwana', 'category': 'medical'},
            {'english': 'neonatal', 'shona': 'vana vachangoberekwa', 'category': 'medical'},
            {'english': 'ward', 'shona': 'wadhi', 'category': 'medical'},
            {'english': 'facility', 'shona': 'nzvimbo yehutano', 'category': 'medical'},
            
            # Technology terms
            {'english': 'system', 'shona': 'hurongwa', 'category': 'technology'},
            {'english': 'technology', 'shona': 'hunyanzvi', 'category': 'technology'},
            {'english': 'application', 'shona': 'application', 'category': 'technology'},
            {'english': 'software', 'shona': 'software', 'category': 'technology'},
            {'english': 'data', 'shona': 'data', 'category': 'technology'},
            {'english': 'digital', 'shona': 'dhijitari', 'category': 'technology'},
            {'english': 'artificial intelligence', 'shona': 'huchenjeri hwekugadzira', 'category': 'technology'},
            {'english': 'decision support', 'shona': 'rutsigiro rwesarudzo', 'category': 'technology'},
            {'english': 'clinical decision support', 'shona': 'rutsigiro rwesarudzo yekiriniki', 'category': 'technology'},
            
            # Research terms
            {'english': 'study', 'shona': 'kudzidza', 'category': 'research'},
            {'english': 'research', 'shona': 'kutsvagisa', 'category': 'research'},
            {'english': 'observation', 'shona': 'kucherechedza', 'category': 'research'},
            {'english': 'analysis', 'shona': 'kuongororwa', 'category': 'research'},
            {'english': 'findings', 'shona': 'zvakawanwa', 'category': 'research'},
            {'english': 'results', 'shona': 'mhedzisiro', 'category': 'research'},
            {'english': 'conclusion', 'shona': 'mhedziso', 'category': 'research'},
            {'english': 'recommendations', 'shona': 'zviratidziro', 'category': 'research'},
            
            # Common words with specific meanings
            {'english': 'experience', 'shona': 'ruzivo', 'category': 'general'},
            {'english': 'workflow', 'shona': 'mukufamba webasa', 'category': 'general'},
            {'english': 'efficiency', 'shona': 'kushanda zvakanaka', 'category': 'general'},
            {'english': 'quality', 'shona': 'kunaka', 'category': 'general'},
            {'english': 'safety', 'shona': 'kuchengeteka', 'category': 'general'},
            {'english': 'training', 'shona': 'kudzidziswa', 'category': 'general'},
            {'english': 'support', 'shona': 'rutsigiro', 'category': 'general'},
            {'english': 'implementation', 'shona': 'kushandiswa', 'category': 'general'},
            {'english': 'evaluation', 'shona': 'kuongororwa', 'category': 'general'},
            {'english': 'feedback', 'shona': 'mhinduro', 'category': 'general'},
            
            # Basic common translations
            {'english': 'hello', 'shona': 'mhoro', 'category': 'basic'},
            {'english': 'good morning', 'shona': 'mangwanani', 'category': 'basic'},
            {'english': 'good afternoon', 'shona': 'masikati', 'category': 'basic'},
            {'english': 'good evening', 'shona': 'manheru', 'category': 'basic'},
            {'english': 'thank you', 'shona': 'ndatenda', 'category': 'basic'},
            {'english': 'please', 'shona': 'ndapota', 'category': 'basic'},
            {'english': 'yes', 'shona': 'hongu', 'category': 'basic'},
            {'english': 'no', 'shona': 'kwete', 'category': 'basic'},
            {'english': 'welcome', 'shona': 'mutauya', 'category': 'basic'},
            {'english': 'goodbye', 'shona': 'chisarai zvakanaka', 'category': 'basic'}
        ]
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['english', 'shona', 'category'])
            writer.writeheader()
            writer.writerows(default_terms)
        
        logger.info(f"Created default medical/technical terms CSV: {csv_file}")
    
    def _create_default_phrase_csv(self, csv_file: str):
        """Create default phrase translations CSV"""
        default_phrases = [
            {'english': 'what is your name', 'shona': 'zita rako ndiani', 'category': 'conversation'},
            {'english': 'how are you', 'shona': 'makadii', 'category': 'conversation'},
            {'english': 'i am fine', 'shona': 'ndiri right', 'category': 'conversation'},
            {'english': 'thank you very much', 'shona': 'ndatenda zvikuru', 'category': 'conversation'},
            {'english': 'please help me', 'shona': 'ndibatsireiwo', 'category': 'conversation'},
            {'english': 'good morning', 'shona': 'mangwanani akanaka', 'category': 'greeting'},
            {'english': 'clinical decision support system', 'shona': 'hurongwa hwekutsigira sarudzo dzekiriniki', 'category': 'medical'},
            {'english': 'healthcare workers', 'shona': 'vashandi vehutano', 'category': 'medical'},
            {'english': 'focus group discussion', 'shona': 'nhaurirano yeboka rekutarisa', 'category': 'research'}
        ]
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['english', 'shona', 'category'])
            writer.writeheader()
            writer.writerows(default_phrases)
        
        logger.info(f"Created default phrase translations CSV: {csv_file}")
    
    def _create_default_abbreviations_csv(self, csv_file: str):
        """Create default abbreviations CSV"""
        default_abbrevs = [
            {'abbreviation': 'HCW', 'expansion': 'healthcare worker', 'category': 'medical'},
            {'abbreviation': 'CDS', 'expansion': 'clinical decision support', 'category': 'medical'},
            {'abbreviation': 'AI', 'expansion': 'artificial intelligence', 'category': 'technology'},
            {'abbreviation': 'NICU', 'expansion': 'neonatal intensive care unit', 'category': 'medical'},
            {'abbreviation': 'ICU', 'expansion': 'intensive care unit', 'category': 'medical'},
            {'abbreviation': 'ER', 'expansion': 'emergency room', 'category': 'medical'},
            {'abbreviation': 'MRI', 'expansion': 'magnetic resonance imaging', 'category': 'medical'},
            {'abbreviation': 'CT', 'expansion': 'computed tomography', 'category': 'medical'},
            {'abbreviation': 'HIV', 'expansion': 'human immunodeficiency virus', 'category': 'medical'},
            {'abbreviation': 'AIDS', 'expansion': 'acquired immunodeficiency syndrome', 'category': 'medical'}
        ]
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['abbreviation', 'expansion', 'category'])
            writer.writeheader()
            writer.writerows(default_abbrevs)
        
        logger.info(f"Created default abbreviations CSV: {csv_file}")
    
    def _create_default_corrections_csv(self, csv_file: str):
        """Create default post-processing corrections CSV"""
        default_corrections = [
            {'pattern': r'\\bmhando\\b', 'replacement': 'shanduko', 'description': 'Fix version translation'},
            {'pattern': r'\\bmanzwiro\\b', 'replacement': 'pfungwa', 'description': 'Better word for feelings/thoughts'},
            {'pattern': r'\\bkuongorora\\b', 'replacement': 'kuongororwa', 'description': 'Standardize examination'},
            {'pattern': r'\\bkubvunza\\b', 'replacement': 'bvunzurudzo', 'description': 'Fix interview translation'},
            {'pattern': r'\\bmubvunzo\\b', 'replacement': 'mubvunzo', 'description': 'Questionnaire consistency'},
            {'pattern': r'\\bzvikuru\\b', 'replacement': 'zvikuru', 'description': 'Very/much consistency'}
        ]
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['pattern', 'replacement', 'description'])
            writer.writeheader()
            writer.writerows(default_corrections)
        
        logger.info(f"Created default post-processing corrections CSV: {csv_file}")
    
    def _create_default_exclusion_list_csv(self, csv_file: str):
        """Create default exclusion list CSV"""
        default_exclusions = [
            # Brand names and proper nouns
            {'term': 'neotree', 'reason': 'Brand name'},
            {'term': "neotree's", 'reason': 'Brand name'},
            {'term': 'sally mugabe central hospital', 'reason': 'Hospital name'},
            {'term': 'chinhoyi provincial hospital', 'reason': 'Hospital name'},
            {'term': 'kamuzu central hospital', 'reason': 'Hospital name'},
            {'term': 'kasungu district hospital', 'reason': 'Hospital name'},
            
            # Technical abbreviations and terms
            {'term': 'cds', 'reason': 'Technical abbreviation'},
            {'term': 'ai', 'reason': 'Technical abbreviation'},
            {'term': 'ai-cds', 'reason': 'Technical term'},
            {'term': 'ai-enabled', 'reason': 'Technical term'},
            {'term': 'nicu', 'reason': 'Medical abbreviation'},
            {'term': 'nnu', 'reason': 'Medical abbreviation'},
            {'term': 'dhis2', 'reason': 'System name'},
            {'term': 'emrs', 'reason': 'System abbreviation'},
            {'term': 'moh', 'reason': 'Government abbreviation'},
            
            # Specific phrases and terms
            {'term': 'healthcare systems usability scale for clinical decision support systems', 'reason': 'Specific assessment tool'},
            {'term': 'gut feeling', 'reason': 'Idiomatic expression'},
            {'term': 'artificial intelligence', 'reason': 'Technical term'},
            {'term': 'aim 2', 'reason': 'Research objective'},
            {'term': 'normalization measure development questionnaire', 'reason': 'Specific assessment tool'}
        ]
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['term', 'reason'])
            writer.writeheader()
            writer.writerows(default_exclusions)
        
        logger.info(f"Created default exclusion list CSV: {csv_file}")
    
    def preprocess_text(self, text: str) -> str:
        """Preprocess text to handle abbreviations"""
        result = text
        
        # Sort abbreviations by length (longest first) to avoid partial replacements
        sorted_abbrevs = sorted(self.abbreviations.items(), key=lambda x: len(x[0]), reverse=True)
        
        for abbrev, expansion in sorted_abbrevs:
            # Only skip if this abbreviation is in exclusion list AND it's the entire text
            if abbrev.lower() in self.exclusion_list and text.lower().strip() == abbrev.lower():
                continue
                
            pattern = r'\b' + re.escape(abbrev) + r'\b'
            result = re.sub(pattern, expansion, result, flags=re.IGNORECASE)
        
        return result
    
    def translate_with_glossary(self, text: str) -> Optional[str]:
        """Try to translate using glossary first"""
        text_lower = text.lower().strip()
        
        # Check if the entire text is in exclusion list
        if text_lower in self.exclusion_list:
            logger.info(f"Excluded from translation: '{text}'")
            return None
        
        # Check for exact phrase matches first
        if text_lower in self.phrase_translations:
            return self.phrase_translations[text_lower]
        
        # Check for exact word matches
        if text_lower in self.medical_technical_glossary:
            return self.medical_technical_glossary[text_lower]
        
        # Check for partial matches and replace terms
        result = text
        replacements_made = False
        
        # Sort by length (longest first) to avoid partial replacements
        sorted_terms = sorted(self.medical_technical_glossary.items(), 
                            key=lambda x: len(x[0]), reverse=True)
        
        for english, shona in sorted_terms:
            # Skip if this term is in exclusion list
            if english.lower() in self.exclusion_list:
                continue
                
            pattern = r'\b' + re.escape(english) + r'\b'
            if re.search(pattern, result, re.IGNORECASE):
                result = re.sub(pattern, shona, result, flags=re.IGNORECASE)
                replacements_made = True
        
        return result if replacements_made else None
    
    def post_process_translation(self, text: str) -> str:
        """Post-process translation to fix common errors"""
        result = text
        
        for pattern, replacement in self.post_processing_corrections.items():
            # Convert string pattern to regex if needed
            if pattern.startswith('\\b'):
                # Already a regex pattern
                result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
            else:
                # Simple string replacement
                result = result.replace(pattern, replacement)
        
        return result
    
    def get_glossary_stats(self) -> Dict[str, int]:
        """Get statistics about loaded glossary data"""
        return {
            'medical_technical_terms': len(self.medical_technical_glossary),
            'phrase_translations': len(self.phrase_translations),
            'abbreviations': len(self.abbreviations),
            'post_processing_corrections': len(self.post_processing_corrections),
            'exclusion_list': len(self.exclusion_list)
        }
