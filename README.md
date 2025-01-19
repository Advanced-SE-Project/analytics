# Analytics Microservice

A microservice for providing financial analytics, designed to aggregate and analyze user transaction data. This microservice is built with **Python, Flask, and Requests**. It integrates with the **Transaction Management** service to retrieve transaction data. If JWT-based security is enforced, it can forward tokens to the Transaction Management service via the API Gateway.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Running the Microservice](#running-the-microservice)
- [API Documentation](#api-documentation)
- [API Endpoints](#api-endpoints)
- [Technologies Used](#technologies-used)

## Features

- **Line Chart Data**: Monthly income vs. expenses over a given date range.
- **Pie Chart Data**: Breakdown of income or expenses by category for a specified period.
- **Bar Chart Data**: Monthly totals for a selected category (income or expense).
- **JWT Forwarding**: If authentication is enabled, JWT tokens are forwarded to the Transaction Management microservice.

## Installation

1. Clone this repository:

   ```bash
   git clone <repository_url>
   cd analytics-microservice
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables

Create a `.env` file in the root directory with the following configuration:

```plaintext
TRANSACTION_SERVICE_URL=http://localhost:3000/transaction-service/api
PORT=5000
DEBUG=True
```

- **TRANSACTION_SERVICE_URL**: The URL of the Transaction Management microservice (often via an API Gateway).
- **PORT**: The port on which the Flask application runs (default: `5000`).
- **DEBUG**: Enables or disables Flask debug mode.

## Running the Microservice

**Ensure that the Transaction Management service is running before starting this microservice.**

1. Set up environment variables (optional if using `.env`):

   ```bash
   # On Windows:
   set FLASK_APP=src.app
   set FLASK_RUN_PORT=5000
   set FLASK_DEBUG=1

   # On Unix/macOS:
   export FLASK_APP=src.app
   export FLASK_RUN_PORT=5000
   export FLASK_DEBUG=1
   ```

2. Start the service:

   ```bash
   flask run
   ```

   The server will start on `http://localhost:5000`.

3. **Using Docker (Optional)**:

   ```bash
   docker build -t analytics-service .
   docker run -p 5000:5000 analytics-service
   ```

## API Documentation

This microservice does not currently include **Swagger documentation** by default. However, the API endpoints are described below.

## API Endpoints

Each endpoint requires a `userId` to identify the user’s transactions. **Date ranges are specified using `startMonth` and `endMonth` in `MM-YYYY` format**.

### 1. Line Chart (Income vs. Expenses)

- **GET** `/analytics/line`
- **Query Parameters**:
  - `userId` (integer, required)
  - `startMonth` (string, required) – Format: `MM-YYYY`
  - `endMonth` (string, required) – Format: `MM-YYYY`
- **Response**:
  ```json
  {
    "labels": ["01-2024", "02-2024", "03-2024"],
    "incomeData": [3000.0, 1400.0, 2800.5],
    "expenseData": [500.0, 1200.75, 1300.5]
  }
  ```


  EXAMPLE: http://localhost:5000/analytics/line?userId=101&startMonth=01-2024&endMonth=12-2024

### 2. Pie Chart (Expenses Breakdown)

- **GET** `/analytics/pie/expense`
- **Query Parameters**:
  - `userId` (integer, required)
  - `startMonth` (string, required) – Format: `MM-YYYY`
  - `endMonth` (string, required) – Format: `MM-YYYY`
- **Response**:
  ```json
  {
    "labels": ["Rent", "Groceries", "Utilities", "Entertainment", "Other"],
    "data": [800.0, 1200.75, 300.0, 50.5, 0.0]
  }
  ```
  EXAMPLE: http://localhost:5000/analytics/pie/expense?userId=101&startMonth=01-2024&endMonth=12-2024

### 3. Pie Chart (Income Breakdown)

- **GET** `/analytics/pie/income`
- **Query Parameters**:
  - `userId` (integer, required)
  - `startMonth` (string, required) – Format: `MM-YYYY`
  - `endMonth` (string, required) – Format: `MM-YYYY`
- **Response**:
  ```json
  {
    "labels": ["Salary", "Investment", "Gift", "Refund", "Other"],
    "data": [2000.0, 300.5, 400.0, 250.0, 50.0]
  }
  ```
  EXAMPLE: http://localhost:5000/analytics/pie/income?userId=101&startMonth=01-2024&endMonth=12-2024

### 4. Bar Chart (Category Trend)

- **GET** `/analytics/bar`
- **Query Parameters**:
  - `userId` (integer, required)
  - `startMonth` (string, required) – Format: `MM-YYYY`
  - `endMonth` (string, required) – Format: `MM-YYYY`
  - `type` (string, required) – Either `"Income"` or `"Expense"`
  - `category` (string, required) – E.g., `"Groceries"`, `"Salary"`
- **Response**:
  ```json
  {
    "labels": ["01-2024", "02-2024", "03-2024"],
    "data": [200.0, 300.25, 0.0]
  }
  ```

  EXAMPLE: http://localhost:5000/analytics/bar?userId=101&startMonth=01-2024&endMonth=12-2024&type=Expense&category=Rent


**Note:** If JWT authentication is enabled, requests must include:

```plaintext
Authorization: Bearer <token>
```

## Technologies Used

- **Python**: High-level programming language.
- **Flask**: A lightweight web framework for building REST APIs.
- **Requests**: Used for making API calls to the Transaction Management microservice.
- **Docker**: Containerization for consistent deployment.
- **JWT (optional)**: If authentication is required, JWT tokens are forwarded via the API Gateway.

---

This **Analytics Microservice** is a core component of the **Personal Budgeting Assistant** project, enabling insightful charts and breakdowns of user financial data.