Zadanie

Zaloguj się do systemu robotów pod adresem xyz.ag3nts.org. Zdobyliśmy login i hasło do systemu (tester / 574e112a). Problemem jednak jest ich system ‘anty-captcha’, który musisz spróbować obejść.Musisz jedynie zautomatyzować proces odpowiadania na pytnie zawarte w formularzu. Przy okazji zaloguj się proszę w naszej centrali (centrala.ag3nts.org). Tam też możesz zgłosić wszystkie znalezione do tej pory flagi. Nie analizuj jeszcze pamięci robota, którą przechwycisz. Zostawmy sobie to na jutro.

Co musisz zrobić w zadaniu?

Zbadaj formularz logowania do podanej wyżej strony (XYZ) i zauważ, że wysyłane są tam trzy zmienne metodą POST: username, password oraz answer. Zawartość dwóch pierwszych już znasz. Trzecia wymaga uzupełnienia

Napisz prostą aplikację, która pobiera aktualne pytanie wyświetlane na stronie (zmienia się ono co 7 sekund)

Wyślij to pytanie do wybranego LLM-a i pobierz odpowiedź

Wyślij trzy zmienne z pkt #1 do strony XYZ, uzupełniając pole answer odpowiedzią z LLM-a

Odczytaj odpowiedź serwera. Będzie tam podany adres URL do tajnej podstrony. Przejdź tam.