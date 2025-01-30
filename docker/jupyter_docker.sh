#!/usr/bin/env bash

IMAGE_NAME=jupyter_img
CONTAINER_NAME=jupyter_cont
JUPYTER_PORT=8888

case $1 in
  build)
    docker build . -t $IMAGE_NAME --platform linux/x86_64
    ;;

  run)
    docker run \
      -v "$PWD"/workspace:/workspace \
      -d \
      -p $JUPYTER_PORT:$JUPYTER_PORT \
      --name $CONTAINER_NAME \
      $IMAGE_NAME
    ;;

  token)
    docker exec $CONTAINER_NAME jupyter notebook list
    ;;

  bash)
    docker exec -it $CONTAINER_NAME /bin/bash
    ;;

  stop)
    docker stop $CONTAINER_NAME
    ;;

  remove)
    docker rm $CONTAINER_NAME
    ;;

  *)
    echo "Unknown command. Please provide a valid command: build | run | token | bash | stop | remove"
    ;;
esac
