from django.shortcuts import render
from .models import Documents
from .forms import LinkForm
import requests
import PyPDF2
import nltk
import base64
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import math
from nltk.probability import FreqDist
from io import BytesIO
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import io
from django.contrib import messages
from sumy.summarizers.lsa import LsaSummarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
import numpy as np
from numpy.linalg import norm

nltk.download('punkt_tab')
nltk.download('wordnet')

docs_vectors = {}
doc_keywords = {}
doc_lemmas = []
lemmatizer = WordNetLemmatizer()

relevance_border = 0.02

def add_link(request):
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            form.save()
            doc = Documents.objects.get(link=form.cleaned_data['link'])
            text = process_link(doc.doc_id)
            doc.text = text
            doc.save()
            messages.success(request, 'The link has been added')
    else:
        form = LinkForm()
    return render(request, 'add_links.html', {'form': form})

def calculate_inverse_term_frequency(Pi):
    return math.log(Documents.objects.count() / Pi)

def process_link(doc_id):
    
    pdf_doc = Documents.objects.get(pk=doc_id)
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(pdf_doc.link, headers=headers)
    response.raise_for_status()
    pdf_file = BytesIO(response.content)

    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    
    for page in reader.pages:
        text += page.extract_text() 
 
    return text

def search_results(request):
    query = request.GET.get('query')
    returned_texts ={}
    returned_documents = {}
    summarized_docs = {}
    if query:
        query_words = [lemmatizer.lemmatize(word.lower()) for word in query.split()]
        processed_texts = {}
        docs_semilesures = {}
        update_lemmas()
        for doc in Documents.objects.all(): 
            processed_texts[doc.doc_id] = doc.text
            doc_vector = get_document_vector(doc.text)
            query_vector = get_query_vector(doc_vector, query_words)
            semilesure = calculate_similesure(doc_vector, query_vector)
            if semilesure >= relevance_border:
                docs_semilesures[Documents.objects.get(doc_id=doc.doc_id)] = semilesure
                summarized_docs[Documents.objects.get(doc_id=doc.doc_id)] = summarize_text(doc.text)
                returned_texts[doc.doc_id] = doc.text
                print(summarize_text(doc.text))
                
        returned_documents = sorted(docs_semilesures.keys(), key=docs_semilesures.get, reverse=True)
                
        request.session['documents_ids'] = [document.doc_id for document in returned_documents]
        request.session['returned_texts'] = returned_texts
        request.session['processed_texts'] = processed_texts
        request.session['search_words'] = query_words
    else:
        return render(request, 'search_results.html', {'documents': summarized_docs})
 
    return render(request, 'search_results.html', {'documents': summarized_docs, 'search_words': query_words})

def update_lemmas():
    all_docs = Documents.objects.all()
    for doc in all_docs:
        doc_lemmas.append([lemmatizer.lemmatize(word.lower()) for word in word_tokenize(doc.text)])

def get_frequencies(text):
    lemmatized_words = [lemmatizer.lemmatize(word.lower()) for word in word_tokenize(text)]
    return FreqDist(lemmatized_words)

def get_query_vector(doc_vector, query_words):
    if doc_vector == []: return []
    query_vector = []
    for word in doc_vector.keys():
        if word in query_words: query_vector.append(1)
        else: query_vector.append(0)
    return query_vector

def calculate_similesure(doc_vector, query_vector):
    if query_vector == []:
        return 0
    doc_vector = [weight for weight in doc_vector.values()]
    semilesure = np.dot(doc_vector, query_vector)/(norm(doc_vector)*norm(query_vector))
    print(f'semilesure = {np.dot(doc_vector, query_vector)}/({norm(doc_vector)}/({norm(query_vector)}))')
    return semilesure

def get_document_vector(text):
    docs_number = Documents.objects.count()
    if text in docs_vectors.keys():
        return docs_vectors[text]
    weights = get_frequencies(text)
    for word in weights.keys():
        docs_with_word = docs_with_word_number(word)
        if docs_with_word == 0: weights[word] = 0
        else: weights[word] = (weights[word])*(math.log(docs_number / docs_with_word))
    sqmean = 0
    for weight in weights.values():
        sqmean += weight**2
    if sqmean == 0: return []
    sqmean = math.sqrt(sqmean)
    for word in weights.keys():
        weights[word] = weights[word] / sqmean
    docs_vectors[text] = weights
    return weights

def docs_with_word_number(word):
    docs_with_word = 0
    for doc_words in doc_lemmas:
        if word in doc_words:
            docs_with_word += 1
    return docs_with_word

def summarize_text(text):
    sum_text = ''
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 3)
    for sentence in summary:
        sum_text += ' ' + str(sentence)
    return sum_text
     
def calculate_precision_recall(relevant_docs, returned_docs):
    relevant_number = len(relevant_docs)
    returned_number = len(returned_docs)
    
    precision = []
    recall = []
    found_relevant = 0
    
    for i in range(returned_number):
        if returned_docs[i] in relevant_docs:
            found_relevant += 1
    
        current_precision = found_relevant / (i + 1) 
        if relevant_number == 0:
            current_recall = 0
        else:
            current_recall = found_relevant / relevant_number 
        
        precision.append(current_precision)
        recall.append(current_recall)

    return precision, recall

