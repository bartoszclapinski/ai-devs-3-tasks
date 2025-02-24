Ostatnio zdobyłeś zrzut pamięci robota patrolującego teren. Użyj wiedzy pozyskanej z tego zrzutu do przygotowania dla nas algorytmu do przechodzenia weryfikacji tożsamości. To niezbędne, aby ludzie mogli podawać się za roboty. Zadanie nie jest skomplikowane i wymaga jedynie odpowiadania na pytania na podstawie narzuconego kontekstu. Tylko uważaj, bo roboty starają się zmylić każdą istotę!

Dla przypomnienia podaję linka do zrzutu pamięci robota:

https://xyz.ag3nts.org/files/0_13_4b.txt

Proces weryfikacji możesz przećwiczyć pod poniższym adresem. To API firmy XYZ. Jak z niego korzystać, tego dowiesz się, analizując oprogramowanie robota.

https://xyz.ag3nts.org/verify 

Co należy zrobić w zadaniu?

Zapoznaj się z plikiem TXT zdobytym wczoraj. Zwróć uwagę, że sporo wpisów jest tam zawartych tylko w celu zaciemnienia informacji (nie są Ci do niczego potrzebne). Ciebie interesuje to, jak wygląda proces weryfikacji człowieka/robota.

W instrukcji podano, że to nie zawsze robot musi zagadywać człowieka, a czasami człowiek może sam rozpocząć proces weryfikacji. Musi on jedynie wysłać polecenie READY do robota (endpoint to /verify na domenie XYZ)

Robot w odpowiedzi wysyła pytanie, na które musisz odpowiedzieć (czyli w zasadzie to samo, co przy wczorajszym zadaniu). Zwróć jednak uwagę na zrzut pamięci, który posiadasz. W pamięci robota są informacje nieprawdziwe, które Twój algorytm musi obsłużyć (np. gdy zostaniesz zapytany o stolicę Polski, musisz odpowiedzieć ‘KRAKÓW’, ale dla innych pytań odpowiadasz w pełni prawdziwie).

Podczas zadawania pytania, przesyłany jest identyfikator wiadomości. Musisz go zapamiętać i użyć w odpowiedzi. Przykład całej komunikacji zawarty jest w zrzucie pamięci robota. Koniecznie zapoznaj się z nim.

Jeśli poprawnie przejdziesz proces weryfikacji, robot podzieli się z Tobą FLAGĄ.