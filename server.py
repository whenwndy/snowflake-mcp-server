import json
import os
from pathlib import Path
from typing import Optional
from fastmcp import FastMCP
from pydantic import Field

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

_DATA_PATH = Path(__file__).parent / "data" / "snowflake.json"
_db: dict = json.loads(_DATA_PATH.read_text())


def _match(record: dict, field: str, value: str) -> bool:
    """Case-insensitive substring match on a field."""
    return value.lower() in str(record.get(field, "")).lower()


# ---------------------------------------------------------------------------
# Server
# ---------------------------------------------------------------------------

mcp = FastMCP(
    name="snowflake-mock",
    version="1.0.0",
    instructions=(
        "Mock Snowflake analytics platform. Query sales, labor, drive-thru ops, "
        "product performance, loyalty, and YoY comparisons across locations."
    ),
)

# ---------------------------------------------------------------------------
# Locations
# ---------------------------------------------------------------------------

@mcp.tool()
def get_locations(
    location_id: Optional[str] = Field(default=None, description="Filter by location ID, e.g. L001"),
    name: Optional[str] = Field(default=None, description="Filter by location name (partial match)"),
    market: Optional[str] = Field(default=None, description="Filter by market (partial match), e.g. Utah Valley"),
    franchise_group: Optional[str] = Field(default=None, description="Filter by franchise group (partial match)"),
) -> list[dict]:
    """List locations. Optionally filter by location_id, name, market, or franchise_group."""
    results = _db["locations"]
    if location_id:
        results = [r for r in results if r["location_id"].upper() == location_id.upper()]
    if name:
        results = [r for r in results if _match(r, "name", name)]
    if market:
        results = [r for r in results if _match(r, "market", market)]
    if franchise_group:
        results = [r for r in results if _match(r, "franchise_group", franchise_group)]
    return results


# ---------------------------------------------------------------------------
# Sales Summary
# ---------------------------------------------------------------------------

@mcp.tool()
def get_sales_summary(
    location_id: Optional[str] = Field(default=None, description="Filter by location ID, e.g. L001"),
    period: Optional[str] = Field(default=None, description="Filter by period (partial match), e.g. 2026-06-08/2026-07-15"),
) -> list[dict]:
    """Return sales summary records including gross sales, net sales, transaction count, and avg ticket."""
    results = _db["sales_summary"]
    if location_id:
        results = [r for r in results if r["location_id"].upper() == location_id.upper()]
    if period:
        results = [r for r in results if _match(r, "period", period)]
    return results


# ---------------------------------------------------------------------------
# Labor Summary
# ---------------------------------------------------------------------------

@mcp.tool()
def get_labor_summary(
    location_id: Optional[str] = Field(default=None, description="Filter by location ID, e.g. L001"),
    period: Optional[str] = Field(default=None, description="Filter by period (partial match)"),
) -> list[dict]:
    """Return labor summary records including total hours, overtime hours, labor cost, and labor cost %."""
    results = _db["labor_summary"]
    if location_id:
        results = [r for r in results if r["location_id"].upper() == location_id.upper()]
    if period:
        results = [r for r in results if _match(r, "period", period)]
    return results


# ---------------------------------------------------------------------------
# Drive-Thru Operations
# ---------------------------------------------------------------------------

@mcp.tool()
def get_drive_thru_operations(
    location_id: Optional[str] = Field(default=None, description="Filter by location ID, e.g. L001"),
    period: Optional[str] = Field(default=None, description="Filter by period (partial match)"),
) -> list[dict]:
    """Return drive-thru operations data including car count, avg service time, SOS by daypart, and order accuracy."""
    results = _db["drive_thru_operations"]
    if location_id:
        results = [r for r in results if r["location_id"].upper() == location_id.upper()]
    if period:
        results = [r for r in results if _match(r, "period", period)]
    return results


# ---------------------------------------------------------------------------
# Product Performance
# ---------------------------------------------------------------------------

@mcp.tool()
def get_product_performance(
    category: Optional[str] = Field(default=None, description="Filter by category (partial match), e.g. Slushies"),
    item_name: Optional[str] = Field(default=None, description="Filter by item name (partial match)"),
) -> list[dict]:
    """Return product performance records including revenue, units sold, revenue %, and attach rate."""
    results = _db["product_performance"]
    if category:
        results = [r for r in results if _match(r, "category", category)]
    if item_name:
        results = [r for r in results if _match(r, "item_name", item_name)]
    return results


# ---------------------------------------------------------------------------
# Customer Loyalty Metrics
# ---------------------------------------------------------------------------

