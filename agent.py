import os
import time
import re
import math
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from presidio_analyzer import AnalyzerEngine, EntityRecognizer, RecognizerResult
from presidio_anonymizer import AnonymizerEngine

from prompts import SYSTEM_META_PROMPT
from presidio_anonymizer.entities import OperatorConfig

load_dotenv()

class OptimizedPrompt(BaseModel):
    persona_used: str = Field(description="The expert persona assigned to this prompt.")
    reasoning: str = Field(description="Brief explanation of how you optimized the prompt.")
    improved_prompt: str = Field(description="The final, highly optimized prompt. DO NOT answer the prompt.")

class EntropyPasswordRecognizer(EntityRecognizer):
    def __init__(self):
        super().__init__(supported_entities=["PASSWORD"])
    
    def load(self) -> None:
        pass

    def analyze(self, text: str, entities, nlp_artifacts=None):
        results = []
        for match in re.finditer(r'\S+', text):
            word = match.group()
            
            # Reverted to your exact logic: only skip single characters
            if len(word) <= 1:
                continue
            
            prob = [float(word.count(c)) / len(word) for c in set(word)]
            entropy = -sum(p * math.log2(p) for p in prob)
            
            # Check for all three types
            has_letter = bool(re.search(r'[a-zA-Z]', word))
            has_num = bool(re.search(r'\d', word))
            has_symbol = bool(re.search(r'[^\w\s]', word))
            
            # Your logic: If it has ALL THREE, it is a password (catches short ones like "1!2e")
            if has_letter and has_num and has_symbol and entropy >= 2.0:
                results.append(RecognizerResult(
                    entity_type="PASSWORD", 
                    start=match.start(), 
                    end=match.end(), 
                    score=0.9
                ))
            # FALLBACK: If it's a longer string (8+) with high entropy and at least a number OR symbol
            elif len(word) >= 8 and (has_num or has_symbol) and entropy >= 3.2:
                results.append(RecognizerResult(
                    entity_type="PASSWORD", 
                    start=match.start(), 
                    end=match.end(), 
                    score=0.9
                ))
                
        return results

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

entropy_recognizer = EntropyPasswordRecognizer()
analyzer.registry.add_recognizer(entropy_recognizer)

parser = PydanticOutputParser(pydantic_object=OptimizedPrompt)

# Restored your exact model
llm = ChatGroq(model_name="openai/gpt-oss-20b", max_tokens=4096, temperature=0.0)

optimizer_prompt_template = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_META_PROMPT),
    ("human", "Raw User Input: {raw_input}")
])

optimizer_chain = optimizer_prompt_template | llm | parser

def mask_pii(text: str) -> str:
    results = analyzer.analyze(
        text=text, 
        entities=["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER", "PASSWORD"], 
        language='en'
    )
    
    custom_operators = {
        "PASSWORD": OperatorConfig("replace", {"new_value": "[REDACTED]"})
    }
    
    anonymized_result = anonymizer.anonymize(
        text=text, 
        analyzer_results=results, 
        operators=custom_operators
    )
    return anonymized_result.text

def optimize_prompt(raw_input: str) -> OptimizedPrompt:
    return optimizer_chain.invoke({
        "raw_input": raw_input,
        "format_instructions": parser.get_format_instructions()
    })

def execute_prompt_with_metrics(prompt_text: str):
    start_time = time.time()
    response = llm.invoke(prompt_text)
    latency = round((time.time() - start_time) * 1000, 2)
    
    token_usage = response.response_metadata.get('token_usage', {})
    total_tokens = token_usage.get('total_tokens', 'N/A')
    
    content = str(response.content).strip()
    if not content:
        content = "*(No response generated for this input)*"
        
    return content, latency, total_tokens


