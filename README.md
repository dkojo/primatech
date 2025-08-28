# Prima Tech Challenge – EKS, Terraform, Python API, and GitHub Actions CI/CD

## Overview

This project demonstrates the end-to-end deployment of a Python-based API server to an AWS Elastic Kubernetes Service (EKS) cluster. It combines **Terraform** for infrastructure provisioning, **`eksctl`** for initial cluster creation, **Helm** for Kubernetes application management, and **GitHub Actions** for automated CI/CD workflows.

The project also integrates **Trivy** for container image vulnerability scanning before pushing images to AWS Elastic Container Registry (ECR).

# I have also included screenshots in the images/ folder as evidence of the work completed throughout the project.

---

## Architecture

The deployment pipeline consists of:

- **EKS Cluster** for running workloads
- **AWS ECR** for image storage
- **Terraform** for infrastructure provisioning
- **Helm** for Kubernetes deployment
- **GitHub Actions** for CI/CD automation
- **Trivy** for container security scanning

---

## Folder Structure

```
prima-tech-challenge/
│
├── .github/workflows/
│   └── deploy.yml
│
├── helm/prima-api/
│   ├── templates/
│   ├── Chart.yaml
│   └── values.yaml
│
├── infra/
│   ├── backend.tf
│   ├── dynamodb.tf
│   ├── ecr.tf
│   ├── iam.tf
│   ├── main.tf
│   ├── s3.tf
│   ├── terraform.tfvars
│   └── variables.tf
│
├── prima-api-server/
│   ├── app/
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .gitignore
│
└── images/
```

---

## Workflow Summary

1. **Repository Creation** – Initialized GitHub repository and structured project.
2. **Cluster Setup** – Created initial EKS cluster with `eksctl`.
3. **Infrastructure Provisioning** – Used Terraform to provision supporting AWS resources.
4. **Application Development** – Built Python API with endpoints and tests.
5. **CI/CD Implementation** – Configured GitHub Actions to build, scan, and deploy the app.
6. **Deployment** – Released application to EKS using Helm.
7. **Verification** – Validated LoadBalancer endpoint and tested API routes.

---

## Infrastructure Setup

### Step 1 – Create EKS Cluster

Used `eksctl` for a quick bootstrap:

```bash
eksctl create cluster \
  --name prima-tech-challenge-cluster \
  --region us-east-1 \
  --nodes 2
```

### Step 2 – Provision AWS Resources with Terraform

Terraform modules in the `infra/` directory create:

- ECR Repository (`prima-api`)
- IAM roles and policies
- S3 for storing image avatars
- DynamoDB for storing users
- Security groups
- Other supporting infrastructure

Commands:

```bash
cd infra
terraform init
terraform apply -auto-approve
```

---

## Application Development

- **Language**: Python 3.11
- **Framework**: FastAPI
- **Entry Point**:

  ```python
  from fastapi import FastAPI
  from fastapi.responses import HTMLResponse
  from app.routes import router

  app = FastAPI()
  app.include_router(router)

  @app.get("/health")
  def health_check():
      return {"status": "ok"}

  @app.get("/", response_class=HTMLResponse)
  def welcome():
      return """<html>... my custom HTML welcome page...</html>"""
  ```

- **Key Features**:

  - `/` — Custom HTML welcome page linking to `/users` and `/docs`.
  - `/health` — Health check endpoint returning JSON status.
  - `/users` — API route (implemented in `app/routes.py`) to list users.
  - `/docs` — Automatically generated Swagger UI for API exploration.

- **Project Structure**:

  - `prima-api-server/app/` — Application logic and route definitions.
  - `prima-api-server/tests/` — Unit tests for API endpoints.
  - `prima-api-server/Dockerfile` — Containerization instructions for deployment.

- **Serving**:

  - Runs with `uvicorn` as the ASGI server inside Docker.
  - Fully compatible with CI/CD pipeline for automated build and deploy.

---

## CI/CD Pipeline

Workflow: `.github/workflows/deploy.yml`

Key stages:

1. **Checkout repository**
2. **Configure AWS credentials via OIDC**
3. **Install Python & dependencies**
4. **Run unit tests with pytest**
5. **Authenticate to AWS ECR**
6. **Build Docker image**
7. **Scan image with Trivy** (fail on CRITICAL)
8. **Push to ECR**
9. **Deploy to EKS with Helm**
10. **Wait for LoadBalancer & test endpoint**

---

## Deployment

**Helm Upgrade/Install:**

```bash
helm upgrade --install prima-api helm/prima-api \
  --set image.repository=${ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/prima-api \
  --set image.tag=$IMAGE_TAG \
  --set image.pullPolicy=Always
```

**Test Endpoint:**

```bash
curl http://<LB_DNS>/users
```

## How to Run Locally

1. **Clone Repository**

```bash
git clone https://github.com/robertyawmegbenu/prima-tech-challenge.git
cd prima-tech-challenge
```

2. **Run API**

```bash
cd prima-api-server
pip install -r requirements.txt
python app.py
```

3. **Access Endpoint**

```
http://localhost:80/users
```

---

## Future Improvements

In future iterations of this project, I plan to enhance functionality, maintainability, and deployment flexibility by implementing the following:

- **Multi-environment deployment strategy** – Introduce separate configurations and pipelines for development, staging, and production environments.
- **Integration testing in CI/CD** – Extend the GitHub Actions pipeline to include end-to-end and integration tests against a deployed environment.
- **Centralized monitoring and logging** – Integrate solutions such as Prometheus and Grafana for metrics, and ELK Stack (Elasticsearch, Logstash, Kibana) for log aggregation and analysis.
- **Advanced deployment strategies** – Adopt blue/green or canary deployment patterns to reduce downtime and mitigate release risks.
