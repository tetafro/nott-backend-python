# Build project

## JS compiler

```
sudo npm install -g requirejs uglify-js
cd project/public/js/
r.js -o build.js
```

## Run

```
Build:
docker build -f configs/docker/build -t nott-build .
Run
docker run \
    --rm \
    --volume /home/tetafro/IT/projects/pet/nott:/srv \
    --workdir /srv/ \
    --tty \
    nott-build \
    scripts/build.sh
```
