-- PRODUCENCI
INSERT INTO PRODUCENCI VALUES (1, 'Solaris');
INSERT INTO PRODUCENCI VALUES (2, 'Moderus');
INSERT INTO PRODUCENCI VALUES (3, 'Rokbus');
INSERT INTO PRODUCENCI VALUES (4, 'Siemens');
INSERT INTO PRODUCENCI VALUES (5, 'Chorzowska Wytwórnia');

-- MODELE 
INSERT INTO MODELE VALUES(1, 'Gamma', 'tramwaj', 'tak', 75, 280, 2);
INSERT INTO MODELE VALUES(2, 'Szybki', 'autobus', 'tak', 40, 73, 3);
INSERT INTO MODELE VALUES(3, 'Wieśbus', 'autobus', 'nie', 33, 82, 3);
INSERT INTO MODELE VALUES(4, 'Beta', 'tramwaj', 'tak', 38, 157, 2);
INSERT INTO MODELE VALUES(5, 'Combino', 'tramwaj', 'tak', 53, 160, 4);
INSERT INTO MODELE VALUES(6, 'Tramino', 'tramwaj', 'tak', 78, 276, 1);

-- MIASTA
INSERT INTO MIASTA (nazwa_miasta, status, liczba_mieszkancow, powierzchnia) 
VALUES('Poznań', 'miasto', 540365, 261.8);

INSERT INTO MIASTA (nazwa_miasta, status, liczba_mieszkancow, powierzchnia) 
VALUES('Rokietnica', 'wies', 7523, 6.8);

INSERT INTO MIASTA (nazwa_miasta, status, liczba_mieszkancow, powierzchnia) 
VALUES('Swarzędz', 'miasto', 30739, 9);

INSERT INTO MIASTA (nazwa_miasta, status, liczba_mieszkancow, powierzchnia) 
VALUES('Przeźmierowo', 'wies', 6455, 3.61);

-- STREFY
INSERT INTO STREFY VALUES('A');
INSERT INTO STREFY VALUES('B');
INSERT INTO STREFY VALUES('C');
INSERT INTO STREFY VALUES('AB');
INSERT INTO STREFY VALUES('ABC');

--KIEROWCY
INSERT INTO kierowcy VALUES('82032509225', 'Damian', 'Paczkowski', 'mezczyzna', 'tak', 'nie', 3415, to_date('2022-01-01', 'YYYY-MM-DD'), 'zonaty');
INSERT INTO kierowcy VALUES('82051517654', 'Daniel', 'Jankowski', 'mezczyzna', 'nie', 'tak', 3556, to_date('2022-01-01', 'YYYY-MM-DD'), 'kawaler');
INSERT INTO kierowcy VALUES('76111853890', 'Anna', 'Maćkowiak', 'kobieta', 'tak', 'nie', 3367, to_date('2022-01-01', 'YYYY-MM-DD'), 'panna');
INSERT INTO kierowcy VALUES('89041709876', 'Krystyna', 'Warda', 'kobieta', 'nie', 'tak', 3405, to_date('2022-01-01', 'YYYY-MM-DD'), 'zamezna');

--LINIE
INSERT INTO linie VALUES(1, 'tramwajowa');
INSERT INTO linie VALUES(2, 'tramwajowa');
INSERT INTO linie VALUES(5, 'tramwajowa');
INSERT INTO linie VALUES(168, 'autobusowa');

-- POJAZDY
INSERT INTO POJAZDY VALUES(1, sum_sits(6), 1, null, 2014, to_date('2023-01-15', 'YYYY-MM-DD'), 6, 1);
INSERT INTO POJAZDY VALUES(2, sum_sits(6), 5, null, 2018, to_date('2023-01-15', 'YYYY-MM-DD'), 6, 1);
INSERT INTO POJAZDY VALUES(3, sum_sits(1), 5, null, 2020, to_date('2024-01-15', 'YYYY-MM-DD'), 1, 2);
INSERT INTO POJAZDY VALUES(4, sum_sits(3), 832, null, 2010, to_date('2023-01-15', 'YYYY-MM-DD'), 3, 3);

--BILETOMATY
insert into biletomaty VALUES(nextval('biletomat_seq'), 'tak', 'tak');
insert into biletomaty VALUES(nextval('biletomat_seq'), 'nie', 'tak');
insert into biletomaty VALUES(nextval('biletomat_seq'), 'tak', 'nie');
insert into biletomaty VALUES(nextval('biletomat_seq'), 'tak', 'tak');

-- KIEROWCY-POJAZDY
INSERT INTO kierowcy_i_pojazdy VALUES(1, 1, 6, 1, '82032509225');
INSERT INTO kierowcy_i_pojazdy VALUES(2, 5, 6, 1, '76111853890');
INSERT INTO kierowcy_i_pojazdy VALUES(3, 5, 1, 2, '82051517654');
INSERT INTO kierowcy_i_pojazdy VALUES(4, 832, 3, 3, '89041709876');
INSERT INTO kierowcy_i_pojazdy VALUES(1, 1, 6, 1, '82032509225');

-- PRZYSTANKI
INSERT INTO przystanki VALUES(NEXTVAL('przystanek_seq'), 'Szymanowskiego', 'Szymanowskiego/Szeligowskiego', 'Poznań', 'nie', 15, 'A');
INSERT INTO przystanki VALUES(NEXTVAL('przystanek_seq'), 'Kurpińskiego', 'Kurpińskiego/Mieszka I', 'Poznań', 'nie', 17, 'A');
INSERT INTO przystanki VALUES(NEXTVAL('przystanek_seq'), 'Poznań Plaza', 'Lechicka/Mieszka I', 'Poznań', 'nie', 18, 'A');
INSERT INTO przystanki VALUES(NEXTVAL('przystanek_seq'), 'Aleje Solidarności', 'Aleje Solidarności', 'Poznań', 'nie', 19, 'A');
INSERT INTO przystanki VALUES(NEXTVAL('przystanek_seq'), 'Słowiańska', 'Słowiańska/mieszka I', 'Poznań', 'nie', 20, 'A');
INSERT INTO przystanki VALUES(NEXTVAL('przystanek_seq'), 'Most Teatralny', 'Roosevelta/Dąbrowskiego', 'Poznań', 'nie', 21, 'A');

-- KASY
INSERT INTO kasy_biletowe VALUES(NEXTVAL('kasa_seq'), TO_TIMESTAMP('00:00:00', 'HH:MI:SS'), TO_TIMESTAMP('15:00:00', 'HH:MI:SS'), 3, 'Poznań', 'A');
INSERT INTO kasy_biletowe VALUES(NEXTVAL('kasa_seq'), TO_TIMESTAMP('08:00:00', 'HH:MI:SS'), TO_TIMESTAMP('15:20:00', 'HH:MI:SS'), 4, 'Poznań', 'A');