# Backend

This is the backend server written on FastAPI and using Postgres as a database.

1. Go to backend directory: 
    ```bash
    cd backend
    ```

2. Create `.env` file with the following variables:
    ```env
    DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres
    SENDGRID_API_KEY=<YOUR SENDGRID API KEY>
    FROM_EMAIL=<EMAIL THAT WILL SEND LOGIN LINKS TO USERS>
    REAL_EMAIL_API_LINK=<YOUR REAL EMAIL API LINK>
    REAL_EMAIL_API_KEY=<YOUR REAL EMAIL API KEY>
    ```

3. To build the backend Dockerfile: 
    ```bash
    DOCKER_BUILDKIT=1 docker build -t backend .
    ```

## Contacts

If you have any questions or ideas, write me in [Telegram](https://telegram.org):
- [@rufusnufus](https://t.me/rufusnufus/)
