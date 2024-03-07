docker build -f Dockerfile-multistage-build -t trannhatnguyen2/sentiment:v1.0.0 .
docker push trannhatnguyen2/sentiment:v1.0.0
# docker run --net=host --gpus all docker.io/trannhatnguyen2/sentiment:v1.0.0