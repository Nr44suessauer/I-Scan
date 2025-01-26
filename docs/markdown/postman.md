## Using Postman

To trigger these API calls using Postman, follow these steps:

1. Open Postman and create a new request.
2. Select the appropriate HTTP method (GET, POST, PUT, DELETE) from the dropdown.
3. Enter the URL for the API endpoint in the request URL field.
4. If the request requires parameters, go to the "Params" tab and add the necessary key-value pairs.
5. For requests that require a body (e.g., POST, PUT), go to the "Body" tab, select "raw", and choose "JSON" from the dropdown. Enter the JSON payload in the text area.
6. Click "Send" to execute the request and view the response.

Example for starting a scan:
1. Select `POST` method.
2. Enter `http://<server>/api/scan/start` in the request URL field.
3. Click "Send".

