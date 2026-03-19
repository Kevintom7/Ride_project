# Ride_project 

## Description
Ride_project is a simple Ride Sharing API built with Django and Django REST Framework.  
It allows users to create rides, track driver locations, and update ride status.

## Features
- User Authentication (JWT)
- Create Ride
- Accept Ride (Driver)
- Update Ride Status
- Update Driver Location

## Tech Stack
- Python 3
- Django
- Django REST Framework
- JWT Authentication

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | /rides/ | Create a ride |
| POST   | /rides/{id}/accept/ | Driver accepts ride |
| POST   | /rides/{id}/update_status/ | Update ride status |
| POST   | /rides/{id}/update_location/ | Update driver location |

