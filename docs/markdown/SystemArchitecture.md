
# System Architecture

This document explains the architecture of the project. Based on the available API with which the user can interact, the underlying processes and structures are explained. This includes the various HTTP methods used to communicate with the server, as well as the specific commands and their functionality within the system.

---

## Table of Contents

1. [Introduction](#system-architecture)
2. [Introduction to REST APIs](#introduction-to-rest-apis)
    - [HTTP Methods](#http-methods)
3. [API-DC Web Server](#api-dc-web-server)
4. [Explanation of Commands](#explanation-of-commands)
    - [DELETE](#delete)
    - [GET](#get)
    - [POST/PUT](#post-put)

---

## Introduction to REST APIs

REST APIs (Representational State Transfer Application Programming Interfaces) are a set of rules and conventions for building and interacting with web services. They allow different systems to communicate over HTTP by using standard HTTP methods such as `GET`, `POST`, `PUT`, and `DELETE`. These methods enable clients to perform various operations on the server, such as retrieving configurations, updating settings, and managing scan processes.

### HTTP Methods

- **GET**: This method is used to retrieve data from the server. It is commonly used to read resources such as files, database entries, or other information. An example would be fetching a list of users.

- **POST**: This method is used to send new data to the server and create a new resource. An example would be creating a new user in a database.

- **PUT**: This method is used to update or replace an existing resource on the server. An example would be updating the information of an existing user.

- **DELETE**: This method is used to delete a resource from the server. An example would be removing a user from a database.

REST APIs are widely used due to their simplicity, scalability, and stateless nature, making them ideal for modern web applications. They provide a flexible and efficient way to exchange data between client and server, enabling the integration of different systems and services.


---

![System Architecture](https://github.com/Nr44suessauer/I-Scan/blob/main/docs/diagram/Architecture_Diagram/SystemArchitecture%20V3.0%20%20Http_server%20+%20Lightmodule.png?raw=true)



--- 

## API-DC Web Server

| Command  | Description            | Variables Sent                                                                 | Return                                      |
|----------|------------------------|-------------------------------------------------------------------------------|---------------------------------------------|
| `DELETE` | Delete general config  | -                                                                             | Status                                      |
| `DELETE` | Delete scan config     | -                                                                             | Status                                      |
| `GET`    | Get general config     | -                                                                             | Configuration (IP addresses of units, etc.) |
| `GET`    | Get single picture     | `Cam X`, `Height of pic (Z-Axis)`, `Angle of pic (Y-Axis)`                     | Single Picture                              |
| `GET`    | Get scan status        | -                                                                             | Status of progress/operation status         |
| `PUT` `POST`    | Update general config  | `General settings: PositionUnit IP addresses`, `Lighting Unit IP addresses`   | Status                                      |
| `PUT` `POST` | Update lighting config | `Lighting Unit`, `Color HEX code (RGB + intensity = 4 Byte)`                  | Status                                      |
| `PUT` `POST`| Update scan config     | `Number of pics`, `Machine resolution (num. of pics / ΔZ)`, `Cameras for use`, `Height of object (rough measurements)`, `Distance to the object (rough measurements - I-Scan to object)` | Status |
| `POST`   | Start scan             | -                                                                             | Status                                      |

---



## Explanation of Commands

### DELETE

- **Delete general config**: This command deletes the general configuration of the system. No variables are sent, and the return value is the status of the operation.
- **Delete scan config**: This command deletes the configuration for the scanning process. No variables are sent, and the return value is the status of the operation.

### GET

- **Get general config**: This command retrieves the general configuration of the system, such as the IP addresses of the units. No variables are sent, and the return value is the configuration.
- **Get single picture**: This command retrieves a single picture from the camera. The variables sent are the camera (Cam X), the height of the picture (Z-Axis), and the angle of the picture (Y-Axis). The return value is the single picture.
- **Get scan status**: This command retrieves the status of the scanning process. No variables are sent, and the return value is the progress or operation status.

### POST/PUT

- **Update general config**: This command updates the general configuration of the system. The variables sent are the general settings such as the IP addresses of the position unit and the lighting unit. The return value is the status of the operation.
- **Update lighting config**: This command updates the configuration of the lighting unit. The variables sent are the lighting unit and the color HEX code (RGB + intensity = 4 bytes). The return value is the status of the operation.
- **Update scan config**: This command updates the configuration for the scanning process. The variables sent are the number of pictures, the machine resolution (number of pictures / ΔZ), the cameras to be used, the height of the object (rough measurements), and the distance to the object (rough measurements - I-Scan to object). The return value is the status of the operation.
- **Start scan**: This command starts the scanning process. No variables are sent, and the return value is the status of the operation.

