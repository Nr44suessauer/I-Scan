
# System Architecture

This document explains the architecture of the project. Based on the available API with which the user can interact, the underlying processes and structures are explained. This includes the various HTTP methods used to communicate with the server, as well as the specific commands and their functionality within the system.

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Introduction to REST APIs](#introduction-to-rest-apis)
    - [HTTP Methods](#http-methods)
3. [System Architecture Overview](#system-architecture-overview)
4. [API-DC Web Server](#api-dc-web-server)
5. [Explanation of Commands](#explanation-of-commands)
    - [DELETE](#delete)
    - [GET](#get)
    - [POST/PUT](#postput)

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

## System Architecture Overview

<div style="display: flex; align-items: center;">
    <div style="flex: 1;">
        <img src="https://github.com/Nr44suessauer/I-Scan/blob/main/docs/diagram/Architecture_Diagram/SystemArchitecture%20V3.0%20%20Http_server%20+%20Lightmodule.png?raw=true" alt="System Architecture">
    </div>
    <div style="flex: 1; padding-left: 20px;">
        The architecture of the <strong>I-Scan</strong> is shown. Through a <strong>REST API</strong>, the user/developer has the opportunity to interact with the various components in this diagram. A <strong>REST API</strong> and a web server are provided for this purpose. Now, the accessible commands are explained, and the processes behind them are discussed. The main system represents the user and has an evaluative function. Photogrammetry or similar processes will take place on this system. The I-Scan runs autonomously after it has been configured and started. Upon completion of the scan, the main system should retrieve the raw scan data via the REST API.
    </div>
</div>

---

## API-DC Web Server

| Command  | Description            | Variables Sent                                                                 | Return                                      | Example Call                                                                 |
|----------|------------------------|-------------------------------------------------------------------------------|---------------------------------------------|------------------------------------------------------------------------------|
| `DELETE` | Delete general config  | -                                                                             | Status                                      | `curl -X DELETE http://<I-Scan Ip adress>/api/config/general`                          |
| `DELETE` | Delete scan config     | -                                                                             | Status                                      | `curl -X DELETE http://<I-Scan Ip adress>/api/config/scan`                             |
| `GET`    | Get general config     | -                                                                             | Configuration (IP addresses of units, etc.) | `curl -X GET http://<I-Scan Ip adress>/api/config/general`                             |
| `GET`    | Get single picture     | `Cam X`, `Height of pic (Z-Axis)`, `Angle of pic (Y-Axis)`                     | Single Picture                              | `curl -X GET "http://<I-Scan Ip adress>/api/picture?cam=X&height=Z&angle=Y"`           |
| `GET`    | Get scan status        | -                                                                             | Status of progress/operation status         | `curl -X GET http://<I-Scan Ip adress>/api/scan/status`                                |
| `PUT` `POST`    | Update general config  | `General settings: PositionUnit IP addresses`, `Lighting Unit IP addresses`   | Status                                      | `curl -X PUT -d '{"positionUnitIPs": [...], "lightingUnitIPs": [...]}' http://<I-Scan Ip adress>/api/config/general` |
| `PUT` `POST` | Update lighting config | `Lighting Unit`, `Color HEX code (RGB + intensity = 4 Byte)`                  | Status                                      | `curl -X PUT -d '{"lightingUnit": ..., "colorHex": ...}' http://<I-Scan Ip adress>/api/config/lighting` |
| `PUT` `POST`| Update scan config     | `Number of pics`, `Machine resolution (num. of pics / ΔZ)`, `Cameras for use`, `Height of object (rough measurements)`, `Distance to the object (rough measurements - I-Scan to object)` | Status | `curl -X PUT -d '{"numPics": ..., "resolution": ..., "cameras": [...], "height": ..., "distance": ...}' http://<I-Scan Ip adress>/api/config/scan` |
| `POST`   | Start scan             | -                                                                             | Status                                      | `curl -X POST http://<I-Scan Ip adress>/api/scan/start`                                |

---

## Explanation of Commands

### DELETE

- **Delete general config**: This command deletes the general configuration of the system. No variables are sent, and the return value is the status of the operation. Example call: `curl -X DELETE http://<I-Scan Ip adress>/api/config/general`
- **Delete scan config**: This command deletes the configuration for the scanning process. No variables are sent, and the return value is the status of the operation. Example call: `curl -X DELETE http://<I-Scan Ip adress>/api/config/scan`

### GET

- **Get general config**: This command retrieves the general configuration of the system, such as the IP addresses of the units. No variables are sent, and the return value is the configuration. Example call: `curl -X GET http://<I-Scan Ip adress>/api/config/general`
- **Get single picture**: This command retrieves a single picture from the camera. The variables sent are the camera (Cam X), the height of the picture (Z-Axis), and the angle of the picture (Y-Axis). The return value is the single picture. Example call: `curl -X GET "http://<I-Scan Ip adress>/api/picture?cam=X&height=Z&angle=Y"`
- **Get scan status**: This command retrieves the status of the scanning process. No variables are sent, and the return value is the progress or operation status. Example call: `curl -X GET http://<I-Scan Ip adress>/api/scan/status`

### POST/PUT

- **Update general config**: This command updates the general configuration of the system. The variables sent are the general settings such as the IP addresses of the position unit and the lighting unit. The return value is the status of the operation. Example call: `curl -X PUT -d '{"positionUnitIPs": [...], "lightingUnitIPs": [...]}' http://<I-Scan Ip adress>/api/config/general`
- **Update lighting config**: This command updates the configuration of the lighting unit. The variables sent are the lighting unit and the color HEX code (RGB + intensity = 4 bytes). The return value is the status of the operation. Example call: `curl -X PUT -d '{"lightingUnit": ..., "colorHex": ...}' http://<I-Scan Ip adress>/api/config/lighting`
- **Update scan config**: This command updates the configuration for the scanning process. The variables sent are the number of pictures, the machine resolution (number of pictures / ΔZ), the cameras to be used, the height of the object (rough measurements), and the distance to the object (rough measurements - I-Scan to object). The return value is the status of the operation. Example call: `curl -X PUT -d '{"numPics": ..., "resolution": ..., "cameras": [...], "height": ..., "distance": ...}' http://<I-Scan Ip adress>/api/config/scan`
- **Start scan**: This command starts the scanning process. No variables are sent, and the return value is the status of the operation. Example call: `curl -X POST http://<I-Scan Ip adress>/api/scan/start`

---






