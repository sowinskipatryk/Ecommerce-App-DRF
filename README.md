# Aplikacja E-commerce

Aplikacja służąca do autoryzacji użytkownika przy pomocy tokenu oraz przetwarzania wysyłanych z front-endu żądań i wysyłania adekwatnych odpowiedzi.
W repozytorium znajduje się baza danych, którą można wykorzystać do natychmiastowego korzystania z aplikacji (użytkownicy client i seller już są dodani i kilka przykładowych produktów).
W innym przypadku należy skorzystać z metody POST endpointa /api/users/signup podając nazwę użytkownika, hasło i email (username, password, email) oraz rolę (client/seller), aby otrzymać token.
Dodawanie produtków jest udostępnione dla roli seller, a dodawanie zamówień dla roli client. Ten należy każdorazowo umieszczać w polu Headers zapytania, aby dotrzeć do interesującej nas treści. W pliku test.rest zawarte są przykładowe testy endpointów. Dodawanie produktów z obrazkiem było testowane przy pomocy Postmana.
