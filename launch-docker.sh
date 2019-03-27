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

docker run -it --rm -p 8888:8888 \
	-v ${PWD}:/home/jovyan/work eturkes/pymice-notebook:py3.5.4v2 \
	/bin/bash -c "source activate PyMICE && jupyter notebook"
