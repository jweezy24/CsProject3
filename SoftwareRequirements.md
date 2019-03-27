# Software requirements for Pong Online

authors: Jack Broncato, Drew Mack, Jack West

# Introduction

# 1 Purpose
This document is for the program Pong Online, a 2 player game of Pong playable over the internet.

# 1.1 Document Conventions
Priorities  for higher-level requirements are assumed to be inherited by detailed requirements.

# 1.2 Intended Audience and Reading Suggestions
This document is intended for developers hoping to understand the program well enough to contribute functionality to it.

# 1.3 Product Scope
The product Pong online is a program meant to connect people who want to play Pong to each other. The objective is to make a program that someone who wants to play Pong can boot up and connect to someone else to play against them. This program would give all the Pong players of the world enjoyment.

# 1.4 References
No references at this point in time, but will likely look up syling guide for UI/Syncing.

# 2 Overall Description

# 2.1 Product Perspective
This is a new self contained product made for the purpose of learning connectivity, syncing, and peer to peer connection.

# 2.2 Product Functions
Functions:
- A menu for navigating to the game or going to the settings
- A setting menu for changing local settings
- A profile system to save/personalize settings, as well as rankings
- A simple database to hold rankings, along with a ranking system
- An interactive Ping game that can be played over internet connection with another player

# 2.3 User Classes and Characteristics
**User:** People who use the program and play online against each other.

# 2.4 Operating Environment
The Environment will be on desktop computers/laptops, or anything that can run the python file.

# 2.5 Design and Implementation Constraints
Since the concept and app is somewhat simple, there are many available options for development. However, whatever is used to develop the web app must be able to connect to and use a database, and be able to manipulate data received to be displayed to a user.

# 2.6 User Documentation
Software use documentation will be provided for testing instructions with the finished product.

# 2.7 Assumptions and Dependencies
Assumptions include: 
- Dilligent teamwork with everyone doing a certain amount of work each week.
- Ability to connect people with a server machine that will be running consistently. 
- Decent syncing with peer to peer connection.

# 3 External Interface Requirements

# 3.1 User Interfaces
Mockups are in a separate document

# 3.2 Hardware Interfaces
The Hardware used will be A server machine(most likely a desktop) to host the website, as well as the computer used to view and play the program using a keyboard.

# 3.3 Software Interfaces
The Software interfaces we will be using will be Pygame for making the game in Python.

# 3.4 Communications Interfaces
This software will use socket programming for sending/recieving packets to peers.

