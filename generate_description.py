from transformers import AutoTokenizer, AutoModelForCausalLM
import numpy as np
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import re

if torch.cuda.is_available():
    device = torch.device('cuda')
    print("CUDA available! Training on GPU.", flush=True)
elif torch.backends.mps.is_available():
    device = torch.device('mps')
    print("MPS available! Training on GPU.", flush=True)
else:
    device = torch.device('cpu')
    print("CUDA NOT available... Training on CPU.", flush=True)

access_token='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'

# model1_checkpoint = "google/gemma-2b-it"

model1_checkpoint = "meta-llama/Llama-3.2-1B-Instruct"

tokenizer1 = AutoTokenizer.from_pretrained(model1_checkpoint, token=access_token)
model1 = AutoModelForCausalLM.from_pretrained(model1_checkpoint, token=access_token)

model1.to(device)

def truncate_at_last_sentence(text, max_words=150):
    """Truncates text at the last complete sentence or max_words."""

    last_index = -1

    for char in [".", "?", "!"]:
        last_occurrence = text.rfind(char)  # Find the *last* occurrence
        if last_occurrence > last_index:
            last_index = last_occurrence

    if last_index != -1:
        return text[:last_index + 1].strip()  # Include punctuation, remove whitespace
    else:  # No sentence ending found
        words = text.split()
        if len(words) <= max_words:
            return text.strip()  # Return the whole thing if short
        else:
            return " ".join(words[:max_words]) + "..."  # Truncate and add ellipsis


def generate_description(landmark, location):
    prompt = f"Write me a short description of {landmark}, located at {location}. Include any historical, environmental, and technological details. Be child-friendly! Do not include any AI type language, just respond with natural language in a paragraph with no more than 200 words, *making sure to end with a complete sentence*.\n"
    inputs = tokenizer1(prompt, return_tensors="pt", max_length=200, truncation=True).to(device)
    outputs = model1.generate(**inputs, max_length=200, do_sample=True, temperature=0.9, num_return_sequences=1)

    text = tokenizer1.decode(outputs[0], skip_special_tokens=True)  # Decode AFTER generation
    final_text = truncate_at_last_sentence(text)
    return final_text


# Example usage
# print(generate_description("Boston Public Library", "Boston, MA"))