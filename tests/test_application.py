"""
Unit tests for the Student Performance Prediction application.
Run with: pytest tests/
"""

import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestApplicationHealth:
    """Test Flask application health and basic functionality."""
    
    def test_imports(self):
        """Test that core modules can be imported."""
        try:
            from application import application
            assert application is not None
        except Exception as e:
            pytest.fail(f"Failed to import application: {e}")
    
    def test_flask_app_exists(self):
        """Test that Flask app instance exists."""
        from application import application
        assert application is not None
        assert hasattr(application, 'config')


class TestPredictionPipeline:
    """Test the ML prediction pipeline."""
    
    def test_custom_data_class(self):
        """Test CustomData class initialization."""
        try:
            from src.pipeline.predict_pipeline import CustomData
            
            data = CustomData(
                gender='male',
                race_ethnicity='group B',
                parental_level_of_education="bachelor's degree",
                lunch='standard',
                test_preparation_course='none',
                reading_score=72,
                writing_score=74
            )
            
            assert data.gender == 'male'
            assert data.reading_score == 72
            assert data.writing_score == 74
        except Exception as e:
            pytest.fail(f"CustomData class test failed: {e}")
    
    def test_data_to_dataframe(self):
        """Test conversion of CustomData to pandas DataFrame."""
        try:
            from src.pipeline.predict_pipeline import CustomData
            
            data = CustomData(
                gender='female',
                race_ethnicity='group A',
                parental_level_of_education='high school',
                lunch='free/reduced',
                test_preparation_course='completed',
                reading_score=85,
                writing_score=88
            )
            
            df = data.get_data_as_data_frame()
            
            assert df is not None
            assert len(df) == 1  # Should have 1 row
            assert 'gender' in df.columns
            assert 'reading_score' in df.columns
            assert df['reading_score'].iloc[0] == 85
        except Exception as e:
            pytest.fail(f"Data to DataFrame conversion failed: {e}")


class TestArtifacts:
    """Test that model artifacts exist."""
    
    def test_model_file_exists(self):
        """Test that trained model file exists."""
        model_path = 'artifacts/model.pkl'
        assert os.path.exists(model_path), f"Model file not found at {model_path}"
    
    def test_preprocessor_exists(self):
        """Test that preprocessor file exists."""
        preprocessor_path = 'artifacts/preprocessor.pkl'
        assert os.path.exists(preprocessor_path), f"Preprocessor not found at {preprocessor_path}"


class TestConfiguration:
    """Test application configuration."""
    
    def test_procfile_exists(self):
        """Test that Procfile exists for deployment."""
        assert os.path.exists('Procfile'), "Procfile not found"
    
    def test_requirements_txt_exists(self):
        """Test that requirements.txt exists."""
        assert os.path.exists('requirements.txt'), "requirements.txt not found"
    
    def test_wsgi_file_exists(self):
        """Test that wsgi.py exists for production deployment."""
        assert os.path.exists('wsgi.py'), "wsgi.py not found"


class TestDataValidation:
    """Test input data validation."""
    
    @pytest.mark.parametrize("score", [0, 50, 100])
    def test_valid_scores(self, score):
        """Test that valid scores (0-100) are accepted."""
        from src.pipeline.predict_pipeline import CustomData
        
        data = CustomData(
            gender='male',
            race_ethnicity='group A',
            parental_level_of_education='high school',
            lunch='standard',
            test_preparation_course='none',
            reading_score=score,
            writing_score=score
        )
        
        assert 0 <= data.reading_score <= 100
        assert 0 <= data.writing_score <= 100
    
    def test_gender_values(self):
        """Test that gender accepts male/female."""
        from src.pipeline.predict_pipeline import CustomData
        
        for gender in ['male', 'female']:
            data = CustomData(
                gender=gender,
                race_ethnicity='group A',
                parental_level_of_education='high school',
                lunch='standard',
                test_preparation_course='none',
                reading_score=75,
                writing_score=75
            )
            assert data.gender in ['male', 'female']


if __name__ == "__main__":
    # Run tests with: python -m pytest tests/ -v
    pytest.main([__file__, '-v'])
