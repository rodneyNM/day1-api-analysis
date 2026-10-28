"""
Day 1 - API Data Analysis Using Python Structures
Squad Python Specialization - Data Science, AI & Analytics
"""

# STEP 1: Import libraries for file paths, API requests, tables, and charts.
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests

# STEP 2: Store the API endpoint and the folder for generated files.
API_URL = "https://jsonplaceholder.typicode.com/users"
OUTPUT_DIR = Path("output")


# STEP 3: Retrieve JSON data from the API and handle request errors.
def get_customers(url: str = API_URL) -> list[dict]:
    """Fetch the customer list. Report failures clearly instead of crashing."""
    try:
        # Send a GET request and stop waiting after 10 seconds.
        response = requests.get(url, timeout=10)
        # Raise an exception if the server responds with an HTTP error.
        response.raise_for_status()
        # Convert the JSON response into Python lists and dictionaries.
        customers = response.json()

        if not isinstance(customers, list):
            print("Failed to retrieve customer data: API response was not a list.")
            return []

        return customers
    except requests.exceptions.RequestException as error:
        print(f"Failed to retrieve customer data: {error}")
        return []
    except ValueError as error:
        print(f"Failed to parse customer data as JSON: {error}")
        return []


# STEP 4: Recursively inspect keys and value types in nested dictionaries/lists.
def explore(record: dict, indent: int = 0) -> None:
    """Print every key in a (possibly nested) record with its type, indented by depth."""
    # Add spaces so nested levels are visually indented.
    prefix = " " * indent

    if isinstance(record, dict):
        # Visit every key/value pair in this dictionary.
        for key, value in record.items():
            print(f"{prefix}{key}: {type(value).__name__}")
            # If this value is nested, explore its contents too.
            if isinstance(value, (dict, list)):
                explore(value, indent + 4)
    elif isinstance(record, list):
        # Lists have numbered items, so enumerate gives each item its index.
        for index, value in enumerate(record):
            print(f"{prefix}[{index}]: {type(value).__name__}")
            if isinstance(value, (dict, list)):
                explore(value, indent + 4)


# STEP 5: Flatten each customer into a dictionary with the required fields.
def extract_attributes(customers: list[dict]) -> list[dict]:
    """Return one flat dict per customer with the attributes listed in the task."""
    # Store one flattened dictionary for each customer.
    rows = []

    for customer in customers:
        # Safely access the nested address, geography, and company objects.
        address = customer.get("address") or {}
        geo = address.get("geo") or {}
        email = customer.get("email") or ""
        company = customer.get("company") or {}

        # Convert latitude to a float; use None if it is absent or invalid.
        try:
            latitude = float(geo["lat"])
        except (KeyError, TypeError, ValueError):
            latitude = None

        # Convert longitude to a float; use None if it is absent or invalid.
        try:
            longitude = float(geo["lng"])
        except (KeyError, TypeError, ValueError):
            longitude = None

        email_domain = email.rsplit("@", 1)[1].lower() if "@" in email else None

        # Assemble the selected fields into one flat customer record.
        rows.append({
            "id": customer.get("id"),
            "name": customer.get("name"),
            "username": customer.get("username"),
            "email": email or None,
            "email_domain": email_domain,
            "phone": customer.get("phone"),
            "city": address.get("city"),
            "zipcode": address.get("zipcode"),
            "latitude": latitude,
            "longitude": longitude,
            "company": company.get("name"),
            "website": customer.get("website"),
        })

    return rows


# STEP 6: Use a set to return each city only once.
def unique_cities(customers: list[dict]) -> set[str]:
    """Return the set of distinct cities."""
    return {
        address.get("city")
        for customer in customers
        if (address := (customer.get("address") or {})).get("city")
    }


# STEP 7: Count customers by city with a normal Python dictionary and loop.
def city_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per city using a loop (no Counter and no pandas)."""
    # Start with an empty dictionary of city totals.
    counts = {}
    for customer in customers:
        address = customer.get("address") or {}
        city = address.get("city")
        if city:
            # Add one to this city; start from zero if it is the first record.
            counts[city] = counts.get(city, 0) + 1
    return counts


# STEP 8: Count email domains using a dictionary comprehension.
def email_domain_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per email domain using a dictionary comprehension."""
    # Extract the part of each valid email address that follows the @ sign.
    domains = [
        email.rsplit("@", 1)[1].lower()
        for customer in customers
        if (email := (customer.get("email") or "")) and "@" in email
    ]
    # Count each distinct domain and return the results as a dictionary.
    return {domain: domains.count(domain) for domain in set(domains)}


# STEP 9: Convert the flattened records into a pandas DataFrame.
def to_dataframe(rows: list[dict]) -> pd.DataFrame:
    """Convert flattened customer records to a pandas DataFrame."""
    # Keep the requested columns in a consistent order.
    return pd.DataFrame(rows, columns=[
        "id", "name", "username", "email", "email_domain", "phone",
        "city", "zipcode", "latitude", "longitude", "company", "website"
    ])


