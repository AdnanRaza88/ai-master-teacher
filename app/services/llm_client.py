import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from app.core.config import APP_CONFIG


class GemmaClient:
    """
    Loads Google Gemma 4 on Kaggle T4 GPU using 4-bit quantization.
    Falls back to smaller model if primary fails.
    """

    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._load_model()

    def _load_model(self):
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
        )

        for model_id in [APP_CONFIG["model_primary"], APP_CONFIG["model_fallback"]]:
            try:
                print(f"[GemmaClient] Loading: {model_id}")
                self.tokenizer = AutoTokenizer.from_pretrained(model_id)
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_id,
                    quantization_config=bnb_config,
                    device_map="auto",
                    torch_dtype=torch.bfloat16,
                    low_cpu_mem_usage=True,
                )
                print(f"[GemmaClient] ✅ Loaded: {model_id}")
                return
            except Exception as e:
                print(f"[GemmaClient] ❌ Failed {model_id}: {e}")
                continue

        raise RuntimeError("Both Gemma 4 models failed to load. Check GPU memory and internet.")

    def generate(self, prompt: str, max_new_tokens: int = None) -> str:
        if self.model is None:
            raise RuntimeError("Model not loaded.")

        max_tokens = max_new_tokens or APP_CONFIG["max_new_tokens"]

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=2048,
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=APP_CONFIG["temperature"],
                top_p=APP_CONFIG["top_p"],
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                repetition_penalty=1.1,
            )

        # Decode only NEW tokens
        new_tokens = outputs[0][inputs["input_ids"].shape[1]:]
        return self.tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
        
