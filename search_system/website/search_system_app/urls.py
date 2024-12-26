from django.urls import path
from . import auto_refereeing, views, lang_recognition, translation, speech_synthesis, speech_recognition
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    
    path('', views.search_results, name='search_results'),
    path('add_links/', views.add_link, name='add_links'),
    path('calculate_metrics/', views.calculate_metrics, name='calculate_metrics'),
    path('lang_recognition/', lang_recognition.language_recognition, name = 'lang_recognition'),
    path('download/', lang_recognition.download_result_json_file, name = 'download'),
    path('auto_refereeing/', auto_refereeing.auto_refereeing, name = 'auto_refereeing'),
    path('translation/', translation.translate_text, name='translation'),
    path('create_tree/', translation.generate_syntax_tree, name='create_tree'),
    path('get_words_freq/', translation.count_word_frequency, name='get_words_freq'),
    path('get_pos_tags/', translation.get_pos_tags, name='get_pos_tags'),
    path('download_report/', auto_refereeing.download_result_txt_file, name='download_report'),
    path('speech_synthesis/', speech_synthesis.speech_synthesis, name='speech_synthesis'),
    path('speech_recognition/', speech_recognition.speech_recognition, name='speech_recognition'),
    path('start/', speech_recognition.start_recognition, name='start_recognition'),
    path('stop/', speech_recognition.stop_recognition, name='stop_recognition'),
    path('conversations/', speech_recognition.get_conversations, name='get_conversations')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)