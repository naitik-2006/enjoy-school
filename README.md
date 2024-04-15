## Requirement :-
* Xampp
* Python

## How to run :-
1. `pip install -r requirement.txt`
2. Start Xampp server (Apache, MySQL).
3. Create a `config.json` file containing information as demonstrated in `demo-config.json`.
4. Create database as shown in the video and main.py file
5. `python main.py`

## Features :-
* Users can sign up as either a teacher or a student.
* Email address verification is required for signup.
* Users can log in, and if they forget their password, they can reset it.
* Teachers can create classes and share a unique class code with students.
* Students can apply to join a class using the unique class code and the "join class" option.
* Teachers can accept student requests in the participants column for a particular class.
* The home column allows teachers to add classwork and view student submissions.
* Each classroom has a "discuss" tab where students and teachers can communicate.
* The website is highly responsive, suitable for any screen size.
* Robust Jinja templating has been employed for optimal performance with Flask.

## Note :-
* Some features, such as sending and accepting files in the "discuss" tab, have not been completed yet.
* Features like scheduling meetings, assigning quizzes, and sharing class codes are currently unavailable.
