# Script for fine-tuning a pre-trained LM (BERT/RoBERTa) for binary classification


import argparse
import os
import pickle

import numpy as np
import pandas as pd
from datasets import Dataset, DatasetDict
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer, AutoConfig
from transformers import AutoTokenizer


# compute precision, recall, score and accuracy
def compute_metrics(p):
    logits, labels = p
    preds = np.argmax(logits, axis=-1)
    return {
        "accuracy": accuracy_score(labels, preds),
        "precision": precision_score(labels, preds),
        "recall": recall_score(labels, preds),
        "f1": f1_score(labels, preds),
    }


# Parses command-line arguments.
def parse_arguments():
    parser = argparse.ArgumentParser(description='Fine-tuning a BERT/Roberta model for binary classification',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-l', '--max_len', type=int, default=256, help='max length of input sequence')
    parser.add_argument('-b', '--batch_size', type=int, default=8, help='batch size')
    parser.add_argument('-e', '--epochs', type=int, default=3, help='number of training epochs')
    parser.add_argument('-r', '--lr', type=float, default=5e-5, help='learning rate')
    parser.add_argument('-d', '--dropout', type=float, default=0.1, help='dropout ratio')
    parser.add_argument('--train_path', type=str, default='', help='path of train file')
    parser.add_argument('--test_path', type=str, default='', help='path of test file')
    return parser.parse_args()


# Tokenize data.
def tokenize_data(examples):
    tokenized_inputs = tokenizer(examples["text"], truncation=True, max_length=args.max_len, padding="max_length")
    return tokenized_inputs


# train and evaluate model
def train_evaluate(args):
    # Config and model setup
    config = AutoConfig.from_pretrained("bert-base-cased", num_labels=2)
    model = AutoModelForSequenceClassification.from_pretrained("bert-base-cased", config=config)

    training_args = TrainingArguments(
        output_dir="models/bert_clf/",
        learning_rate=args.lr,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=16,
        num_train_epochs=args.epochs,
        overwrite_output_dir=True,
        seed=42,
        save_steps=1000000,
        report_to=None
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_data["train"],
        eval_dataset=tokenized_data["test"],
        tokenizer=tokenizer,
        compute_metrics=compute_metrics,
    )

    trainer.train()
    evaluation_results = trainer.evaluate()
    prediction_results = trainer.predict(tokenized_data["test"])
    out_path = args.test_path.replace("data", "models")
    os.makedirs(out_path, exist_ok=True)
    with open(f"{out_path}/eval_results.pkl", "wb") as file:
        pickle.dump(evaluation_results, file)
    with open(f"{out_path}/pred_results.pkl", "wb") as file:
        pickle.dump(prediction_results.predictions, file)


if __name__ == '__main__':
    args = parse_arguments()

    train_df = pd.read_csv(args.train_path)
    test_df = pd.read_csv(args.test_path)

    # Convert the dataframes to HuggingFace datasets
    train_dataset = Dataset.from_pandas(train_df)
    test_dataset = Dataset.from_pandas(test_df)
    dataset_dict = DatasetDict({"train": train_dataset, "test": test_dataset})

    tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")

    tokenized_data = dataset_dict.map(tokenize_data, batched=True)

    train_evaluate(args)
