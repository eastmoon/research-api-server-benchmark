# Declare variable

# Declare function

# Execute script
if [ $(find /tmp -type f | wc -l) -gt 0 ]; then
    rm -rf /tmp/*
fi
