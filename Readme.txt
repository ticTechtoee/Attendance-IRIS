*********************************************************************************************************
*													*
*				--- FACE RECOGNITION ATTENDANCE SYSTEM ---				*
*													*
*********************************************************************************************************
*               			--- INTRODUCTION ---
*
*	Face Recognition Attendance system (FRAS) is designed to mark the attendance of student 
*	to detect their face. The system will provide secure attendance management via face detection.
*	The system has the capability to mark the attendance automatically to detect the face.
*
*
*********************************************************************************************************
*
*               			--- REQUIREMENTS ---
*
* 	1. Visual Studio Code
*
*		Download Visual Studio Code Software at --> https://code.visualstudio.com/download
*
*	 2. Anaconda
*
*		Download Anaconda software at --> https://www.anaconda.com/products/distribution
*
*	 3. Web Browser
*		You can use any web browser like (Chrome, Firefox, Microsoft Edge)
*
*	 	Download your favorite web browser to follow the link
*
*		Google Chrome --> https://www.google.com/intl/en_pk/chrome/
*		Firefox --> https://www.mozilla.org/en-US/firefox/new/
*		Microsoft Edge --> https://www.microsoft.com/en-us/edge
*
*********************************************************************************************************
*
*               			--- INSTALLATION ---
*
*	1. Install Visual Studio code and Anaconda in your PC
*
*	2. Place the project code file where you want
*	
*	Note: Place your project file in the drive where you install the Anaconda software
*
*	3. Now open the project code in Visual Studio Code
*
*	4. Create a virtual environment using Anaconda
*
*		conda create -n virenv python=x.x anaconda
*
*	5. Install the required dependencies of requirement.txt file
*	   You can get requirement.txt file by using the command
*
*		pip freeze > requirements. txt
*
*	6. Activate virtual environment using Anaconda by entering the command
*
*		conda activate virenv
*
*	Note: Here "virenv" is the virtual environment that you create. Replace your virtual environment name with "virenv"
*
*	7. Run the command to install the project location in the Anaconda
*
*		cd: your_project_location
*
*	8. Now you will able to running the project by entering the command
*
*		py manage.py runserver
*
*********************************************************************************************************
*               			--- DATABASE ---
*
*	Run the command to create Database
*	
*		py manage.py makemigrations
*
*		then
*
*		py manage.py migrate
*
*
*********************************************************************************************************