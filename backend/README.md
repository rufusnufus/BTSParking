# Backend

This is the backend server written on FastAPI and using Postgres as a database. In addition, we install pgAdmin in our docker-compose to see our Database easily. Also, we are using alembic for db migrations.

0. Go to backend directory: 
    ```bash
    cd backend
    ```

1. To build the backend: 
    ```bash
    docker-compose build
    ```
2. *To make migration: 
    ```bash
    docker-compose run web alembic revision --autogenerate
    ```

3. *To run the migration: 
    ```bash
    docker-compose run web alembic upgrade head
    ```

4. To run the backend: 
    ```bash
    docker-compose up
    ```
5. Go to [localhost:8000/docs](localhost:8000/docs) to interact with API.
