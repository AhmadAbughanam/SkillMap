import os
import threading
from typing import Optional

# Example: Using llama-cpp-python or HuggingFace local model
# Import your preferred local LLM interface here
# For demonstration, I'll sketch a llama-cpp-python wrapper pattern

try:
    from llama_cpp import Llama
except ImportError:
    Llama = None

# MODEL_PATH = os.environ.get(
#     "LLM_MODEL_PATH", "../models/mistral-7b-instruct-v0.1.Q2_K.gguf"
# )

MODEL_PATH = os.path.join("app", "models", "mistral-7b-instruct-v0.1.Q2_K.gguf")


_llm_instance = None
_llm_lock = threading.Lock()


def get_llm_instance():
    global _llm_instance
    if _llm_instance is None:
        if Llama is None:
            raise RuntimeError("llama_cpp not installed or unavailable")
        _llm_instance = Llama(model_path=MODEL_PATH)
    return _llm_instance


def generate_llm_insight(skill, section: Optional[str] = "general") -> str:
    """
    Generate an insight string from the local LLM based on the skill and section.

    Args:
        skill: Skill model instance with attributes like name, description, milestones
        section: The insight section/topic requested (e.g. 'motivation', 'next steps')

    Returns:
        Generated insight string
    """
    prompt = build_prompt(skill, section)

    llm = get_llm_instance()
    with _llm_lock:
        response = llm.create_completion(prompt=prompt, max_tokens=512, temperature=0.7)
        # Adjust parameters based on your model and llama-cpp-python version

    text = (
        response["choices"][0]["text"].strip()
        if response and "choices" in response and response["choices"]
        else "No insight generated."
    )
    return text or "No insight generated."


def build_prompt(skill, section) -> str:
    milestones_summary = "\n".join(
        f"- {m.timestamp.strftime('%Y-%m-%d')}: {m.progress_level or 'Progress'} - {(m.note or '')[:100]}"
        for m in sorted(skill.milestones, key=lambda x: x.timestamp, reverse=True)[:5]
    )

    return f"""
You are an AI assistant that provides insightful, actionable advice on personal skill development.

Skill: {skill.name}
Category: {skill.category or 'General'}
Description: {skill.description or 'No description provided.'}

Recent Milestones:
{milestones_summary or 'No recent milestones.'}

Please provide a detailed insight focusing on the following topic: {section}

Answer in clear, concise paragraphs.
""".strip()
