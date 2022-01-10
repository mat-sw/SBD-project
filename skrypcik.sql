DROP TABLE biletomaty CASCADE;
DROP TABLE bilety CASCADE;
-- DROP TABLE do_zakupienia CASCADE;
DROP TABLE kasy_biletowe CASCADE;
DROP TABLE kierowcy CASCADE;
DROP TABLE kierowcy_i_pojazdy CASCADE;
DROP TABLE linie CASCADE;
DROP TABLE miasta CASCADE;
DROP TABLE modele_pojazdow CASCADE;
DROP TABLE pojazdy CASCADE;
DROP TABLE producenci CASCADE;
DROP TABLE przyjazdy CASCADE;
DROP TABLE przystanki CASCADE;
DROP TABLE przystanki_w_linii CASCADE;
DROP TABLE strefy CASCADE;

DROP TYPE IF EXISTS t_n;
DROP TYPE IF EXISTS type_czas_przejazdu;
DROP TYPE IF EXISTS type_typ_strefy;
DROP TYPE IF EXISTS type_plec;
DROP TYPE IF EXISTS type_stan;
DROP TYPE IF EXISTS type_linia;
DROP TYPE IF EXISTS type_status;


CREATE TYPE t_n as ENUM('tak', 'nie');
CREATE TYPE type_czas_przejazdu as ENUM('15', '30', '60');
CREATE TYPE type_typ_strefy as ENUM ('A', 'B', 'C', 'AB', 'ABC');
CREATE TYPE type_plec as ENUM('kobieta', 'mezczyzna');
CREATE TYPE type_stan as ENUM('zonaty', 'zamezna', 'wdowiec', 'wdowa', 'panna', 'kawaler', 'rozwiedziony', 'rozwiedziona', 'w separacji');
CREATE TYPE type_linia as ENUM('autobusowa', 'tramwajowa');
CREATE TYPE type_status as ENUM('miasto', 'wies');

CREATE TABLE biletomaty (
    id_biletomatu     INTEGER NOT NULL,
    platnosc_gotowka  t_n NOT NULL,
    platnosc_karta    t_n NOT NULL
);

ALTER TABLE biletomaty ADD CONSTRAINT biletomat_pk PRIMARY KEY ( id_biletomatu );

CREATE TABLE bilety (
    id_biletu                     INTEGER NOT NULL,
    czy_ulgowy                    t_n NOT NULL,
    cena                          FLOAT NOT NULL,
    czas_przejazdu                type_czas_przejazdu NOT NULL,
    strefa_typ_strefy             type_typ_strefy NOT NULL
);

ALTER TABLE bilety ADD CONSTRAINT bilet_pk PRIMARY KEY ( id_biletu );

CREATE TABLE kasy_biletowe (
    id_kasy                         INTEGER NOT NULL,
    godzina_otwarcia                DATE NOT NULL,
    godzina_zamkniecia              DATE NOT NULL,
    przystanki_id_przystanku        INTEGER,
    przystanki_miasta_nazwa_miasta  VARCHAR(30),
    przystanki_strefy_typ_strefy    type_typ_strefy NOT NULL
);

ALTER TABLE kasy_biletowe ADD CONSTRAINT kasa_biletowa_pk PRIMARY KEY ( id_kasy );

CREATE TABLE kierowcy (
    pesel                   VARCHAR(11) NOT NULL,
    imie                    VARCHAR(20) NOT NULL,
    nazwisko                VARCHAR(30) NOT NULL,
    plec                    type_plec     NOT NULL,
    uprawnienia_autobusowe  t_n,
    uprawnienia_tramwajowe  t_n,
    placa                   FLOAT NOT NULL,
    data_zatrudnienia       DATE,
    stan_cywilny            type_stan
);

ALTER TABLE kierowcy ADD CONSTRAINT kierowca_pk PRIMARY KEY ( pesel );

CREATE TABLE kierowcy_i_pojazdy (
    pojazdy_id_pojazdu      INTEGER NOT NULL,
    pojazdy_linie_id_linii  INTEGER NOT NULL,
    pojazdy_id_modelu       INTEGER NOT NULL,
    pojazdy_id_producenta   INTEGER NOT NULL,
    kierowcy_pesel          VARCHAR(11) NOT NULL
);

ALTER TABLE kierowcy_i_pojazdy
    ADD CONSTRAINT relation_15_pk PRIMARY KEY ( pojazdy_id_pojazdu,
                                                pojazdy_linie_id_linii,
                                                pojazdy_id_modelu,
                                                pojazdy_id_producenta,
                                                kierowcy_pesel );

