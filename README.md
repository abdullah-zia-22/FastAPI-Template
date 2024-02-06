# Python FastAPI Application Deployment with CI/CD Pipeline
This repository contains a Continuous Integration/Continuous Deployment (CI/CD) pipeline that automates the deployment of a Python FastAPI application using Docker to an EC2 instance. The pipeline uses GitHub Actions to build and deploy the application whenever changes are pushed to the main branch. It has User Data Modeling, pydantic schemas and JWT authentication.

# Prerequisites
Before setting up this CI/CD pipeline, make sure you have the following prerequisites:
* An AWS EC2 instance where you want to deploy your FastAPI application.
* GitHub repository containing your FastAPI application code.
* SSH access to the EC2 instance.
* AWS Security Group rules allowing traffic on the necessary ports (e.g., 7001).
  
These files are required for database setup.
  
# Setting Up Secrets
To securely store sensitive information like SSH keys and server details, you need to add these secrets to your GitHub repository. Follow these steps:
In your GitHub repository, go to Settings > Secrets > New repository secret.
Add the following secrets:
* SSH_PRIVATE_KEY: Your SSH private key for accessing the EC2 instance.
* EC2_HOST: The hostname or IP address of your EC2 instance.
* SSH_USERNAME: The username to use when connecting to the EC2 instance (e.g., ubuntu).
* SSH_PORT: The SSH port of your EC2 instance (usually 22).
* DEPLOY_PORT: The port for allowing traffic on the requests (e.g., 7001).
* DB_HOST: Host for Database connection
* DB_USER: User for Database connection
* DB_PASSWORD: Password for Database connection
* DB_NAME: Name of Database
* DB_PORT: Port of Database connection
* ENVIRONMENT:development

# NOTE
* Make sure to change api running port number in CMD command in dockerfile and in workflow .yml file in docker run command
  
# CI/CD Workflow
The CI/CD pipeline is defined in the .github/workflows/aws.yml file. Here's an overview of what the workflow does:
* It triggers whenever changes are pushed to the main branch.
* The pipeline runs on an Ubuntu environment provided by GitHub Actions.
* It checks out the latest code from the repository.
* It sets up Python 3.x as the runtime environment.
* The workspace is cleaned up.
* SSH key and directory are set up for secure access to the EC2 instance.
* GitHub user configurations are set for the repository.
  
# The FastAPI application is deployed to the EC2 instance using SSH.
* The latest code is pulled from the repository.
* Latest code has changes in codebase.
* Dockerfile is being build and run on port.
* The pipeline opens port (added in secrets) on the EC2 instance and restarts Nginx to apply changes.

# Usage
To use this CI/CD pipeline for your FastAPI application:

* Fork this repository to your GitHub account.
* Add your FastAPI application code to your forked repository.
* Set up the necessary secrets in your repository's Settings > Secrets.
* Push changes to the main branch of your forked repository to trigger the pipeline.
* Monitor the workflow progress in the "Actions" tab of your repository.
* Once the pipeline completes successfully, your FastAPI application should be accessible on the specified port (e.g., http://your_ec2_instance_ip:7001).

# Contributing
Feel free to contribute to this project by opening issues or pull requests. We welcome any suggestions or improvements to make this CI/CD pipeline even more robust.