"""Placeholder for AkShare-to-SQLite data synchronization.

Planned flow:
1. Fetch a small selected A-share universe from AkShare.
2. Fetch one year of daily prices for each selected stock.
3. Fetch one latest quote snapshot.
4. Normalize Chinese column names into stable English SQL columns.
5. Write stocks, daily_prices, and stock_quotes into SQLite.
"""


def main() -> None:
    raise NotImplementedError("AkShare sync will be implemented after the schema is finalized.")


if __name__ == "__main__":
    main()
