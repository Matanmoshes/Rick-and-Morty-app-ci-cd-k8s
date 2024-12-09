# Rick and Morty App

## Description 
This project is devide to four section
1. Rick and Morty Rest API app
2. Running the app on K8S
3. Helm chart for the Rick and Morty app

---

## Rick and Morty Rest API app
This application queries the Rick and Morty API at startup to find all characters who are:
- Species: Human
- Status: Alive
- Origin: Contains "Earth"

It then hosts the results on a REST endpoint, allowing you to retrieve them as JSON.

#### How to Build and Run the Docker Image

1. **Build the Docker image:**
   ```bash
   docker build -t my-rick-and-morty-app .
   ```

2. **Run the Docker container:**
   ```bash
   docker run -d -p 5010:5010 --name rick-app my-rick-and-morty-app
   ```
   
   This maps the container’s port 5010 to your host’s port 5010.
   
3. **Test the application:**
   - Healthcheck:
     ```bash
     curl http://localhost:5010/healthcheck
     ```
     Expected response:
     ```json
     {
       "status": "OK"
     }
     ```
   
   - Get Characters Data:
     ```bash
     curl http://localhost:5010/characters
     ```
     Expected response: JSON array of characters similar to:
     ```json
     [
       {
         "Name": "Rick Sanchez",
         "Location": "Citadel of Ricks",
         "Image": "https://rickandmortyapi.com/api/character/avatar/1.jpeg"
       },
       {
         "Name": "Summer Smith",
         "Location": "Earth (Replacement Dimension)",
         "Image": "https://rickandmortyapi.com/api/character/avatar/3.jpeg"
       },
       ...
     ]
     ```

>[!Notes]
>- The data is fetched only once at application startup. If you need updated data, restart the container.
>- Adjust the `Dockerfile` and `requirements.txt` as necessary for your environment and dependency versions.
>- The default port is `5000`. If you change this inside the Dockerfile or code, update the `docker run` command accordingly.

---

# Rick and Morty REST Application on Kubernetes

## Overview
This repository contains Kubernetes manifests (`Deployment.yaml`, `Service.yaml`, and `Ingress.yaml`) for deploying the Rick and Morty RESTful API application. The application provides filtered character data from the Rick and Morty API and exposes two main endpoints:

- **/healthcheck** for checking the service status.
- **/characters** for retrieving the filtered character data.

## Prerequisites
- A running Kubernetes cluster (using kind, minikube, kubeadm, or any other distribution) i used kubeadm.
- An ingress controller installed and configured (e.g., NGINX Ingress Controller).
- Im on a bare-metal environment and using kubeadm on EC2, im using a load balancer solution like MetalLB for external IP assignment.
- The Docker image `matanm66/rickandmorty:v1.0` should be available to your cluster (pushed to a container registry accessible by the cluster, or loaded directly into kind/minikube using their respective commands).

#### **Install MetalLB on kubeadm cluster**

1. install the yaml file
```bash
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.14.8/config/manifests/metallb-native.yaml
```

2. Create the `memberlist` Secret

MetalLB uses the `memberlist` protocol for internal communication between `speaker` pods.

```bash
kubectl create secret generic -n metallb-system memberlist --from-literal=secretkey="$(openssl rand -base64 128)"
```

**If the secret already exists, delete and recreate it:**

```bash
kubectl delete secret memberlist -n metallb-system
kubectl create secret generic -n metallb-system memberlist --from-literal=secretkey="$(openssl rand -base64 128)"
```

**Verify the Secret:**

```bash
kubectl describe secret memberlist -n metallb-system
```

**Expected Output:**

```plaintext
Name:         memberlist
Namespace:    metallb-system
Type:         Opaque

Data
====
secretkey:  174 bytes
```

3. Create an `IPAddressPool`

Define the range of IP addresses that MetalLB can assign to `LoadBalancer` services.

**Create `metallb-ipaddresspool.yaml`:**

```yaml
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: default-addresspool
  namespace: metallb-system
spec:
  addresses:
  - 10.0.1.200-10.0.1.210  # Update this range to match your available IPs
```

**Apply the Configuration:**

```bash
kubectl apply -f metallb-ipaddresspool.yaml
```

4. Create an `L2Advertisement`

Configure MetalLB to announce IPs using Layer 2 mode.

**Create `metallb-l2advertisement.yaml`:**

```yaml
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: default-l2advertisement
  namespace: metallb-system
spec:
  ipAddressPools:
  - default-addresspool
```

**Apply the Configuration:**

```bash
kubectl apply -f metallb-l2advertisement.yaml
```

5. Verify MetalLB Installation

6. Check MetalLB Pods

```bash
kubectl get pods -n metallb-system
```

**Expected Output:**

```plaintext
NAME                           READY   STATUS    RESTARTS   AGE
controller-77676c78d9-qmncn    1/1     Running   0          10m
speaker-5bxm8                  1/1     Running   0          10m
speaker-c22gc                  1/1     Running   0          10m
...
```

All `controller` and `speaker` pods should be in the `Running` state.


7. Check Services

Ensure that the MetalLB webhook service is running:

```bash
kubectl get svc -n metallb-system
```

**Expected Output:**

```plaintext
NAME                   TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
metallb-webhook-service ClusterIP   10.96.0.1       <none>        443/TCP   10m
```

