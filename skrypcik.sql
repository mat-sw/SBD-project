CREATE TABLE bilet (
    id_typu_biletu                         INTEGER NOT NULL,
    czy_ulgowy                             CHAR(1) NOT NULL,
    cena                                   FLOAT NOT NULL,
    czas_przejazdu                         INTEGER NOT NULL, 
    dz_kb_id_kasy    INTEGER NOT NULL, 
    dz_biletomat_id_biletomatu  INTEGER NOT NULL,
    do_zakupienia_id_biletu                INTEGER NOT NULL, 
    czasy_p_czas_przejazdu        INTEGER NOT NULL
);

CREATE UNIQUE INDEX bilet__idx ON
    bilet (
        dz_kb_id_kasy
    ASC,
        dz_biletomat_id_biletomatu
    ASC,
        do_zakupienia_id_biletu
    ASC );

ALTER TABLE bilet ADD CONSTRAINT bilet_pk PRIMARY KEY ( id_typu_biletu,
                                                        czasy_p_czas_przejazdu );

CREATE TABLE biletomat (
    id_biletomatu     INTEGER NOT NULL,
    platnosc_gotowka  CHAR(1) NOT NULL,
    platnosc_karta    CHAR(1) NOT NULL
);

ALTER TABLE biletomat ADD CONSTRAINT biletomat_pk PRIMARY KEY ( id_biletomatu );

CREATE TABLE czasy_przejazdow (
    czas_przejazdu INTEGER NOT NULL
);

ALTER TABLE czasy_przejazdow ADD CONSTRAINT czasy_przejazdow_pk PRIMARY KEY ( czas_przejazdu );

CREATE TABLE do_zakupienia (
    bilet_id_typu_biletu     INTEGER NOT NULL,
    biletomat_id_biletomatu  INTEGER NOT NULL,
    kasa_biletowa_id_kasy    INTEGER NOT NULL,
    id_biletu                INTEGER NOT NULL,
    data_zakupu              DATE,
    czas_przejazdu           INTEGER NOT NULL
);

CREATE UNIQUE INDEX do_zakupienia__idx ON
    do_zakupienia (
        bilet_id_typu_biletu
    ASC );

CREATE UNIQUE INDEX do_zakupienia__idx2 ON
    do_zakupienia (
        bilet_id_typu_biletu
    ASC,
        czas_przejazdu
    ASC );

ALTER TABLE do_zakupienia
    ADD CONSTRAINT do_zakupienia_pk PRIMARY KEY ( kasa_biletowa_id_kasy,
                                                  biletomat_id_biletomatu,
                                                  id_biletu );

CREATE TABLE kasa_biletowa (
    id_kasy                         INTEGER NOT NULL,
    godzina_otwarcia                DATE NOT NULL,
    godzina_zamknięcia              DATE NOT NULL,
    przystanek_id_przystanku        INTEGER,
    przystanek_miasto_nazwa_miasta  VARCHAR(30),
    przystanek_strefa_typ_strefy    VARCHAR(3) 
);

ALTER TABLE kasa_biletowa ADD CONSTRAINT kasa_biletowa_pk PRIMARY KEY ( id_kasy );

CREATE TABLE kierowca (
    pesel                   VARCHAR(11) NOT NULL,
    imie                    VARCHAR(20) NOT NULL,
    nazwisko                VARCHAR(30) NOT NULL,
    plec                    CHAR(1) NOT NULL,
    uprawnienia_autobusowe  CHAR(1),
    uprawnienia_tramwajowe  CHAR(1),
    placa                   FLOAT NOT NULL,
    data_zatrudnienia       DATE,
    stan_cywilny            VARCHAR(20) 
);

ALTER TABLE kierowca ADD CONSTRAINT kierowca_pk PRIMARY KEY ( pesel );

CREATE TABLE linia (
    id_linii   INTEGER NOT NULL,
    typ_linii  VARCHAR(20) NOT NULL
);

ALTER TABLE linia ADD CONSTRAINT linia_pk PRIMARY KEY ( id_linii );

CREATE TABLE miasto (
    nazwa_miasta        VARCHAR(30) NOT NULL,
    status              VARCHAR(10),
    liczba_mieszkancow  INTEGER,
    powierzchnia        FLOAT
);

ALTER TABLE miasto ADD CONSTRAINT miasto_pk PRIMARY KEY ( nazwa_miasta );

CREATE TABLE model_pojazdu (
    id_modelu                 INTEGER NOT NULL,
    nazwa_modelu              VARCHAR(30) NOT NULL,
    typ_pojazdu               VARCHAR(10) NOT NULL,
    czy_niskopodlogowy        CHAR(1),
    liczba_miejsc_siedzących  INTEGER,
    liczba_miejsc_stojacych   INTEGER,
    producent_id_producenta   INTEGER NOT NULL
);

ALTER TABLE model_pojazdu ADD CONSTRAINT model_pojazdu_pk PRIMARY KEY ( id_modelu,
                                                                        producent_id_producenta );

