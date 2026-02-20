from pathlib import Path

from fastapi import FastAPI, HTTPException

from app import service
from app.models import Order, SalesPerCity

app = FastAPI(
    title="Luxottica Orders API",
    description="API for querying orders and sales data from parquet",
    version="1.0.0",
)


@app.on_event("startup")
def startup_load_parquet():
    """Load parquet data into memory at application startup."""
    base_dir = Path(__file__).resolve().parent.parent
    parquet_path = base_dir / "data" / "orders.parquet"
    try:
        service.load_orders(parquet_path)
    except FileNotFoundError as e:
        raise RuntimeError(
            f"Failed to start: {e}. Ensure data/orders.parquet exists."
        ) from e


@app.get(
    "/order/{order_id}",
    response_model=Order,
    responses={
        200: {"description": "Order found"},
        404: {"description": "Order not found"},
        503: {"description": "Service unavailable"},
    },
)
def get_order(order_id: str):
    """Get a single order by order_id."""
    try:
        order = service.get_order(order_id)
        if order is None:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.get(
    "/sales-per-city",
    response_model=list[SalesPerCity],
    responses={
        200: {"description": "Sales per city"},
        503: {"description": "Service unavailable"},
    },
)
def get_sales_per_city():
    """Get total sales grouped by city."""
    try:
        return service.get_sales_per_city()
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
