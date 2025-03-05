Musisz poprawić plik kalibracyjny dla jednego z robotów przemysłowych. To dość popularny w 2024 roku format JSON. Dane testowe zawierają prawdopodobnie błędne obliczenia oraz luki w pytaniach otwartych. Popraw proszę ten plik i prześlij nam go już po poprawkach. Tylko uważaj na rozmiar kontekstu modeli LLM, z którymi pracujesz — plik się nie zmieści w tym limicie.

Plik do pobrania zabezpieczony jest Twoim kluczem API. Podmień “TWOJ-KLUCZ” w adresie na wartość klucza z centrali.

https://centrala.ag3nts.org/data/TWOJ-KLUCZ/json.txt

Poprawną odpowiedź wyślij proszę pod poniższy adres, w formie takiej, jak w przypadku Poligonu. Nazwa zadanie to JSON.

https://centrala.ag3nts.org/report 

Co trzeba zrobić w zadaniu?

Pobierasz plik TXT podany wyżej (tylko podmień TWOJ-KLUCZ) na poprawną wartość

Ten plik się nie zmienia. Nie musisz go pobierać cyklicznie. Jest statyczny

Plik zawiera błędy w obliczeniach - musisz je poprawić (ale gdzie one są?)

Plik w niektórych danych testowych zawiera pole “test” z polami “q” (question/pytanie) oraz “a” (answer/odpowiedź). To LLM powinien udzielić odpowiedzi.

Rozmiar dokumentu jest zbyt duży, aby ogarnąć go współczesnymi LLM-ami (zmieści się w niektórych oknach kontekstowych wejścia, ale już nie w oknie wyjścia).

Zadanie na pewno trzeba rozbić na mniejsze części, a wywołanie LLM-a prawdopodobnie będzie wielokrotne (ale da się to także zrobić jednym requestem)

W tym zadaniu trzeba mądrze zdecydować, którą część zadania należy delegować do sztucznej inteligencji, a którą warto rozwiązać w klasyczny, programistyczny sposób. Decyzja oczywiście należy do Ciebie, ale zrób to proszę rozsądnie.