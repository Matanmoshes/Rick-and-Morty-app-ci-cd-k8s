# Rick and Morty App CI/CD Pipeline

This repository includes two GitHub Actions workflows:

1. **CI (Continuous Integration)**: Defined in `.github/workflows/ci.yaml`
2. **CD (Continuous Deployment)**: Defined in `.github/workflows/cd.yaml`

The CI workflow is triggered on every push or pull request to the `main` branch. It runs tests, and if successful, builds and pushes a Docker image to Docker Hub. The CD workflow is triggered after the CI workflow completes successfully. It sets up a local Kubernetes cluster (using minikube), deploys the application via Helm, and tests the running service.

## CI Workflow Overview (`ci.yaml`)

**Trigger:**
- On push and pull_request to `main`.

**Jobs:**

### test_app
- **runs-on:** `ubuntu-latest`
- **Steps:**
  1. **Checkout code:** Uses `actions/checkout@v4` to fetch the repository code.
  2. **Set up Python:** Uses `actions/setup-python@v4` to install Python 3.10.
  3. **Install dependencies:** Installs application and test dependencies from `requirements.txt`.
  4. **Set PYTHONPATH:** Ensures that the application can be found during tests.
  5. **Run tests:** Runs `pytest` to execute unit tests. If tests fail, the job stops, preventing further steps.

If the tests pass, the workflow moves on to the next job.

### build_push
- **needs:** `test_app` (this job only runs if `test_app` passes)
- **runs-on:** `ubuntu-latest`
- **Steps:**
  1. **Checkout code:** Fetches the repository code again.
  2. **Load environment variables:** Sources a file (`DOCKER_VARS`) containing Docker image info and sets them as environment variables.
  3. **Set up Docker Buildx:** Prepares the environment for building multi-architecture Docker images.
  4. **Login to DockerHub:** Authenticates with Docker Hub using secrets for username/password.
  5. **Build and push Docker image:** Uses `docker/build-push-action` to build the image from `rick_and_morty_rest_app/Dockerfile` and push it to Docker Hub with two tags (`VERSION` and `latest`).

At the end of the CI workflow, you have a tested and built Docker image in your Docker Hub repository.

## CD Workflow Overview (`cd.yaml`)

**Trigger:**
- On `workflow_run` completion of the CI workflow (only when CI finishes successfully).

**Jobs:**

### build-and-test
- **runs-on:** `ubuntu-latest`
- **Steps:**
  1. **Checkout Code:** Uses `actions/checkout@v4` to fetch the repository code.
  2. **Setup Minikube:** Uses `medyagh/setup-minikube@latest` to start a local Kubernetes cluster in the runner environment.
  3. **Enable Minikube Ingress:** Enables the NGINX Ingress controller addon in minikube.
  4. **Install kubectl and helm:** Uses `yokawasa/action-setup-kube-tools` to install `kubectl` and `helm`.
  5. **Wait for Ingress Controller:** Uses `kubectl wait` commands to ensure the ingress controller is ready before deploying the application.
  6. **Helm install application:** Runs `helm install` to deploy the `rickandmorty` Helm chart, enabling ingress.
  7. **Wait for Pods to be Ready:** Uses `kubectl wait` to ensure the pods defined by the Helm chart are running and ready.
  8. **Get pods and services:** Lists pods and services for debugging.
  9. **Port forward service:** Sets up port-forwarding from the cluster’s service to the local host, making the app accessible via `http://localhost:5010`.
  10. **Sleep:** Waits a moment to ensure port-forward is established.
  11. **Test characters endpoint:** Uses `curl` to hit `http://localhost:5010/characters_data` and expects a 200 response.
  12. **Sleep:** A short pause before the next test.
  13. **Test healthcheck endpoint:** Uses `curl` again to test `http://localhost:5010/healthcheck`.

If both endpoints respond as expected, the CD job finishes successfully. This ensures that the newly built image from CI can run and is functional within a local Kubernetes environment.

## Summary of the Pipeline

- **CI**:
  - Checks out code, installs dependencies, and runs tests.
  - If tests pass, builds and pushes a Docker image to Docker Hub.
  
- **CD**:
  - Triggered after CI succeeds.
  - Sets up a local Kubernetes environment with minikube.
  - Deploys the application using Helm into the `rick-and-morty` namespace.
  - Waits for pods and services to be ready.
  - Port-forwards the service and tests endpoints locally to confirm the application is running correctly.

## How to Use

- Push changes to `main` or open a pull request against `main`.
- The CI workflow will run tests and, if successful, produce a new Docker image.
- After CI completes, the CD workflow will start, deploy the application, and test it in a minikube environment.

