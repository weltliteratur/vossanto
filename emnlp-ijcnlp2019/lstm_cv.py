# crowdsourcing


# ignore all warnings
import warnings

warnings.filterwarnings("ignore")
# imports
import nltk

from gensim.models import KeyedVectors
import re
import numpy
import keras
from keras.regularizers import l2
from keras.callbacks import *
from keras.models import *
from keras.optimizers import *
from keras.utils.np_utils import to_categorical
from keras.layers.core import *
from keras.layers import Input, Embedding, LSTM, Dense, Bidirectional
from keras.preprocessing.sequence import pad_sequences
from keras import backend as K
from keras import metrics

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.test.utils import get_tmpfile

# files,
vossantos_file = "cd_wd_bl_lstm.tsv"
glove_file = "glove.6B.100d.txt"
# prediction_file=" "
# prediction_file_2=" "
# convert the GloVe file format to the word2vec file format.
word_embeddings_file = get_tmpfile("glove_word2vec.txt")
glove2word2vec(glove_file, word_embeddings_file)

# selects sentences out of file
def preprocess_prediction_file(file_path):
    with open(file_path, "r") as file:
        reader = csv.reader(file, delimiter="\t")
        sents = [line[0] for line in reader]
        return sents


# read input data (vossanto file)
def read_file(file_path):
    with open(file_path) as tsvfile:
        reader = csv.reader(tsvfile, delimiter="\t")
        reader = list(reader)
    return reader


# preprocess train and test data
vossantos = read_file(vossantos_file)
# prediction_set=preprocess_prediction_file(prediction_file)
# prediction_set_2=preprocess_prediction_file(prediction_file_2)
# print(prediction_set)
print("data size: ", len(vossantos))
# print("prediction set size: ",len(prediction_set))

# read pre-trained word vectors (puts vocabularity from glove to the dict vocab_v2w and to vocab_w2v (same dict, but key and value changed)
word2vec = KeyedVectors.load_word2vec_format(word_embeddings_file, binary=False)
vocab_v2w = {}
vocab_w2v = {key: idx + 1 for idx, key in enumerate(word2vec.vocab)}
vocab_w2v["UNK"] = 0
for key in vocab_w2v:
    vocab_v2w[vocab_w2v[key]] = key

X = []
y = []
true = []
false = []

for text, label in vossantos:
    # parts = v.split("\t")
    # text = parts[0]
    # label = parts[1]
    text = text.lower().strip()
    text = re.sub("[^0-9a-zA-Z ]+", "", text)
    statement_text = text.split(" ")
    X_inst = []
    for word in statement_text:
        if word not in vocab_w2v:
            X_inst.append(vocab_w2v["UNK"])
        else:
            X_inst.append(vocab_w2v[word])
    # add the label of the instance
    if label == "True":
        y.append(1)
        true.append(X_inst)
    elif label == "False":
        y.append(0)
        false.append(X_inst)
    else:
        continue  # for cases without a label
    X.append(X_inst)

# X_predict=[]
# for sent in prediction_set:
#     sent=sent.lower()
#     sent= re.sub('[^0-9a-zA-Z ]+', '', sent)
#     statement_text = sent.split(' ')
#     X_inst_p = []
#     for word in statement_text:
#         if word not in vocab_w2v:
#             X_inst_p.append(vocab_w2v['UNK'])
#         else:
#             X_inst_p.append(vocab_w2v[word])
#     X_predict.append(X_inst_p)


print("Number of true vossantos: " + str(len(true)))
print("Number of false vossantos: " + str(len(false)))
print(
    "Accuracy of ZeroR-Classifier: " + str(100 * len(false) / (len(true) + len(false)))
)

# encode data, pad sequences to max length in data (data has to be the same length)
# max_len = 500
max_len = max(len(x) for x in X)
num_classes = 2
X = pad_sequences(X, maxlen=max_len, value=vocab_w2v["UNK"], padding="pre")
# X_predict = pad_sequences(X_predict, maxlen=max_len, value=vocab_w2v['UNK'], padding='pre')
from sklearn.preprocessing import LabelBinarizer


encoder = LabelBinarizer()
# split data into train and test data
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)
# y_train = encoder.fit_transform(y_train)
# y_test = encoder.fit_transform(y_test)
# print(len(X_train),len(y_train),len(X_test),len(y_test),len(X_predict))

y_train = encoder.fit_transform(y)
# X_test_list=X_test.tolist()
# X_list=X.tolist()
# X_test_indexes=[X_list.index(sent) for sent in X_test_list]

X_train = X

# create embedding matrix
emb_dim = 100  # length of the word vectors
embeddings = 1 * np.random.randn(len(vocab_v2w) + 1, emb_dim)  # initializing matrix
embeddings[0] = 0  # So that the padding will be ignored
for index, word in vocab_v2w.items():
    if word in word2vec.vocab:
        embeddings[index] = word2vec.word_vec(word)[:emb_dim]

print("length of vocab: ", len(vocab_v2w))
print("embedding matrix size: ", len(embeddings))
print("max length: ", max_len)


# set hyper-parameters
lstm_units = 300
epochs = 80
batch_size = 128
dropout_rate = 0.25


######################################################################### Cross validation ################################################################
# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)

from sklearn.model_selection import StratifiedKFold

