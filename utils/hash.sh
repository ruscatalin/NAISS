# Input parameter: file name

# Output: hash value using bs3sum "file_name"

# Example: hash.sh "file_name"

HASH=$(bs3sum $1)

# return the hash value

echo $HASH