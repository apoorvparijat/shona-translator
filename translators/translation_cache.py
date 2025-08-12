#!/usr/bin/env python3
"""
Translation Cache - Smart caching system for reusing translations across providers
"""

import os
import json
import logging
import hashlib
from typing import Optional, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)

class TranslationCache:
    """Smart caching system for translations across all providers"""
    
    def __init__(self, cache_file: str = "translation_cache.json"):
        self.cache_file = cache_file
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.stats = {
            'hits': 0,
            'misses': 0,
            'total_requests': 0
        }
        self._load_cache()
        logger.info(f"Translation cache initialized with {len(self.cache)} entries")
    
    def _get_cache_key(self, text: str) -> str:
        """Generate a cache key for the given text"""
        # Normalize text for consistent caching
        normalized_text = text.strip().lower()
        return hashlib.md5(normalized_text.encode('utf-8')).hexdigest()
    
    def get(self, text: str, provider: str = None) -> Optional[str]:
        """Get translation from cache"""
        if not text.strip():
            return text
        
        self.stats['total_requests'] += 1
        cache_key = self._get_cache_key(text)
        
        if cache_key in self.cache:
            entry = self.cache[cache_key]
            
            # If provider is specified, check if that provider has a translation
            if provider and provider in entry['translations']:
                translation_data = entry['translations'][provider]
                if translation_data and translation_data['text'] and translation_data['text'].strip():
                    self.stats['hits'] += 1
                    logger.debug(f"Cache HIT for '{text[:50]}...' from {provider}")
                    return translation_data['text']
            
            # If no specific provider or provider not found, return the best available translation
            best_translation = self._get_best_translation(entry)
            if best_translation:
                self.stats['hits'] += 1
                logger.debug(f"Cache HIT for '{text[:50]}...' (best available)")
                return best_translation
        
        self.stats['misses'] += 1
        logger.debug(f"Cache MISS for '{text[:50]}...'")
        return None
    
    def set(self, text: str, translation: str, provider: str, confidence: float = 1.0) -> None:
        """Store translation in cache"""
        if not text.strip() or not translation.strip():
            return
        
        cache_key = self._get_cache_key(text)
        
        if cache_key not in self.cache:
            self.cache[cache_key] = {
                'original_text': text,
                'translations': {},
                'metadata': {
                    'first_seen': self._get_timestamp(),
                    'last_updated': self._get_timestamp()
                }
            }
        
        entry = self.cache[cache_key]
        entry['translations'][provider] = {
            'text': translation,
            'confidence': confidence,
            'timestamp': self._get_timestamp()
        }
        entry['metadata']['last_updated'] = self._get_timestamp()
        
        logger.debug(f"Cached translation for '{text[:50]}...' from {provider}")
        self._save_cache()
    
    def _get_best_translation(self, entry: Dict[str, Any]) -> Optional[str]:
        """Get the best available translation from an entry"""
        if not entry['translations']:
            return None
        
        # Sort by confidence and timestamp (newer is better)
        translations = []
        for provider, data in entry['translations'].items():
            if data['text'] and data['text'].strip():
                translations.append((provider, data))
        
        if not translations:
            return None
        
        # Sort by confidence (highest first), then by timestamp (newest first)
        translations.sort(key=lambda x: (x[1]['confidence'], x[1]['timestamp']), reverse=True)
        
        return translations[0][1]['text']
    
    def get_all_translations(self, text: str) -> Dict[str, str]:
        """Get all available translations for a text"""
        cache_key = self._get_cache_key(text)
        
        if cache_key in self.cache:
            entry = self.cache[cache_key]
            return {
                provider: data['text']
                for provider, data in entry['translations'].items()
                if data['text'] and data['text'].strip()
            }
        
        return {}
    
    def has_translation(self, text: str, provider: str = None) -> bool:
        """Check if translation exists in cache"""
        if not text.strip():
            return True  # Empty text doesn't need translation
        
        cache_key = self._get_cache_key(text)
        
        if cache_key not in self.cache:
            return False
        
        if provider:
            return provider in self.cache[cache_key]['translations']
        
        return bool(self.cache[cache_key]['translations'])
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_entries = len(self.cache)
        total_translations = sum(len(entry['translations']) for entry in self.cache.values())
        
        provider_stats = {}
        for entry in self.cache.values():
            for provider in entry['translations'].keys():
                provider_stats[provider] = provider_stats.get(provider, 0) + 1
        
        hit_rate = (self.stats['hits'] / self.stats['total_requests'] * 100) if self.stats['total_requests'] > 0 else 0
        
        return {
            'total_entries': total_entries,
            'total_translations': total_translations,
            'provider_stats': provider_stats,
            'hits': self.stats['hits'],
            'misses': self.stats['misses'],
            'total_requests': self.stats['total_requests'],
            'hit_rate': round(hit_rate, 2)
        }
    
    def clear_cache(self) -> None:
        """Clear the cache"""
        self.cache.clear()
        self.stats = {'hits': 0, 'misses': 0, 'total_requests': 0}
        self._save_cache()
        logger.info("Translation cache cleared")
    
    def _get_timestamp(self) -> float:
        """Get current timestamp"""
        import time
        return time.time()
    
    def _load_cache(self) -> None:
        """Load cache from file"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.cache = data.get('cache', {})
                    self.stats = data.get('stats', {'hits': 0, 'misses': 0, 'total_requests': 0})
                logger.info(f"Loaded translation cache from {self.cache_file}")
        except Exception as e:
            logger.warning(f"Failed to load cache from {self.cache_file}: {e}")
            self.cache = {}
            self.stats = {'hits': 0, 'misses': 0, 'total_requests': 0}
    
    def _save_cache(self) -> None:
        """Save cache to file"""
        try:
            data = {
                'cache': self.cache,
                'stats': self.stats
            }
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Failed to save cache to {self.cache_file}: {e}")

# Global cache instance
_translation_cache = None

def get_translation_cache() -> TranslationCache:
    """Get the global translation cache instance"""
    global _translation_cache
    if _translation_cache is None:
        _translation_cache = TranslationCache()
    return _translation_cache
