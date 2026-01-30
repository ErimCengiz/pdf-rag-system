from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os 
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"

MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"

_tokenizer = None
_model = None

def load_model():
    global _tokenizer, _model

    if _model is not None and _tokenizer is not None:
        return _tokenizer, _model
    

    _tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME,
        use_fast = True,
    )

    _model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype = torch.float16,
        device_map = "auto",
    )
    _model.eval()


    return _tokenizer, _model


def generate_answer(context: str, question: str) -> str:
    tokenizer, model = load_model()
    
    prompt = f"""
You are an AI assistant answering questions strictly based on the provided document excerpts.

Rules:
- Use ONLY the information from the context.
- If the answer is not in the context, say:
  "The answer is not available in the provided documents."
- Do NOT use outside knowledge.
- Answer concisely and clearly.
- Paraphrase instead of copying text.

Context:
{context}

Question:
{question}

Answer:
"""
    inputs = tokenizer(prompt, 
                       return_tensors = "pt", 
                       truncation = True, 
                       max_length = 2048
                       ).to(model.device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens = 100,
            temperature = 0.0,
            do_sample = False,
            pad_token_id = tokenizer.eos_token_id,
        )
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    answer = decoded.split("Answer:")[-1].strip()
    del inputs, outputs
    torch.cuda.empty_cache()

    return answer