# Fine-tune Gemma 4 with QLoRA on K-drama dataset
import os
import torch
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer, SFTConfig


MODEL_ID = "google/gemma-4-E4B-it"
OUTPUT_DIR = "./kdrama-model"
DATA_FILE = "./data/kdramas.txt"


def load_kdramas(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = content.strip().split("[SERIE]")
    blocks = [b.strip() for b in blocks if b.strip()]

    samples = []
    for block in blocks:
        lines = block.split("\n")
        nome = ""
        genero = ""
        sinopse = ""

        for line in lines:
            if line.startswith("Nome:"):
                nome = line.replace("Nome:", "").strip()
            elif line.startswith("Gênero:"):
                genero = line.replace("Gênero:", "").strip()
            elif line.startswith("Sinopse:"):
                sinopse = line.replace("Sinopse:", "").strip()

        if nome and sinopse:
            samples.append({
                "text": f"<start_of_turn>user\nMe recomende um kdrama de {genero}.<end_of_turn>\n"
                        f"<start_of_turn>model\nEu recomendo **{nome}**! {sinopse}<end_of_turn>"
            })
            samples.append({
                "text": f"<start_of_turn>user\nO que você sabe sobre o kdrama {nome}?<end_of_turn>\n"
                        f"<start_of_turn>model\n**{nome}** é um kdrama do gênero {genero}. {sinopse}<end_of_turn>"
            })
            samples.append({
                "text": f"<start_of_turn>user\nMe fale sobre algum dorama bom.<end_of_turn>\n"
                        f"<start_of_turn>model\nVocê precisa assistir **{nome}**! É um dorama de {genero}. {sinopse}<end_of_turn>"
            })

    return Dataset.from_list(samples)


def main():
    print("Loading dataset...")
    dataset = load_kdramas(DATA_FILE)
    print(f"Total training samples: {len(dataset)}")

    print(f"Loading tokenizer from {MODEL_ID}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )

    print(f"Loading model {MODEL_ID} in 4-bit...")
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        quantization_config=bnb_config,
        device_map="auto",
        torch_dtype=torch.bfloat16,
    )

    model = prepare_model_for_kbit_training(model)

    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        lora_dropout=0.05,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        bias="none",
        task_type="CAUSAL_LM",
    )

    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    training_config = SFTConfig(
        output_dir=OUTPUT_DIR,
        num_train_epochs=3,
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        weight_decay=0.01,
        warmup_steps=10,
        logging_steps=5,
        save_strategy="epoch",
        bf16=True,
        max_seq_length=1024,
        dataset_text_field="text",
        gradient_checkpointing=True,
    )

    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        args=training_config,
        processing_class=tokenizer,
    )

    print("Starting training...")
    trainer.train()

    print(f"Saving model to {OUTPUT_DIR}...")
    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)

    print("Training complete!")


if __name__ == "__main__":
    main()
