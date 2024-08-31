
This is the Blood Map Project -  A Python Flask based application for managing blood donation activities. We are demoing at [https://blood-map.onrender.com](https://blood-map.onrender.com). 

## Aim of the Blood Map Project
The Blood Map Project aims to enable greater blood donation, especially in the rural parts of India where there is a massive shortage of blood. Wokring on a distance matrix estimation, the project aims to reach out to donors based on their proximity to the hospital/blood bank. 

This enables a much higher probability of obtaining blood as donors are more inclined to donate if the recipient is close by.

This project is still a work in progress and we intend to keep working on it to make it better and reach audiences as soon as possible.

If you still wish to see how the project was made follow the below steps:

## Requirements
- Python 3.x
- Flask
- PyMongo
- Passlib

## Installation

1. Install Python (if not already installed).
2. Install Flask, PyMongo, and Passlib using pip:

   ```
   pip install requirements.txt
   ```

## Usage

1. Run the Flask application:

   ```
   python app.py
   ```

2. Access the application through a web browser at `http://localhost:81/`.

## File Structure

- **app.py**: Contains the main Flask application code.
- **templates/**: Directory containing HTML templates for rendering web pages.
- **static/**: Directory containing static files like CSS, JavaScript, etc.

## Features
- **User Management**: Allows users to sign up, log in, and log out.
- **User Dashboard**: Provides a dashboard for registered users to view and update their information.
- **Collector Management**: Enables blood service collectors to sign up, log in, and log out.
- **Collector Dashboard**: Provides a dashboard for blood service collectors to manage their activities.
