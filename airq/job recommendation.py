#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors
import nltk
from nltk.corpus import wordnet
nltk.download('punkt')
nltk.download('wordnet')


def preprocess_text(df):
    """Preprocesses job descriptions by merging text fields and converting to lowercase."""
    df = df.copy()
    df[['title', 'description', 'skills_desc']] = df[['title', 'description', 'skills_desc']].astype(str)
    df['text'] = (df['title'] + ' ' + df['description'] + ' ' + df['skills_desc']).str.lower()
    return df


def expand_skills(skills):
    """Expands skills by finding synonyms using WordNet."""
    expanded_skills = set(skills.split())
    for word in skills.split():
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                expanded_skills.add(lemma.name().replace('_', ' '))
    return ' '.join(expanded_skills)


def build_bert_knn_model(df):
    """Builds a BERT-based embedding model and KNN model."""
    model = SentenceTransformer('all-MiniLM-L6-v2')
    job_embeddings = model.encode(df['text'].tolist(), convert_to_numpy=True)
    knn = NearestNeighbors(n_neighbors=10, metric='cosine', algorithm='brute', n_jobs=-1).fit(job_embeddings)
    return model, knn, job_embeddings


def get_recommendations(job_input, df, model, knn, job_embeddings, num_recommendations=5, similarity_threshold=0.35):
    """Retrieves job recommendations based on BERT embeddings and cosine similarity."""
    if df.empty:
        return None, None, None
    
    expanded_input = expand_skills(job_input.lower())
    input_embedding = model.encode([expanded_input], convert_to_numpy=True)
    distances, indices = knn.kneighbors(input_embedding)
    
    recommendations = []
    similarity_scores = 1 - distances[0]  # Convert distances to similarity scores
    
    filtered_scores = [
        round(similarity_scores[i], 4)
        for i in range(len(indices[0])) if similarity_scores[i] > similarity_threshold
    ]
    
    for i, score in zip(indices[0], filtered_scores):
        job = df.iloc[i]
        recommendations.append({
            "title": job.get('title', 'N/A'),
            "company": job.get('company_id', 'N/A'),
            "location": job.get('location', 'N/A'),
            "description": job.get('description', 'N/A')[:500] + "...",
            "work_type": job.get('formatted_work_type', 'N/A'),
            "similarity_score": score
        })
    
    mean_similarity = round(np.mean(filtered_scores), 4) if filtered_scores else 0
    median_similarity = round(np.median(filtered_scores), 4) if filtered_scores else 0
    
    return recommendations[:num_recommendations], mean_similarity, median_similarity


if __name__ == "__main__":
    try:
        file_path = r"C:\\Users\\DELL\\Downloads\\Jobs - Jobs.csv"
        df = pd.read_csv(file_path)
        df = preprocess_text(df)
        
        model, knn, job_embeddings = build_bert_knn_model(df)
        
        user_input = input("\nEnter your skills: ")
        recommendations, mean_similarity, median_similarity = get_recommendations(user_input, df, model, knn, job_embeddings)
        
        if recommendations:
            print("\n\033[1mTop Matching Jobs (Similarity > 35%):\033[0m")
            for idx, job in enumerate(recommendations, start=1):
                print(f"\n\033[1;34mJob {idx}:\033[0m")
                print("\033[1mTitle:\033[0m", job['title'])
                print("\033[1mCompany ID:\033[0m", job['company'])
                print("\033[1mLocation:\033[0m", job['location'])
                print("\033[1mWork Type:\033[0m", job['work_type'])
                print("\033[1mSimilarity Score:\033[0m", job['similarity_score'])
                print("\033[1mDescription:\033[0m", job['description'])
            
            print(f"\n\033[1;32mMean Similarity Score:\033[0m {mean_similarity}")
            print(f"\n\033[1;33mMedian Similarity Score:\033[0m {median_similarity}")
        else:
            print("\n\033[1;31mNo matching jobs found with similarity > 35%.\033[0m")
    except Exception as e:
        print("\n\033[1;31mError:\033[0m", str(e))


# In[ ]:


# Save the model
import pickle
with open('job_recc_ardra.pkl', 'wb') as file:
    pickle.dump(knn, file)

print("Model saved successfully!")

