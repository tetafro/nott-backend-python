find .. \
    -not \( -path '../venv' -prune \) \
    -not \( -path '../*/migrations' -prune \) \
    -not \( -name 'wsgi.py' \) \
    -not \( -name '__init__.py' \) \
    -not \( -name 'manage.py' \) \
    -not \( -name 'populate.py' \) \
    -name '*.py' \
    -exec echo '>>> ' {} \; \
    -exec pylint --reports=n --disable=F0401,C0111 {} \;
