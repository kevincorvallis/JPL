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


### Installing
You will need **Matplotlib** and **Pandas** as packages. 

Below is how to install external libraries into your python in bash. 
```
python -m pip install pandas
```
```
python -m pip install matplotlib
```
```
python -m pip install LIBRARY
```


## Running the tests
**To run**
```
python analyzeMarginUse.py
```
This should create different graphs you can view. Additionally, it will give you the statistics of the percentile idle time in minutes of each activity. (sb, all, arm, drive) 

* To retrieve statistics of the graph that was created using the data run:
```
python totalSubsAndSols.py
```




<!-- ### Break down into end to end tests
```
```

### And coding style tests
```
```

## Deployment -->


## Built With
* Microsoft Visual Studio
* Anaconda Juypter Notebook

<!-- ## Contributing -->

## Versioning
Version 1.0 July 15, 2019 
## License
NASA JPL 
## Acknowledgments
Chris Bennet for providing framework submasterDurations.py that creates the .json files. 

Kevin Lee 


