# StoryQuest: An Interactive Storytelling Kit
Welcome to StoryQuest, an application that enables students to incorporate RFID readers and tags into storytelling, allowing for rich and immersive storytelling experiences. View a sample demo student project about a Climate Change board game [here](www.youtube.com/video/aNDTwkaymow).

Read more about the application in general [here](https://github.com/khushkaran/490-capstone/blob/main/StoryQuest%20Documentation.pdf) and a technical overview of the application [here](https://github.com/khushkaran/490-capstone/blob/main/Technical%20Documentation.pdf).

This application was created as a capstone project for CSC490, Physical Computing in K-12.

## Getting Started
### Arduino Setup
There are four .ino files, one for each Arduino. Upload the code (found under `arduino-rfid-reader-mega-x/arduino-rfid-reader-mega-x.ino`) onto each Arduino Mega. 

### Setting up communication to Arduino and enabling sound
Run `pythonBackend/basic_play_audio`

### Running StoryQuest
Run `backend/server.py` - you may need to `pip install -r requirements.txt` before this. 
Then, run the StoryQuest UI locally by running `npm i` and `npm start` in the `frontend` folder. 