CREATE TABLE pojazd (
    id_pojazdu                             INTEGER NOT NULL,
    max_liczba_osob                        INTEGER,
    linia_id_linii                         INTEGER NOT NULL,
    biletomat_id_biletomatu                INTEGER NOT NULL,
    rok_produkcji                          INTEGER,
    data_waznosci_przeglądu                DATE NOT NULL,
    model_poj_id_modelu                INTEGER NOT NULL, 
    model_poj_prod_id_producenta  INTEGER NOT NULL
);

CREATE UNIQUE INDEX pojazd__idx ON
    pojazd (
        biletomat_id_biletomatu
    ASC );

ALTER TABLE pojazd
    ADD CONSTRAINT pojazd_pk PRIMARY KEY ( id_pojazdu,
                                           linia_id_linii,
                                           model_poj_id_modelu,
                                           model_poj_prod_id_producenta );

CREATE TABLE producent (
    id_producenta     INTEGER NOT NULL,
    nazwa_producenta  VARCHAR(30) NOT NULL
);

ALTER TABLE producent ADD CONSTRAINT producent_pk PRIMARY KEY ( id_producenta );

CREATE TABLE przyjazd (
    pwl_kolejnosc                     INTEGER NOT NULL, 
    pwl_linia_id_linii                INTEGER NOT NULL, 
    pwl_przystanek_id_przystanku      INTEGER NOT NULL, 
    pwl_przystanek_nazwa_miasta       VARCHAR(30) NOT NULL,
    id_przyjazdu                                     INTEGER NOT NULL,
    data_przyjazdu                                   DATE NOT NULL, 
    pwl_przyst_strefa_typ_strefy  VARCHAR(30) NOT NULL
);

ALTER TABLE przyjazd ADD CONSTRAINT przyjazd_pk PRIMARY KEY ( id_przyjazdu );

CREATE TABLE przystanek (
    id_przystanku            INTEGER NOT NULL,
    nazwa_przystanku         VARCHAR(30) NOT NULL,
    adres                    VARCHAR(30) NOT NULL,
    miasto_nazwa_miasta      VARCHAR(30) NOT NULL,
    czy_zajezdnia            CHAR(1),
    biletomat_id_biletomatu  INTEGER NOT NULL,
    strefa_typ_strefy        VARCHAR(3)
     NOT NULL
);

CREATE UNIQUE INDEX przystanek__idx ON
    przystanek (
        biletomat_id_biletomatu
    ASC );

ALTER TABLE przystanek
    ADD CONSTRAINT przystanek_pk PRIMARY KEY ( id_przystanku,
                                               miasto_nazwa_miasta,
                                               strefa_typ_strefy );

CREATE TABLE przystanek_w_linii (
    kolejnosc                       INTEGER NOT NULL,
    linia_id_linii                  INTEGER NOT NULL,
    przystanek_id_przystanku        INTEGER NOT NULL,
    przystanek_miasto_nazwa_miasta  VARCHAR(30) NOT NULL,
    przystanek_strefa_typ_strefy    VARCHAR(5) NOT NULL
);

ALTER TABLE przystanek_w_linii
    ADD CONSTRAINT przystanek_w_linii_pk PRIMARY KEY ( kolejnosc,
                                                       linia_id_linii,
                                                       przystanek_id_przystanku,
                                                       przystanek_miasto_nazwa_miasta,
                                                       przystanek_strefa_typ_strefy );

CREATE TABLE relation_15 (
    pojazd_id_pojazdu      INTEGER NOT NULL,
    pojazd_linia_id_linii  INTEGER NOT NULL,
    pojazd_id_modelu       INTEGER NOT NULL,
    pojazd_id_producenta   INTEGER NOT NULL,
    kierowca_pesel         VARCHAR(11) NOT NULL
);

ALTER TABLE relation_15
    ADD CONSTRAINT relation_15_pk PRIMARY KEY ( pojazd_id_pojazdu,
                                                pojazd_linia_id_linii,
                                                pojazd_id_modelu,
                                                pojazd_id_producenta,
                                                kierowca_pesel );

CREATE TABLE relation_20 (
    strefa_typ_strefy      VARCHAR(3) NOT NULL,
    bilet_id_typu_biletu   INTEGER NOT NULL,
    bilet_czas_przejazdu1  INTEGER
);

ALTER TABLE relation_20
    ADD CONSTRAINT relation_20_pk PRIMARY KEY ( strefa_typ_strefy,
                                                bilet_id_typu_biletu,
                                                bilet_czas_przejazdu1 );

CREATE TABLE strefa (
    typ_strefy VARCHAR(3) NOT NULL
);

ALTER TABLE strefa ADD CONSTRAINT strefa_pk PRIMARY KEY ( typ_strefy );

