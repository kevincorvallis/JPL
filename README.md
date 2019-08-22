# Marginal Analysis Tool
The task is to develop a tool that analyzes the marginal use of the Curiosity rover actual vs. estimated from EVR files. If possible, James wants to look deeper into the individual sub-master processes that happens within each block for better efficiency. Eventually, make it simple enough to be a command to feed in intervals and generate statistics. Make it maintainable and document thoroughly for someone else to pick up.

## Getting Started
1) Copy the repository in a desired location. 
```
git clone https://github.jpl.nasa.gov/kevinl/MWG
```
### Prerequisites

**Python 2** is required to run this program. 
Have internet access to download packages if necessary.

I am running Python 2.7.10

Run this to find out what python version you are running
```
python --version
```
Packages used... 
```
import os, sys, json, re
from math import *
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
```

Version of each package

To find out:
```
python -m pip freeze | grep PACKAGE
```
```
Python 2.7.10
matplotlib==1.3.1
scipy==1.2.2
numpy==1.16.4
pandas==0.24.2
functools32==3.2.3.post2
nose==1.3.7
jsonschema==3.0.1
```



### Installing
You will need **Matplotlib** and **Pandas** as packages. 

Below is how to install external libraries into your python in bash. 
```python
python -m pip install pandas
```
```python
python -m pip install matplotlib
```
```python
python -m pip install LIBRARY
```


## Running the tests
**To run**
```
python analyzeMarginUse.py
```
This should create different graphs you can view. Additionally, it will give you the statistics of the percentile idle time in minutes of each activity. (sb, all, arm, drive) 

* To retrieve statistics of the graph that was created using the data run:
``` bash
python totalSubsAndSols.py
```




### Break down of submasterDurations.py
submasterDuration is essensailly the parser that translates the EVR files into useful .json files that analyzeMarginUse.py can use. 

Most of the erros I encountered running this program were the different versions of packages that were installed in indiviudal computers. It is **ABSOLUTELY VITAL** that you are running the same version of packages as I am or else your program will fail and spend a lot of time trying to figure out what is happening.

Ex. Error in `hits, _ = spazzObj.get_as_run_sequences(seqids=[seqId])`(line 245) raised an eror saying: `raise HTTP_EXCEPTIONS.get(status_code, TransportError)(status_code, error_message, additional_info)
elasticsearch.exceptions.RequestError.`

This problem was resoluted by installing a previous python ***elasticsearch*** package.
```
python -m pip install "elasticsearch-dsl<2.0.0" --user
```
Required packages: 
```
https://github.jpl.nasa.gov/MSLEO/msl-datalytics
scipy==1.2.2
elasticsearch1==1.10.0
spazz
```
Spazz is built from msl-datalytics repository that contains shared resources that utilize the Analytics cloud infrastructure to query,index, and analyze MSL Data. 



<!-- ### And coding style tests
```
hello

``` -->

## **Why Python**
Python offers numerous benefits over other laguages and one of the main purpose I chose to use python is it's **versatiliy** and **adaptibility**. 

***Bigger Picture***

It's fast to develop, easy to use and learn, neat, readable, and well-structured. Knowing that no software is permanent, there will always be need of re-implemnetation or editing done in the future for a program. Some common program languages to use for data science is Ruby, R, C#, C, and Python. However, as a emerging data scientist in 2019, I've observed the rise of popularity in python and a lot data science is gravitating towards Python. Python is the most wide-known language that is currently still developing compared to other languages which are no longer being developed. The open source vibrant community cannot be overpowered which in turns provides maintinability and stability

Furthermore, JPL is a diverse community with multiple engineers from  different backgrounds. There was an anticipation that not everyone who will be looking at this program in a deeper level will not be software engineers. Thus, the decision to use Python for it's popularity and diverse set of tools it has been considered. 

In a programmer point of view, the benefit of choosing a lower-level language for tool is volatile. As this tool is not being used constnatly, the run time of this program is not a high prioritization. In result, the specific algorithm that program uses was not taken in consideration. Going down the lower level language path will only add time to implement and to re-implement for future programmers. 


***Smaller Picture***

There are now over 70,000 libraries in the Python Pckage Index and that number continues to grow. Aforementioned, libraries are mostly geared towards data science. Arguably, a reliable and most popular data analysis library is an open scource library called Pandas. 

In this program, I use pandas to store my data. Controversially, I would have created a co-occurance matrix or a linked-list format of data structures to represent data in lower-level language. There are more asepcts to consdier such as memory in creating these data-structures and de-bugging becomes difficult even with the right tools like valgrind/gdb becuase of its complexity. The benefit of using pandas is it's simplicity to understand and its reliability. Nonethless, Python has the tooolset to perform a variety of powerful functions whether it be predictive casual analytics or prescriptive analytics.


When it comes to web support, the web-framework Python supports such as Django makes it possible for a secure, python-supported, SQL supported, and Object Relation Mapping (ORM) capable website.  


##Problems I've encountered building the JavaScript 


###Reading data from the .csv files
There are multiple methods of improting data. In my case, it is vital to read the .csv data as I am creating the graphs in .js. I didn't worry about creating the graphs quite yet just because I needed some data to work with. 

Regardless, I first tried by importing the local file of using d3.import. It did not work and it gave me an error saying `Cross origin requests are only supported for protocal schems: http, data, chrome, chrome-extension, https.` So I tried using my jpl git and importing it in the RAW form only to find out saying `Origin IPADDRESS is not allowed by Access-Control=Allow-Origin.` with other issues saying `XMLHTtpRequest cannot load due to access control checks`.

The solution, after extensive amount of resaerch, I found out is that opening an html file in the browser on personal computer is not the same as a server sending the file to the computer. Localhosing simulates what it would look like to recieve the data file from a server on the internet as if I had visited the url. Thus, in VS code I downloaded the API to run it and learned that it was a good habit to develop like this as programs will be always connected to the internet and i'm testing it in a realistic form. `Jquery, AJAX`. 



*Matplotlib*

Some sample Matplotlib graphs:


![Image of Graph]
(https://github.jpl.nasa.gov/kevinl/MWG/tree/master/Output/Post-Update/Post-UpdatePlannedMarginPercents.png)

<--------------------------------------------------------->

Useful site about different graphs that matplotlib can do.

(https://matplotlib.org/3.1.1/tutorials/introductory/sample_plots.html)
(https://matplotlib.org/users/pyplot_tutorial.html)

##Closing Notes
To whomever will be taking up on this project, my process was to

1) Understand the EVR (Event Reports) as much as I can

2) Skim submasterDurations.py 
Understand how I am parsing the data and what is specifically being used. 

3) Now look into d3.js and see how the data is visualized.
I was never able to produce the graphs using d3.js but there is an exmaple of 
plotly. 
Everything is available on git and feel free to email me with any questions if you have. 


## Built With
* Microsoft Visual Studio
* Anaconda Juypter Notebook

<!-- ## Contributing -->

## Versioning
Version 1.0 July 15, 2019 
## License
NASA Jet Propulsion Labratory 
## Acknowledgments
Chris Bennet for providing framework submasterDurations.py that creates the .json files. 

Kevin Lee 

