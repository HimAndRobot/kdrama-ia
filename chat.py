# Interactive chat with the fine-tuned K-drama Gemma model
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel


BASE_MODEL_ID = "google/gemma-4-E4B-it"
ADAPTER_DIR = "./kdrama-model"


def load_model():
    print("Loading base model...")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )

    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL_ID,
        quantization_config=bnb_config,
        device_map="auto",
        torch_dtype=torch.bfloat16,
    )

    print("Loading fine-tuned adapter...")
    model = PeftModel.from_pretrained(model, ADAPTER_DIR)

    return model, tokenizer


def generate(model, tokenizer, prompt, max_new_tokens=512):
    chat = f"<start_of_turn>user\n{prompt}<end_of_turn>\n<start_of_turn>model\n"
    inputs = tokenizer(chat, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.7,
            top_p=0.9,
            top_k=50,
            repetition_penalty=1.15,
            do_sample=True,
        )

    response = tokenizer.decode(outputs[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
    return response.strip()


def main():
    model, tokenizer = load_model()
    print("\n=== KDrama IA Chat ===")
    print("Digite sua pergunta sobre K-dramas (ou 'sair' para encerrar)\n")

    while True:
        user_input = input("Você: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("sair", "exit", "quit"):
            print("Até mais!")
            break

        response = generate(model, tokenizer, user_input)
        print(f"\nKDrama IA: {response}\n")


if __name__ == "__main__":
    main()
