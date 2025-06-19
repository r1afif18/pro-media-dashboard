import pandas as pd
import numpy as np
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st

def deep_sentiment_analysis(df, text_column='content'):
    # Analisis sentimen lebih mendalam
    df['sentiment_score'] = df[text_column].apply(
        lambda x: TextBlob(x).sentiment.polarity
    )
    
    # Kategorikan sentimen
    df['sentiment_category'] = pd.cut(
        df['sentiment_score'],
        bins=[-1, -0.1, 0.1, 1],
        labels=['negatif', 'netral', 'positif']
    )
    
    return df

def topic_modeling(df, text_column='content', n_topics=5):
    # Ekstrak topik dengan LDA
    vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
    tfidf = vectorizer.fit_transform(df[text_column])
    
    lda = LatentDirichletAllocation(
        n_components=n_topics,
        max_iter=5,
        learning_method='online',
        learning_offset=50.,
        random_state=0
    )
    lda.fit(tfidf)
    
    # Tampilkan topik
    feature_names = vectorizer.get_feature_names_out()
    topics = {}
    
    for topic_idx, topic in enumerate(lda.components_):
        topics[f"Topik {topic_idx+1}"] = [
            feature_names[i] for i in topic.argsort()[:-10 - 1:-1]
        ]
    
    return pd.DataFrame(topics)

def source_network_analysis(df, source_column='source'):
    # Analisis jaringan sumber berita
    G = nx.Graph()
    
    # Tambahkan node (sumber)
    sources = df[source_column].unique()
    G.add_nodes_from(sources)
    
    # Tambahkan edges berdasarkan kolaborasi (jika ada)
    # Contoh sederhana: hubungkan sumber yang sering muncul di hari yang sama
    df['date'] = pd.to_datetime(df['date'])
    df['date_str'] = df['date'].dt.date.astype(str)
    
    source_date = df.groupby([source_column, 'date_str']).size().reset_index()
    source_pairs = source_date.groupby('date_str')[source_column].apply(list)
    
    for date, sources in source_pairs.items():
        if len(sources) > 1:
            for i in range(len(sources)):
                for j in range(i+1, len(sources)):
                    if G.has_edge(sources[i], sources[j]):
                        G[sources[i]][sources[j]]['weight'] += 1
                    else:
                        G.add_edge(sources[i], sources[j], weight=1)
    
    # Visualisasi
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, k=0.5)
    nx.draw_networkx_nodes(G, pos, node_size=2000, node_color='skyblue')
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Jaringan Sumber Berita")
    plt.axis('off')
    
    return plt