# define 5-fold cross validation test harness
kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
cvscores = []
prec_scores = []
recall_scores = []
f1_scores = []
acc_scores = []
for train, test in kfold.split(X_train, y_train):
    ######################################################################### Cross validation end ################################################################
    # build model
    main_input = Input(shape=(max_len,), dtype="int32", name="main_input")
    tensor = Embedding(
        len(embeddings),
        emb_dim,
        weights=[embeddings],
        input_length=max_len,
        trainable=True,
    )(
        main_input
    )  # set trainable to False?
    tensor = Bidirectional(LSTM(lstm_units, return_sequences=True))(tensor)
    tensor = Dropout(dropout_rate)(tensor)  # counter overfitting
    tensor = Flatten()(tensor)
    output = Dense(1, activation="sigmoid")(tensor)  # decide final label
    model = Model(input=main_input, output=output)
    model.compile(loss="binary_crossentropy", optimizer=Adam(), metrics=["acc"])
    model.summary()

    ######################################################################### Cross validation ################################################################
    # train model
    model.fit(
        X_train[train],
        y_train[train],
        epochs=epochs,
        batch_size=batch_size,
        validation_split=0.1,
    )

    # evaluate model
    scores = model.evaluate(X_train[test], y_train[test], verbose=0)
    tests = model.predict(X_train[test])
    tests = [[1] if y[0] >= 0.5 else [0] for y in tests]
    conf_matrix = confusion_matrix(y_train[test], tests)
    true_pos = conf_matrix[1][1]
    true_neg = conf_matrix[0][0]
    false_pos = conf_matrix[0][1]
    false_neg = conf_matrix[1][0]
    precision_bias = true_pos / float((true_pos + false_pos))
    acc_bias = (true_pos + true_neg) / (true_pos + true_neg + false_pos + false_neg)
    print("Accuracy testset=%.3f " % acc_bias)

    print("Precision testset=%.3f" % precision_bias)

    recall_bias = true_pos / float((true_pos + false_neg))
    print("Recall testsetl=%.3f" % recall_bias)

    f1 = 2 * (precision_bias * recall_bias) / (precision_bias + recall_bias)
    print("F1=%.3f" % f1)
    print(
        "Accuracy of ZeroR-Classifier: "
        + str(100 * len(false) / (len(true) + len(false)))
    )
    prec_scores.append(precision_bias * 100)
    recall_scores.append(recall_bias * 100)
    f1_scores.append(f1 * 100)
    acc_scores.append(acc_bias * 100)
    cvscores.append(scores[1] * 100)

print("%.2f%% (+/- %.2f%%)" % (numpy.mean(cvscores), numpy.std(cvscores)))
print("%.2f%% (+/- %.2f%%)" % (numpy.mean(acc_scores), numpy.std(acc_scores)))
print("%.2f%% (+/- %.2f%%)" % (numpy.mean(prec_scores), numpy.std(prec_scores)))
print("%.2f%% (+/- %.2f%%)" % (numpy.mean(recall_scores), numpy.std(recall_scores)))
print("%.2f%% (+/- %.2f%%)" % (numpy.mean(f1_scores), numpy.std(f1_scores)))
######################################################################### Cross validation end ################################################################

# test model
# scores = model.evaluate(X_test, y_test, verbose=0)
# tests = model.predict(X_test)
# tests = [[1] if y[0] >= 0.5 else [0] for y in tests]
# X_test_indexes
# output="testdata.tsv"
# with open(output,"w") as output_file:
#     writer = csv.writer(output_file, delimiter='\t', quoting=csv.QUOTE_ALL)
#     for i in range(len(tests)):
#         writer.writerow([vossantos[X_test_indexes[i]], tests[i],y_test[i]])

# conf_matrix = confusion_matrix(y_test, tests)
# print(len(X_predict))
# print(len(X_predict[0]))
# predictions = model.predict(X_predict)
# predictions_2 = model.predict(X_predict_2)
# count=0
# predictions = [[1] if y[0] >= 0.5 else [0] for y in predictions]
# predictions_2 = [[1] if y[0] >= 0.5 else [0] for y in predictions_2]
# count_true=0
# count_false=0
#
# # predict new data
# output="prediction_data.tsv"
# with open(output,"w") as output_file:
#     writer = csv.writer(output_file, delimiter='\t', quoting=csv.QUOTE_ALL)
#     for i in range(len(predictions)):
#         writer.writerow([prediction_set[i],predictions[i]])
#         if predictions[i]==[1]:
#             count_true+=1
#         else:
#             count_false += 1
#     for i in range(len(prediction_set_2)):
#         writer.writerow([prediction_set_2[i],predictions_2[i]])
#         if predictions_2[i]==[1]:
#             count_true+=1
#         else:
#             count_false += 1
#
# print("# 'true' in predictionsets: ",count_true)
# print("# 'false' in predictionsets: ",count_false)


# evaluation of test data set
# print("conf_matrix:")
# print (conf_matrix)
#
# true_pos = conf_matrix[1][1]
# true_neg = conf_matrix[0][0]
# false_pos = conf_matrix[0][1]
# false_neg = conf_matrix[1][0]
#
# precision_bias = true_pos / float((true_pos + false_pos))
# acc_bias=(true_pos+true_neg)/(true_pos+true_neg+false_pos+false_neg)
# print("Accuracy testset=%.3f " % acc_bias)
#
# print('Precision testset=%.3f' % precision_bias)
#
# recall_bias = true_pos / float((true_pos + false_neg))
# print('Recall testsetl=%.3f' % recall_bias)
#
# f1 = 2 * (precision_bias * recall_bias) / (precision_bias + recall_bias)
# print ('F1=%.3f' % f1)
# print("Accuracy of ZeroR-Classifier: "+str(100*len(false)/(len(true)+len(false))))
