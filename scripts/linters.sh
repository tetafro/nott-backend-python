LOG=linters.log
: > $LOG

echo '>>    ' >> $LOG
echo '> JSCS' >> $LOG
echo '>>    ' >> $LOG
find ../project/public/js/ \
    -not \( -path '../project/public/js/libs' -prune \) \
    -not \( -path '../project/public/js/templates' -prune \) \
    -not \( -name 'script.js' \) \
    -name '*.js' \
    -exec echo '>>> ' {} \; \
    -exec jscs {} \; \
    >> $LOG

echo '>>    ' >> $LOG
echo '> PEP8' >> $LOG
echo '>>    ' >> $LOG
find ../project/apps \
    -not \( -path '../project/apps/*/migrations' -prune \) \
    -not -path "*/__pycache__/*" \
    -name '*.py' \
    -exec echo '>>> ' {} \; \
    -exec pep8 {} \; \
    >> $LOG
find ../project/core \
    -not \( -name 'manage.py' \) \
    -not -path "*/__pycache__/*" \
    -exec echo '>>> ' {} \; \
    -exec pep8 {} \; \
    >> $LOG

echo '>>        ' >> $LOG
echo '> PyFlakes' >> $LOG
echo '>>        ' >> $LOG
find ../project/apps \
    -not \( -path '../project/apps/*/migrations' -prune \) \
    -not -path "*/__pycache__/*" \
    -name '*.py' \
    -exec echo '>>> ' {} \; \
    -exec pyflakes {} \; \
    >> $LOG
find ../project/core \
    -not \( -name 'manage.py' \) \
    -not -path "*/__pycache__/*" \
    -exec echo '>>> ' {} \; \
    -exec pyflakes {} \; \
    >> $LOG

echo '>>      ' >> $LOG
echo '> PyLint' >> $LOG
echo '>>      ' >> $LOG
find ../project/apps \
    -not \( -path '../project/apps/*/migrations' -prune \) \
    -not -path "*/__pycache__/*" \
    -name '*.py' \
    -exec echo '>>> ' {} \; \
    -exec pylint --reports=n --disable=F0401,C0111 {} \; \
    >> $LOG
find ../project/core \
    -not \( -name 'manage.py' \) \
    -not -path "*/__pycache__/*" \
    -exec echo '>>> ' {} \; \
    -exec pylint --reports=n --disable=F0401,C0111 {} \; \
    >> $LOG
