# Atomic Games AI (Atomic Games 2017)

The [Atomic Games](http://atomic-games.atomicobject.com/) is a programming competition/recruiting opportunity hosted by [Atomic Object](https://atomicobject.com/).  The 2017 games had participants design an AI to play a simple 1v1 style video game.  This project is an extension of an AI [Alex Cadigan](https://github.com/AlexCadigan) and [Skyler Norgaard](https://github.com/skylernorgaard1) designed during the Atomic Games.  

## Getting Started

### Prerequisites

#### Mac

* Install [Python](https://www.python.org/downloads/) 
* Install Ruby 2.3.X or newer
  * Install [Homebrew](https://brew.sh/)
  * `$ brew install ruby`
* Install [Gosu](https://github.com/gosu/gosu/wiki/Getting-Started-on-OS-X)
* Install [Bundler](https://bundler.io/)

#### Windows

* Install [Python](https://www.python.org/downloads/)
* Install [Ruby 2.3.X](https://rubyinstaller.org/downloads/) or newer
* Install [Gosu](https://github.com/gosu/gosu/wiki/Getting-Started-on-Windows)
* Install [Bundler](https://bundler.io/)

#### Linux

* Install [Python](https://www.python.org/downloads/)
* Install [Ruby 2.3.X](https://rubyinstaller.org/downloads/) or newer
* Install [Gosu](https://github.com/gosu/gosu/wiki/Getting-Started-on-Linux)
* Install [Bundler](https://bundler.io/)

### Setting up the Game

* `$ cd Server`
* `$ bundle install`

### Running the Game

#### Clients

* `$ cd Clients`
* `$ python Client1.py`
* `$ python Client2.py`

Note: clients must be run in seperate terminal windows

#### Server

* `$ cd Server`
* `$ ruby src/app.rb`

## Authors

* [Atomic Object](https://atomicobject.com/) - Created all sdks and the server to run the game
* [Alex Cadigan](https://github.com/AlexCadigan)
* [Skyler Norgaard](https://github.com/skylernorgaard1)
