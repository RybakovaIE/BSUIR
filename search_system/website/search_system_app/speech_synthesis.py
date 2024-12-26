import os
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from gtts import gTTS
from playsound import playsound
import uuid

def speech_synthesis(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        speed = float(request.POST.get('speed', 1.0))
        
        if text:
            filename = f"speech_{uuid.uuid4()}.mp3"
            audio_path = os.path.join(settings.MEDIA_ROOT, 'audio')
            os.makedirs(audio_path, exist_ok=True)
            filepath = os.path.join(audio_path, filename)
            tts = gTTS(text=text, lang='de', slow=(speed < 1.0))
            tts.save(filepath)
            return JsonResponse({
                'success': True,
                'audio_url': f'/media/audio/{filename}'
            })
            
        return JsonResponse({'success': False, 'error': 'No text provided'})
        
    return render(request, 'speech_synthesis.html')