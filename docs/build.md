# Build project

```
docker build -f configs/dockerfiles/build -t nott-build .
docker run \
    --rm \
    --volume /home/tetafro/IT/projects/pet/nott:/srv \
    --workdir /srv/ \
    --tty \
    nott-build \
    scripts/build.sh
```
