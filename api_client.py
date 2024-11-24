import os
import json
from openai import OpenAI
from dotenv import load_dotenv
import logging
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class APIClient:
    def __init__(self, perplexity_api_key, openai_api_key):
        self.perplexity_api_key = perplexity_api_key
        self.openai_api_key = openai_api_key
        
        # Initialize Perplexity client
        self.perplexity_client = OpenAI(
            api_key=self.perplexity_api_key,
            base_url="https://api.perplexity.ai"
        )
        
        # Initialize OpenAI client
        self.openai_client = OpenAI(
            api_key=self.openai_api_key
        )

    def analyze_article(self, article_url):
        """
        Analyze an article using the Perplexity API to extract key knowledge and insights
        """
        try:
            # First, get the article content
            response = requests.get(article_url)
            if response.status_code != 200:
                logger.error(f"Failed to fetch article from {article_url}")
                return None

            article_text = response.text

            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a knowledgeable AI assistant that extracts valuable insights from articles. "
                        "Focus on extracting factual information, technical details, and practical knowledge. "
                        "Provide your analysis in a strict JSON format with the following structure:"
                        "{"
                        "  'key_insights': ['Array of main technical or practical insights'],"
                        "  'technical_details': ['Array of specific technical information or specifications'],"
                        "  'practical_applications': ['Array of real-world applications or use cases'],"
                        "  'considerations': ['Array of important considerations or limitations'],"
                        "  'context': 'A brief summary of the article context'"
                        "}"
                    )
                },
                {
                    "role": "user",
                    "content": f"Extract valuable knowledge and insights from this article: {article_text}"
                }
            ]

            response = self.perplexity_client.chat.completions.create(
                model="llama-3.1-sonar-small-128k-online",
                messages=messages,
                temperature=0.2,
                top_p=0.9
            )

            # Extract and parse the response content
            analysis = response.choices[0].message.content
            try:
                # Try to parse as JSON
                return json.loads(analysis)
            except json.JSONDecodeError:
                # If parsing fails, return structured format
                return {
                    "key_insights": [analysis],
                    "technical_details": [],
                    "practical_applications": [],
                    "considerations": [],
                    "context": ""
                }

        except Exception as e:
            logger.error(f"Error analyzing article with Perplexity API: {str(e)}")
            return None

    def generate_linkedin_post(self, data):
        """
        Generate a knowledge-focused LinkedIn post in French using OpenAI
        """
        try:
            prompt = f"""
            En vous basant sur cet article dont le titre est : "{data['title']}"
            Et le contexte : "{data.get('context', '')}"
            
            Créez un post LinkedIn éducatif en français qui :
            1. Commence par une brève mise en contexte de l'article pour introduire le sujet
            2. Partage des connaissances techniques approfondies sur le sujet
            3. Explique les concepts complexes de manière accessible
            4. Fournit des insights pratiques que les lecteurs peuvent appliquer
            5. Maintient un ton professionnel et éducatif
            
            Le post doit :
            - Avoir une accroche captivante
            - Inclure le contexte de l'article de manière concise
            - Développer des points techniques ou pratiques
            - Se terminer par une conclusion réflexive
            - Inclure 8 -10 hashtags pertinents en français
            
            Formatez le post pour qu'il soit prêt à être copié directement sur LinkedIn.
            """

            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "Vous êtes un expert technique qui partage des connaissances approfondies en français. Créez du contenu qui enseigne des concepts techniques et des compétences pratiques. Le contenu doit être entièrement en français et adapté à la culture professionnelle française."
                    },
                    {"role": "user", "content": prompt}
                ]
            )

            return {
                "post": response.choices[0].message.content.strip()
            }

        except Exception as e:
            logger.error(f"Error generating LinkedIn post: {str(e)}")
            return None