## Manifests
The `yamls` directory contains the following files:

- `Deployment.yaml`: Defines a Deployment for the Rick and Morty application with multiple replicas.
- `Service.yaml`: Defines a Service (type: LoadBalancer) to expose the application internally and, with MetalLB or a cloud provider’s load balancer, externally.
- `Ingress.yaml`: Defines an Ingress resource to route HTTP traffic to the Service using a specified hostname.

## Steps to Deploy

1. **Apply the Manifests:**
   ```bash
   kubectl apply -f yamls/Deployment.yaml
   kubectl apply -f yamls/Service.yaml
   kubectl apply -f yamls/Ingress.yaml
   
   This will create the Deployment, Service, and Ingress resources in your cluster.

2. **Verify Resource Creation:**
   Check that your resources have been created successfully:
   ```bash
   kubectl get deployments
   kubectl get services
   kubectl get ingress
   ```
   
   You should see the `rickandmorty-deployment`, `rickandmorty-service`, and `rickandmorty-ingress` listed.

3. **Configure Hostname Resolution:**
   - The provided `Ingress.yaml` uses `rickandmorty.local` as a host.
   - If you’re using minikube or kind, you can retrieve the ingress controller’s IP address (often the minikube IP or the LoadBalancer IP assigned by MetalLB) and add it to your `/etc/hosts` file:
     ```bash
     echo "<EXTERNAL_IP> rickandmorty.local" | sudo tee -a /etc/hosts
     ```
   
   Replace `<EXTERNAL_IP>` with the actual IP address of the LoadBalancer or the node where the ingress is exposed. If using minikube:
   ```bash
   minikube ip
   ```
   Then map that IP to `rickandmorty.local`.

4. **Accessing the Application:**
   Once DNS resolution is set up (via `/etc/hosts` or DNS), you can access the endpoints:
   
   - View the load balancer service ip:
   ```bash
    ubuntu@ip-10-0-1-100:~/yaml$ kubectl get svc
    NAME                   TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
    kubernetes             ClusterIP      10.96.0.1       <none>        443/TCP        90m
    rickandmorty-service   LoadBalancer   10.98.255.250   10.0.1.200    80:30687/TCP   6m2s
   ```

   - Run health on loclahost:
   ```Bash
    ubuntu@ip-10-0-1-100:~/yaml$ curl http://10.0.1.200/healthcheck
    {"status":"OK"}
   ```

   - Health Check Endpoint:
     ```bash
     curl http://rickandmorty.local/healthcheck
     ```
     Expected response:
     ```json
     {"status":"OK"}
     ```
   
   - Characters Data Endpoint:
     ```bash
     curl http://rickandmorty.local/characters
     ```
     Expected response: A JSON array containing characters that are human, alive, and originate from variants of "Earth."


---

# Rick and Morty Helm Chart

This Helm chart deploys the Rick and Morty REST application on a Kubernetes cluster.

## Prerequisites
- A running Kubernetes cluster.
- Helm 3 installed.
- An ingress controller configured if you want to use the ingress resource (e.g. Nginx Ingress Controller).
- Optionally, a load balancer solution like MetalLB if on bare metal and using `LoadBalancer` type Services.

## Helm chart structure:

```
helm
└── rickandmorty
    ├── chart.yml
    ├── templates
    │   ├── _helpers.tpl
    │   ├── deployment.yml
    │   ├── ingress.yml
    │   └── service.yml
    └── values.yml

```


## Installing the Chart

1. Ensure that your Docker image (`matanm66/rickandmorty:v1.0` by default) is accessible by your cluster.

2. Navigate to the directory containing the Helm chart:
   ```bash
   cd helm/rickandmorty

3. Install the chart with a release name, e.g. `my-release`:
   ```bash
   helm install my-release .
   ```

   This command will:
   - Deploy the `rickandmorty` Deployment.
   - Create a Service of type `LoadBalancer`.
   - Create an Ingress if enabled (by default it is).

## Uninstalling the Chart
To remove the release and all associated resources:
```bash
helm uninstall my-release
```

## Accessing the Application

- **Ingress Access**:
  If the ingress is enabled and configured with `rickandmorty.local` as the host, you need to point that hostname to your ingress controller’s external IP. For example:
  ```bash
  echo "<INGRESS_CONTROLLER_IP> rickandmorty.local" | sudo tee -a /etc/hosts
  ```
  Then:
  ```bash
  curl http://rickandmorty.local/healthcheck
  curl http://rickandmorty.local/characters
  ```

- **Service Access**:
  If you’re using a `LoadBalancer` service and MetalLB or a cloud provider’s load balancer assigns an external IP, run:
  ```bash
  kubectl get svc
  ```
  and find the external IP of `my-release-rickandmorty`. Then:
  ```bash
  curl http://<EXTERNAL_IP>/healthcheck
  curl http://<EXTERNAL_IP>/characters
  ```

## Customizing Values

You can modify the `values.yaml` file to change:
- `replicaCount`: Number of application replicas.
- `image.repository`, `image.tag`: Docker image and tag.
- `service.type`, `service.port`, `service.targetPort`: Service type and ports.
- `ingress.enabled`, `ingress.host`, `ingress.className`: Ingress configuration.

For example, to override values without editing the file directly:
```bash
helm install my-release . --set replicaCount=3 --set ingress.enabled=false
```
