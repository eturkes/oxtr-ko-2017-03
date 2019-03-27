#!/bin/sh

#    This file is part of oxtr-ko-2017-03.
#    Copyright (C) 2018-2019  Emir Turkes
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    Emir Turkes can be contacted at eturkes@bu.edu

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

	echo "" >> hab1.ini
	echo "[Corner Occupation ${i}]" >> hab1.ini
	echo "start = ${start_date}" >> hab1.ini
	echo "end = ${end_date}" >> hab1.ini
	echo "tzinfo = Etc/GMT-9" >> hab1.ini
	true $((i=i+1))

	start_date=${end_date}
done
