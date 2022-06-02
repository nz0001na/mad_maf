# Synopsis

Camera ID code ported to Python

# Documentation

Camera Identification based on PRNU signal (Python implementation). 
The naming convention throughout the code follows the CamelCase style similar to MATLAB.

# Copyright

Copyright © 2021, The State University of New York, The Research Foundation for The State University of New York, Morteza Darvish Morshedi Hosseini. All Rights Reserved.

By entering this site and accessing downloading the Camera Fingerprint program © 2021 The State University of New York ("SUNY"), Research Foundation for The State University of New York (“RF SUNY”), Morteza Darvish Morshedi Hosseini (“the Work”), you agree to use the Work for internal, scholarly evaluation and research purposes only, and that you will not commercially use, reproduce the Work,  prepare derivative works based upon the Work, distribute or loan copies of the Work, publicly perform or display the Work, or any results obtained using the Work, or otherwise make it available to third parties.  You furthermore agree to properly acknowledge the Work in future publications reporting results based on it.  No license is granted to create derivative works.  Any inquiry regarding a license beyond the right granted above should be directed to Mr. Scott Moser, Technology Licensing Associate, Office of Entrepreneurship & Innovation Partnerships, Binghamton University smoser@binghamton.edu.

YOU FURTHER UNDERSTAND AND ACCEPT THAT THE WORK IS EXPERIMENTAL IN NATURE AND IS PROVIDED ON AN "AS IS" BASIS.  NO WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, AS TO ANY MATTER INCLUDING, BUT NOT LIMITED TO, WARRANTY OF FITNESS FOR A PARTICULAR PURPOSE, OR MERCHANTABILITY, EXCLUSIVITY, RESULTS OBTAINED FROM USE, OR RESPECT TO FREEDOM FROM PATENT, TRADEMARK, OR COPYRIGHT INFRINGEMENT IS MADE OR GIVEN BY THE AUTHOR, SUNY OR RF SUNY.  IN NO EVENT WILL THE AUTHORS, SUNY OR RF SUNY BE LIABLE FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES RESULTING FROM THE USE OF THE WORK, INCLUDING WITHOUT LIMITATION, FOR LOST DATA OR DOWNTIME. LIABILITY OF THE AUTHOR, SUNY OR RF SUNY SHALL BE LIMITED TO THE AMOUNT PAID TO, AND RECEIVED BY THE AUTHOR, SUNY AND RF SUNY, RESPECTIVELY.


# Inputs/Outputs

A set of images from a single camera should be used to extract the fingerprint (the first input). Another input is the probe image. Output is a PCE value and its location.

# Prerequisits

Our code was prepared in Anaconda 4.8.3 environment.

# Installation

Using a virtual environment is recommended:
`conda create -n cameraId python=3.7`
`conda activate cameraId`

Then requirements needs to be installed:
`pip install --upgrade pip`
`pip install --requirement ./requirements.txt`


# Usage & Test

To use our code, observe/run the example file:
`python Example.py`
 

 

