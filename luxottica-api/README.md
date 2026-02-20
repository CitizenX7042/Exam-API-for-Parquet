# Luxottica Orders API

A FastAPI application that serves order and sales data from a Parquet file.

## Project Structure

```
luxottica-api/
│
├── app/
│   ├── main.py      # FastAPI app & endpoints
│   ├── service.py   # Business logic & parquet handling
│   └── models.py    # Pydantic response models
│
├── data/
│   └── orders.parquet
│
├── requirements.txt
└── README.md
```

## Setup

### 1. Create Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Create Sample Data (if needed)

If `data/orders.parquet` doesn't exist, run:

```bash
python scripts/create_sample_parquet.py
```

## Run the API

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

### GET /order/{order_id}

Returns a single order by ID.

**Path parameter:** `order_id` (string)

**Example:** `GET /order/O1001`

**Response:**
```json
{
  "order_id": "O1001",
  "customer_name": "Arjun",
  "email": "user@mail.com",
  "product": "Laptop",
  "price": 1200.5,
  "quantity": 1,
  "city": "Hyderabad",
  "status": "Completed",
  "order_time": "2024-01-06T00:00:00"
}
```

Returns **404** if the order is not found.

### GET /sales-per-city

Returns total sales grouped by city (sum of price × quantity per city).

**Example:** `GET /sales-per-city`

**Response:**
```json
[
  {
    "city": "Hyderabad",
    "total_sales": 12345.67
  },
  {
    "city": "Mumbai",
    "total_sales": 5678.9
  }
]
```

## Testing the Endpoints

### Using curl

```bash
# Get single order
curl http://127.0.0.1:8000/order/O1001

# Order not found (returns 404)
curl http://127.0.0.1:8000/order/O9999

# Sales per city
curl http://127.0.0.1:8000/sales-per-city
```

### Using the Swagger UI

Open your browser and go to:

- **Swagger UI:** http://127.0.0.1:8000/docs  
- **ReDoc:** http://127.0.0.1:8000/redoc  

You can try out all endpoints interactively from the Swagger UI.
