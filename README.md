# Game Order FastAPI Project

This project, **Game Order**, is a FastAPI application designed to manage game orders. The application uses PostgreSQL as its database and Redis for caching purposes. The project is containerized using Docker, making it easy to set up and run in any environment.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Running the Application](#running-the-application)
- [Stopping the Application](#stopping-the-application)


## Prerequisites

Make sure you have the following installed on your machine:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

To get started with the Game Order application, follow these steps:


## Getting Started

1. **Clone the Repository**:

   ```sh
   git clone https://github.com/yourusername/game-order.git
   cd game-order
   
## Running the Application

1. **Build and Start the Services**

   To build the Docker images and start the services defined in `docker-compose.yml`, run the following command in the root of the project:

   ```sh
   docker-compose up --build
2. **Access the Application**
   
    Once the containers are up and running, you can access The interactive API documentation (Swagger UI) at:
   
   ```sh
   http://localhost:8000/docs
## Stopping the Application
   To stop the application and remove the containers, run:
   ```sh
   docker-compose down


