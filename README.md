# IIScWebDev

![2024-03-24_20-02](https://github.com/eKeiran/IIScWebDev/assets/34791715/e6197c42-544e-41c0-8da5-d36ea4dc820a)

Round 1 screening test project for CiSTUP @ IISc, Bangalore's Web Dev internship.
You can view the final demo.mp4

## Web Application Setup Guide

This guide will help you set up, run, and test the web application locally.

### Installation

1. Clone the repository:
`git clone https://github.com/eKeiran/IIScWebDev`

2. Navigate to the main project folder:
`cd IIScWebDev`

3. Install Python dependencies using pip:
`pip install -r requirements.txt`

4. Navigate to the frontend folder:
`cd object-detection-app`

5. Install Node.js dependencies using npm:
`npm install`

### Running the Application

1. Start the Django backend server:
- Navigate to the backend folder after making sure you are in the main project folder:
  ```
  cd detection_backend
  ```
- Run the Django server:
  ```
  python manage.py runserver
  ```

2. Start the frontend server:
- Go back to the main project folder:
  ```
  cd ../
  ```
- Navigate to the frontend folder:
  ```
  cd object-detection-app
  ```
- Start the frontend server:
  ```
  npm start
  ```

### Testing

To test the web application locally, ensure both the backend and frontend servers are running.

1. Open your web browser and navigate to:
http://localhost:8000

2. Interact with the web application and test its functionality.

### Dependencies

- Django (Python): Backend web framework
- Node.js: JavaScript runtime for the frontend
- React: Frontend UI components
- OpenCV: Library for computer vision, used for object detection
