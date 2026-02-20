"""Script to create sample orders.parquet for the API. Run: python -m pip install pyarrow pandas && python scripts/create_sample_parquet.py"""
import pyarrow as pa
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

table = pa.table({
    "order_id": ["O1001", "O1002", "O1003", "O1004"],
    "customer_name": ["Arjun", "Priya", "Ravi", "Sneha"],
    "email": ["user@mail.com", "priya@mail.com", "ravi@mail.com", "sneha@mail.com"],
    "product": ["Laptop", "Monitor", "Keyboard", "Mouse"],
    "price": [1200.50, 350.00, 89.99, 45.50],
    "quantity": [1, 2, 3, 5],
    "city": ["Hyderabad", "Mumbai", "Hyderabad", "Bangalore"],
    "status": ["Completed", "Completed", "Shipped", "Completed"],
    "order_time": ["2024-01-06T00:00:00", "2024-01-07T10:30:00", "2024-01-08T14:15:00", "2024-01-09T09:00:00"],
})

pa.parquet.write_table(table, DATA_DIR / "orders.parquet")
print(f"Created {DATA_DIR / 'orders.parquet'}")
