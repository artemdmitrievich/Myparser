
import requests
import pandas as pd
import time

class MovingAverageCrossover:
    def __init__(self, symbol, interval, short_period, long_period, sleep_interval):
        self.symbol = symbol
        self.interval = interval
        self.short_period = short_period
        self.long_period = long_period
        self.sleep_interval = sleep_interval
        self.base_url = 'https://api.bybit.com'

    def get_historical_data(self, limit=200):
        """Получает исторические данные для указанного символа."""
        endpoint = '/v5/public/kline/list'
        params = {
            'symbol': self.symbol,
            'interval': self.interval,
            'limit': limit
        }

        try:
            response = requests.get(self.base_url + endpoint, params=params)
            response.raise_for_status()
            return response.json()['result']
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:  # Код ошибки "Too Many Requests"
                print("Слишком много запросов. Ожидание перед повторной попыткой...")
                time.sleep(60)  # Увеличьте задержку, если необходимо
            else:
                print(f"Ошибка при получении исторических данных: {e}")
            return []

    def calculate_moving_averages(self, data):
        """Вычисляет скользящие средние на основе исторических данных."""
        df = pd.DataFrame(data)
        df['close'] = pd.to_numeric(df['close'])
        df['short_ma'] = df['close'].rolling(window=self.short_period).mean()
        df['long_ma'] = df['close'].rolling(window=self.long_period).mean()
        return df

    def check_crossovers(self, df):
        """Проверяет пересечения скользящих средних и возвращает сигналы покупки и продажи."""
        buy_signals = []
        sell_signals = []

        for i in range(1, len(df)):
            if df['short_ma'].iloc[i] > df['long_ma'].iloc[i] and df['short_ma'].iloc[i-1] <= df['long_ma'].iloc[i-1]:
                buy_signals.append(df['close'].iloc[i])
                sell_signals.append(None)
            elif df['short_ma'].iloc[i] < df['long_ma'].iloc[i] and df['short_ma'].iloc[i-1] >= df['long_ma'].iloc[i-1]:
                buy_signals.append(None)
                sell_signals.append(df['close'].iloc[i])
            else:
                buy_signals.append(None)
                sell_signals.append(None)

        df['buy_signal'] = buy_signals
        df['sell_signal'] = sell_signals
        return df

    def run(self):
        """Запускает цикл для постоянного получения данных о пересечении скользящих средних."""
        while True:
            historical_data = self.get_historical_data()
            if not historical_data:  # Проверяем, не пустые ли данные
                continue
            moving_average_df = self.calculate_moving_averages(historical_data)
            crossover_df = self.check_crossovers(moving_average_df)

            # Выводим последние сигналы
            print(crossover_df[['close', 'short_ma', 'long_ma', 'buy_signal', 'sell_signal']].dropna())

            time.sleep(self.sleep_interval)

# Пример использования класса
if __name__ == "__main__":
    ma_crossover = MovingAverageCrossover(symbol="BTCUSD", interval=1, short_period=10, long_period=30, sleep_interval=60)
    ma_crossover.run()


