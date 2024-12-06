from django.shortcuts import render
import os
import requests
from sklearn.neural_network import MLPClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import cosine
import json
from django.http import HttpResponse
import PyPDF2
from io import BytesIO
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


lemmatizer = WordNetLemmatizer()
not_words = ['.', ',', ':', ';', "'", "'s", "'m", '?', '!', '-', '«', '»', '–', '—', '(', ')', '[', ']']

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read().lower().replace('\n', '')
    return text

english_text = read_file(os.path.abspath('search_system_app/train_texts/english.txt'))
russian_text = read_file(os.path.abspath('search_system_app/train_texts/russian.txt'))

def freq_profile(text):
    lemmatized_words = [lemmatizer.lemmatize(word) for word in word_tokenize(text) if not (word in not_words)]
    fdist = FreqDist(lemmatized_words)
    print(fdist)
    frequent_words = dict(fdist.most_common(20))
    print('frequent_words ', frequent_words)
    for word in frequent_words.keys():
        frequent_words[word] = frequent_words[word]/len(lemmatized_words)
    print('probabilities ', frequent_words)
    return frequent_words

def short_profile(text):
    lemmatized_words = [lemmatizer.lemmatize(word) for word in word_tokenize(text) if (not (word in not_words) and len(word) <= 5)]
    frequent_words = FreqDist(lemmatized_words)
    print('frequent_words short 1', frequent_words)
    frequent_words = {word: count for word, count in frequent_words.items() if count > 3}
    print('frequent_words short 2', frequent_words)
    for word in frequent_words.keys():
        frequent_words[word] = frequent_words[word]/len(lemmatized_words)
    return frequent_words

english_freq_profile = freq_profile(english_text)
russian_freq_profile = freq_profile(russian_text)
english_short_profile = short_profile(english_text)
russian_short_profile = short_profile(russian_text)

def calculate_probability(english_profile, russian_profile, doc_text):
    doc_words = [lemmatizer.lemmatize(word) for word in word_tokenize(doc_text) if not (word in not_words)]
    english_probability = compare_text(english_profile, doc_words)
    russian_probability = compare_text(russian_profile, doc_words)
    if english_probability > russian_probability: lang = 'English'
    else: lang = 'Russian'
    return english_probability, russian_probability, lang
    
def compare_text(profile, text_words):
    probability = 0
    for profile_word, profile_probability in profile.items():
        if profile_word in text_words:
            text_probability = text_words.count(profile_word) / len(text_words)
            probability += freqality(profile_probability, text_probability)
    return probability / len(profile)
            
def freqality(probability1, probability2):
    bigger = max(probability1, probability2)
    smaller = min(probability1, probability2)
    return smaller / bigger

def train_model():
    texts = [english_text, russian_text]
    labels = ['English', 'Russian']
    
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)
    print('vectorized text ', X)
    
    model = MLPClassifier(max_iter=1000)
    model.fit(X, labels)
    
    return model, vectorizer

def predict_language(text, model, vectorizer):
    text_vector = vectorizer.transform([text]).toarray().flatten()
    prediction = model.predict([text_vector])
    
    english_vector = vectorizer.transform([english_text]).toarray().flatten()
    russian_vector = vectorizer.transform([russian_text]).toarray().flatten()
    
    english_distance = cosine(text_vector, english_vector)
    russian_distance = cosine(text_vector, russian_vector)
    
    return prediction[0], english_distance, russian_distance

def language_recognition(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        text = read_pdf(url)
        model, vectorizer = train_model()
        predicted_language, cos_english, cos_russian = predict_language(text, model, vectorizer)
        
        freq_english, freq_russian, freq_lang = calculate_probability(english_freq_profile, russian_freq_profile, text)
        short_english, short_russian, short_lang = calculate_probability(english_short_profile, russian_short_profile, text)
        results = {'Frequent words method': [freq_english, freq_russian, freq_lang], 'Short words method': [short_english, short_russian, short_lang], 'Neural network method': [cos_english, cos_russian, predicted_language]}

        results_for_download = {'Frequent words method': {'English probability metric': freq_english, 'Russian probability metric': freq_russian, 'Language of the text':freq_lang}, 'Short words method': {'English probability metric': short_english, 'Russian probability metric': short_russian, 'Language of the text':short_lang}, 'Neural network method': {'English distance metric': cos_english, 'Russian distance metric': cos_russian, 'Language of the text':predicted_language}}
        
        request.session['results_for_download'] = results_for_download
        return render(request, 'lang_recognition.html', {'results': results, 'url': url})
    else:
        return render(request, 'lang_recognition.html')
    
def read_pdf(link):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(link, headers=headers)
    response.raise_for_status()
    pdf_file = BytesIO(response.content)

    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() 
 
    return text


def download_result_json_file(request):
    results_for_download = request.session.get('results_for_download', {})
    formatted_result = json.dumps(results_for_download, indent=4, separators=(',', ': '))
    response = HttpResponse(formatted_result, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="result.json"'
    
    return response
