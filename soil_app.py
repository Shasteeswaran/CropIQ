from flask import Flask, request, render_template
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import os

app = Flask(__name__)

# Load the trained Keras model
model = tf.keras.models.load_model("soil_class.h5")

output_class = ['Alluvial soil', 'Black soil', 'Clay soil', 'Red soil']



@app.route('/')
def index():
    return render_template('soil.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get the uploaded image
    img = request.files['image']
        
    if img.filename == '':
        raise ValueError("No file selected") # Save the uploaded image
    img_path = "static/uploaded_image.jpg" 
    img.save(img_path)

    test_image = image.load_img(img_path, target_size=(224, 224))
    test_image = image.img_to_array(test_image) / 255
    test_image = np.expand_dims(test_image, axis=0)

    predicted_array = model.predict(test_image)
    predicted_value = output_class[np.argmax(predicted_array)]
    predicted_accuracy = round(np.max(predicted_array) * 100, 2)
        
       

    return render_template('soil.html', prediction_value=predicted_value,
                               prediction_accuracy=predicted_accuracy,image_path=img_path)
    

if __name__ == '__main__':
    app.run(debug=True)
