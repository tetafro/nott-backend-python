#!/bin/bash

LOG=linters.log
: > $LOG

echo '>>      ' >> $LOG
echo '> ESLint' >> $LOG
echo '>>      ' >> $LOG
find ./project/public/js/src \
    -name '*.js' \
    -exec echo '>>> ' {} \; \
    -exec eslint -c .eslintrc.json {} \; \
    >> $LOG

echo '>>    ' >> $LOG
echo '> PEP8' >> $LOG
echo '>>    ' >> $LOG
find ./project/apps \
    -not \( -path './project/apps/*/migrations' -prune \) \
    -not -path "*/__pycache__/*" \
    -name '*.py' \
    -exec echo '>>> ' {} \; \
    -exec pep8 {} \; \
    >> $LOG
find ./project/core \
    -not \( -name 'manage.py' \) \
    -not -path "*/__pycache__/*" \
    -exec echo '>>> ' {} \; \
    -exec pep8 {} \; \
    >> $LOG

echo '>>      ' >> $LOG
echo '> Flake8' >> $LOG
echo '>>      ' >> $LOG
find ./project/apps \
    -not \( -path './project/apps/*/migrations' -prune \) \
    -not -path "*/__pycache__/*" \
    -name '*.py' \
    -exec echo '>>> ' {} \; \
    -exec pyflakes {} \; \
    >> $LOG
find ./project/core \
    -not \( -name 'manage.py' \) \
    -not -path "*/__pycache__/*" \
    -exec echo '>>> ' {} \; \
    -exec pyflakes {} \; \
    >> $LOG
