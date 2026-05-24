from django.shortcuts import render, redirect
from django.conf import settings
from .forms import PlantUploadForm
from .models import PlantDiagnosis
from google import genai
from PIL import Image
import os

def home(request):
    result = None
    if request.method == 'POST':
        form = PlantUploadForm(request.POST, request.FILES)
        if form.is_valid():
            diagnosis = form.save()
            
            api_key = getattr(settings, 'GEMINI_API_KEY', None)
            client = genai.Client(api_key=api_key)
            
            try:
                img_path = diagnosis.image.path
                pil_image = Image.open(img_path)
                
                # JOGABY BÖLÜP ALMAK ÜÇIN PROFESSIONAL STRUKTURAN PROMPT
                prompt = (
                    f"Sen professional agronom we ösümlik kesellerini anyklaýan emeli intellektsiň. "
                    f"Suratdaky ösümlik: {diagnosis.get_plant_type_display()}. "
                    f"Suraty berk gözden geçir we jogaby diňe we diňe türkmen dilinde, aşakdaky gurluşda ber. "
                    f"Sözleriň arasynda asla başga artykmaç düşündiriş ýazma, göni şu 3 belligi ulan:\n\n"
                    f"STATUS: [Bw ýere gysgaça ýeke söz bilen keseliň adyny ýa-da 'Sagdyn' diýip ýaz]\n"
                    f"ANALIZ: [Bu ýere keseliň sebäbini, ýaprakdaky alamatlary uly we düşnükli düşündir]\n"
                    f"BEJERGI: [Bu ýere daýhan näme derman sepmeli, nähili ideg etmeli, anyk we madda-madda ýaz]"
                )
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[pil_image, prompt]
                )
                
                raw_text = response.text
                
                # Gelýän teksti bölüp aýratyn fildlere ýazmak logikasy
                status_part = "Anyklanyp bilinmedi"
                analysis_part = raw_text
                treatment_part = "Ýokarda maslahat berildi."
                
                if "STATUS:" in raw_text and "ANALIZ:" in raw_text and "BEJERGI:" in raw_text:
                    try:
                        parts = raw_text.split("ANALIZ:")
                        status_part = parts[0].replace("STATUS:", "").strip()
                        
                        sub_parts = parts[1].split("BEJERGI:")
                        analysis_part = sub_parts[0].strip()
                        treatment_part = sub_parts[1].strip()
                    except:
                        pass
                
                # Bazada uly edip aýratyn saklaýarys
                diagnosis.status = status_part
                diagnosis.ai_analysis = analysis_part
                diagnosis.treatment_plan = treatment_part
                diagnosis.save()
                
                result = diagnosis
                
            except Exception as e:
                print(f"AI Error: {e}")
                diagnosis.status = "Säwlik boldy"
                diagnosis.ai_analysis = f"Baglanyşykda ýalňyşlyk boldy: {e}"
                diagnosis.save()
                result = diagnosis
    else:
        form = PlantUploadForm()

    return render(request, 'home.html', {'form': form, 'result': result})

def history(request):
    # Ähli barlanylan ösümlikleri iň täzeden könä tarap düzüp ugradýarys
    history_list = PlantDiagnosis.objects.all().order_by('-created_at')
    return render(request, 'history.html', {'history_list': history_list})