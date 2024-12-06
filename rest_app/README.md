### README.md
#### Description
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

#### REST API Endpoints

- **GET /healthcheck**
  - Returns a simple JSON response indicating the service is running.
  - Example:
    ```bash
    curl http://localhost:5010/healthcheck
    ```
    ```json
    {"status":"OK"}
    ```
  
- **GET /characters**
  - Returns the filtered characters as JSON.
  - Example:
    ```bash
    curl http://localhost:5010/characters
    ```
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

#### Notes
- The data is fetched only once at application startup. If you need updated data, restart the container.
- Adjust the `Dockerfile` and `requirements.txt` as necessary for your environment and dependency versions.
- The default port is `5000`. If you change this inside the Dockerfile or code, update the `docker run` command accordingly.