find ../project/public/js/ \
    -not \( -path '../project/public/js/libs' -prune \) \
    -not \( -path '../project/public/js/templates' -prune \) \
    -not \( -name 'script.js' \) \
    -name '*.js' \
    -exec echo '>>> ' {} \; \
    -exec jscs {} \; \
    > jscs.log
