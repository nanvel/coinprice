from decimal import Decimal
from enum import Enum

import requests
import typer


app = typer.Typer()


class BinanceSpotExchange:
    def get_symbol_price(self, symbol: str) -> Decimal:
        response = requests.get(
            f"https://api.binance.com/api/v3/avgPrice?symbol={symbol}"
        )
        return Decimal(response.json()["price"])


class BinanceUSDFuturesExchange:
    def get_symbol_price(self, symbol: str) -> Decimal:
        response = requests.get(
            f"https://fapi.binance.com/fapi/v1/ticker/price?symbol={symbol}"
        )
        return Decimal(response.json()["price"])


class ExchangeEnum(str, Enum):
    BINANCE_SPOT = "binance_spot"
    BINANCE_USD_FUTURES = "binance_usd_futures"


EXCHANGES = {
    ExchangeEnum.BINANCE_SPOT: BinanceSpotExchange(),
    ExchangeEnum.BINANCE_USD_FUTURES: BinanceUSDFuturesExchange(),
}


def main(exchange: ExchangeEnum, symbol: str):
    price = EXCHANGES[exchange].get_symbol_price(symbol)

    print(price)


if __name__ == "__main__":
    typer.run(main)
