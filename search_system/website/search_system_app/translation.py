import requests

from deep_translator import GoogleTranslator
from deep_translator import PonsTranslator
from nltk.stem import WordNetLemmatizer
import PyPDF2
from io import BytesIO
from nltk.tokenize import word_tokenize
from collections import Counter
import spacy
from django.shortcuts import render
from .models import Word
from spacy import displacy
import nltk
from nltk.tokenize import sent_tokenize
import spacy

nltk.download('punkt')
lemmatizer = WordNetLemmatizer()
nlp = spacy.load("en_core_web_sm")

def translate_text(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        text = read_pdf(url)
        translated = translate(text)
        
        save_translations(text.lower())
        
        request.session['sentences_of_input_text'] = sent_tokenize(translated) 
        request.session['text'] = text
        return render(request, 'translation.html', {
            'url': url,
            'input_text': text,
            'translated_text': translated,
        })
    return render(request, 'translation.html')

def translate(text):
    if len(text) > 5000:
        translated = ''
        text_parts = devide_text(text)
        for part in text_parts:
            translated += GoogleTranslator(source='english', target='german').translate(part)
    else:
        translated = GoogleTranslator(source='english', target='german').translate(text)
    return translated

def devide_text(text):
    text_parts = []
    pos = 0
    while len(text) - pos > 5000:
        new_pos = text.rfind('.', pos, pos+5000)
        text_parts.append(text[pos:new_pos])
        pos = new_pos
    return text_parts

def translate_word(word):
    print('word: ', word )
    translated_word = PonsTranslator(source='english', target='german').translate(word, return_all=False)
    return translated_word

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

def save_translations(text):
    doc = nlp(' '.join(set(text.split())))
    for token in doc:
        if token.text.isalpha() and (not Word.objects.filter(english_word=token.text).exists()):
            try:
                translation = translate_word(token.text)
                Word.objects.create(english_word=token.text, german_translation=translation, pos_tag=token.pos_)
            except:
                pass

def count_word_frequency(request):
    text = request.session.get('text')
    words = [lemmatizer.lemmatize(word.lower()) for word in word_tokenize(text)]
    words_freq = Counter(words)
    return render(request, 'words_freq.html', {'words_freq': dict(words_freq)})

def get_pos_tags(request):
    text = request.session.get('text')
    doc = nlp(text)
    pos_tags = [(token.text, token.pos_) for token in doc]
    return render(request, 'pos_tags.html', {'pos_tags': pos_tags})

def generate_syntax_tree(request):
    html_trees = {}
    sentences = request.session.get('sentences_of_input_text')
    for sentence in sentences:
        doc = nlp(sentence) 
        html_trees[sentence] = displacy.render(doc, style='dep', page=True)
    return render(request, 'trees.html', {'syntax_trees_html': html_trees})