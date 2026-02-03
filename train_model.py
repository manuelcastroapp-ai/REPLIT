#!/usr/bin/env python3
"""
Script de entrenamiento para el modelo SuperDevAgent

Este script entrena un modelo de lenguaje local avanzado especializado
en desarrollo de agentes IA, usando fine-tuning con HuggingFace.
"""

import os
import json
import torch
from torch.utils.data import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
import argparse

class SuperDevAgentDataset(Dataset):
    """Dataset personalizado para SuperDevAgent"""

    def __init__(self, data_path, tokenizer, max_length=512):
        with open(data_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]

        # Formatear el texto de entrenamiento
        instruction = item['instruction']
        input_text = item.get('input', '')
        output = item['output']

        if input_text:
            text = f"### Instruction:\n{instruction}\n\n### Input:\n{input_text}\n\n### Response:\n{output}"
        else:
            text = f"### Instruction:\n{instruction}\n\n### Response:\n{output}"

        # Tokenizar
        encodings = self.tokenizer(
            text,
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt'
        )

        return {
            'input_ids': encodings['input_ids'].flatten(),
            'attention_mask': encodings['attention_mask'].flatten(),
            'labels': encodings['input_ids'].flatten()
        }

def load_model_and_tokenizer(model_name, use_4bit=True):
    """Carga el modelo y tokenizer"""

    print(f"Cargando modelo: {model_name}")

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token

    if use_4bit:
        # Cargar en 4-bit para ahorrar memoria
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            load_in_4bit=True,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        model = prepare_model_for_kbit_training(model)
    else:
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )

    return model, tokenizer

def setup_lora_config():
    """Configura LoRA para fine-tuning eficiente"""

    lora_config = LoraConfig(
        r=16,  # Rank de LoRA
        lora_alpha=32,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],  # Atención
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )

    return lora_config

def train_model(args):
    """Función principal de entrenamiento"""

    print("🚀 Iniciando entrenamiento del SuperDevAgent...")

    # Cargar modelo y tokenizer
    model, tokenizer = load_model_and_tokenizer(args.model_name, args.use_4bit)

    # Configurar LoRA
    lora_config = setup_lora_config()
    model = get_peft_model(model, lora_config)

    print(f"Parámetros entrenables: {model.print_trainable_parameters()}")

    # Cargar dataset
    train_dataset = SuperDevAgentDataset(args.dataset_path, tokenizer, args.max_length)

    # Configurar entrenamiento
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.num_epochs,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.gradient_accumulation,
        learning_rate=args.learning_rate,
        fp16=args.use_fp16,
        logging_steps=10,
        save_steps=100,
        save_total_limit=3,
        evaluation_strategy="no",
        load_best_model_at_end=False,
        report_to="none",  # Desactivar wandb/tensorboard
        remove_unused_columns=False,
    )

    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )

    # Crear trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        data_collator=data_collator,
    )

    print("🏃‍♂️ Iniciando entrenamiento...")
    trainer.train()

    # Guardar modelo
    print(f"💾 Guardando modelo en {args.output_dir}")
    trainer.save_model(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)

    print("✅ Entrenamiento completado!")

def main():
    parser = argparse.ArgumentParser(description="Entrenar SuperDevAgent")
    parser.add_argument("--model_name", type=str, default="microsoft/DialoGPT-medium",
                       help="Modelo base para fine-tuning")
    parser.add_argument("--dataset_path", type=str, default="training_dataset.json",
                       help="Ruta al dataset de entrenamiento")
    parser.add_argument("--output_dir", type=str, default="./superdevagent_model",
                       help="Directorio de salida para el modelo entrenado")
    parser.add_argument("--num_epochs", type=int, default=3,
                       help="Número de epochs de entrenamiento")
    parser.add_argument("--batch_size", type=int, default=4,
                       help="Tamaño del batch")
    parser.add_argument("--gradient_accumulation", type=int, default=2,
                       help="Acumulación de gradientes")
    parser.add_argument("--learning_rate", type=float, default=2e-4,
                       help="Tasa de aprendizaje")
    parser.add_argument("--max_length", type=int, default=512,
                       help="Longitud máxima de secuencia")
    parser.add_argument("--use_4bit", action="store_true", default=True,
                       help="Usar cuantización 4-bit")
    parser.add_argument("--use_fp16", action="store_true", default=True,
                       help="Usar precisión mixta FP16")

    args = parser.parse_args()

    # Verificar que existe el dataset
    if not os.path.exists(args.dataset_path):
        print(f"❌ Dataset no encontrado: {args.dataset_path}")
        return

    # Crear directorio de salida
    os.makedirs(args.output_dir, exist_ok=True)

    # Entrenar modelo
    train_model(args)

if __name__ == "__main__":
    main()
