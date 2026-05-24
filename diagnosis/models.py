from django.db import models

class PlantDiagnosis(models.Model):
    PLANT_TYPES = [
        # Gökatlar we Bakja ekinleri
        ('tomato', 'Pomidor'),
        ('cucumber', 'Hyýar'),
        ('pepper', 'Burç (Süýji/Ajy)'),
        ('eggplant', 'Badamjan'),
        ('strawberry', 'Ýertut (Klubnika)'),
        ('melon', 'Gawun'),
        ('watermelon', 'Garpyz'),
        ('pumpkin', 'Kädi'),
        
        # Ýyladyşhana we Daşary meýdan ekinleri
        ('potato', 'Ýer alma (Kartoşka)'),
        ('onion', 'Sogan'),
        ('garlic', 'Sarymsak'),
        ('cabbage', 'Karam'),
        ('carrot', 'Gök önüm (Säbi/Gäşir)'),
        
        # Miweli baglar
        ('apple', 'Alma'),
        ('grape', 'Üzüm'),
        ('lemon', 'Limon / Sitruslar'),
        ('peach', 'Şetaly'),
        ('pomegranate', 'Nar'),
        
        # Beýlekiler
        ('other', 'Başga ösümlik / Gül'),
    ]

    plant_type = models.CharField(max_length=30, choices=PLANT_TYPES, default='tomato')
    image = models.ImageField(upload_to='plant_images/')
    
    # AI tarapyndan geljek maglumatlar
    status = models.CharField(max_length=100, blank=True)
    ai_analysis = models.TextField(blank=True)
    treatment_plan = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_plant_type_display()} - {self.status} ({self.created_at.strftime('%Y-%m-%d')})"