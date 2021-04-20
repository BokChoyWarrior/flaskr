# flaskr
This repository is basically just a space for testing purposes - I plan to add api capabilities to it soon (because we will definitely need that in the future).

For now, it's just the simplest blog!

### Prerequisites
To set up the app, you'll need some things installed:
- python 3
- pip
- git

## Setup
1. First of all, create and navigate to a directory in which you'd like to store the project. E.g. `C:\Dev\Flask_site`

2. Create a virtual environment with
    - Windows: `python -m venv venv`
    - Linux: `python3 -m venv venv`

3. Clone the project with `git clone https://github.com/BokChoyWarrior/flaskr`. In windows you'll need to run this from git bash terminal **Make sure you clone into the directory you made in step 1!**

4. Activate the virtual environment:
    - Windows: `venv\Scripts\activate.bat`
    - Linux: `source venv/bin/activate`

5. Install required packages with `pip install -r requirements.txt`

6. Initialise database `flask init-db`

7. Set environment variables and run app:

#### Windows: 
```
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

#### Linux:
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```


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