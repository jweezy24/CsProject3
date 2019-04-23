# CsProject3

[![Build Status](https://travis-ci.com/jweezy24/CsProject3.svg?branch=master)](https://travis-ci.com/jweezy24/CsProject3)

Online Pong. Users can play matches of pong on a local network. *Does not work on windows.* 

## Getting Started

Make sure to look at installing before starting the program.

To run the local client, run the command `python3 /pong.py` in the ./pong directory. This will run the game. The game will load into a searching screen. In this screen UDP packets are broadcasted over the user's local internet looking for the match making server. To launch the server, run from the parent directory, `python3 ./server/serverMain.py`. You will need another player on that network to play with you.  


## Functionality

  ### Pong

  * Classic pong game-play

  * Username functionality

  * Able to remember win rate

  * Instant local peer to peer match making

  * Very little lag

  * Rare desyncing

  ### Server

  * Local data storage using CSV files to maintain a local database

  * Json packet communication

  * UDP socket management

  * Multicast support for matching players

  * Basic lobby management



## Installing

Before running the code, you need to install the requirements. To do this run the command.

`python3 -m pip install -r requirements.txt`

After that we need to make sure everything is setup correctly. Run, `sudo python3 setup.py install`. This will install all local packages so that there are no module errors.

Then you should be all set to go.

## Running the tests

All tests will be ran in travis. Although, running the tests manually is also an option. From the parent directory run these commands to see all the tests.

### Player Tests
`python3 ./tests/player_tests.py`

### Ball Tests
`python3 ./tests/ball_tests.py`

### Server Tests
`python3 ./tests/server_tests.py`

## Built With/Requirements

* [Python3](https://www.python.org/downloads/release/python-372/) - The compiler for device manager

    * [Pygame](https://www.pygame.org/wiki/about) - This package is needed for device manager to grab ip



## Authors

* **Jack West** - *Pong base and Net code development* - [jweezy24](https://github.com/jweezy24)
* **Drew Mack** - *User features for Pong* - [drew-mack](https://github.com/drew-mack)
* **Jack Broncato** - *Matchmaking and customization settings* - [jman11111](https://github.com/jman11111)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.