@mcp.tool()
def get_customer_loyalty_metrics(
    location_id: Optional[str] = Field(default=None, description="Filter by location ID, e.g. L001"),
    period: Optional[str] = Field(default=None, description="Filter by period (partial match)"),
) -> list[dict]:
    """Return customer loyalty metrics including active members, visit frequency, avg spend, and redemption rate."""
    results = _db["customer_loyalty_metrics"]
    if location_id:
        results = [r for r in results if r["location_id"].upper() == location_id.upper()]
    if period:
        results = [r for r in results if _match(r, "period", period)]
    return results


# ---------------------------------------------------------------------------
# Void and Discount Report
# ---------------------------------------------------------------------------

@mcp.tool()
def get_void_and_discount_report(
    location_id: Optional[str] = Field(default=None, description="Filter by location ID, e.g. L001"),
    period: Optional[str] = Field(default=None, description="Filter by period (partial match)"),
) -> list[dict]:
    """Return void and discount report records including void counts/amounts, discounts, comps, refunds, and top reason."""
    results = _db["void_and_discount_report"]
    if location_id:
        results = [r for r in results if r["location_id"].upper() == location_id.upper()]
    if period:
        results = [r for r in results if _match(r, "period", period)]
    return results


# ---------------------------------------------------------------------------
# Year-Over-Year Comparison
# ---------------------------------------------------------------------------

@mcp.tool()
def get_year_over_year_comparison(
    location_id: Optional[str] = Field(default=None, description="Filter by location ID, e.g. L001"),
    period: Optional[str] = Field(default=None, description="Filter by period (partial match)"),
) -> list[dict]:
    """Return year-over-year comparison records including net sales, transactions, labor %, and YoY growth %."""
    results = _db["year_over_year_comparison"]
    if location_id:
        results = [r for r in results if r["location_id"].upper() == location_id.upper()]
    if period:
        results = [r for r in results if _match(r, "period", period)]
    return results


# ---------------------------------------------------------------------------
# Employee Labor Detail
# ---------------------------------------------------------------------------

@mcp.tool()
def get_employee_labor_detail(
    location_id: Optional[str] = Field(default=None, description="Filter by location ID, e.g. L001"),
    employee_id: Optional[str] = Field(default=None, description="Filter by employee ID, e.g. E101"),
    position: Optional[str] = Field(default=None, description="Filter by position (partial match), e.g. Shift Lead"),
) -> list[dict]:
    """Return employee-level labor detail including hours worked, overtime, labor cost, and avg clock-in/out times."""
    results = _db["employee_labor_detail"]
    if location_id:
        results = [r for r in results if r["location_id"].upper() == location_id.upper()]
    if employee_id:
        results = [r for r in results if r["employee_id"].upper() == employee_id.upper()]
    if position:
        results = [r for r in results if _match(r, "position", position)]
    return results


# ---------------------------------------------------------------------------
# Hourly Sales Heatmap
# ---------------------------------------------------------------------------

@mcp.tool()
def get_hourly_sales_heatmap(
    location_id: Optional[str] = Field(default=None, description="Filter by location ID, e.g. L001"),
    day_of_week: Optional[str] = Field(default=None, description="Filter by day of week (partial match), e.g. Monday"),
    hour: Optional[int] = Field(default=None, description="Filter by hour of day (0-23), e.g. 12"),
) -> list[dict]:
    """Return hourly sales heatmap records including gross sales and transaction count by location, day, and hour."""
    results = _db["hourly_sales_heatmap"]
    if location_id:
        results = [r for r in results if r["location_id"].upper() == location_id.upper()]
    if day_of_week:
        results = [r for r in results if _match(r, "day_of_week", day_of_week)]
    if hour is not None:
        results = [r for r in results if r["hour"] == hour]
    return results


# ---------------------------------------------------------------------------
# New Location Ramp Report
# ---------------------------------------------------------------------------

@mcp.tool()
def get_new_location_ramp_report(
    location_id: Optional[str] = Field(default=None, description="Filter by location ID, e.g. L006"),
    week: Optional[int] = Field(default=None, description="Filter by ramp week number, e.g. 1"),
) -> list[dict]:
    """Return new location ramp report records comparing a new location's weekly performance against chain averages."""
    results = _db["new_location_ramp_report"]
    if location_id:
        results = [r for r in results if r["location_id"].upper() == location_id.upper()]
    if week is not None:
        results = [r for r in results if r["week"] == week]
    return results


# ---------------------------------------------------------------------------
# Catering and Large Order Summary
# ---------------------------------------------------------------------------

@mcp.tool()
def get_catering_summary(
    location_id: Optional[str] = Field(default=None, description="Filter by location ID, e.g. L001"),
    period: Optional[str] = Field(default=None, description="Filter by period (partial match)"),
) -> list[dict]:
    """Return catering and large order summary records including order count, avg order value, lead time, and fulfillment accuracy."""
    results = _db["catering_and_large_order_summary"]
    if location_id:
        results = [r for r in results if r["location_id"].upper() == location_id.upper()]
    if period:
        results = [r for r in results if _match(r, "period", period)]
    return results


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
