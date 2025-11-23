from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from pipeline.predict_pipeline import PredictPipeline, CustomData

application = Flask(__name__)
app = application

# Route for home page (show form)
@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    
    else:
        try:
            # Collect form inputs
            data = CustomData(
                gender = request.form.get('gender'),
                race_ethnicity = request.form.get('race_ethnicity'),
                parental_level_of_education = request.form.get('parental_level_of_education'),
                lunch = request.form.get('lunch'),
                test_preparation_course = request.form.get('test_preparation_course'),
                reading_score = float(request.form.get('reading_score')),
                writing_score = float(request.form.get('writing_score'))
            )

            # Convert form data to DataFrame
            pred_df = data.get_data_as_data_frame()
            print("Input DataFrame:\n", pred_df)

            # Predict using model pipeline
            predict_pipeline = PredictPipeline()
            prediction = predict_pipeline.predict(pred_df)

            # Return prediction to template
            return render_template('home.html', prediction=prediction[0])
        
        except Exception as e:
            return f"Error: {str(e)}"

# Run Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
