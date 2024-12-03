import time
import winsound  # Для воспроизведения звуков на Windows
import threading

# Настройки метронома
BPM = 120  # Установите нужные значения BPM
beat_duration = 60 / BPM

# Коннакол-фразы
konnakol_phrases = [
    "ta ka di mi",
    "ta ti ta",
    "ta na na",
    "ta ka ta ka",
    "dheem thaka",
]

# Функция для воспроизведения метронома
def play_metronome():
    while True:
        winsound.Beep(1000, 100)  # Звуковой сигнал (1000 Гц, 100 мс)
        time.sleep(beat_duration)

# Начать метроном в отдельном потоке
metronome_thread = threading.Thread(target=play_metronome)
metronome_thread.daemon = True
metronome_thread.start()

# Основной цикл программы
print("Ритм: {} BPM".format(BPM))
print("Программа коннакол:")
print("Используйте следующие фразы:")
for i, phrase in enumerate(konnakol_phrases, start=1):
    print(f"{i}: {phrase}")

try:
    while True:
        choice = input("Выберите фразу (1-5) или нажмите 'q' для выхода: ")
        if choice.lower() == 'q':
            break
        if choice.isdigit() and 1 <= int(choice) <= len(konnakol_phrases):
            print(f"Ваша фраза: {konnakol_phrases[int(choice) - 1]}")
            print("Повторяйте фразу в ритме метронома.")
        else:
            print("Неверный ввод. Попробуйте снова.")
except KeyboardInterrupt:
    print("Выход из программы.")
