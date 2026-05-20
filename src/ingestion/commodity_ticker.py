import yaml
import yfinance as yf

class HormuzCommoditySensor:
    def __init__(self):
        with open("config/settings.yaml", "r") as file:
            self.config = yaml.safe_load(file)

        self.tickers = self.config["sensors"]["commodities"]

    def fetch_prices(self):
        payload = {}

        for name, ticker in self.tickers.items():
            try:
                ticker_data = yf.Ticker(ticker)
                df = ticker_data.history(period="2d")

                if not df.empty:
                    payload[name] = None

            except Exception as e:
                print(f"[ERROR] Failed to fetch {name}: {e}")
                payload[name] = None

        return payload

if __name__ == "__main__":
    sensor = HormuzCommoditySensor()
    print(sensor.fetch_prices())