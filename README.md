# Generative AI - Course Project - YouTube Summary Model

## Project Overview: 
This project aims to create an AI-powered model that generates summaries of YouTube videos. The model utilizes both speech-to-text technology and image captioning to extract key information from video, providing users with quick and informative summaries. 

## Important remarks: 
1. Be aware that the GUI can be slow on MacOS. Some of the fields and buttons may take some time to load. 
If you are using a Mac to run this program, you should therefore give the GUI some time to load. 

We have also noticed that the GUI is not working on certain Mac-computers. We have not been able to find the reason behind this problem, but we think it might be because of some unknown issues with SSL-certificates on some Macs. 
This problem could be bypassed by adding this to the `S_to_T.py`-file, but it is not recommended: 

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

2. When entering a YouTube video into the program, the video will be downloaded on your computer. 
This includes the video, the audio and the video chunks. Depending on the length of the video you input,
you will get an amount of chunks downloaded on your computer. These can be deleted when you have received your summary. 
3. We recommend that you use BLIP as there is not a great difference between BLIP and BLIP-2 when it comes to
the summaries, but BLIP-2 is more computationally heavy. To use the BLIP-2 model, we recommend to have Cuda. 
4. The YouTube video must be in English as the Google ... only supports English.  


## How to run the program: 
1. Download the code from the zip-file or clone the GitHub repository: 
```bash
git clone
```

2. It is recommended that you use a virtual environment to install the dependencies. Create a virtual environment: 
```bash
python3 -m venv venv
```
Activate the virtual environment: 
```bash
source venv/bin/activate
```

3. Install dependencies: 
```bash
pip3 install -r requirements.txt 
```

If your Mac gives you a tkinter-error, try installing the package with brew: 
```bash
brew install python-tk
```
You may also specify your Python version, for example:
```bash
brew install python-tk@3.10
```

4. Run the project:
```bash
python3 gui.py
```

## How the program works: 
1. Enter the url of the YouTube video you want summarized. Please note that the video should be in English.
2. Choose the number of sentences you want the summary to be. 
3. Choose between BLIP and BLIP-2. Note that we recommend that you have Cuda for BLIP-2. 
4. Choose the personality of the summary. The summary is written differently depending on which personality 
you want the agent to have. Do you want it to be as if it is from a professor? Or maybe you want a mafioso to summarize the video for you? Are you a beginner in something and want it explained as if you are a baby? No 
problem, just choose the kindergarten-personality! 
5. Click the "Summarize"-button and wait as the program processes your video. 

If you want a short video to test the program with, this is a video explaining the C programming language in 100 seconds: https://www.youtube.com/watch?v=U3aXWizDbQ4 

## Program structure 
![Program Structure][def]

[def]: gui.png