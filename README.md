<p>
<img src="images/logo.png" width="600px" alt="BTSParking"/>&nbsp;
</p>

![Svelte](https://img.shields.io/badge/svelte-%23f1413d.svg?style=for-the-badge&logo=svelte&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
[![GitHub license](https://img.shields.io/badge/license-mit-orange.svg?style=for-the-badge)](https://github.com/rufusnufus/btsparking/blob/main/LICENSE)
[![GitHub contributors](https://img.shields.io/github/contributors/rufusnufus/btsparking?style=for-the-badge)](https://github.com/rufusnufus/btsparking/graphs/contributors)

## Overview
A web application with ability to reserve parking spaces and get parking usage statistics.

In addition, here you can find our [API Design](https://github.com/rufusnufus/btsparking/blob/main/openapi.yaml), [Feature List](https://github.com/rufusnufus/btsparking/blob/main/FeatureList.md), [Concept Design](https://www.figma.com/file/lD5kokYM41T9ARgYedur8B/ParKovKa?node-id=0%3A1) and [Lean Canvas](https://miro.com/app/board/o9J_llilfDA=/?invite_link_id=839831490288).

## Getting Started

### Docker installation
Before running the application, please install its prerequisites:
* [Docker 20.10.7+](https://docs.docker.com/get-docker/)

To run from the master branch, follow the instructions below:
1. Clone web application repository locally.
    ```bash
    git clone https://github.com/rufusnufus/BTSParking.git
    cd BTSParking
    ```
2. [Optional] Build the docker-compose.
    ```bash
    docker-compose build
   ```
3. Run the services. Web app will open at [http://127.0.0.1:80/](http://localhost:80/). Backend of the app is available at [http://127.0.0.1:8000/docs](http://localhost:8000/docs).
    ```
    docker-compose up -d
    ```
