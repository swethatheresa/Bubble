# Tink-her-hack-Tech3
Bubble:
Bubble is a web app which serves as a platform for learning enthusiasts to know about events like workshops, webinars, talk sessions happening around them to schedule such events and also to participate in active conversations in the interested fields using talkrooms and communities. The design tool used was Figma. The web app was developed using html,css as frontend and django as backend.
The user is first welcomed to a sign in screen where he/she can enter credentials and sign in if already signed in or sign up. On signing up, the user must enter details like email,password,college of study,city etc. The main page of the web app displays the user's feed which is filtered with user's nearby location and field of interest as criterias. The user can post an event by adding the event poster and details. Each post displayed gives the user a provision to add the event to his/her google calendar and to join talkrooms for that event. The user's calendar is displayed on the right and the location map is given on the left. The user can also create talkroom on the topic he/she is interested in. In the talkroom page the user can select talkrooms based on interested field using search field. He/she can join talkrooms and have a discussion. The user can logout from the main page.

 
Cloning the repository:
--> Clone the repository using the command below :

git clone https://github.com/divanov11/StudyBud.git
--> Move into the directory where we have the project files :

cd StudyBud
--> Create a virtual environment :

# Let's install virtualenv first
pip install virtualenv

# Then we create our virtual environment
virtualenv envname
--> Activate the virtual environment :

envname\scripts\activate
--> Install the requirements :

pip install -r requirements.txt

Including api:
pip install google-api-client-python

Running the App:
--> To run the App, we use :

python manage.py runserver
⚠ Then, the development server will be started at http://127.0.0.1:8000/