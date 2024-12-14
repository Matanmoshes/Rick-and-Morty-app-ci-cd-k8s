# Rick and Morty App CI/CD Pipeline

This repository implements a Continuous Integration (CI) and Continuous Deployment (CD) pipeline using GitHub Actions, Helm, and Minikube. The pipeline ensures that code changes are automatically tested and validated, and subsequently deployed to a local Kubernetes cluster for verification.
---
## Overview

The pipeline consists of two primary workflows:

1. **CI (Continuous Integration)**:  
   - Triggered on every push or pull request to the `main` branch.
   - Installs and tests the application using `pytest`.
   - If tests pass, it builds and pushes a Docker image to Docker Hub.

2. **CD (Continuous Deployment)**:  
   - Triggered when the CI workflow completes successfully.
   - Sets up a local Kubernetes cluster using Minikube.
   - Installs the NGINX Ingress Controller.
   - Deploys the application using Helm into a dedicated namespace.
   - Waits for the application pods to become ready.
   - Port-forwards the application’s service and tests the endpoints to ensure the deployment is successful.

---
## Workflows Breakdown

### CI Workflow (ci.yaml)

**Location:** `.github/workflows/ci.yaml`

**Triggers:**  
- `push` to `main` branch  
- `pull_request` to `main` branch

**Steps:**

1. **Checkout code:**  
   Uses the `actions/checkout@v4` action to bring the repository’s code into the build environment.

2. **Set up Python:**  
   Uses `actions/setup-python@v4` to install and configure Python 3.10.

3. **Install dependencies:**  
   Installs the Python dependencies listed in `requirements.txt` and `test/requirements.txt`.  
   - `pip install -r rick_and_morty_rest_app/requirements.txt`
   - `pip install -r test/requirements.txt`

4. **Set PYTHONPATH:**  
   Ensures that the application directory is on the Python path so tests can import the application.

5. **Run tests:**  
   Executes `pytest` against the test directory. If tests fail, the workflow stops. If they pass, the workflow continues.

**If Tests Pass:**

6. **Checkout code (again, for build step):**  
   Checks out the code for the build and push job.

7. **Load environment variables from DOCKER_VARS:**  
   Reads variables like `DOCKER_REPO` and `VERSION` and sets them as environment variables.

8. **Set up Docker Buildx:**  
   Configures Docker Buildx for building multi-architecture images if needed.

9. **Login to DockerHub:**  
   Uses `docker/login-action@v3` with credentials stored as GitHub secrets.

10. **Build and push Docker image:**  
    Uses `docker/build-push-action@v4` to build the Docker image from the `rick_and_morty_rest_app` directory and push it to Docker Hub.  
    Tags:
    - `:latest`
    - `:${VERSION}` (from DOCKER_VARS)

**Outcome:**  
A successful run results in a tested and validated Docker image pushed to Docker Hub.

### CD Workflow (cd.yaml)

**Location:** `.github/workflows/cd.yaml`

**Trigger:**
- `workflow_run` event:
  - Runs when the `CI` workflow has completed successfully.

**Steps:**

1. **Checkout code:**  
   Pulls down the repository code to the runner.

2. **Set up Minikube:**  
   Uses `medyagh/setup-minikube@latest` to create a local Kubernetes cluster on the runner.

3. **Enable Minikube Ingress:**  
   `minikube addons enable ingress` to install the NGINX Ingress Controller in the cluster.

4. **Install kubectl and helm:**  
   Uses `yokawasa/action-setup-kube-tools@v0.11.2` to install `kubectl` and `helm`.

5. **Wait for Ingress Controller:**  
   Waits until the ingress controller pod is ready in the `ingress-nginx` namespace.

6. **Helm install application:**  
   Runs `helm install` to deploy the `rickandmorty` chart into the `rick-and-morty` namespace with ingress enabled.

7. **Wait for Pods to be Ready:**  
   Uses `kubectl wait` to ensure the deployed pods are up and running.

8. **Get pods and services:**  
   For debugging and verification, `kubectl get` commands are run to list pods and services.

9. **Port forward service:**  
   For testing the application endpoints, it port-forwards the `rickandmorty` service to localhost port 5010.

10. **Test endpoints:**
    - `curl http://localhost:5010/characters_data` to verify the characters endpoint.
    - `curl http://localhost:5010/healthcheck` to verify the health endpoint.

**Outcome:**  
If these steps pass, it confirms that the application was successfully deployed and is working as expected inside the Minikube cluster.

---
## Screenshots



