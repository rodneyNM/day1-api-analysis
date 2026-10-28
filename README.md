# Pesa Pulse Customer Data Analysis

**An end-to-end Python project for retrieving, cleaning, analysing, and visualising customer data from an API.**

## 1. Project Overview

Pesa Pulse is a fictional Nairobi-based fintech start-up that wants to understand its customer distribution before planning regional marketing campaigns.

In this project, I use Python to retrieve customer records from an API, explore the structure of the data, extract important customer attributes, analyse customer locations, and present the results through CSV files and visualisations.

The project demonstrates how Python can be used to transform raw JSON data into structured information that is easier to analyse and understand.

**Data source:** [JSONPlaceholder Users API](https://jsonplaceholder.typicode.com/users)


## 2. Project Objectives

The main objectives of this project are to:

- Retrieve JSON data from an API using Python Requests.
- Handle network errors and unsuccessful HTTP responses.
- Explore nested dictionaries and lists.
- Extract and flatten relevant customer attributes.
- Identify unique cities using Python sets.
- Count customers by city and email domain using dictionaries and comprehensions.
- Convert the extracted records into a pandas DataFrame.
- Validate Python aggregation results against pandas calculations.
- Export the results to CSV files.
- Create charts to communicate the findings visually.

## 3. Tools and Technologies

| Tool                  | Purpose                                      |
| --------------------- | -------------------------------------------- |
| Python                | Data processing and analysis                 |
| Requests              | Retrieving data from the API                 |
| JSON                  | Working with structured API responses        |
| Dictionaries and sets | Extracting, identifying, and counting values |
| pandas                | Organising data and validating calculations  |
| Matplotlib            | Creating data visualisations                 |
| CSV                   | Exporting structured data                    |
| Git and GitHub        | Version control and project sharing          |

## 4. Project Workflow

### Step 1: Retrieve Customer Data

I use the Python Requests library to send a GET request to the API endpoint.

The request includes a timeout to avoid waiting indefinitely. I also check the HTTP response status and handle request failures so the program displays a clear error message instead of an unhandled traceback.

### Step 2: Explore the Data Structure

The API returns customer records as a list of dictionaries. Some fields contain additional nested dictionaries.

I use a recursive function called `explore()` to print each key, its Python data type, and its position within the nested structure.

For example, geographic coordinates are accessed through:

```python
customer["address"]["geo"]["lat"]
customer["address"]["geo"]["lng"]
```

This step helps me understand how the information is organised before extracting it.

### Step 3: Extract and Flatten Customer Attributes

I use `extract_attributes()` to create a flat dictionary for each customer.

The extracted attributes include:

- Customer ID
- Name and username
- Email address and email domain
- Phone number
- City and ZIP code
- Latitude and longitude
- Company name
- Website

Latitude and longitude are converted into floating-point numbers to make them suitable for numerical and geographic analysis.

Flattening the records makes it easier to analyse the data in a table.

### Step 4: Identify Unique Cities

I use a Python set to identify distinct cities in the customer records.

A set stores unique values, so repeated city names appear only once.

I then compare the number of unique cities with the total number of customer records to understand whether customers share locations or are distributed across different cities.

### Step 5: Analyse Customer Distribution

I calculate customer counts using two approaches:

**Customers by city:** I use a Python loop and dictionary to count the number of customer records associated with each city.

**Customers by email domain:** I extract the domain from each valid email address and use a dictionary comprehension to count its occurrences.

I sort both summaries from the most common category to the least common category.

### Step 6: Convert Data into a DataFrame

I use pandas to convert the flattened customer records into a DataFrame.

I inspect the first few rows, print the DataFrame's shape, and check the data types of its columns.

I also use `value_counts()` to compare the pandas results with the counts calculated using plain Python. This provides a simple validation check.

### Step 7: Export the Results

I save the processed data and summary results as CSV files without the pandas index.

These files can be opened in spreadsheet applications or imported into other data analysis tools.

### Step 8: Visualise the Results

I use Matplotlib to create two bar charts:

1. **Customer Distribution by City:** Shows the number of customer records associated with each city.
2. **Customers by Email Domain:** Shows the number of records associated with each email domain.

The charts include titles and axis labels so they can be understood when shared in a report or presentation.

## 5. Project Structure

```text
day1-api-analysis/
├── analysis.py            
├── output/
│   ├── customers.csv
│   ├── city_counts.csv
│   └── customer_distribution.png
├── requirements.txt
└── README.md
```

### File descriptions

- `analysis.py`: Contains the Python functions and the complete analysis workflow.
- output/
- `customers.csv`: Contains the flattened customer records.
- `city_counts.csv`: Contains customer counts by city.
- `customer_distribution.png`: Visualises customer counts by city.
- `email_domain_distribution.png`: Visualises customer counts by email domain.
- `requirements.tx`t: requests, pandas, matplotlib
- `README.md`: Documents the project, methods, and findings.

##

## 6. Key Findings and Interpretation

The analysis helps answer three basic questions:

**How many customer records are available?**

The total number of records is displayed after retrieving the API response.

**Where are the customers located?**

The unique-city calculation and city count summary show how the sample records are distributed across cities.

**What does the email-domain distribution look like?**

The email-domain counts show how frequently each email domain occurs in the sample.

The city chart may show one record per city, resulting in bars of equal height. In that case, the email-domain chart may be more useful for demonstrating variation between categories, although it does not explain geographic distribution.

Because this project uses sample data, these results should not be interpreted as actual Pesa Pulse customer behaviour.

For real marketing decisions, verified customer locations could be grouped by county, region, or campaign territory to identify areas with higher customer concentrations.

## 7. Challenges and Learning Outcomes

Through this project, I practise:

- Making API requests and handling errors.
- Navigating nested JSON structures.
- Using recursion to inspect dictionaries and lists.
- Extracting and transforming data into a flat structure.
- Applying sets, loops, and dictionary comprehensions.
- Working with pandas DataFrames.
- Validating calculations using two different approaches.
- Exporting datasets and creating visualisations.
- Documenting a reproducible data analysis workflow.

The project reinforces the importance of understanding the source data before drawing conclusions from it.

## 8. Conclusion

This project demonstrates an end-to-end workflow for retrieving, transforming, analysing, and visualising data using Python.

By combining core Python data structures with pandas and Matplotlib, I turn a nested API response into structured datasets and visual summaries.

The experience provides a foundation for working with real-world business data and communicating findings that can support data-driven decisions.
