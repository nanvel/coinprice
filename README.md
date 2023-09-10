# Duck typing, Abstract Basic Classes, and Typing Protocols

Made for [ThaiPy#95](https://www.meetup.com/thaipy-bangkok-python-meetup/events/293650816/) lightning talk.

[Typing Protocols](https://peps.python.org/pep-0544/): Structural subtyping (static duck typing)

1. Duck Typing (the current main.py content)
2. Use BaseExchange class
   1. Without raise NotImplementedError
   2. With raise NotImplementedError
3. Use ABC
4. Use ExchangeProtocol

## Make it broken

```diff
class BinanceUSDFuturesExchange(BaseExchange):
-     def get_symbol_price(self, symbol: str) -> Decimal:
+     def get_symbol_prices(self, symbol: str) -> Decimal:
```

## BaseExchange

```python
class BaseExchange:
    def get_symbol_price(self, symbol: str) -> Decimal:
        pass


class BinanceSpotExchange(BaseExchange):
    def get_symbol_price(self, symbol: str) -> Decimal:
        response = requests.get(
            f"https://api.binance.com/api/v3/avgPrice?symbol={symbol}"
        )
        return Decimal(response.json()["price"])


class BinanceUSDFuturesExchange(BaseExchange):
    def get_symbol_prices(self, symbol: str) -> Decimal:
        response = requests.get(
            f"https://fapi.binance.com/fapi/v1/ticker/price?symbol={symbol}"
        )
        return Decimal(response.json()["price"])
```

## NotImplementedError

```python
class BaseExchange:
    def get_symbol_price(self, symbol: str) -> Decimal:
        raise NotImplementedError()
```

## ABC

```python
class BaseExchange(ABC):
    @abstractmethod
    def get_symbol_price(self, symbol: str) -> Decimal:
        pass
```

## ExchangeProtocol

```python
class ExchangeProtocol(Protocol):
    def get_symbol_price(self, symbol: str) -> Decimal:
        pass


EXCHANGES: Dict[ExchangeEnum, ExchangeProtocol] = {
    ExchangeEnum.BINANCE_SPOT: BinanceSpotExchange(),
    ExchangeEnum.BINANCE_USD_FUTURES: BinanceUSDFuturesExchange(),
}
```
