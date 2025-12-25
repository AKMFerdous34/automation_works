#!/bin/bash

echo -e " \n ~~ Bingo Number Generator ~~ \n "

#for((i=0;i<=75; i++)) 
 # do
TEXT="The next number is, " 
NUMBER=$((RANDOM%75+1))
#echo $TEXT
#echo $NUMBER
if (($NUMBER <= 15)) then
  echo $TEXT "B:" $NUMBER
elif [[ $NUMBER -lt 30 ]] then 
  echo $TEXT "I:" $NUMBER
elif [[ $NUMBER -lt 46 ]] then
  echo $TEXT "N:" $NUMBER
elif [[ $NUMBER -lt 61 ]] then
  echo $TEXT "G:" $NUMBER    
else
  echo $TEXT "O:" $NUMBER   
fi 
 # done
#echo $NUMBER

