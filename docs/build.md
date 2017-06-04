# Build project

## JS compiler

```
sudo npm install -g requirejs uglify-js
cd project/public/js/
r.js -o build.js
```

## Run

```
docker build -f configs/docker/build -t nott-build .
docker run \
    --rm \
    --volume /home/tetafro/IT/projects/pet/nott:/srv \
    --workdir /srv/ \
    --tty \
    nott-build \
    scripts/build.sh
```
