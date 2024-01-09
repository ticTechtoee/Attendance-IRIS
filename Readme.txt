Attendence System using IRIS Scanning.

HOW TO CREATE THE VIRTUAL ENVIRONMENT FOR THE PROJECT

Create your Virtual Environment using `virtualenv venv` command.
To Use `virtualenv` install package using `pip install virtualenv`.

PYTHON VERSION

`python version 3.12` has conflicts with few packages that were used in this project therefore use the `python version 3.11`

HOW TO RUN THIS PROJECT

1 -  Create a superuser to use as an "Admin".
2 -  Login to the system using "Admin" credentials
3 -  Go to the "Register Person" page and Register a person for which you want to mark the attendance.
4 -  On the Next Page Capture Multiple Pictures of the person's eye to train the Model.
	Select the Unique ID of the Person.
	Use sophisticated camera IR cameras to capture the Eye Pupil, Pupil structure and Vein Structure.
	The system is using a Pattern storage system that's why the system will capture and store the pattern of the Training Data. 
	Use well lit area to capture the images and take multiple images of a similar area to make the model familiar with the Data.
	System will automatically save the Image of each person in a folder named after the Unique ID and Name of the Person (e.g: 1001_Farhan_Basheer).
	Each person will have a separate folder.

6 -  Once Admin is done with capturing the Images of the Persons(Label) go to the "Train Model" page and click on the Train Model Button.
	The system will automatically train the model on the images and will create a .dat file in a special folder.

7 -  Login as a User in the system and take the image to mark the attendence.
8 -  If the system has recognized the person then it will automatically mark the attendance, save the data in the database.
9 -  Admin and a User can "Search" the record by visiting the "Search" page.
10 - Admin and User can Generate the report in .xlsx format by clicking on the "Export to Excel button".