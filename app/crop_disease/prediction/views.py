from django.shortcuts import render
from .forms import PredictionForm
from .models import Prediction
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import numpy as np
import tensorflow as tf

def home(request):
    if request.method == 'POST':
        form = PredictionForm(request.POST, request.FILES)
        if form.is_valid():
            model = load_model('model.h5')
            image = form.cleaned_data['image']
            image_array = img_to_array(image)
            image_array = np.expand_dims(image_array, axis=0)
            image_array = image_array / 255.0
            result = model.predict(image_array)
            if result[0][0] > 0.5:
                prediction = 'Corn___Common_Rust'
            elif result[0][1] > 0.5:
                prediction = 'Corn___Gray_Leaf_Spot'
            # Add code for remaining predictions
            else:
                prediction = 'Unknown'
            prediction_obj = Prediction(image=image, result=prediction)
            prediction_obj.save()
            return render(request, 'prediction/result.html', {'prediction': prediction})
    else:
        form = PredictionForm()
    return render(request, 'prediction/home.html', {'form': form})
