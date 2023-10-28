# NeuraMesh
For VandyHacks 2024

Build the docker image with:
```
docker build -t neuramesh .
```

To start a docker instance to handle jobs, run:
```
docker run -e REDIS_HOST=redis-17437.c284.us-east1-2.gce.cloud.redislabs.com -e REDIS_PORT=17437 -it neuramesh
```

