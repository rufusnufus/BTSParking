<p>
<img src="./images/banner-for-github.svg" width="100%" alt="BTS.Parking banner with a logo" />&nbsp;
</p>

![Svelte](https://img.shields.io/badge/svelte-%23f1413d.svg?style=for-the-badge&logo=svelte&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
[![GitHub license](https://img.shields.io/badge/license-mit-orange.svg?style=for-the-badge)](https://github.com/rufusnufus/btsparking/blob/main/LICENSE)
[![GitHub contributors](https://img.shields.io/github/contributors/rufusnufus/btsparking?style=for-the-badge)](https://github.com/rufusnufus/btsparking/graphs/contributors)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=rufusnufus_BTSParking&metric=alert_status)](https://sonarcloud.io/dashboard?id=rufusnufus_BTSParking)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=rufusnufus_BTSParking&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=rufusnufus_BTSParking)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=rufusnufus_BTSParking&metric=bugs)](https://sonarcloud.io/dashboard?id=rufusnufus_BTSParking)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=rufusnufus_BTSParking&metric=code_smells)](https://sonarcloud.io/dashboard?id=rufusnufus_BTSParking)
<br>

# BTS.Parking

## Overview
A web application with ability to reserve parking spaces and get parking usage statistics.

In addition, you may refer to our [API Design](https://github.com/rufusnufus/btsparking/blob/main/openapi.yaml), [Feature List](https://github.com/rufusnufus/btsparking/blob/main/FeatureList.md), [UI Design](https://www.figma.com/file/lD5kokYM41T9ARgYedur8B/ParKovKa?node-id=0%3A1) and [Lean Canvas](https://miro.com/app/board/o9J_llilfDA=/?invite_link_id=839831490288).

## Getting Started

### Docker installation
Before running the application, please, install its prerequisites:
* [Docker 20.10.7+](https://docs.docker.com/get-docker/)

To run from the `main` branch, follow the instructions below:
1. Clone the repository:
   ```bash
   git clone https://github.com/rufusnufus/BTSParking.git
   cd BTSParking
   ```
2. Add environment variables to the backend (see [backend/README.md](./backend/README.md)).
3. Run the services:
   ```bash
   DOCKER_BUILDKIT=1 docker-compose up -d
   ```
   The web app will be available at [localhost](http://localhost). OpenAPI documentation for the API will be available at [localhost:8000/docs](http://localhost:8000/docs).
