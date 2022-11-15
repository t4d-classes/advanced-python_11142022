# Exercise 2

How to run the client and server.

From the `python_demos` folder, run the server:

```bash
python -m rates_demo.rates_api
```

From the `python_demos` folder, run the client:

```bash
python -m rates_demo 
```

1. Implement this code in `__main__.py` in the `rates_demo` folder. 

2. Install the "requests" package from PyPi.org.

https://docs.python-requests.org/en/master/user/quickstart/#make-a-request

3. Using the "requests" package API, call the following URL for each date returned from the "business_days" function. Import the `business_days` function from the `business_days` module.

http://127.0.0.1:5000/api/2021-04-08?base=INR&symbols=USD,EUR

Specify a start date and an end date, and for each business day in the range, get the rate information from the rates API.

4. Create a list of text values from each response. The text value is formatted as JSON. Do not parse the JSON. Just put each JSON response in the list.

5. Display each list items in the console.