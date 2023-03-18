# Data and code of our paper: "Der Frank Sinatra der Wettervorhersage": Cross-Lingual Vossian Antonomasia Extraction



## Datasets

### English datasets

- [NYT-0](nyt.org): The dataset contains more sentences since they are
  split up, such that each sentence only contains one VA. If a
  sentence contains multiple VA expressions, the sentence appears
  multiple times with different annotations in this dataset. Needs to
  be preprocessed. Also duplicate sentences from different articles
  are not removed yet.

### German datasets

- [UMBL](umblaetterer.org)
- [ZEIT](zeit.org)
- [NEG1](neg_1.txt)
- [NEG2](neg_2.txt)
- [NEG3](neg_3.txt)

## Code

* [translate.py](translate.py): translates sentences from english to german or vice versa
* [align.py](align.py): aligns tags from original sentence to translated sentence

Fine-tuning and inference is conducted using [Huggingface' transformers library](https://github.com/huggingface/transformers/tree/main/examples/pytorch/token-classification) and adapting [the example script](https://github.com/huggingface/transformers/blob/main/examples/pytorch/token-classification/run_ner.py).
