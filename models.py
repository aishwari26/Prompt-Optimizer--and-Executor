from pydantic import BaseModel, Field

class OptimizedPrompt(BaseModel):
    improved_prompt: str = Field(
        description="The fully optimized, highly detailed prompt ready to be executed."
    )
    reasoning: str = Field(
        description="A 1-2 sentence explanation of why these improvements were made."
    )
    persona_used: str = Field(
        description="The expert persona assigned to the prompt (e.g., Senior Software Engineer, Expert Copywriter)."
    )