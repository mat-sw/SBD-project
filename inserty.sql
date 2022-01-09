-- PRODUCENCI
INSERT INTO PRODUCENCI VALUES (1, 'Solaris');
INSERT INTO PRODUCENCI VALUES (2, 'Moderus');

-- MIASTA
INSERT INTO MIASTA (nazwa_miasta, status, liczba_mieszkancow, powierzchnia) 
VALUES('Poznań', 'miasto', 540365, 261.8);

INSERT INTO MIASTA (nazwa_miasta, status, liczba_mieszkancow, powierzchnia) 
VALUES('Rokietnica', 'wieś', 7523, 6.8);

INSERT INTO MIASTA (nazwa_miasta, status, liczba_mieszkancow, powierzchnia) 
VALUES('Swarzędz', 'miasto', 30739, 9);

INSERT INTO MIASTA (nazwa_miasta, status, liczba_mieszkancow, powierzchnia) 
VALUES('Przeźmierowo', 'wieś', 6455, 3.61);

-- STREFY
INSERT INTO STREFA VALUES('A');
INSERT INTO STREFY VALUES('B');
INSERT INTO STREFY VALUES('C');
INSERT INTO STREFY VALUES('AB');
INSERT INTO STREFY VALUES('ABC');

--KIEROWCY
INSERT INTO kierowcy VALUES('82032509225', 'Damian', 'Paczkowski', 'mezczyzna', 'tak', 'nie', 3415, to_date('2022-01-01', 'YYYY-MM-DD'), 'zonaty');
INSERT INTO kierowcy VALUES('82051517654', 'Daniel', 'Jankowski', 'mezczyzna', 'nie', 'tak', 3556, to_date('2022-01-01', 'YYYY-MM-DD'), 'kawaler');
INSERT INTO kierowcy VALUES('76111853890', 'Anna', 'Maćkowiak', 'kobieta', 'tak', 'nie', 3367, to_date('2022-01-01', 'YYYY-MM-DD'), 'panna');
INSERT INTO kierowcy VALUES('89041709876', 'Krystyna', 'Warda', 'kobieta', 'nie', 'tak', 3405, to_date('2022-01-01', 'YYYY-MM-DD'), 'mezatka');

--BILETOMATY
insert into biletomaty VALUES(nextval('biletomat_seq'), 'tak', 'tak');
insert into biletomaty VALUES(nextval('biletomat_seq'), 'nie', 'tak');
insert into biletomaty VALUES(nextval('biletomat_seq'), 'tak', 'nie');
insert into biletomaty VALUES(nextval('biletomat_seq'), 'tak', 'tak');

--LINIE
INSERT INTO linie VALUES(1, 'tramwajowa');
INSERT INTO linie VALUES(2, 'tramwajowa');
INSERT INTO linie VALUES(5, 'tramwajowa');
INSERT INTO linie VALUES(168, 'autobusowa');