-- SEQUENCES
CREATE SEQUENCE producer_seq START 1;
CREATE SEQUENCE pojazd_seq START 1;
CREATE SEQUENCE przystanek_seq START 1;
CREATE SEQUENCE kasa_seq START 1;
CREATE SEQUENCE bilet_seq START 1;
CREATE SEQUENCE biletomat_seq START 1;
CREATE SEQUENCE model_seq START 1;

-- FUNCTIONS
CREATE OR REPLACE FUNCTION UzupelnijCeny()
	RETURNS TRIGGER
	LANGUAGE PLPGSQL
	AS $$
BEGIN
	IF NEW.czy_ulgowy LIKE 'tak' THEN
         IF czas_przejazdu LIKE '15' THEN
             UPDATE bilety SET cena = 2;
         ELSIF czas_przejazdu LIKE '30' THEN
             UPDATE bilety SET cena = 3;
         ELSE
             UPDATE bilety SET cena = 4;
         END IF;
	ELSE
		IF czas_przejazdu LIKE '15' THEN
			 UPDATE bilety SET cena = 4;
		ELSIF czas_przejazdu LIKE '30' THEN
			UPDATE bilety SET cena = 6;
		ELSE
			UPDATE bilety SET cena = 8;
		END IF;
	END IF;
	IF strefa_typ_strefy LIKE 'B' THEN
		 UPDATE bilety SET cena = cena + 0.5;
	ELSIF strefa_typ_strefy LIKE 'C' THEN
		 UPDATE bilety SET cena = cena + 0.6;
	ELSIF strefa_typ_strefy LIKE 'AB' THEN
		 UPDATE bilety SET cena = cena + 0.7;
	ELSIF strefa_typ_strefy LIKE 'ABC' THEN
		 UPDATE bilety SET cena = cena + 1;
	END IF;
	RETURN NEW;
END; $$

CREATE OR REPLACE FUNCTION GestoscZaludnienia()
    RETURNS TRIGGER
	LANGUAGE PLPGSQL
	AS $$
BEGIN
	UPDATE miasta SET gestosc_zaludnienia = liczba_mieszkancow / powierzchnia;
	RETURN NEW;
END; $$

-- TRIGGERS
CREATE TRIGGER UzupelnijCene
    AFTER INSERT ON bilety
	EXECUTE PROCEDURE UzupelnijCeny();    

CREATE TRIGGER ObliczGestosc
	AFTER INSERT ON miasta
	EXECUTE PROCEDURE GestoscZaludnienia();