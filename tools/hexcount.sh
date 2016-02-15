#!/usr/bin/env bash
#
# hexcount -  POSIX Shell script to count from $1 to $2 in hex,
#             separated by ";" and with the precision set to the
#             maximum digits of $1 and $2.
# Usage:      hexcount lo hi
# Example:    hexcount FFF 1200

FROM=$1 TO=$2
if test ${#FROM} -gt ${#TO}; then
    FORMAT="%0${#FROM}X\n"
else
    FORMAT="%0${#TO}X\n"
fi
FROM=$(printf '%d' 0x$FROM) TO=$(printf '%d' 0x$TO)
while test $FROM -le $TO; do
    printf $FORMAT $FROM
    FROM=$((FROM+1))
done
