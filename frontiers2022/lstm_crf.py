# Train a bidirectional LSTM with a CRF on top using a concatenation of glove and elmo embeddings
import argparse

from flair.data import Corpus
from flair.datasets import UD_ENGLISH
from flair.embeddings import TokenEmbeddings, WordEmbeddings, StackedEmbeddings, ELMoEmbeddings
from flair.data import Corpus
from flair.datasets import ColumnCorpus
import allennlp
from flair.models import SequenceTagger
import os
from torch.optim.adam import Adam
from flair.trainers import ModelTrainer




# Parses command-line arguments.
def parse_arguments():
    parser = argparse.ArgumentParser(description='Fine-tuning a BLSTM-CRF model for sequence tagging using FLAIR',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-b', '--batch_size', type=int, default=8, help='batch size')
    parser.add_argument('-e', '--epochs', type=int, default=3, help='number of training epochs')
    parser.add_argument('-r', '--lr', type=float, default=5e-5, help='learning rate')
    parser.add_argument('--path', type=str, default='', help='path to directory that contains train and test files')
    return parser.parse_args()


def train_evaluate(args):
    tag_type = 'va'
    columns = {0: 'text', 1: 'va'}

    embedding_types = [
        WordEmbeddings('glove'),
        ELMoEmbeddings("top"),
    ]

    embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)


    corpus: Corpus = ColumnCorpus(args.path, columns,
                                  train_file='train.txt',
                                  test_file='test.txt',
                                  dev_file='dev.txt')

    tag_dictionary = corpus.make_label_dictionary(label_type=tag_type)
    tagger: SequenceTagger = SequenceTagger(hidden_size=100,
                                            embeddings=embeddings,
                                            tag_dictionary=tag_dictionary,
                                            tag_type=tag_type,
                                            use_crf=True)


    trainer: ModelTrainer = ModelTrainer(tagger, corpus)

    out_path = args.path.replace("data", "models")
    os.makedirs(out_path, exist_ok=True)
    trainer.train(base_path=out_path,
                  learning_rate=args.lr,
                  mini_batch_size=args.batch_size,
                  max_epochs=args.epochs,
                  optimizer=Adam,
                  )


if __name__ == '__main__':
    args = parse_arguments()
    train_evaluate(args)