CREATE TABLE linie (
    id_linii   INTEGER NOT NULL,
    typ_linii  type_linia NOT NULL
);

ALTER TABLE linie ADD CONSTRAINT linia_pk PRIMARY KEY ( id_linii );

CREATE TABLE miasta (
    nazwa_miasta        VARCHAR(30) NOT NULL,
    status              type_status,
    liczba_mieszkancow  INTEGER,
    powierzchnia        FLOAT,
	gestosc_zaludnienia	FLOAT
);

ALTER TABLE miasta ADD CONSTRAINT miasto_pk PRIMARY KEY ( nazwa_miasta );

CREATE TABLE modele_pojazdow (
    id_modelu                 INTEGER NOT NULL,
    nazwa_modelu              VARCHAR(30) NOT NULL,
    typ_pojazdu               VARCHAR(10) NOT NULL,
    czy_niskopodlogowy        t_n,
    liczba_miejsc_siedzacych  INTEGER,
    liczba_miejsc_stojacych   INTEGER,
    producenci_id_producenta  INTEGER NOT NULL
);

ALTER TABLE modele_pojazdow ADD CONSTRAINT model_pojazdu_pk PRIMARY KEY ( id_modelu,
                                                                          producenci_id_producenta );

CREATE TABLE pojazdy (
    id_pojazdu                     INTEGER NOT NULL,
    max_liczba_osob                INTEGER,
    linie_id_linii                 INTEGER NOT NULL,
    biletomaty_id_biletomatu       INTEGER NOT NULL,
    rok_produkcji                  INTEGER,
    data_waznosci_przegladu        DATE NOT NULL,
    modele_poj_id_modelu           INTEGER NOT NULL,
    modele_poj_prod_id_producenta  INTEGER NOT NULL
);

CREATE UNIQUE INDEX pojazd__idx ON
    pojazdy (
        biletomaty_id_biletomatu
    ASC );

ALTER TABLE pojazdy
    ADD CONSTRAINT pojazd_pk PRIMARY KEY ( id_pojazdu,
                                           linie_id_linii,
                                           modele_poj_id_modelu,
                                           modele_poj_prod_id_producenta );

CREATE TABLE producenci (
    id_producenta     INTEGER NOT NULL,
    nazwa_producenta  VARCHAR(30) NOT NULL
);

ALTER TABLE producenci ADD CONSTRAINT producent_pk PRIMARY KEY ( id_producenta );

CREATE TABLE przyjazdy (
    pwl_kolejnosc                 INTEGER NOT NULL,
    pwl_linie_id_linii            INTEGER NOT NULL,
    pwl_przystanki_id_przystanku  INTEGER NOT NULL,
    pwl_przystanki_nazwa_miasta   VARCHAR(30) NOT NULL,
    id_przyjazdu                  INTEGER NOT NULL,
    data_przyjazdu                DATE NOT NULL,
    pwl_przyst_strefy_typ_strefy  type_typ_strefy NOT NULL
);

ALTER TABLE przyjazdy ADD CONSTRAINT przyjazd_pk PRIMARY KEY ( id_przyjazdu );

CREATE TABLE przystanki (
    id_przystanku             INTEGER NOT NULL,
    nazwa_przystanku          VARCHAR(30) NOT NULL,
    adres                     VARCHAR(30) NOT NULL,
    miasta_nazwa_miasta       VARCHAR(30) NOT NULL,
    czy_zajezdnia             t_n,
    biletomaty_id_biletomatu  INTEGER NOT NULL,
    strefy_typ_strefy         type_typ_strefy NOT NULL
);

CREATE UNIQUE INDEX przystanek__idx ON
    przystanki (
        biletomaty_id_biletomatu
    ASC );

ALTER TABLE przystanki
    ADD CONSTRAINT przystanek_pk PRIMARY KEY ( id_przystanku,
                                               miasta_nazwa_miasta,
                                               strefy_typ_strefy );

CREATE TABLE przystanki_w_linii (
    kolejnosc                       INTEGER NOT NULL,
    linie_id_linii                  INTEGER NOT NULL,
    przystanki_id_przystanku        INTEGER NOT NULL,
    przystanki_miasta_nazwa_miasta  VARCHAR(30) NOT NULL,
    przystanki_strefy_typ_strefy    type_typ_strefy NOT NULL
);

