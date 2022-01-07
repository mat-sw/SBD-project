-- PRODUCENCI
INSERT INTO PRODUCENT
VALUES (1, 'Solaris');

INSERT INTO PRODUCENT
VALUES (2, 'Moderus');

-- MIASTA
INSERT INTO MIASTO
VALUES('Poznań', 'miasto', 540365, 261.8);


INSERT INTO MIASTO
VALUES('Rokietnica', 'wieś', 7523, 6.8);


INSERT INTO MIASTO
VALUES('Swarzędz', 'wieś', 30739, 9);

-- STREFY
INSERT INTO STREFA
VALUES('A');

INSERT INTO STREFA
VALUES('ABC');

INSERT INTO STREFA
VALUES('B');

INSERT INTO STREFA
VALUES('C');

--KIEROWCY
INSERT INTO kierowca VALUES('82032509225', 'Damian', 'Paczkowski', 'm', 't', 'n', 3415, to_date('2022-01-01', 'YYYY-MM-DD'), 'zonaty');
INSERT INTO kierowca VALUES('82051517654', 'Daniel', 'Jankowski', 'm', 'n', 't', 3556, to_date('2022-01-01', 'YYYY-MM-DD'), 'kawaler');
INSERT INTO kierowca VALUES('76111853890', 'Anna', 'Maćkowiak', 'k', 't', 'n', 3367, to_date('2022-01-01', 'YYYY-MM-DD'), 'panna');
INSERT INTO kierowca VALUES('89041709876', 'Krystyna', 'Warda', 'k', 'n', 't', 3405, to_date('2022-01-01', 'YYYY-MM-DD'), 'mezatka');

--BILETOMATY
insert into biletomat VALUES(nextval('biletomat_seq'), 't', 't');
insert into biletomat VALUES(nextval('biletomat_seq'), 'n', 't');
insert into biletomat VALUES(nextval('biletomat_seq'), 't', 'n');
insert into biletomat VALUES(nextval('biletomat_seq'), 't', 't');