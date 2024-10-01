# Image Processing API

## Table of Content

---

- [Image Processing API](#image-processing-api)
  - [Table of Content](#table-of-content)
  - [Version](#version)
  - [About this project](#about-this-project)
  - [Design](#design)
    - [Overall API Design](#overall-api-design)
  - [Technologies](#technologies)
  - [Out of Scope](#out-of-scope)
  - [Future Integrations](#future-integrations)
  - [User Guide - Installation](#user-guide---installation)
    - [Use example](#use-example)

## Version

---

V 1.0
This version only contemplates common operations on images

## About this project

---

The following project is an API to perform some of the most common image processing operations such as:

- Gray Scale
- Binary Image
- Image Scale
- Color Histogram
- Image Restoration (Basic version)
- RGB Image
- RGBA Image

This API is coded in Python and Django the operations that are performed on images can be done through system configuration (Image filter parameters) or the user can provide their own parameters.

## Design

---
> Important:
> Current version of this project doesn't not contemplate asynchronous processing and authentication. Images are not stored in database all the images are processed in memory and then deleted after operations are performed

### Overall API Design

![Image processing](/Design/image_processing.png)

The diagram shows the overall design, this design is simple and is only intended to show the logic and responsibility distribution. We can see that we split the image processing logic into a dedicated module this will help us to make the system more modular and maintainable for future integrations and make every end-point to request services from image processing modules.

## Technologies

- Django 5.1
- Python 3.12.3

## Out of Scope

This project at the current version does not contemplate the following features

- Authentication System
- API Throttling handling
- Live version (to test the system must be installed locally)
- Asynchronous processing
- Advanced Image processing operations such as
  - AI image processing integrations
  - Object detection
  - Text detection
  - Advanced Image filters and operations
- Database and in memory limitations -> Images are stored in-memory so there is no a defined limit of images that this system can handle
- Security system such as image encryption

## Future Integrations

- Live version
- AWS image storage to increase performance
- AI advanced filters
- API Throttling
- Image encryption for secure data exchange

## User Guide - Installation

To run this project on your local machine please follow these steps

1. Clone this repository in your machine by running **git clone**
2. Create a virtual environment in git repository
3. After virtual environment is create make sure to activate it and run **pip install requirements.txt**
4. After all dependencies are installed you can run the development sever by running python manage.py runserver
5. You will now have access to endpoints to perform operations with images

### Use example

Let's start with a simple image
![test image](/Design/testImage.jpg)
If we visit localhost/api/grayscale and send the image the
output will be as follows
![output image](/Design/response.png)
You can also add additional parameters such as channel weights.
