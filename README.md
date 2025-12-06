# 🎓 Student Performance Predictor - End-to-End ML Project

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen)](http://studentperformanceenv1-env.eba-wbvx3wpb.eu-north-1.elasticbeanstalk.com/)
[![CI/CD](https://github.com/sunilverma231/End-to-end-Machine-Learning-Project-/actions/workflows/deploy.yml/badge.svg)](https://github.com/sunilverma231/End-to-end-Machine-Learning-Project-/actions/workflows/deploy.yml)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![AWS](https://img.shields.io/badge/AWS-Elastic_Beanstalk-orange)](https://aws.amazon.com/elasticbeanstalk/)
[![Flask](https://img.shields.io/badge/Flask-3.1.0-lightgrey)](https://flask.palletsprojects.com/)

> **Live Application:** [http://studentperformanceenv1-env.eba-wbvx3wpb.eu-north-1.elasticbeanstalk.com/](http://studentperformanceenv1-env.eba-wbvx3wpb.eu-north-1.elasticbeanstalk.com/)

A production-ready machine learning application that predicts student math scores based on various demographic and academic factors. Deployed on AWS Elastic Beanstalk with **automated CI/CD pipeline** using GitHub Actions.

---

## 📋 Table of Contents
- [Overview](#overview)
- [Live Demo](#live-demo)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Project Architecture](#project-architecture)
- [ML Models](#ml-models)
- [Deployment Challenges & Solutions](#deployment-challenges--solutions)
- [Local Setup](#local-setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Key Learnings](#key-learnings)

---

## 🎯 Overview

This project demonstrates a complete machine learning workflow from data exploration to production deployment:
- **Data Analysis**: Comprehensive EDA on student performance dataset
- **Model Training**: Trained and evaluated 6 different regression models
- **API Development**: Built RESTful API using Flask
- **Cloud Deployment**: Deployed on AWS Elastic Beanstalk with production-grade configurations
- **Resource Optimization**: Engineered solution to run on AWS free tier (t2.micro)

---

## 🚀 Live Demo

**Application URL:** [http://studentperformanceenv1-env.eba-wbvx3wpb.eu-north-1.elasticbeanstalk.com/](http://studentperformanceenv1-env.eba-wbvx3wpb.eu-north-1.elasticbeanstalk.com/)

**Try it out:**
1. Visit the application URL
2. Fill in student information (gender, ethnicity, parental education, etc.)
3. Enter reading and writing scores
4. Click "Predict your Maths Score"
5. Get instant prediction powered by trained ML models

---

## 🛠️ Tech Stack

### **Machine Learning & Data Science**
- **Python 3.11** - Core programming language
- **scikit-learn** - Model training (Random Forest, Gradient Boosting, AdaBoost, etc.)
- **CatBoost** - Gradient boosting algorithm
- **pandas & numpy** - Data manipulation and analysis
- **matplotlib & seaborn** - Data visualization

### **Web Development**
- **Flask 3.1.0** - Web framework for API
- **Gunicorn** - Production WSGI server
- **HTML/CSS** - Frontend interface

### **Deployment & DevOps**
- **AWS Elastic Beanstalk** - Cloud hosting platform
- **AWS Application Load Balancer** - Traffic distribution and health checks
- **GitHub Actions** - CI/CD pipeline automation
- **Nginx** - Reverse proxy server
- **Git** - Version control

### **Model Serialization**
- **joblib** - Model persistence
- **dill** - Preprocessing pipeline serialization

---

## ✨ Features

- ✅ **Real-time Predictions**: Instant math score predictions based on student attributes
- ✅ **Multiple ML Models**: Ensemble of 6 regression models for robust predictions
- ✅ **Production-Ready API**: RESTful endpoints with health checks
- ✅ **Responsive UI**: Clean, user-friendly web interface
- ✅ **Auto-scaling**: AWS infrastructure handles traffic spikes
- ✅ **Cost-Optimized**: Runs on AWS free tier (t2.micro instance)

---

## 🏗️ Project Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────────┐
│   User      │ ───> │  Flask API   │ ───> │  ML Pipeline    │
│  (Browser)  │      │ (Gunicorn)   │      │ (6 Models)      │
└─────────────┘      └──────────────┘      └─────────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  AWS EB      │
                     │  (t2.micro)  │
                     └──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  ALB + Nginx │
                     │  (Port 80)   │
                     └──────────────┘
```

**Request Flow:**
1. User submits form data via web interface
2. Nginx reverse proxy forwards request to Gunicorn
3. Flask application validates and preprocesses input
4. ML pipeline transforms data using trained preprocessor
5. Ensemble model predicts math score
6. Result returned to user in <1 second

---

## 🤖 ML Models

Trained and evaluated **6 regression models** using GridSearchCV:

| Model | Description | Status |
|-------|-------------|--------|
| **Random Forest** | Ensemble of decision trees | ✅ Active |
| **Gradient Boosting** | Sequential boosting algorithm | ✅ Active |
| **CatBoost** | Gradient boosting for categorical features | ✅ Active |
| **AdaBoost** | Adaptive boosting ensemble | ✅ Active |
| **Decision Tree** | Single decision tree regressor | ✅ Active |
| **Linear Regression** | Linear model baseline | ✅ Active |

**Model Selection Process:**
- Cross-validation with 5 folds
- Hyperparameter tuning via GridSearchCV
- Best model selected based on R² score
- Model saved to `artifacts/model.pkl`

**Why CatBoost over XGBoost?**
- Smaller package size (saves 223MB vs xgboost)
- Better handling of categorical features
- Comparable or superior performance
- Enables deployment on AWS free tier

---

## 💡 Deployment Challenges & Solutions

### **Challenge 1: 502 Bad Gateway Errors**
**Problem:** Application URL returned 502 errors after initial deployment  
**Root Cause:** Incorrect WSGIPath configuration in `.ebextensions/01_packages.config`  
**Solution:** Changed `WSGIPath` from `wsgi:application` (module:callable format) to `wsgi.py` (file path format) to match EB's Gunicorn wrapper requirements

### **Challenge 2: Health Check Failures**
**Problem:** Environment stuck in "Degraded" state with validation errors  
**Root Cause:** Invalid namespace for health check configuration (`aws:elasticbeanstalk:application`)  
**Solution:** Corrected to `aws:elasticbeanstalk:environment:process:default` namespace with proper HealthCheckPath setting

### **Challenge 3: Disk Space Exhaustion**
**Problem:** Deployment failed with "No space left on device" error during pip install  
**Root Cause:** xgboost package (223.6 MB) exceeded t2.micro disk capacity (8-10GB)  
**Solution:** 
- Removed xgboost from dependencies
- Retained CatBoost as gradient boosting alternative
- Reduced total package size by 223MB
- Successfully deployed on free tier infrastructure

### **Challenge 4: Procfile Parse Errors**
**Problem:** Deployment failed with "Procfile could not be parsed"  
**Root Cause:** Tab characters in multi-line Procfile command  
**Solution:** Reformatted to single-line command with spaces only

---

## 🔄 CI/CD Pipeline

This project uses **GitHub Actions** for automated deployment to AWS Elastic Beanstalk.

### **Pipeline Workflow**
```
Git Push → GitHub Actions → Tests → Build → S3 Upload → EB Deploy → Health Check
```

### **What happens on every push to main:**
1. ✅ **Linting**: Code quality checks with flake8
2. ✅ **Testing**: Runs pytest (if tests exist)
3. ✅ **Build**: Creates deployment package (excludes dev files)
4. ✅ **Upload**: Sends package to S3 bucket
5. ✅ **Deploy**: Updates EB environment with new version
6. ✅ **Verify**: Waits for health check to pass

### **Setup CI/CD (One-time)**

**📋 Step-by-Step Guide (15 minutes):** [`.github/SETUP_WALKTHROUGH.md`](.github/SETUP_WALKTHROUGH.md)

**Quick Summary:**
1. **AWS:** Create IAM user `github-actions-deployer` with EB + S3 permissions
2. **AWS:** Generate access keys (save them!)
3. **GitHub:** Add 3 secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_ACCOUNT_ID`
4. **Test:** Push to main branch → Auto-deploy! 🚀

**Additional Resources:**
- 📖 [Detailed Setup Guide](.github/AWS_SETUP.md)
- ✅ [Printable Checklist](.github/CHECKLIST.txt)
- 🎯 [Quick Reference](.github/QUICK_REFERENCE.md)
- 📊 [Pipeline Architecture](.github/CICD_ARCHITECTURE.md)

### **Manual Deployment (Alternative)**
Still works if you prefer manual control:
```bash
bash scripts/make_eb_bundle.sh
# Upload the generated zip via AWS EB Console
```

---

## 🖥️ Local Setup

### **Prerequisites**
- Python 3.11+
- pip package manager

### **Installation Steps**

1. **Clone the repository**
```bash
git clone https://github.com/sunilverma231/End-to-end-Machine-Learning-Project-.git
cd End-to-end-Machine-Learning-Project-
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python application.py
```

5. **Access locally**
```
http://localhost:5000
```

---

## 📊 Usage

### **Making Predictions**

**Via Web Interface:**
1. Navigate to the application URL
2. Fill in the form:
   - Gender: Male/Female
   - Race/Ethnicity: Group A-E
   - Parental Education: High school, Bachelor's, Master's, etc.
   - Lunch Type: Standard/Free-Reduced
   - Test Preparation: Completed/None
   - Reading Score: 0-100
   - Writing Score: 0-100
3. Submit to get math score prediction

**Via API (cURL):**
```bash
curl -X POST http://studentperformanceenv1-env.eba-wbvx3wpb.eu-north-1.elasticbeanstalk.com/predict \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "gender=male&race_ethnicity=group B&parental_level_of_education=bachelor's degree&lunch=standard&test_preparation_course=completed&reading_score=72&writing_score=74"
```

---

## 📁 Project Structure

```
End-to-end-Machine-Learning-Project-/
│
├── application.py              # Flask application entry point
├── wsgi.py                     # WSGI entry for Gunicorn
├── Procfile                    # AWS EB process configuration
├── requirements.txt            # Python dependencies
├── setup.py                    # Package setup configuration
│
├── .ebextensions/              # AWS EB configuration
│   ├── 01_packages.config      # WSGIPath and Python settings
│   └── 02_healthcheck.config   # ALB health check configuration
│
├── scripts/                    # Deployment scripts
│   └── make_eb_bundle.sh       # Creates deployment bundle
│
├── src/                        # Source code
│   ├── components/             # ML pipeline components
│   │   ├── data_ingestion.py
│   │   ├── data_transformation.py
│   │   ├── model_trainer.py
│   │   └── utils.py
│   └── pipeline/               # Prediction pipeline
│       ├── predict_pipeline.py
│       └── train_pipeline.py
│
├── notebook/                   # Jupyter notebooks
│   ├── 1. EDA STUDENT PERFORMANCE.ipynb
│   └── 2. MODEL TRAINING.ipynb
│
├── artifacts/                  # Trained models & preprocessors
│   ├── model.pkl
│   └── preprocessor.pkl
│
└── templates/                  # HTML templates
    ├── index.html
    └── home.html
```

---

## 🎓 Key Learnings

### **Technical Skills Demonstrated**
- ✅ End-to-end ML project lifecycle (EDA → Training → Deployment)
- ✅ Production API development with Flask and Gunicorn
- ✅ AWS cloud deployment and configuration
- ✅ Resource optimization for cost-effective hosting
- ✅ Debugging production issues (502 errors, health checks, disk space)
- ✅ Infrastructure as Code (.ebextensions configuration)

### **Problem-Solving Highlights**
- Diagnosed and fixed WSGIPath misconfiguration
- Resolved ALB health check namespace issues  
- Optimized dependencies to fit free-tier constraints (removed 223MB package)
- Debugged Procfile parsing errors

### **Best Practices Implemented**
- Modular code architecture with separation of concerns
- Version control with meaningful commit messages
- Health check endpoints for monitoring
- Logging for debugging and diagnostics
- Clean deployment bundles with .ebignore

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📧 Contact

**Sunil Verma**
- GitHub: [@sunilverma231](https://github.com/sunilverma231)
- LinkedIn: [https://www.linkedin.com/in/sunil-verma-operations-analyst/]
- Email: [sunilverma00027@gmail.com]

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- Dataset: Student Performance Dataset
- AWS Free Tier for hosting
- scikit-learn and CatBoost communities

---

**⭐ If you found this project helpful, please consider giving it a star!** 