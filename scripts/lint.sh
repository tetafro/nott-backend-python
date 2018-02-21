#!/bin/bash

for command in eslint flake8 pylint; do
    if ! hash $command 2>/dev/null; then
        echo Error: $command is not installed
        exit 1
    fi
done

echo '>>'
echo '> ESLint'
echo '>>'
find ./project/public/js/src \
    -name '*.js' \
    -exec echo '>>> ' {} \; \
    -exec eslint -c .eslintrc.json {} \;

echo '>>'
echo '> Flake8'
echo '>>'
find ./project/apps \
    -not \( -path './project/apps/*/migrations' -prune \) \
    -not -path "*/__pycache__/*" \
    -not -path "*/migrations/*" \
    -name '*.py' \
    -exec echo '>>> ' {} \; \
    -exec flake8 {} \;
find ./project/core \
    -not \( -name 'manage.py' \) \
    -not -path "*/__pycache__/*" \
    -not -path "*/migrations/*" \
    -exec echo '>>> ' {} \; \
    -exec flake8 {} \;

echo '>>'
echo '> PyLint'
echo '>>'
find ./project/apps \
    -not \( -path './project/apps/*/migrations' -prune \) \
    -not -path "*/__pycache__/*" \
    -not -path "*/migrations/*" \
    -name '*.py' \
    -exec echo '>>> ' {} \; \
    -exec pylint {} \;
find ./project/core \
    -not \( -name 'manage.py' \) \
    -not -path "*/__pycache__/*" \
    -not -path "*/migrations/*" \
    -exec echo '>>> ' {} \; \
    -exec pylint {} \;
