find ../project/apps \
    -not \( -path '../project/apps/*/migrations' -prune \) \
    -not -path "*/__pycache__/*" \
    -name '*.py' \
    -exec echo '>>> ' {} \; \
    -exec pep8 {} \; \
    > pep8.log

find ../project/core \
    -not \( -name 'manage.py' \) \
    -not -path "*/__pycache__/*" \
    -exec echo '>>> ' {} \; \
    -exec pep8 {} \; \
    >> pep8.log
