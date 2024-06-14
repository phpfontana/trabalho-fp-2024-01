from typing import Any
from langchain_core.language_models.llms import BaseLLM
from langchain_community.llms.ollama import Ollama
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

def load_llm_hf(model_id: str, task: str, **kwargs) -> BaseLLM:
    """
    Load language model.

    Args:
        model_name (str): Model name
        task (str): Task
        kwargs (Dict[str, Any]): Additional arguments

    Returns:
        BaseLLM: The loaded language model.
    """
 
    # Load model tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    
    # Load model
    model = AutoModelForCausalLM.from_pretrained(model_id)

    # Load pipeline
    pipe = pipeline(
        task=task,
        model=model,
        tokenizer=tokenizer,
        **kwargs
    )

    # Instantiate LLM
    llm = HuggingFacePipeline(pipeline=pipe)

    return llm

def load_llm_ollama(model_name: str, base_url: str, **kwargs) -> BaseLLM:
    """
    Load large language model from Ollama.

    Args:
        model_name (str): The name of the model to load
        pipeline_kwargs Optional(Dict[str, Any]): The pipeline actions.

    Returns:
        BaseLLM: The loaded language model.
    
    Raises:
        ValueError: If there is an error loading the model
    """
    try:
        llm = Ollama(model=model_name, base_url=base_url, **kwargs )
    except Exception as e:
        raise ValueError(f"Error loading model {model_name}: {e}") from e        
    
    return llm
    
async def generate_response(prompt: str, llm: BaseLLM) -> Any:
    """
    Generate a response using large language model.

    Args:
        prompt (String): The user prompt.
        llm (BaseLLM): The loaded language model.

    Returns:
        Any: The generated response or a streaming response
    """
    try:
        return llm.invoke(prompt)
    except Exception as e:
        raise ValueError(f"Error generating: {str(e)}") from e


async def generate_streaming_response(prompt: str, llm: BaseLLM) -> Any:
    """
    Generate a response using large language model.

    Args:
        promt (String): The llm prompt.
        llm (BaseLLM): The loaded language model.

    Returns:
        Any: The generated streaming response.
    """
    try:
        for chunks in llm.stream(prompt):
            yield chunks
    except Exception as e:
        raise ValueError(f"Error generating: {str(e)}") from e