# STEP 10: Create and save the customer-by-city chart.
def plot_distribution(counts: dict[str, int], path: Path) -> None:
    """Save a labelled chart of a distribution to path."""
    # Ensure the destination folder exists before saving the chart.
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    # Sort from highest count to lowest, then alphabetically for ties.
    sorted_items = sorted(counts.items(), key=lambda item: (-item[1], item[0]))

    labels = [item[0] for item in sorted_items]
    values = [item[1] for item in sorted_items]

    # Create the bar chart and label it for a reader or presentation slide.
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(labels, values)
    ax.set_title("Pesa Pulse: Customer Distribution by City")
    ax.set_xlabel("City")
    ax.set_ylabel("Number of customers")
    ax.tick_params(axis="x", labelrotation=45)
    for label in ax.get_xticklabels():
        label.set_horizontalalignment("right")
    fig.tight_layout()
    # Save a high-resolution PNG and close the figure to free resources.
    # Save the PNG and close the figure when finished.
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


# STEP 11: Create a second chart showing customers by email domain.
def plot_email_domain_distribution(counts: dict[str, int], path: Path) -> None:
    """Save a second chart, showing customers by email domain."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    sorted_items = sorted(counts.items(), key=lambda item: (-item[1], item[0]))

    labels = [item[0] for item in sorted_items]
    values = [item[1] for item in sorted_items]

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(labels, values)
    ax.set_title("Pesa Pulse: Customers by Email Domain")
    ax.set_xlabel("Email domain")
    ax.set_ylabel("Number of customers")
    ax.tick_params(axis="x", labelrotation=45)
    for label in ax.get_xticklabels():
        label.set_horizontalalignment("right")
    fig.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)


# STEP 12: Run the complete workflow from retrieval through export.
def main() -> None:
    # Create the output folder if it does not already exist.
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Retrieve the customer data; stop if the request failed or returned no rows.
    customers = get_customers()
    if not customers:
        print("No customer data retrieved; stopping analysis.")
        return

    print(f"Total customer records: {len(customers)}")

    # STEP 12A: Explore the nested structure of the first customer.
    print("\n--- Nested structure of first record ---")
    explore(customers[0])

    # STEP 12B: Flatten the nested records and convert them to a DataFrame.
    rows = extract_attributes(customers)
    df = to_dataframe(rows)

    # STEP 12C: Compare the number of unique cities with the total records.
    cities = unique_cities(customers)
    print(f"\nUnique cities: {len(cities)}")
    print(f"Customer records: {len(customers)}")
    print(
        "Marketing interpretation: comparing unique cities with total records "
        "shows whether the sample has repeated city locations or one distinct "
        "city per record."
    )

    # STEP 12D: Calculate plain-Python city and email-domain summaries.
    cities_by_count = sorted(city_counts(customers).items(),
                             key=lambda item: (-item[1], item[0]))
    domains_by_count = sorted(email_domain_counts(customers).items(),
                              key=lambda item: (-item[1], item[0]))

    print("\n--- Customer counts by city (plain Python) ---")
    for city, count in cities_by_count:
        print(f"{city}: {count}")

    print("\n--- Customer counts by email domain (plain Python) ---")
    for domain, count in domains_by_count:
        print(f"{domain}: {count}")

    # STEP 12E: Recalculate the summaries in pandas to verify the Python counts.
    pandas_city_counts = df["city"].value_counts()
    pandas_domain_counts = df["email_domain"].value_counts()

    print("\n--- Customer counts by city (pandas) ---")
    print(pandas_city_counts)
    print("\n--- Customer counts by email domain (pandas) ---")
    print(pandas_domain_counts)

    # Compare both sets of counts after sorting their labels.
    python_city = pd.Series(city_counts(customers), dtype="int64").sort_index()
    pandas_city = pandas_city_counts.sort_index()
    python_domains = pd.Series(email_domain_counts(customers), dtype="int64").sort_index()
    pandas_domains = pandas_domain_counts.sort_index()

    print("\nCity counts agree with pandas:", python_city.equals(pandas_city))
    print("Email-domain counts agree with pandas:", python_domains.equals(pandas_domains))

    # STEP 12F: Print a preview, dimensions, and data types of the DataFrame.
    print("\n--- DataFrame preview ---")
    print(df.head())
    print("\nDataFrame shape:", df.shape)
    print("\nDataFrame dtypes:")
    print(df.dtypes)

    # STEP 12G: Export customer details to CSV without the DataFrame index.
    df.to_csv(OUTPUT_DIR / "customers.csv", index=False)

    # Export city totals with the required city and count columns.
    city_df = pd.DataFrame(cities_by_count, columns=["city", "count"])
    city_df.to_csv(OUTPUT_DIR / "city_counts.csv", index=False)

    # STEP 12H: Save the city chart and the additional email-domain chart.
    plot_distribution(dict(cities_by_count), OUTPUT_DIR / "customer_distribution.png")
    plot_email_domain_distribution(
        dict(domains_by_count), OUTPUT_DIR / "email_domain_distribution.png"
    )

    print(f"\nOutputs saved in: {OUTPUT_DIR.resolve()}")


# STEP 13: Run main() only when this file is executed directly.
if __name__ == "__main__":
    main()
