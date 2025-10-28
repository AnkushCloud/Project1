
Requirements : ProblemStatement.png

## Components Interaction:
1. Terraform provisions GKE cluster and infrastructure
2. Docker image is built and pushed to Container Registry
3. Helm deploys application with HPA configuration
4. LoadBalancer Service exposes application externally
5. HPA monitors CPU and scales pods between 1-3 based on 50% threshold
6. Load testing generates traffic to trigger autoscaling


## Prerequisites Setup:

## Tools -- 

# Install Google Cloud SDK
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Install Terraform
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install terraform

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Install Docker
sudo apt-get update
sudo apt-get install docker.io
sudo usermod -aG docker $USER



## Google Cloud --

# Login to GCP
gcloud auth login
gcloud auth configure-docker

# Set your project
export PROJECT_ID="your-project-id"
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable container.googleapis.com
gcloud services enable compute.googleapis.com
gcloud services enable containerregistry.googleapis.com



Update project id in following files --
kubernetes/helm-chart/values.yaml
terraform/variables.tf


# Build the application image
cd app
docker build -t gcr.io/$PROJECT_ID/web-app:1.0 .

# Push to Google Container Registry
docker push gcr.io/$PROJECT_ID/web-app:1.0


## Deploy via terraform --

cd terraform
terraform init
terraform plan
terraform apply

## Validate --
# Get cluster credentials
gcloud container clusters get-credentials web-app-cluster --region us-central1 --project $PROJECT_ID

# Check all resources
kubectl get all

# Verify pods are running
kubectl get pods -l app=web-app

# Check services
kubectl get services

# Check HPA
kubectl get hpa


## Testing --

# Get the external IP
EXTERNAL_IP=$(kubectl get service web-app-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

echo "Application URL: http://$EXTERNAL_IP"

# Test basic endpoints
curl http://$EXTERNAL_IP
curl http://$EXTERNAL_IP/health
curl http://$EXTERNAL_IP/config


## Load Testing --

# Test CPU intensive endpoint
curl http://$EXTERNAL_IP/cpu-intensive

# Test memory intensive endpoint  
curl http://$EXTERNAL_IP/memory-intensive

# Run multiple requests in parallel
for i in {1..10}; do
  curl -s http://$EXTERNAL_IP/cpu-intensive > /dev/null &
done
wait


## Monitor AutoScaling (real-time) --
kubectl get pods -l app=web-app -w