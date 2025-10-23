import os
import vlc
import time

# Nazwa pliku, w którym będą przechowywane dane stacji
NAZWA_PLIKU_Z_DANYMI = "radio_lista.txt"

def wczytaj_stacje():
    """Wczytuje listę stacji z pliku."""
    stacje = []
    if os.path.exists(NAZWA_PLIKU_Z_DANYMI):
        with open(NAZWA_PLIKU_Z_DANYMI, 'r', encoding='utf-8') as f:
            for linia in f:
                linia = linia.strip()
                if linia and ';' in linia:
                    try:
                        nazwa, url = linia.split(';', 1)
                        stacje.append({'nazwa': nazwa, 'url': url})
                    except ValueError:
                        print(f"Błąd parsowania linii: {linia}")
    return stacje

def zapisz_stacje(stacje):
    """Zapisuje listę stacji do pliku."""
    with open(NAZWA_PLIKU_Z_DANYMI, 'w', encoding='utf-8') as f:
        for stacja in stacje:
            f.write(f"{stacja['nazwa']};{stacja['url']}\n")

def dodaj_stacje(stacje):
    """Dodaje nową stację do listy."""
    print("\n--- Dodawanie Nowej Stacji ---")
    nazwa = input("Podaj nazwę stacji: ").strip()
    url = input("Podaj adres URL strumienia stacji: ").strip()

    if not nazwa or not url:
        print("Nazwa i URL nie mogą być puste. Próba dodania anulowana.")
        return

    # Sprawdzenie, czy stacja o tej nazwie już istnieje
    for stacja in stacje:
        if stacja['nazwa'].lower() == nazwa.lower():
            print(f"Stacja o nazwie '{nazwa}' już istnieje.")
            return

    stacje.append({'nazwa': nazwa, 'url': url})
    zapisz_stacje(stacje)
    print(f"Stacja '{nazwa}' została dodana.")

def wyswietl_stacje(stacje):
    """Wyświetla listę wszystkich stacji."""
    if not stacje:
        print("\nLista stacji jest pusta.")
        return

    print("\n--- Twoje Ulubione Stacje Radiowe ---")
    for i, stacja in enumerate(stacje):
        print(f"{i + 1}. {stacja['nazwa']} ({stacja['url']})")
    print("------------------------------------")

def usun_stacje(stacje):
    """Usuwa stację z listy na podstawie numeru."""
    wyswietl_stacje(stacje)
    if not stacje:
        return

    try:
        numer = int(input("Podaj numer stacji do usunięcia (lub 0, aby anulować): "))
        if numer == 0:
            print("Anulowano usuwanie.")
            return
        if 1 <= numer <= len(stacje):
            usuniete = stacje.pop(numer - 1)
            zapisz_stacje(stacje)
            print(f"Stacja '{usuniete['nazwa']}' została usunięta.")
        else:
            print("Nieprawidłowy numer stacji.")
    except ValueError:
        print("Nieprawidłowe dane. Podaj numer.")

def uruchom_stacje(stacje):
    """Próbuje uruchomić wybraną stację w zewnętrznym odtwarzaczu."""
    wyswietl_stacje(stacje)
    if not stacje:
        return

    try:
        numer = int(input("Podaj numer stacji do uruchomienia (lub 0, aby anulować): "))
        if numer == 0:
            print("Anulowano uruchamianie.")
            return
        if 1 <= numer <= len(stacje):
            wybrana_stacja = stacje[numer - 1]
            url = wybrana_stacja['url']
            nazwa = wybrana_stacja['nazwa']

            # W zależności od systemu operacyjnego, możesz użyć różnych komend
            # Poniższe są przykładami. Może być potrzebna konfiguracja lub instalacja
            # np. programu VLC media player, który potrafi otwierać strumienie URL.

            # Przykłady komend (mogą wymagać dostosowania):
            if os.name == 'nt':  # Windows
                # os.startfile(url) # Czasem działa, ale nie zawsze z URL
                print(f"Na Windows, możesz spróbować wpisać w konsoli: start \"{url}\"")
                print("Lub otworzyć VLC i wkleić URL.")
            elif os.name == 'posix': # Linux/macOS
               player = vlc.MediaPlayer(url)
               player.play()
               time.sleep(10)
            else:
                print("Nieznany system operacyjny. Nie mogę automatycznie uruchomić strumienia.")

            print("Jeśli powyższe nie zadziała, skopiuj ręcznie URL i wklej do swojego ulubionego odtwarzacza.")

        else:
            print("Nieprawidłowy numer stacji.")
    except ValueError:
        print("Nieprawidłowe dane. Podaj numer.")


def main():
    """Główna funkcja programu."""
    stacje = wczytaj_stacje()

    while True:
        print("\n===== Zarządzanie Stacjami Radiowymi =====")
        print("1. Wyświetl listę stacji")
        print("2. Dodaj nową stację")
        print("3. Usuń stację")
        print("4. Uruchom stację (wymaga zewnętrznego odtwarzacza)")
        print("5. Zakończ program")
        print("==========================================")

        wybor = input("Wybierz opcję (1-5): ").strip()

        if wybor == '1':
            wyswietl_stacje(stacje)
        elif wybor == '2':
            dodaj_stacje(stacje)
        elif wybor == '3':
            usun_stacje(stacje)
        elif wybor == '4':
            uruchom_stacje(stacje)
        elif wybor == '5':
            print("Dziękujemy za skorzystanie z programu. Zapisywanie zmian...")
            zapisz_stacje(stacje) # Upewnij się, że wszystko jest zapisane
            print("Do widzenia!")
            break
        else:
            print("Nieprawidłowa opcja. Spróbuj ponownie.")

if __name__ == "__main__":
    main()
