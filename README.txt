Django project for using leaguevine.com via its API for Windmill Windup 2012.
Everything is experimental up to now!

Windmill Windup 2012 is over, these scripts will not be developped any further.
If you are interested in using any of this, please contact Christian Schaffner (huebli@mgail.com)


This project consists of 3 modules:
1. Leaguevine control tool
2. SMS functionality
3. Spirit scores

existing scripts:
* import team data into local database from ffindr csv-exports
* create according teams in leaguevine
* create new tournament on leaguevine (one per division)
* add teams to tournament
* add a new swissdraw round
* add results
* retrieve standings

to do:
* check if they are properly computed
* check if next round is properly computed
* check if fields are properly assigned
* create new playoff bracket
* rest of the teams continue with swissdraw

SMS-functionality:
* create SMS like last year
* send SMS through a provider

Spirit-scores:
* provide a simple interface for spirit chair to enter spirit scores
* todo: display the resulting averages

Public-Screen project:
* provide live information to front-end
* make front-end