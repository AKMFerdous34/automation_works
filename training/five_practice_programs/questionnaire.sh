#! /bin/bash

echo -e "\n~~ Questionnaire ~~\n"
QUESTION1="What's your name?"
echo $QUESTION1

NAME=""
read NAME

QUESTION2="Where are you from?"
echo $QUESTION2

LOCATION=""
read LOCATION

QUESTION3="What's your favorite coding website?"
echo $QUESTION3

WEBSITE=""
read WEBSITE

echo -e "\nHello $NAME from $LOCATION. \nI learned that your favorite coding website is $WEBSITE! \n"