ALTER TABLE bilet
    ADD CONSTRAINT bilet_czasy_przejazdow_fk FOREIGN KEY ( czasy_p_czas_przejazdu )
        REFERENCES czasy_przejazdow ( czas_przejazdu );

ALTER TABLE do_zakupienia
    ADD CONSTRAINT do_zakupienia_biletomat_fk FOREIGN KEY ( biletomat_id_biletomatu )
        REFERENCES biletomat ( id_biletomatu );

ALTER TABLE do_zakupienia
    ADD CONSTRAINT do_zakupienia_kasa_biletowa_fk FOREIGN KEY ( kasa_biletowa_id_kasy )
        REFERENCES kasa_biletowa ( id_kasy );

ALTER TABLE kasa_biletowa
    ADD CONSTRAINT kasa_biletowa_przystanek_fk FOREIGN KEY ( przystanek_id_przystanku,
                                                             przystanek_miasto_nazwa_miasta,
                                                             przystanek_strefa_typ_strefy )
        REFERENCES przystanek ( id_przystanku,
                                miasto_nazwa_miasta,
                                strefa_typ_strefy );

ALTER TABLE model_pojazdu
    ADD CONSTRAINT model_pojazdu_producent_fk FOREIGN KEY ( producent_id_producenta )
        REFERENCES producent ( id_producenta );

ALTER TABLE pojazd
    ADD CONSTRAINT pojazd_biletomat_fk FOREIGN KEY ( biletomat_id_biletomatu )
        REFERENCES biletomat ( id_biletomatu );

ALTER TABLE pojazd
    ADD CONSTRAINT pojazd_linia_fk FOREIGN KEY ( linia_id_linii )
        REFERENCES linia ( id_linii );

ALTER TABLE pojazd
    ADD CONSTRAINT pojazd_model_pojazdu_fk FOREIGN KEY ( model_poj_id_modelu,
                                                         model_poj_prod_id_producenta )
        REFERENCES model_pojazdu ( id_modelu,
                                   producent_id_producenta );

ALTER TABLE przyjazd
    ADD CONSTRAINT przyjazd_przystanek_w_linii_fk FOREIGN KEY ( pwl_kolejnosc,
                                                                pwl_linia_id_linii,
                                                                pwl_przystanek_id_przystanku,
                                                                pwl_przystanek_nazwa_miasta,
                                                                pwl_przyst_strefa_typ_strefy )
        REFERENCES przystanek_w_linii ( kolejnosc,
                                        linia_id_linii,
                                        przystanek_id_przystanku,
                                        przystanek_miasto_nazwa_miasta,
                                        przystanek_strefa_typ_strefy );

ALTER TABLE przystanek
    ADD CONSTRAINT przystanek_biletomat_fk FOREIGN KEY ( biletomat_id_biletomatu )
        REFERENCES biletomat ( id_biletomatu );

ALTER TABLE przystanek
    ADD CONSTRAINT przystanek_miasto_fk FOREIGN KEY ( miasto_nazwa_miasta )
        REFERENCES miasto ( nazwa_miasta );

ALTER TABLE przystanek
    ADD CONSTRAINT przystanek_strefa_fk FOREIGN KEY ( strefa_typ_strefy )
        REFERENCES strefa ( typ_strefy );

ALTER TABLE przystanek_w_linii
    ADD CONSTRAINT przystanek_w_linii_linia_fk FOREIGN KEY ( linia_id_linii )
        REFERENCES linia ( id_linii );

ALTER TABLE przystanek_w_linii
    ADD CONSTRAINT pwl_przystanek_fk FOREIGN KEY ( przystanek_id_przystanku,
                                                                  przystanek_miasto_nazwa_miasta,
                                                                  przystanek_strefa_typ_strefy )
        REFERENCES przystanek ( id_przystanku,
                                miasto_nazwa_miasta,
                                strefa_typ_strefy );

ALTER TABLE relation_15
    ADD CONSTRAINT relation_15_kierowca_fk FOREIGN KEY ( kierowca_pesel )
        REFERENCES kierowca ( pesel );

ALTER TABLE relation_15
    ADD CONSTRAINT relation_15_pojazd_fk FOREIGN KEY ( pojazd_id_pojazdu,
                                                       pojazd_linia_id_linii,
                                                       pojazd_id_modelu,
                                                       pojazd_id_producenta )
        REFERENCES pojazd ( id_pojazdu,
                            linia_id_linii,
                            model_poj_id_modelu,
                            model_poj_prod_id_producenta );

ALTER TABLE relation_20
    ADD CONSTRAINT relation_20_bilet_fk FOREIGN KEY ( bilet_id_typu_biletu,
                                                      bilet_czas_przejazdu1 )
        REFERENCES bilet ( id_typu_biletu,
                           czasy_p_czas_przejazdu );

ALTER TABLE relation_20
    ADD CONSTRAINT relation_20_strefa_fk FOREIGN KEY ( strefa_typ_strefy )
        REFERENCES strefa ( typ_strefy );
