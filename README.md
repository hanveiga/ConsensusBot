# ConsensusBot
ConsensusBot for HackZurich

## Table of content

1. About
2. Installation
3. Libraries


## 1. About

ConsensusBot is the bot for telegram communicator.
Imagine a scenario, you have communication window with a few friends, you want to meet with each other. 
What do you usually do? 
Everyone writes their availability or unavailability.
Ok who will organize it?
Usually no one.
Someone create an doodle pool.
But nobody wants to enter external link (especially from mobile).
Finally there is no meeting or only part of users meets.
 
What to do?
Use ConsensusBot!

ConsensusBot tries to locate your preferences from your text.
Joins knowledge passed by other users.
Proposes best matching time interval according to Social Choice Theory for all users.
If somebody couldn't be at specified time or doesn't declare his availability,
ConsensusBot asks directly for changing or declaring preferences.
If all users don't agree next best matching interval from list is proposed.


Goal of this scenario is meeting of all interested users, by using an old approach of group reasoning: Common Knowledge.
New approaches to group reasoning provides abstractions on running other scenarios, like partial meeting of the possible biggest subgroup.


## 2. Installation

First of all you should create virtualenv with python2.7. 

```sh
virtualenv --no-site-packages --distribute -p python /path/to/your/env
```
Than, using virtualenv, install package
```sh
. /path/to/your/env/bin/activate
```

install requirements
```sh
pip install -r requirements.txt
```

Register your bot using botFather:
https://core.telegram.org/bots#6-botfather

## 3. Libraries
Libraries requested by project:
1. requests - used for communication with doodle API
2. python-telegram-bot - bot communicating with users 
3. wit - syntax/datetime parser
4. python-dateutil - reach dates
Moreover it is strongly recommended to use:
5. ipython - great shell for python
