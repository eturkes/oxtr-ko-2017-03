#!/bin/sh
# Make 1 minute bins by adding phases to the timeline

start_date='2017-03-20 11:02:07'

# 60 minutes total
i=1
max=61
while [ $i -lt $max ]
do	
	# Implementation derived from Ask Ubuntu, part of the Stack Exchange network
	# https://askubuntu.com/questions/408775/add-seconds-to-a-given-date-in-bash
	# Question asked by: Markus https://askubuntu.com/users/212156/markus
	# Answer given by: steeldriver https://askubuntu.com/users/178692/steeldriver
	start_secs=$(date +%s --date="${start_date}")
	end_date="$(date '+%Y-%m-%d %H:%M:%S' --date="@$((start_secs + 60))")"

	echo "" >> comp+old-behav-flex_timeline.ini
	echo "[Corner Occupation ${i}]" >> comp+old-behav-flex_timeline.ini
	echo "start = ${start_date}" >> comp+old-behav-flex_timeline.ini
	echo "end = ${end_date}" >> comp+old-behav-flex_timeline.ini
	echo "tzinfo = Etc/GMT-9" >> comp+old-behav-flex_timeline.ini
	true $((i=i+1))

	start_date=${end_date}
done