def calculate_metrics(request):
    returned_docs, unreturned_docs ={}, {}
    documents_ids = request.session.get('documents_ids', [])
    documents = [Documents.objects.get(doc_id=document_id) for document_id in documents_ids]
    processed_texts = request.session.get('processed_texts', {})
    returned_texts = request.session.get('returned_texts', {})
    search_words = request.session.get('search_words', [])
    for doc_id, text in processed_texts.items(): 
        if text in returned_texts.values():
            returned_docs[doc_id] = calculate_relevant(search_words, text)
        else:
            unreturned_docs[doc_id] = calculate_relevant(search_words, text)
        
    returned_number = len(returned_docs)
    sorted_relevant_docs = dict(sorted(returned_docs.items(), key=lambda item: min(item[1].values()), reverse=True))

    a = sum(1 for word_counts in returned_docs.values() if not any(count < 5 for count in word_counts.values()))
    rel_docs = [list(returned_docs.keys()).index(doc_id) for doc_id, word_counts in returned_docs.items() if not any(count < 5 for count in word_counts.values())]
    c = sum(1 for word_counts in unreturned_docs.values() if not any(count < 5 for count in word_counts.values()))
    if c != 0:
        rel_docs = rel_docs + [list(unreturned_docs.keys()).index(doc_id)
                                       for doc_id, word_counts in unreturned_docs.items() if not any(count < 5 for count in word_counts.values())]
    
    relevant_indexes = list(sorted_relevant_docs.keys())
    returned_indexes = list(returned_docs.keys())

    d = sum(1 for word_counts in unreturned_docs.values() if any(count < 5 for count in word_counts.values()))
    b = returned_number - a
    if a == 0:
        precision = 0
    else:
        precision = round(a / (a + b), 2)
    if a == 0 and c == 0:  
        recall = 0 
    else:
        recall = round(a / (a + c), 2)
    accuracy = round((a + d) / (a + c + b + d), 2)
    error = round((b + c) / (a+b+c+d), 2)
    if precision == 0 or recall == 0:
        f_measure = 0
    elif precision == recall:
        f_measure = precision
    else:
        f_measure = round(2 / (1 / precision + 1 / recall), 2) 

    if a == 0:
        avg_Prec = precision_n = 0 
    else:
        precision_n =  round(a / returned_number, 2)
        avg_Prec = calculate_average_precision(relevant_indexes, returned_indexes)

    recall_values = np.arange(0.0, 1.1, 0.1)
    interpolated_precision = []
    all_relevant_number = len(relevant_indexes)
    returned_relevant_pos = [1 if returned_index in relevant_indexes else 0 for returned_index in returned_indexes]

    relevant_count = 0
    docs_count = 0
    recall_pos = 0
    for relevance in returned_relevant_pos:
        relevant_count += relevance
        docs_count += 1
        precision = round(relevant_count / docs_count, 2)
        recall = relevant_count / all_relevant_number
        while recall_pos <= recall and recall_pos <= 1:
            interpolated_precision.append(precision)
            recall_pos += 0.1
    interpolated_precision += [0 for i in range(len(recall_values) - len(interpolated_precision))]

    plt.figure(figsize=(10, 6))
    plt.plot(recall_values, interpolated_precision, marker='o')
    plt.title('График полноты/точности')
    plt.xlabel('Полнота')
    plt.ylabel('Точность')
    plt.grid()
    plt.xticks(np.arange(0.0, 1.1, 0.1))
    plt.yticks(np.arange(0.0, 1.1, 0.1))
    plt.axhline(0, color='black', lw=0.5)
    plt.axvline(0, color='black', lw=0.5)
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    graphic = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    
    avg_Prec = sum(interpolated_precision)/len(recall_values)

    return render(request, 'calculate_metrics.html', {'documents': documents, 'search_words': search_words, 'relevant_docs': sorted_relevant_docs,
        'precision': precision, 'recall': recall, 'accuracy': accuracy, 'error': error, 'f_measure': f_measure, 'precision_n': precision_n, 'avg_Prec': avg_Prec, 'graphic': graphic})
 
def calculate_relevant(search_words, text):
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(text)
    lemmatized_words = [lemmatizer.lemmatize(word.lower()) for word in words]
    lemmatized_word_counts = Counter(lemmatized_words)

    relevant_search_word = {word: (lemmatized_word_counts.get(lemmatizer.lemmatize(word.lower()), 0)) for word in search_words}
    
    return relevant_search_word

def calculate_average_precision(relevant_indexes, returned_indexes):
    avg_prec = 0
    for i in range(len(relevant_indexes)):
        if relevant_indexes[i] in returned_indexes:
            avg_prec += (i+1) / (returned_indexes.index(relevant_indexes[i]) + 1)
    avg_prec = avg_prec / len(relevant_indexes)
    return round(avg_prec, 2)
