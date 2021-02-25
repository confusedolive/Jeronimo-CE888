The data from original unfiltered london data is used to obtain postcodes through latitude and longitude 
using lat_long_to_txt function found in preprocessing.py
this txt files are available under text postcode and boroughs
function add_postcode_df is used to add the postcodes from txt file into the database
then the function add borough to do the same thing wiht boroughs
both functions take directory paths and iteretate through each dataset/txt file

after this is done join_dataset is used to join all datasets into one

in preprocessingdata.py the merged dataset gets filtered and relevant information from london borough profiles 
gets imported into it, boroughs that are not officially london boroughs get dropped

in datasetforgraphs.py a dataset for visualization gets created and used for plot lineplots using sns

in data used for jupyter map you can find all the files needed to make the choropleth maps of london
in ChoroplethLondon.ipynb you can find the code for this maps, had to use jupyter as geopandas was not functioning
correctly in windows
in visualization of the data there are some graphs and maps that could not be added to the pdf due to space