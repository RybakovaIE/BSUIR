import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import requests
from django.shortcuts import render
from django.http import HttpResponse
import PyPDF2
from io import BytesIO
from nltk.stem import WordNetLemmatizer
import PyPDF2
from io import BytesIO
from nltk.probability import FreqDist

nltk.download('punkt')
nltk.download('stopwords')

stop_words = stopwords.words('english') + stopwords.words('russian') + ['the']
lemmatizer = WordNetLemmatizer()
    
def auto_refereeing(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        text = read_pdf(url).replace('\n', ' ')
        abstract = get_abstract(text)
        keywords_abstract = get_keywords_abstract(text)
        results_for_download = f'abstract:\n{abstract}\n\nkeywords:\n{keywords_abstract}'
        request.session['results_for_download'] = results_for_download
        return render(request, 'auto_refereeing.html', {'abstract': abstract, 'keywords_abstract': keywords_abstract, 'url': url})
    else:
        return render(request, 'auto_refereeing.html')
    
def get_keywords_abstract(text):
    lemmatized_text = ' '.join([lemmatizer.lemmatize(word.lower()) for word in word_tokenize(text) if not (word in stop_words)])
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform([lemmatized_text])
    indices = (-X.toarray()[0]).argsort()[:10]
    keywords = [vectorizer.get_feature_names_out()[index] for index in indices]
    i = 9
    while(i >= 0):
        if keywords[i] == 'the':
            keywords.pop(i)
        i -= 1
    return ', '.join(keywords)
    
def get_abstract(text):
    sentences = get_sentences(text)
    text_freqs = FreqDist(lemmatizer.lemmatize(word.lower()) for word in word_tokenize(text))
    max_tf = max(text_freqs.values())
    pos_weights = calculate_pos_weight(sentences, len(text))
    
    weights = {}
    for sentence in sentences:
        weights[sentence[0]] = calculate_tf_idf(sentence, text_freqs, max_tf)
        print(calculate_tf_idf(sentence, text_freqs, max_tf), weights[sentence[0]])

    best_sentences = sorted(weights.items(), key=lambda x: x[1], reverse=True)[:10]
    best_sentences = [sent[0] for sent in best_sentences]
    abstract_sentences = []
    for sentence in sentences:
        if sentence[0] in best_sentences: 
            abstract_sentences.append(sentence[0])
    
    return ' '.join(abstract_sentences)

def calculate_pos_weight(sentences, chars_number):
    current_pos = 0
    pos_weights = {}
    for sentence in sentences:
        pos_weights[sentence[0]] = 1 - (current_pos / chars_number)
        current_pos += len(sentence[0])
    return pos_weights

def calculate_tf_idf(sentence, text_freq, max_tf):
    tf_idf = 0
    sent_freqs = FreqDist(sentence[1])
    for word in sentence[1]:
        tf_idf += sent_freqs[word] * 0.5*(1 + (text_freq[word])/max_tf)
    return tf_idf/len(sentence[1])

    
def get_sentences(text):
    text_sentences = sent_tokenize(text)
    sentences = []
    for sentence in text_sentences:
        words = [lemmatizer.lemmatize(word.lower()) for word in word_tokenize(sentence) if (not (word in stop_words) and not (word.isnumeric()) and word != 'the')]
        sentences.append((sentence, words))
    return sentences
    
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

def download_result_txt_file(request):
    result_for_download = request.session.get('results_for_download')
    response = HttpResponse(result_for_download, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="result.txt"'
    return response