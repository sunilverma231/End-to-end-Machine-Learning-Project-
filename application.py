from flask import Flask, request, render_template
import os
import sys
import logging

# Add current directory to path to ensure src imports work
sys.path.insert(0, os.path.dirname(__file__))

# Configure basic logging (Gunicorn will capture stdout/stderr)
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# Main application object for Gunicorn
application = Flask(__name__)
app = application
app.logger.info("application.py imported; Flask app instantiated")

# Health check endpoint for AWS EB
@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

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
            # Import here to avoid loading models at startup
            from src.pipeline.predict_pipeline import PredictPipeline, CustomData
            
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
            import traceback
            error_details = traceback.format_exc()
            app.logger.error(f"Prediction error: {error_details}")
            return f"Error: {str(e)}<br><pre>{error_details}</pre>", 500

# Run locally only
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    application.run(host='0.0.0.0', port=port, debug=True)
