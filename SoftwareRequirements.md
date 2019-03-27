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
No references at this point in time, but will likely look up styling guide for UI/Syncing.

# 2 Overall Description

# 2.1 Product Perspective
This is a new self contained product made for the purpose of learning connectivity, syncing, and peer to peer connection.

# 2.2 Product Functions
Functions:
- A menu for navigating to the game or going to the settings
- A setting menu for changing local settings
- A profile system to save/personalize settings, as well as rankings
- A simple database to hold rankings, along with a ranking system
- An interactive Pong game that can be played over internet connection with another player

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
This software will use socket programming for sending/receiving packets to peers.

# 4 System Features

# 4.1 Online Play

# 4.1.1	Description and Priority
Lets the player play against someone over the internet instead of locally(High priority).

# 4.1.2	Stimulus/Response Sequences
Player would have to go to the menu and hit "Start" to access this feature.

# 4.1.3	Functional Requirements
REQ-1: Socket connection between two computers for peer to peer connection for gameplay, returning errors if the connection is unsuccessful.
REQ-2: Initial Socket connection to server for match making as well as potentially fetching ranking to local.

# 4.2 User Accounts

# 4.2.1	Description and Priority
A profile system to save/personalize settings, as well as rankings(Medium priority).

# 4.2.2	Stimulus/Response Sequences
Player would have to go to the menu and hit "Settings" to modify this aspect as well as look at 	rankings.

# 4.2.3	Functional Requirements
REQ-1: Local profile data as well as server profile data that will sync when connected to look for game.
REQ-2: Also ranking storage tied to the accounts, completely server side that will be pulled to local.

# 4.3 Ranking System

# 4.3.1	Description and Priority
database to hold rankings, and updates to rankings will be calculated on the server

# 4.3.2	Stimulus/Response Sequences
Player would have to go to the menu and hit "Settings" to view their profile and ranking, it will be updated after matches.

# 4.3.3	Functional Requirements
REQ-1: Server database to hold rankings tied to profiles.
REQ-2: A fair and logical calculation of increased/decreased ranking after a match.

# 5 Other Nonfunctional Requirements

# 5.1 Performance Requirements
The main performance requirement is going to be connection speed and updating, both will need to be as fast as possible in order to create a unified and enjoyable experience for the players.

# 5.2 Safety Requirements
The only possible safety requirements needed are safeguards against abuse of the socket connection system, to stop people from using modified clients to cheat or attack opponents over the connection.

# 5.3 Security Requirements
See above, hopefully no breaches come from the connection between the two computers, though there is no precious data stored by the program.

# 5.4 Software Quality Attributes
Maintainability and Adaptability would be the main attributes we would need for a successful game, Maintainability of client integrity if the server host is switched or upgraded, and Adaptability for handling switching connection types in the future possible.

# 5.5 Business Rules
All teammates will have access to all code, however pushing to others branches is not to be done unless permission has been given.

# 6 Other Requirements
The only other requirement is database stability, as the database will need to be persistent and keep its data so rankings can mean something over time instead of getting reset when the server is shut off.
