# train a LSTM-ATT model, adapted from https://github.com/gao-g/metaphor-in-context
# todo: before using this script, you have to pre-compute ELMo embeddings:
# !allennlp elmo path_to_train_file train.hdf5 --average --use-sentence-keys

import csv
import os

import h5py
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
from lstm_att_model import RNNSequenceClassifier
from torch.autograd import Variable
from torch.utils.data import DataLoader
from lstm_att_utils import TextDatasetWithGloveElmo as TextDataset
from lstm_att_utils import evaluate, et_num_lines, get_vocab, embed_sequence, get_word2idx_idx2word, get_embedding_matrix

# load and preprocess data
def load_preprocess_data(path, filename):
    raw_data = []
    with open(os.path.join(path, filename), encoding='latin-1') as f:
        lines = csv.reader(f)
        next(lines)
        for line in lines:
            raw_data.append([line[0], int(line[1])])
    return draw_data


# computes glove embeddings and concatenates glove and pre-computed elmo embeddings and set up dataloader
def compute_emb(args, raw_train, raw_val, raw_test):
    vocab = get_vocab(raw_train + raw_val + raw_test)
    # two dictionaries. <PAD>: 0, <UNK>: 1
    word2idx, idx2word = get_word2idx_idx2word(vocab)
    # glove_embeddings a nn.Embeddings
    glove_embeddings = get_embedding_matrix(os.path.join(args.glove_emb_path, "glove840B300d.txt"), word2idx, idx2word,
                                            normalization=False)
    # elmo_embeddings
    elmo_train = h5py.File(os.path.join(args.elmo_emb_path, 'train.hdf5'), 'r')
    elmo_val = h5py.File(os.path.join(args.elmo_emb_path, 'val.hdf5'), 'r')
    elmo_test = h5py.File(os.path.join(args.elmo_emb_path, 'test.hdf5'), 'r')

    embedded_train = [[embed_sequence(example[0], word2idx,
                                      glove_embeddings, elmo_train), example[1]]
                      for example in raw_train]
    embedded_val = [[embed_sequence(example[0], word2idx,
                                    glove_embeddings, elmo_val), example[1]]
                    for example in raw_val]
    embedded_test = [[embed_sequence(example[0], word2idx,
                                     glove_embeddings, elmo_test), example[1]]
                     for example in raw_test]

    # Separate the input (embedded_sequence) and labels in the indexed train sets.
    train_dataset = TextDataset([example[0] for example in embedded_train],
                                [example[1] for example in embedded_train])
    val_dataset = TextDataset([example[0] for example in embedded_val],
                              [example[1] for example in embedded_val])
    test_dataset = TextDataset([example[0] for example in embedded_test],
                               [example[1] for example in embedded_test])

    # Set up a DataLoader for the training, validation, and test dataset
    train_dataloader = DataLoader(dataset=train_dataset, batch_size=args.batch_size, shuffle=True,
                                  collate_fn=TextDataset.collate_fn)
    val_dataloader = DataLoader(dataset=val_dataset, batch_size=args.batch_size,
                                collate_fn=TextDataset.collate_fn)
    test_dataloader = DataLoader(dataset=test_dataset, batch_size=args.batch_size,
                                 collate_fn=TextDataset.collate_fn)

    return train_dataloader, val_dataloader, test_dataloader


# train and evaluate model
def train_eval(args, train_dataloader, val_dataloader, test_dataloader):
    # Instantiate the model
    # embedding_dim = glove + elmo
    # dropout1: dropout on input to RNN
    # dropout2: dropout in RNN; would be used if num_layers=1
    # dropout3: dropout on hidden state of RNN to linear layer
    rnn_clf = RNNSequenceClassifier(num_classes=2, embedding_dim=300 + 1024, hidden_size=300, num_layers=1, bidir=True,
                                    dropout1=args.dropout, dropout2=args.dropout, dropout3=args.dropout)
    # Move the model to the GPU if available
    if args.using_GPU:
        rnn_clf = rnn_clf.cuda()
    # Set up criterion for calculating loss
    nll_criterion = nn.NLLLoss()
    # Set up an optimizer for updating the parameters of the rnn_clf
    rnn_clf_optimizer = optim.SGD(rnn_clf.parameters(), lr=args.lr, momentum=0.9)

    # train
    val_loss = []
    val_f1 = []
    num_iter = 0
    for epoch in range(args.epochs):
        print("Starting epoch {}".format(epoch + 1))
        for (example_text, example_lengths, labels) in train_dataloader:
            example_text = Variable(example_text)
            example_lengths = Variable(example_lengths)
            labels = Variable(labels)
            if args.using_GPU:
                example_text = example_text.cuda()
                example_lengths = example_lengths.cuda()
                labels = labels.cuda()
            # predicted shape: (batch_size, 2)
            predicted = rnn_clf(example_text, example_lengths)
            batch_loss = nll_criterion(predicted, labels)
            rnn_clf_optimizer.zero_grad()
            batch_loss.backward()
            rnn_clf_optimizer.step()
            num_iter += 1
            # Calculate validation and training set loss and accuracy every 200 gradient updates
            if num_iter % 200 == 0:
                avg_eval_loss, eval_accuracy, precision, recall, f1, fus_f1 = evaluate(val_dataloader, rnn_clf,
                                                                                       nll_criterion, args.using_GPU)
                val_loss.append(avg_eval_loss)
                val_f1.append(f1)
                print(
                    "Iteration {}. Validation Loss {}. Validation Accuracy {}. Validation Precision {}. Validation Recall {}. Validation F1 {}. Validation class-wise F1 {}.".format(
                        num_iter, avg_eval_loss, eval_accuracy, precision, recall, f1, fus_f1))
                # avg_eval_loss, eval_accuracy, precision, recall, f1, fus_f1 = evaluate(train_dataloader, rnn_clf,
                #                                                                        nll_criterion, args.using_GPU)
    print("Training done!")

    # evaluate the model
    avg_eval_loss, eval_accuracy, precision, recall, f1, fus_f1 = evaluate(test_dataloader, rnn_clf,
                                                                           nll_criterion, args.using_GPU)
    print("Test Accuracy {}. Test Precision {}. Test Recall {}. Test F1 {}. Test class-wise F1 {}.".format(
        eval_accuracy, precision, recall, f1, fus_f1))


def parse_arguments():
    parser = argparse.ArgumentParser(description='Fine-tuning a BERT/Roberta model for sequence tagging',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-l', '--max_len', type=int, default=256, help='max length of input sequence')
    parser.add_argument('-b', '--batch_size', type=int, default=8, help='batch size')
    parser.add_argument('-e', '--epochs', type=int, default=3, help='number of training epochs')
    parser.add_argument('-r', '--lr', type=float, default=5e-5, help='learning rate')
    parser.add_argument('-d', '--dropout', type=float, default=0.1, help='dropout ratio')
    parser.add_argument('--path', type=str, default='', help='path of data (train, test, val files)')
    parser.add_argument('--test_path', type=str, default='', help='path of test file')
    parse.add_argument('--elmo_emb_path', type=str, default='',
                       help='path of pre-computed elmo embeddings for train test and validation data')
    parse.add_argument('--glove_emb_path', type=str, default='', help='path of glove embeddings')
    parser.add_argument('--using_GPU', action='store_true', help='activate to use GPU')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    train = load_preprocess_data(args.path, "train.csv")
    val = load_preprocess_data(args.path, "val.csv")
    test = load_preprocess_data(args.path, "test.csv")
    emb_train, emb_val, emb_test = compute_emb(args, train, val, test)
    train_eval(args, train, val, emb_train, emb_val, emb_test)
