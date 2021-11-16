## Building a Docker image

This app's Dockerfile requires [BuildKit](https://docs.docker.com/develop/develop-images/build_enhancements/):

```sh
env DOCKER_BUILDKIT=1 docker build . -t bts-parking-frontend:1.0.0
```

The image exposes port 3000 on the container for the application.
