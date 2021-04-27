# flaskr
Testing blog for testing things

### Planned Features
##### General
- [x] Actual post page
- [ ] Likes (WIP)
- [x] Comments
    - [ ] System for ~~threaded comments (Backburner)~~
- [ ] User profile
- [ ] Different media type posts (video, audio, pic)
- [ ] Blog sections
- [ ] Pagination

##### Tech stuff
- [ ] Websockets (see likes realtime)
- [ ] The ~~API~~
	- Api was attempted but should really be moved into it's own service!


## Setup
### Prerequisites
To set up the app, you'll need some things installed:
- python 3
- pip
- git

If installing on linux, please make your your package manager is up-to-date and you have `python 3.6 or higher` and `python3-venv` installed.
### Installation
1. First of all, create and navigate to a directory in which you'd like to store the project. E.g. `C:\Dev\`

2. Clone the project with `git clone https://github.com/BokChoyWarrior/flaskr`. In windows you'll need to run this from git bash terminal **Make sure you clone into the directory you made in step 1!**

3. Change your current directory to `xyz/flaskr/`, so if you ran the **clone** command in `C:\Dev\`, you would now want to be inside `C:\Dev\flaskr\`

4. Create a virtual environment with
    - Windows: `python -m venv venv`
    - Linux: `python3 -m venv venv`

5. Activate the virtual environment:
    - Windows: `venv\Scripts\activate.bat`
    - Linux: `source venv/bin/activate`

6. Install required packages with `pip install -r requirements.txt`

7. Set environment variables:
##### Windows: 
```
set FLASK_APP=flaskr
set FLASK_ENV=development
```

##### Linux:
```
export FLASK_APP=flaskr
export FLASK_ENV=development
```


8. Initialise database `flask init-db`

9. Run the app with `python run.py`(windows), or `python3 run.py`(linux)

You should see output similar to this:
```
* Serving Flask app "flaskr"
* Environment: development
* Debug mode: on
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: 855-212-761
```

Visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to see the app!

If you have any problems with installation let me know and I can help figure them out!


### Testing - on hold and may __**not work**__
To run some unit tests, you'll first need to install the project to the venv as a module.

1. With the venv active, and in the root directory of the repository, use the command `pip install -e .`.

2. You can then use command `pytest` to run the tests, or `coverage run -m pytest` to see the code coverage of said tests.

More detailed explanation [on the flask tutorial site.](https://flask.palletsprojects.com/en/1.1.x/tutorial/tests/)