ALTER TABLE przystanki_w_linii
    ADD CONSTRAINT przystanek_w_linii_pk PRIMARY KEY ( kolejnosc,
                                                       linie_id_linii,
                                                       przystanki_id_przystanku,
                                                       przystanki_miasta_nazwa_miasta,
                                                       przystanki_strefy_typ_strefy );

CREATE TABLE strefy (
    typ_strefy type_typ_strefy NOT NULL
);

ALTER TABLE strefy ADD CONSTRAINT strefa_pk PRIMARY KEY ( typ_strefy );

ALTER TABLE bilety
    ADD CONSTRAINT bilet_strefa_fk FOREIGN KEY ( strefa_typ_strefy )
        REFERENCES strefy ( typ_strefy );

ALTER TABLE kasy_biletowe
    ADD CONSTRAINT kasa_biletowa_przystanek_fk FOREIGN KEY ( przystanki_id_przystanku,
                                                             przystanki_miasta_nazwa_miasta,
                                                             przystanki_strefy_typ_strefy )
        REFERENCES przystanki ( id_przystanku,
                                miasta_nazwa_miasta,
                                strefy_typ_strefy );

ALTER TABLE modele_pojazdow
    ADD CONSTRAINT model_pojazdu_producent_fk FOREIGN KEY ( producenci_id_producenta )
        REFERENCES producenci ( id_producenta );

ALTER TABLE pojazdy
    ADD CONSTRAINT pojazd_biletomat_fk FOREIGN KEY ( biletomaty_id_biletomatu )
        REFERENCES biletomaty ( id_biletomatu );

ALTER TABLE pojazdy
    ADD CONSTRAINT pojazd_linia_fk FOREIGN KEY ( linie_id_linii )
        REFERENCES linie ( id_linii );

ALTER TABLE pojazdy
    ADD CONSTRAINT pojazd_model_pojazdu_fk FOREIGN KEY ( modele_poj_id_modelu,
                                                         modele_poj_prod_id_producenta )
        REFERENCES modele_pojazdow ( id_modelu,
                                     producenci_id_producenta );

ALTER TABLE przyjazdy
    ADD CONSTRAINT przyjazd_przystanek_w_linii_fk FOREIGN KEY ( pwl_kolejnosc,
                                                                pwl_linie_id_linii,
                                                                pwl_przystanki_id_przystanku,
                                                                pwl_przystanki_nazwa_miasta,
                                                                pwl_przyst_strefy_typ_strefy )
        REFERENCES przystanki_w_linii ( kolejnosc,
                                        linie_id_linii,
                                        przystanki_id_przystanku,
                                        przystanki_miasta_nazwa_miasta,
                                        przystanki_strefy_typ_strefy );

ALTER TABLE przystanki
    ADD CONSTRAINT przystanek_biletomat_fk FOREIGN KEY ( biletomaty_id_biletomatu )
        REFERENCES biletomaty ( id_biletomatu );

ALTER TABLE przystanki
    ADD CONSTRAINT przystanek_miasto_fk FOREIGN KEY ( miasta_nazwa_miasta )
        REFERENCES miasta ( nazwa_miasta );

ALTER TABLE przystanki
    ADD CONSTRAINT przystanek_strefa_fk FOREIGN KEY ( strefy_typ_strefy )
        REFERENCES strefy ( typ_strefy );

ALTER TABLE przystanki_w_linii
    ADD CONSTRAINT przystanek_w_linii_linia_fk FOREIGN KEY ( linie_id_linii )
        REFERENCES linie ( id_linii );

ALTER TABLE przystanki_w_linii
    ADD CONSTRAINT pwl_przystanek_fk FOREIGN KEY ( przystanki_id_przystanku,
                                                                  przystanki_miasta_nazwa_miasta,
                                                                  przystanki_strefy_typ_strefy )
        REFERENCES przystanki ( id_przystanku,
                                miasta_nazwa_miasta,
                                strefy_typ_strefy );

ALTER TABLE kierowcy_i_pojazdy
    ADD CONSTRAINT relation_15_kierowca_fk FOREIGN KEY ( kierowcy_pesel )
        REFERENCES kierowcy ( pesel );

ALTER TABLE kierowcy_i_pojazdy
    ADD CONSTRAINT relation_15_pojazd_fk FOREIGN KEY ( pojazdy_id_pojazdu,
                                                       pojazdy_linie_id_linii,
                                                       pojazdy_id_modelu,
                                                       pojazdy_id_producenta )
        REFERENCES pojazdy ( id_pojazdu,
                             linie_id_linii,
                             modele_poj_id_modelu,
                             modele_poj_prod_id_producenta );

