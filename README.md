# Implementation of Customer segmentation
Customer segmentation of stackoverflow user's, using RFM and K-means algorithm based on python
## Deep into the Project
this project is implementation of RFM segmentation and clustering using
k-means algorith.
First we map the dataset into Recency, Frequency and monetary value,
the we count the RFM Score and add it to target data.
at the end we use an Elbow method to find the best k for k-means algorithm. 
then we use that k to cluster out dataset.
the used Scoring is "RFM Score = M*5 + F*3 + R*2 ".
## Running the project

First of all you need to install pip3
```
sudo apt-get -y install python3-pip

```
We have all the requirements listed in requirments.txt so you can use that to install all of them.
```
pip3 install -r /path/to/requirements.txt

```
Also the requirements are listed as
```
pandas~=1.1.2
matplotlib~=3.3.2
sklearn~=0.0
scikit-learn~=0.23.2
```
## Built With

* [Python](https://www.python.org/) - Programming language

## Author

* **Ahmadreza Samadi** - *Developer* - [Ahmadreza samadi](https://github.com/ahmadreza-smdi)

*Thanks for your attention.*
