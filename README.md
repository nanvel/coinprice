# Duck typing, Abstract Base Classes, and Typing Protocols

Made for [ThaiPy#95](https://www.meetup.com/thaipy-bangkok-python-meetup/events/293650816/) lightning talk.

[PEP 544](https://peps.python.org/pep-0544/) - Protocols: Structural subtyping (static duck typing)

Since Python 3.8.

1. Static vs at runtime
2. Duck Typing (the current main.py content)
3. Use BaseExchange class
   1. Without raise NotImplementedError
   2. With raise NotImplementedError
4. Use ABC
5. Use ExchangeProtocol

## Structural subtyping

Structural subtyping: an object that has certain properties is treated
independently of its actual runtime class.

Nominal subtyping: based on inheritance.

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
        raise NotImplementedError
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
