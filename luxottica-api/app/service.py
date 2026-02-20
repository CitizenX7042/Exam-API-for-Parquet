import pandas as pd
from pathlib import Path

from app.models import Order, SalesPerCity


# In-memory dataframe (loaded at startup)
_orders_df: pd.DataFrame | None = None


def load_orders(parquet_path: str | Path) -> None:
    """Load orders from parquet file into memory."""
    global _orders_df
    path = Path(parquet_path)
    if not path.exists():
        raise FileNotFoundError(f"Parquet file not found: {path}")
    _orders_df = pd.read_parquet(path)


def get_order(order_id: str) -> Order | None:
    """Get a single order by order_id. Returns None if not found."""
    if _orders_df is None:
        raise RuntimeError("Orders not loaded. Ensure load_orders() was called at startup.")
    row = _orders_df[_orders_df["order_id"] == order_id]
    if row.empty:
        return None
    record = row.iloc[0].to_dict()
    # Convert order_time to string (handle NaT/NaN)
    ot = record.get("order_time")
    if pd.isna(ot):
        record["order_time"] = ""
    elif hasattr(ot, "isoformat"):
        record["order_time"] = ot.isoformat()
    return Order(**record)


def get_sales_per_city() -> list[SalesPerCity]:
    """Get total sales grouped by city."""
    if _orders_df is None:
        raise RuntimeError("Orders not loaded. Ensure load_orders() was called at startup.")
    df = _orders_df.copy()
    df["line_total"] = df["price"] * df["quantity"]
    grouped = df.groupby("city")["line_total"].sum().reset_index()
    grouped.columns = ["city", "total_sales"]
    return [SalesPerCity(city=row["city"], total_sales=round(row["total_sales"], 2)) for _, row in grouped.iterrows()]
