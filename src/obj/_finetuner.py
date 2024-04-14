import torch
from transformers import LlamaForCausalLM, LlamaTokenizer, default_data_collator, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import load_dataset
from pathlib import Path
import json
from datetime import datetime
from peft import get_peft_model, LoraConfig, TaskType
from transformers import TrainerCallback
from contextlib import nullcontext

"""
Tuning Logic from https://github.com/jstonge/kitty-llama/
"""

class FineTuner:
  def __init__(self, model_filepath = '', data_filepath = '', prompt = '', format = '', output_path = '', training_params:dict = {}):
    self.model_filepath = model_filepath
    self.data_filepath = data_filepath
    self.prompt = prompt
    self.format = format
    self.training_params = training_params
    self.output_path = output_path

  def load_model(self, model_filepath):
    tokenizer = LlamaTokenizer.from_pretrained(model_filepath)
    model = LlamaForCausalLM.from_pretrained(model_filepath, device_map='auto', torch_dtype=torch.float16)
    return model, tokenizer
  
  def split_data(self, data_filepath, train_test_split_ratio = 0.5):
    dataset = load_dataset('json', data_files=data_filepath)
    dataset = dataset['train'].train_test_split(test_size=train_test_split_ratio, seed=42, shuffle=True)
    return dataset
  
  def formatting_func(self, example, format_str):
    text = f"""<s>[INST] <<SYS>> {self.prompt} <</SYS>>

    ```{example['input']}``` 
    {format_str} [/INST] {example['output']}
    """
    return text
  
  def generate_and_tokenize_prompt(self, prompt, tokenizer, formatting_func, format_str):
    return tokenizer(formatting_func(prompt, format_str))
  
  def initialize_training(self, model):
    peft_config = LoraConfig(
          task_type=TaskType.CAUSAL_LM,
          inference_mode=False,
          r=256, # tune this
          lora_alpha=512, # and this
          lora_dropout=0.05,
          # the target modules can also be tuned
          target_modules=[
          "q_proj",
          "k_proj",
          "v_proj",
          "o_proj",
          "gate_proj",
          "up_proj",
          "down_proj",
          "lm_head",
        ]
      )
    model = get_peft_model(model, peft_config)
    model.print_trainable_parameters()

      # also tune-able
    config = {
        'lora_config': peft_config,
        'learning_rate': self.training_params['learning_rate'],
        'num_train_epochs': self.training_params['num_train_epochs'],
        'gradient_accumulation_steps': 1,
        'per_device_train_batch_size': 1,
        'gradient_checkpointing': True,
    }
    self.enable_profiler = False
    # Set up profiler, and connect to wandb.ai
    if self.enable_profiler:
        wait, warmup, active, repeat = 1, 1, 2, 1
        total_steps = (wait + warmup + active) * (1 + repeat)
        schedule =  torch.profiler.schedule(wait=wait, warmup=warmup, active=active, repeat=repeat)
        profiler = torch.profiler.profile(
            schedule=schedule,
            on_trace_ready=torch.profiler.tensorboard_trace_handler(f"{self.output_path}/logs/tensorboard"),
            record_shapes=True,
            profile_memory=True,
            with_stack=True)
        
        class ProfilerCallback(TrainerCallback):
            def __init__(self, profiler):
                self.profiler = profiler
                
            def on_step_end(self, *args, **kwargs):
                self.profiler.step()

        self.profiler_callback = ProfilerCallback(profiler)
    else:
        profiler = nullcontext()
    return model, config, profiler
  
  def train_model(self, model, profiler, tokenized_train_dataset, tokenized_validate_dataset, tokenizer, config, total_steps):
     # Define training args
    training_args = TrainingArguments(
        output_dir=self.output_path,
        overwrite_output_dir=True,
        fp16=True,  # Use BF16 if available
        # logging strategies
        logging_dir=f"{self.output_path,}/logs",
        logging_strategy="steps",
        logging_steps=10,
        save_strategy="no",
        evaluation_strategy="steps",
        eval_steps=10,
        optim="adamw_torch_fused",
        max_steps=total_steps if self.enable_profiler else -1,
        **{k:v for k,v in config.items() if k != 'lora_config'}
    )

    with profiler:
        # Create Trainer instance
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_train_dataset,
            eval_dataset= tokenized_validate_dataset,
            data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
            callbacks=[self.profiler_callback] if self.enable_profiler else [],
        )
        # Start training
        trainer.train()

    return model

  def save_model(self, model, tokenizer):
    model = model.merge_and_unload()
    # save the model
    model.save_pretrained(self.output_path)
    tokenizer.save_pretrained(self.output_path)

  def run(self):
    model, tokenizer = self.load_model(self.model_filepath)
    dataset = self.split_data(self.data_filepath, self.training_params['train_test_split_ratio'])
    tokenized_train_dataset = dataset["train"].map(self.generate_and_tokenize_prompt)
    tokenized_validate_dataset = dataset["test"].map(self.generate_and_tokenize_prompt)

    tokenizer.pad_token = tokenizer.eos_token
    model.gradient_checkpointing_enable()

    model, config, profiler  = self.initialize_training(model)

    model = self.train_model(model, profiler, tokenized_train_dataset, tokenized_validate_dataset, tokenizer, config, self.training_params['total_steps'])

    self.save_model(model, tokenizer)


