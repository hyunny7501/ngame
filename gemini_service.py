import os
import logging
from google import genai
from google.genai import types

class GeminiNRowService:
    def __init__(self):
        """Initialize Gemini client with API key from environment"""
        api_key = os.getenv("GEMINI_API_KEY", "")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        self.client = genai.Client(api_key=api_key)
        
    def generate_nrow_poem(self, word: str) -> str:
        """
        Generate Korean N-행시 (acrostic poem) for the given word
        
        Args:
            word (str): Korean word to create N-행시 from
            
        Returns:
            str: Generated N-행시 poem with emojis
        """
        try:
            # Create a detailed prompt for Korean N-행시 generation
            prompt = f"""
당신은 아이들을 위한 창의적인 한국어 N행시 작가입니다. 
주어진 단어 '{word}'로 재미있고 창의적인 N행시를 만들어주세요.

규칙:
1. 각 줄은 해당 글자로 시작해야 합니다
2. 아이들이 이해하기 쉬운 단어와 표현을 사용하세요
3. 긍정적이고 밝은 내용으로 작성하세요
4. 각 줄에 적절한 이모티콘을 1-2개씩 추가하세요
5. 운율이나 리듬감을 고려하세요
6. 교육적이거나 상상력을 자극하는 내용이면 더 좋습니다

예시 형식:
[첫째글자] 첫 번째 줄 내용 🌟
[둘째글자] 두 번째 줄 내용 🎈
...

단어: {word}
N행시:
"""

            # Generate content using Gemini
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.8,  # Higher creativity for poems
                    top_p=0.9,
                    max_output_tokens=1000
                )
            )
            
            if response.text:
                return response.text.strip()
            else:
                return "죄송해요, N행시를 만들지 못했어요. 다시 시도해주세요! 😅"
                
        except Exception as e:
            logging.error(f"Error generating N-row poem: {e}")
            return f"오류가 발생했어요: {str(e)} 😢\n다시 시도해주세요!"
    
    def validate_korean_word(self, word: str) -> tuple[bool, str]:
        """
        Validate if the input is a valid Korean word
        
        Args:
            word (str): Word to validate
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not word:
            return False, "단어를 입력해주세요! 📝"
        
        if len(word.strip()) == 0:
            return False, "공백만 입력하셨어요. 한글 단어를 입력해주세요! ✏️"
        
        # Check if word contains Korean characters
        korean_chars = any('\uac00' <= char <= '\ud7a3' for char in word)
        if not korean_chars:
            return False, "한글 단어를 입력해주세요! 🇰🇷"
        
        # Remove spaces and check length
        clean_word = word.replace(" ", "")
        if len(clean_word) > 10:
            return False, "단어가 너무 길어요! 10글자 이하로 입력해주세요! 📏"
        
        if len(clean_word) < 2:
            return False, "2글자 이상의 단어를 입력해주세요! 📖"
        
        return True, ""
