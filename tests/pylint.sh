find ../project/apps \
    -not \( -path '../project/apps/*/migrations' -prune \) \
    -not -path "*/__pycache__/*" \
    -name '*.py' \
    -exec echo '>>> ' {} \; \
    -exec pylint --reports=n --disable=F0401,C0111 {} \; \
    > pylint.log

find ../project/core \
    -not \( -name 'manage.py' \) \
    -not -path "*/__pycache__/*" \
    -exec echo '>>> ' {} \; \
    -exec pylint --reports=n --disable=F0401,C0111 {} \; \
    >> pylint.log
