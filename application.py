from flask import Flask, request, render_template
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import PredictPipeline, CustomData

# Main application object for Gunicorn
application = Flask(__name__)
app = application

# Route for home page
@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        try:
            data = CustomData(
                gender=request.form.get('gender'),
                race_ethnicity=request.form.get('race_ethnicity'),
                parental_level_of_education=request.form.get('parental_level_of_education'),
                lunch=request.form.get('lunch'),
                test_preparation_course=request.form.get('test_preparation_course'),
                reading_score=float(request.form.get('reading_score')),
                writing_score=float(request.form.get('writing_score'))
            )

            pred_df = data.get_data_as_data_frame()
            predict_pipeline = PredictPipeline()
            prediction = predict_pipeline.predict(pred_df)

            return render_template('home.html', prediction=prediction[0])
        
        except Exception as e:
            return f"Error: {str(e)}"

# Run locally only
if __name__ == "__main__":
    application.run(debug=True)
