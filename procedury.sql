-- SEQUENCES
CREATE SEQUENCE producer_seq START 1;
CREATE SEQUENCE pojazd_seq START 1;
CREATE SEQUENCE przystanek_seq START 1;
CREATE SEQUENCE kasa_seq START 1;
CREATE SEQUENCE bilet_seq START 1;
CREATE SEQUENCE biletomat_seq START 1;
CREATE SEQUENCE model_seq START 1;

CREATE OR REPLACE TRIGGER UzupelnijCene
    BEFORE INSERT ON bilety
    FOR EACH ROW
BEGIN
    IF :NEW.czy_ulgowy LIKE 't' THEN
        IF :NEW.czas_przejazdu LIKE '15' THEN
            UPDATE bilety SET cena = 2;
        ELSIF :NEW.czas_przejazdu LIKE '30' THEN
            UPDATE bilety SET cena = 3;
        ELSE
            UPDATE bilety SET cena = 4;
        END IF;
    ELSE
       IF :NEW.czas_przejazdu LIKE '15' THEN
            UPDATE bilety SET cena = 4;
        ELSIF :NEW.czas_przejazdu LIKE '30' THEN
            UPDATE bilety SET cena = 6;
        ELSE
            UPDATE bilety SET cena = 8;
        END IF;
    END IF;
END;


CREATE OR REPLACE FUNCTION GestoscZaludnienia
    (pNazwa IN miasta.nazwa_miasta%TYPE)
    RETURN FLOAT IS
    vGestosc FLOAT;
    vLiczbaMieszkancow INTEGER;
    vPowierzchnia FLOAT;
BEGIN
    SELECT liczba_mieszkancow, powierzchnia
    INTO (vLiczbaMieszkancow, vPowierzchnia)
    FROM miasta
    WHERE nazwa_miasta = pNazwa;
    vGestosc = vLiczbaMieszkancow / vPowierzchnia;
    RETURN vGestosc;
END GestoscZaludnienia;