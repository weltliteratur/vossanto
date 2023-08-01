# Script for fine-tuning a pre-trained LM (BERT/RoBERTa) for a sequence tagging task


import argparse
import ast
import os
import pickle

import evaluate
import numpy as np
import pandas as pd
from datasets import Dataset, DatasetDict
from transformers import AutoModelForTokenClassification, TrainingArguments, Trainer, AutoConfig
from transformers import AutoTokenizer
from transformers import DataCollatorForTokenClassification


# tokenize and align labels with respect to tokens
def tokenize_and_align_labels(examples):
    tokenized_inputs = tokenizer(examples["tokens"], truncation=True, is_split_into_words=True)
    labels = []
    for i, label in enumerate(examples["tags"]):
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        previous_word_idx = None
        label_ids = []
        # Set the special tokens to -100.
        for word_idx in word_ids:
            if word_idx is None:
                label_ids.append(-100)
            # Only label the first token of a given word.
            elif word_idx != previous_word_idx:
                label_ids.append(label[word_idx])

            else:
                label_ids.append(-100)
            previous_word_idx = word_idx
        labels.append(label_ids)
    tokenized_inputs["labels"] = labels
    return tokenized_inputs


# compute precision, recall, score and accuracy
def compute_metrics(p):
    predictions, labels = p
    predictions = np.argmax(predictions, axis=2)

    true_predictions = [
        [label_list[p] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]
    true_labels = [
        [label_list[l] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]

    results = seqeval.compute(predictions=true_predictions, references=true_labels)
    return {
        "precision": results["overall_precision"],
        "recall": results["overall_recall"],
        "f1": results["overall_f1"],
        "accuracy": results["overall_accuracy"],
    }


# train and evaluate model
def train_evaluate(args):
    config = AutoConfig.from_pretrained(
        "bert-base-cased",
        hidden_dropout_prob=args.dropout,
        attention_probs_dropout_prob=args.dropout,
        num_labels=len(label_list),
        id2label=id2label,
        label2id=label2id
    )
    model = AutoModelForTokenClassification.from_pretrained(
        "bert-base-cased", config=config)

    training_args = TrainingArguments(
        output_dir="models/bert_seq/",
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
        data_collator=data_collator,
        compute_metrics=compute_metrics,
    )
    trainer.train()
    evaluation_results = trainer.evaluate()
    prediction_results = trainer.predict(tokenized_data["test"])
    out_path = args.test_path.replace("data", "models")
    os.makedirs(out_path, exist_ok=True)
    with open(f"{out_path}/eval_results.pkl",
              "wb") as file:
        pickle.dump(evaluation_results, file)
    with open(f"{out_path}/pred_results.pkl",
              "wb") as file:
        pickle.dump(prediction_results.predictions, file)


# Parses command-line arguments.
def parse_arguments():
    parser = argparse.ArgumentParser(description='Fine-tuning script for sequence tagging a BERT/Roberta model',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-l', '--max_len', type=int, default=256, help='max length of input sequence')
    parser.add_argument('-b', '--batch_size', type=int, default=8, help='batch size')
    parser.add_argument('-e', '--epochs', type=int, default=3, help='number of training epochs')
    parser.add_argument('-r', '--lr', type=float, default=5e-5, help='learning rate')
    parser.add_argument('-d', '--dropout', type=float, default=0.1, help='dropout ratio')
    parser.add_argument('--train_path', type=str, default='', help='path of train file')
    parser.add_argument('--test_path', type=str, default='', help='path of test file')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    label_list = [
        "O",
        "B-SRC",
        "I-SRC",
    ]

    id2label = {i: k for i, k in zip(range(len(label_list)), label_list)}
    label2id = {k: i for (i, k) in id2label.items()}

    train_df = pd.read_csv(args.train_path, sep="\t")
    # train_df["tags"] = train_df.tags.apply(ast.literal_eval)
    train_df["tags"] = train_df.tags.apply(lambda x: [label2id[t] for t in x])
    train_df["tokens"] = train_df.tokens.apply(ast.literal_eval)

    test_df = pd.read_csv(args.test_path, sep="\t")
    # test_df["tags"] = test_df.tags.apply(ast.literal_eval)
    test_df["tags"] = test_df.tags.apply(lambda x: [label2id[t] for t in x])
    test_df["tokens"] = test_df.tokens.apply(ast.literal_eval)

    # Convert the dataframes to HuggingFace datasets (dicts)
    train_dataset = Dataset.from_pandas(train_df)
    test_dataset = Dataset.from_pandas(test_df)
    dataset_dict = DatasetDict({"train": train_dataset, "test": test_dataset})

    tokenizer = AutoTokenizer.from_pretrained("bert-base-cased", max_length=args.max_len, padding="max_length",
                                              truncation=True)

    tokenized_data = dataset_dict.map(tokenize_and_align_labels, batched=True)
    data_collator = DataCollatorForTokenClassification(tokenizer=tokenizer)

    seqeval = evaluate.load("seqeval")

    train_evaluate(args)
