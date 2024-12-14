### README.md

# Rick & Morty Character Explorer

## Overview
The **Rick & Morty Character Explorer** is a Flask-based web application that allows users to explore human characters who are alive and originate from Earth-like locations in the Rick and Morty universe. The app provides a visual interface, downloadable CSV files, and JSON REST API endpoints for programmatic data access.

---

## Requirements
To run the application, ensure you have the following:
- Python 3.x installed locally
- Docker installed (if running as a container)
- Required Python dependencies (from `requirements.txt`)

---

## Folder Structure
```
rick_and_morty_rest_app/
├── DOCKER_VARS             
├── Dockerfile              
├── README.md               
├── __init__.py             
├── app.py                  
├── characters.csv          
├── requirements.txt        
├── static/                 
│   ├── background.png
│   ├── rick-and-morty-toilets.jpg
│   └── space_background.png
├── templates/              
│   ├── 404.html
│   ├── 500.html
│   ├── characters.html
│   └── index.html
```

---

## Building and Running the Docker Image

### 1. **Build the Docker Image**
Navigate to the project directory and build the Docker image:
```bash
docker build -t rick-and-morty-app .
```

### 2. **Run the Docker Container**
Run the container while exposing port `5010`:
```bash
docker run -d -p 5010:5010 --name rick_and_morty_container rick-and-morty-app
```

The app will now be accessible at `http://localhost:5010`.

---

## REST API Endpoints

### **1. Home Page**
- **URL**: `/`
- **Method**: `GET`
- **Description**: Displays the home page with links to the available features.

---

### **2. Service Health Check**
- **URL**: `/healthcheck`
- **Method**: `GET`
- **Description**: Returns the health status of the service.
- **Sample Response**:
    ```json
    {
        "status": "OK"
    }
    ```

---

### **3. View Characters**
- **URL**: `/characters`
- **Method**: `GET`
- **Description**: Displays a list of characters in a visually styled HTML page.

---

### **4. Download CSV**
- **URL**: `/download`
- **Method**: `GET`
- **Description**: Downloads a CSV file containing character data.

---

### **5. Fetch Characters Data as JSON**
- **URL**: `/characters_data`
- **Method**: `GET`
- **Description**: Returns character data in JSON format.
- **Sample Response**:
    ```json
    [
        {
            "Name": "Rick Sanchez",
            "Location": "Earth (C-137)",
            "Image": "https://rickandmortyapi.com/api/character/avatar/1.jpeg"
        },
        {
            "Name": "Morty Smith",
            "Location": "Earth (C-137)",
            "Image": "https://rickandmortyapi.com/api/character/avatar/2.jpeg"
        }
    ]
    ```

---

## How to Fetch Data
To programmatically fetch data from the API, you can use `curl` or a tool like Postman:

1. **Fetch JSON Data**:
   ```bash
   curl http://localhost:5010/characters_data
   ```

2. **Download the CSV**:
   ```bash
   curl -O http://localhost:5010/download
   ```

---

## Author
Project by [Matan Moshe](https://github.com/Matanmoshes/Rick-and-Morty-app-ci-cd-k8s).