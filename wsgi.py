"""
WSGI entry point for AWS Elastic Beanstalk
This file serves as a backup if application.py import fails
"""
from application import application

# AWS EB looks for 'application' callable
if __name__ == "__main__":
    application.run()
