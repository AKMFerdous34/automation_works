#!/bin/bash

echo -e "\n~~Countdown Timer~~\n"


# this program will count down to zero from a given argument

if [ $1 -gt 0 ]; then
  for (( i=$1; i>=0; i-- ))
    do
      echo $i
      sleep 1s
    done
    echo "Timer has completed counting"
else
  echo "include a positive integer as the first argument"
fi




