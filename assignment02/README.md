# The influence of an area’s socio economic status in the outcome of stop and search procedures. A causal analysis of police bias in London.
> A study on the effect socio economical status of an area has in police decisions during stop and search procedures in London. 

## Table of contents
* [General info](#general-info)
* [Images](#images)
* [Setup](#setup)
* [How to](#how-to)
* [External resources](#external-resources-used)
* [Status](#status)
* [Contact](#contact)

## General info
A study on police bias in London , with an emphasis in socioeconimcal status. Focusing on causal inference and utilizing the DoWhy library to estimate the effect of socieconomic status (treatment) in the outcome of a stop and search procedure.

## Images
![Examples](./chloropleth/pjimage.jpg "London chloropleth maps")

## Setup
* Python= 3.x.x
* Pandas=1.2.1
* ScikitLearn=0.24.1
* Numpy=1.19.5
* DoWhy=0.6.0
* Matplotlib=3.2.2
* Seaborn=0.11.1
* Scipy=1.6.0
><br/>can be installed using:<br/>
>> pip install -r /path/to/requirements.txt

## How to
The folder [Examples](https://github.com/confusedolive/Jeronimo-CE888/tree/main/assignment02/Examples) contains examples of how some snippets of code work,
the folder [visuals](https://github.com/confusedolive/Jeronimo-CE888/tree/main/assignment02/visuals) contain relevant graphs and plots created. [Visualunderstanding.py](https://github.com/confusedolive/Jeronimo-CE888/blob/main/assignment02/Visualunderstanding.py) contains all the code used to create the relevant graphs found on visuals folder, other then the chloropeth folder which code is available in [here](https://github.com/confusedolive/Jeronimo-CE888/blob/main/Assingment01/ChoroplethLondon.ipynb). The folder [data](https://github.com/confusedolive/Jeronimo-CE888/tree/main/assignment02/data) contains the final merged dataset utilized for analysis and visualization, the code utilized to create this dataset can be found in [here](https://github.com/confusedolive/Jeronimo-CE888/tree/main/Assingment01), it also contains the London-borough information dataset which is also utilized to retrieve borough level information. The [causal analysis&preprocessing.py](https://github.com/confusedolive/Jeronimo-CE888/blob/main/assignment02/causal%20analysis%26preprocessing.py) contains the code utilized to further preprocess data and causal analysis.

## External resources used 
* https://github.com/Microsoft/dowhy , Dowhy library.
* http://geodojo.net/uk/converter/ , Geodojo to convert latitude/longitude to postcodes.
* https://www.doogal.co.uk/BatchGeocoding.php , Doogal to convert postcodes to London Boroughs.
* https://data.london.gov.uk/dataset/ , London Datastore to obtain relevant borough information.
* https://data.police.uk/data/,  Monthly databases of stop and search occurences.

## To-do list:
- [x] Understand DoWhy library
- [x] More research on casual inference
- [x] Get more data processed and ready
- [x] Any extra preliminary visualization
- [x] Implement dowhy in available data
- [x] write relevant results 

## Status
Project is: _finished_<br/>


## Notes
To be updated when the new census(2021) data becomes available.
## Contact
Created by Jeronimo Oliva Cano <br/> E-mail: jo20296@essex.ac.uk
