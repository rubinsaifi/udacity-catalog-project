## Item Catalog Project
Part of Udacity's Full Stack Developer Nanodegree program

## Requirements
Develop Item Catalog application that provides a list of items within a variety of categories, as well as provide a user registration and authentication system. 

## About
This application provides a list of items in different sports categories. Edit/Delete/Update requires user login via Google OAuth.

## Features
- OAuth based user authentication
- Full CRUD support using SQLAlchemy and Flask
- JSON Endpoints

## System Requirement and Prerequisites
- Python3.x
- *NIX Machine (Vagrant+Virtualbox+FullStackVM or BareMetal Unix/Linux/MacOS)

## Structure
```
|____sportitemwithusers.db
|____database_setup.py
|____static
| |____top-banner.jpg
| |____styles.css
| |____blank_user.gif
|____templates
| |____deleteSport.html
| |____newSport.html
| |____editmenuitem.html
| |____menu.html
| |____deletemenuitem.html
| |____editSport.html
| |____login.html
| |____editmenuitem copy.html
| |____main.html
| |____landing.html
| |____header.html
| |____newmenuitem.html
|____lotsofmenus.py
|____project.py
|____client_secrets.json
```
## Project deployment steps
1. Download and Install [Vagrant](https://www.vagrantup.com/downloads.html).
2. Download [Virtualbox](https://www.virtualbox.org/wiki/Downloads).
3. Clone Vagrant VM configuration provided in course from [here](https://github.com/udacity/fullstack-nanodegree-vm).
4. Start VM and ssh into it 
```bash vagrant up
bash vagrant ssh
```
5. Go to Vagrant folder `cd /vagrant` and clone this repo
6. Install Flask and run `database_setup.py`
```
sudo apt-get install python3
python database_setup.py
```
7. Run db popular
```python lotsofmenus.py```
8. Run the app
```python project.py```
9. Open `http://localhost:5000` in any web browser

## JSON Endpoints
Get complete data as JSON
```
/sport/catalog.json
```
Get Sports Categories
```
/sport/JSON
```
Other endpoints
```
/sport/<int:sport_id>/menu/JSON
/sport/<int:sport_id>/menu/<int:menu_id>/JSON
```

## Reporting Bugs
This project is a part of Nanodegree although you can sent pull requests by forking this project.

## Licence
MIT License

Copyright (c) [2019] [Rubin Saifi]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Credits and Special Thanks
[Udacity](https://udacity.com) Team for making this amazing course
