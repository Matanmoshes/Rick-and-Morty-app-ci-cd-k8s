### README.md

# Rick & Morty Kubernetes Deployment

## Overview
This guide explains how to deploy the **Rick & Morty Character Explorer** application to a Kubernetes cluster using `kubectl`. The deployment includes the following Kubernetes manifests:
- `deployment.yaml` to create pods and manage replicas.
- `service.yaml` to expose the application via a LoadBalancer.
- `ingress.yaml` to manage external access via an Ingress Controller.

The app is deployed on a bare-metal Kubernetes cluster with MetalLB configured for external IP assignment.

```
yamls
    ├── README.md
    ├── deployment.yaml
    ├── ingress.yaml
    ├── metallb-ipaddresspool.yaml
    ├── metallb-l2advertisement.yaml
    └── service.yaml

```

---

## Prerequisites
1. **Kubernetes Cluster**:
   - A running Kubernetes cluster (e.g., created using `kubeadm`).
2. **Ingress Controller**:
   - NGINX Ingress Controller installed and configured.
3. **MetalLB**:
   - Installed and configured for LoadBalancer support on bare-metal.
4. **Docker Image**:
   - Ensure the image `matanm66/rickandmorty:v1.0` is accessible to your cluster.
5. **kubectl**:
   - Installed and configured to manage your cluster.

---

## MetalLB Configuration

1. **Install MetalLB**:
   ```bash
   kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.14.8/config/manifests/metallb-native.yaml
   ```

2. **Create the Memberlist Secret**:
   ```bash
   kubectl create secret generic -n metallb-system memberlist --from-literal=secretkey="$(openssl rand -base64 128)"
   ```

3. **Define an IP Address Pool**:
   Create `metallb-ipaddresspool.yaml`:
   ```yaml
   apiVersion: metallb.io/v1beta1
   kind: IPAddressPool
   metadata:
     name: default-addresspool
     namespace: metallb-system
   spec:
     addresses:
     - 10.0.1.200-10.0.1.210  
   ```

   Apply the configuration:
   ```bash
   kubectl apply -f metallb-ipaddresspool.yaml
   ```

4. **Configure L2 Advertisement**:
   Create `metallb-l2advertisement.yaml`:
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

   Apply the configuration:
   ```bash
   kubectl apply -f metallb-l2advertisement.yaml
   ```

---

## Deployment Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Matanmoshes/Rick-and-Morty-app-ci-cd-k8s
   cd Rick-and-Morty-app-ci-cd-k8s
   ```

2. **Apply Kubernetes Manifests**:
   Deploy the application using the manifests:
   ```bash
   kubectl apply -f deployment.yaml
   kubectl apply -f service.yaml
   kubectl apply -f ingress.yaml
   ```

3. **Verify Deployments**:
   Check that the pods are running:
   ```bash
   kubectl get pods
   ```
   Expected Output:
   ```plaintext
   NAME                                    READY   STATUS    RESTARTS   AGE
   rickandmorty-deployment-xxxxx           1/1     Running   0          1m
   rickandmorty-deployment-yyyyy           1/1     Running   0          1m
   ```
![Screenshot 2024-12-14 at 21 46 13](https://github.com/user-attachments/assets/ae1f08c1-81e6-4104-a2cd-455db86459dd)



   Verify the service:
   ```bash
   kubectl get svc
   ```
   Expected Output:
   ```plaintext
   NAME                    TYPE           CLUSTER-IP      EXTERNAL-IP       PORT(S)        AGE
   rickandmorty-service    LoadBalancer   10.96.101.120   10.0.1.200        80:32123/TCP   1m
   ```
![Screenshot 2024-12-14 at 21 46 33](https://github.com/user-attachments/assets/a9848c69-2d57-4add-ba75-e9ca0b5de1da)


   Check the ingress:
   ```bash
   kubectl get ingress
   ```
   Expected Output:
   ```plaintext
   NAME                  CLASS   HOSTS             ADDRESS       PORTS   AGE
   rickandmorty-ingress  nginx   rickandmorty.local 10.0.1.200   80      1m
   ```

![Screenshot 2024-12-14 at 21 47 08](https://github.com/user-attachments/assets/4e479a92-eb69-4f3a-9487-533fd32aba11)

---

## Accessing the Application

### 1. **DNS Configuration**:
   Update your `/etc/hosts` file to point `rickandmorty.local` to the external IP (e.g., `10.0.1.200`):
   ```plaintext
   10.0.1.200 rickandmorty.local
   ```

### 2. **Access the Application**:
   Open your browser and visit:
   - **Home Page**: `http://rickandmorty.local/`
   - **Characters**: `http://rickandmorty.local/characters`
   - **Download CSV**: `http://rickandmorty.local/download`
   - **Health Check**: `http://rickandmorty.local/healthcheck`

![Screenshot 2024-12-14 at 21 49 28](https://github.com/user-attachments/assets/2fda718b-34a7-46a0-a469-d1c800b0e12d)

---

## Troubleshooting

1. **Pods Not Running**:
   Check the logs for errors:
   ```bash
   kubectl logs <pod-name>
   ```

2. **Ingress Not Working**:
   Ensure the NGINX Ingress Controller is installed and running:
   ```bash
   kubectl get pods -n ingress-nginx
   ```

3. **Service IP Not Assigned**:
   Verify MetalLB configuration:
   ```bash
   kubectl get pods -n metallb-system
   kubectl describe ipaddresspool default-addresspool -n metallb-system
   ```

---

## Cleanup
To remove the application:
```bash
kubectl delete -f ingress.yaml
kubectl delete -f service.yaml
kubectl delete -f deployment.yaml
```
