import ast
import os
import re
import zipfile

import hdbscan
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
import requests
import seaborn as sns
import spacy
import umap
from ivis import Ivis
from nltk.corpus import stopwords
from scipy import stats
from sentence_transformers import SentenceTransformer
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from spacy_wordnet.wordnet_annotator import WordnetAnnotator  # must be imported for pipe creation
import collections


# todo: add topic modelling from notebook

# load and preprocess data data
def load_and_preprocess(args):
    data = pd.read_csv(args.path, sep="\t")
    data.fillna("", inplace=True)
    data = data[data["modifier"] != ""]
    data_pos = data[data["label"] == 1]
    return data_pos


# get all unique modifiers
def get_modifiers(data):
    modifier_unique = data_pos.modifier.drop_duplicates()
    modifier_unique = modifier_unique.reset_index(drop=True)
    return modifier_unique


# compute embeddings using sentence transformers
def compute_embeddings(mods):
    model = SentenceTransformer('all-mpnet-base-v2')
    embeddings = model.encode(mods)
    # normalization
    embeddings = preprocessing.normalize(embeddings)
    return embeddings


# computes cluster for the modifier embeddings using kmeans
def kmeans_cluster(embeddings, n):
    kmeans = KMeans(n_clusters=n, random_state=0).fit(embeddings)
    return kmeans.labels_


# computes cluster for the modifier embeddings using dbscan
def hdbscan_cluster(embeddings, min_cluster_size):
    hdbscan_cluster = hdbscan.HDBSCAN(min_cluster_size=15,
                                      metric='euclidean',
                                      cluster_selection_method='eom').fit(umap_10d_embeddings)
    return hdbscan_cluster.labels_


def reduce_dim(high_embs, name):
    if name == "tsne":
        tsne = TSNE(n_components=2, perplexity=10, random_state=6,
                    learning_rate=1000, n_iter=1500)
        tsne_emb = tsne.fit_transform(high_embs)
        reduced_embs = np.round(tsne_emb, 4)
    elif name == "pca_tsne":
        pca = PCA(n_components=50, random_state=42)
        pca_50d_emb = pca.fit_transform(high_embs)
        tsne = TSNE(n_components=2, perplexity=10, random_state=6,
                    learning_rate=1000, n_iter=1500)
        tsne_pca_emb = tsne.fit_transform(pca_50d_emb)
        reduced_embs = np.round(tsne_pca_emb, 4)
    elif name == "umap":
        umap = umap.UMAP(n_neighbors=15, n_components=2, min_dist=0.0, metric='cosine')
        umap_emb = umap.fit_transform(high_embs)
        reduced_embs = np.round(umap_emb, 4)
    elif name == "ivis":
        ivis = Ivis(k=15)
        ivis.fit(high_embs)
        ivis_emb = ivis.transform(high_embs)
        reduced_embs = np.round(ivis_emb, 4)
    return reduced_embs


# visualize reduced embeddings and differentiate clusters by color
def visualize(reduced_embs, cluster_labels):
    plt.figure(figsize=(64, 32))
    p1 = sns.scatterplot(
        x=reduced_embs[:, 0], y=reduced_embs[:, 1],
        hue=cluster_labels,
        palette=sns.color_palette("Set3", len(np.unique(cluster_labels))),
        legend=False,
        alpha=1,
        size=1000
    )
    plt.show()
    plt.savefig('modifier_clustering.svg')




# Parses command-line arguments.
def parse_arguments():
    parser = argparse.ArgumentParser(description='Fine-tuning script for sequence tagging a BERT/Roberta model',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--train_path', type=str, default='', help='path of file')
    parser.add_argument('num_clusters', type=int, default=10, help='number of clusters when applying kmeans')
    parser.add_argument('min_size', type=int, default=20,
                        help='minimal number of elements per cluster when applying hdbscan')
    parser.add_argument('--reduction_algo', type=str, default='tsne_pca',
                        help='choose which reduction algorihtm to apply')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    data = load_and_preprocess(args)
    modifier_unique = get_modifiers(data)
    modifier_embs = compute_embeddings(modifier_unique)
    labels = kmeans_cluster(modifier_embs, args.num_clsuters)
    reduced_embeddings = (reduce_dim
                          (modifier_embs, args.reduction_algo))
    visualize(reduced_embs, labels)
