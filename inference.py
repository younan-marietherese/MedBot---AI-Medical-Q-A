import os
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch, json

# Writable cache on Spaces + quiet tokenizer threads
os.environ["HF_HOME"] = "/tmp/hf"
os.environ["TRANSFORMERS_CACHE"] = "/tmp/hf"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "medbot_model"  # your exported LoRA folder (tokenizer + adapter)

# Safe generation defaults (CPU or GPU)
GEN_CFG = {
    "max_new_tokens": 160,
    "temperature": 0.7,
    "top_p": 0.9,
    "do_sample": True,
}
cfg_path = MODEL_DIR / "generation_config.json"
if cfg_path.exists():
    try:
        GEN_CFG.update(json.loads(cfg_path.read_text(encoding="utf-8")))
    except Exception:
        pass

# Base model ID (fallback to TinyLlama chat)
base_model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
base_txt = MODEL_DIR / "BASE_MODEL.txt"
if base_txt.exists():
    t = base_txt.read_text(encoding="utf-8").strip()
    if t:
        base_model_id = t

# Use *slow* tokenizer for LLaMA/TinyLlama to avoid fast-tokenizer JSON issues
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_DIR.as_posix(),   # load tokenizer from your LoRA export
    use_fast=False,
    legacy=True
)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Device / dtype (GPU on Spaces if available)
use_cuda = torch.cuda.is_available()
dtype = torch.float16 if use_cuda else torch.float32
device_map = "auto" if use_cuda else "cpu"

# Load base model by ID (Spaces will download/cache it the first time)
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_id,
    torch_dtype=dtype,
    device_map=device_map,
)

# Apply your LoRA adapters
model = PeftModel.from_pretrained(base_model, MODEL_DIR.as_posix())
model.eval()
for p in model.parameters():
    p.requires_grad_(False)

def _format_prompt(user_text: str) -> str:
    if hasattr(tokenizer, "apply_chat_template"):
        return tokenizer.apply_chat_template(
            [
                {"role": "system", "content": "You are a helpful medical assistant."},
                {"role": "user", "content": user_text.strip()},
            ],
            tokenize=False,
            add_generation_prompt=True,
        )
    return f"<|system|>\nYou are a helpful medical assistant.\n<|user|>\n{user_text.strip()}\n<|assistant|>"

@torch.inference_mode()
def _generate(prompt: str) -> str:
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    out = model.generate(
        **inputs,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id,
        **GEN_CFG,
    )
    new_tokens = out[0, inputs["input_ids"].shape[-1]:]
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()

def get_answer(question: str) -> str:
    text = (question or "").strip()
    if not text:
        return "Please enter a question."
    ans = _generate(_format_prompt(text))
    disclaimer = ("MedBot provides general information only and is not a substitute for professional medical advice. "
                  "If this is an emergency, call your local emergency number.")
    return f"{disclaimer}\n\n{ans or 'I’m sorry—please rephrase your question.'}"
