CREATE TABLE biletomaty (
    id_biletomatu     INTEGER NOT NULL,
    platnosc_gotowka  ENUM('t', 'n') NOT NULL,
    platnosc_karta    ENUM('t', 'n') NOT NULL
);

ALTER TABLE biletomaty ADD CONSTRAINT biletomat_pk PRIMARY KEY ( id_biletomatu );

CREATE TABLE bilety (
    id_typu_biletu                INTEGER NOT NULL,
    czy_ulgowy                    ENUM('t', 'n') NOT NULL,
    cena                          FLOAT NOT NULL,
    czas_przejazdu                ENUM('15', '30', '60') NOT NULL,
    do_zak_kasy_biletowe_id_kasy  INTEGER NOT NULL,
    do_zak_bil_id_biletomatu      INTEGER NOT NULL,
    do_zak_id_biletu              INTEGER NOT NULL
);

CREATE UNIQUE INDEX bilet__idx ON
    bilety (
        do_zak_kasy_biletowe_id_kasy
    ASC,
        do_zak_bil_id_biletomatu
    ASC,
        do_zak_id_biletu
    ASC );

ALTER TABLE bilety ADD CONSTRAINT bilet_pk PRIMARY KEY ( id_typu_biletu );
                                                     
CREATE TABLE bilety_i_strefy (
    strefa_typ_strefy      ENUM('A', 'B', 'C') NOT NULL,
    bilet_id_typu_biletu   INTEGER NOT NULL,
    bilet_czas_przejazdu1  ENUM('15', '30', '60') NOT NULL
);

ALTER TABLE bilety_i_strefy
    ADD CONSTRAINT relation_20_pk PRIMARY KEY ( strefa_typ_strefy,
                                                bilet_id_typu_biletu,
                                                bilet_czas_przejazdu1 );

CREATE TABLE do_zakupienia (
    bilety_id_typu_biletu     INTEGER NOT NULL,
    biletomaty_id_biletomatu  INTEGER NOT NULL,
    kasy_biletowe_id_kasy     INTEGER NOT NULL,
    id_biletu                 INTEGER NOT NULL,
    data_zakupu               DATE,
    czas_przejazdu            ENUM('15', '30', '60') NOT NULL
);

CREATE UNIQUE INDEX do_zakupienia__idx ON
    do_zakupienia (
        bilety_id_typu_biletu
    ASC );

CREATE UNIQUE INDEX do_zakupienia__idxv1 ON
    do_zakupienia (
        bilety_id_typu_biletu
    ASC,
        czas_przejazdu
    ASC );

ALTER TABLE do_zakupienia
    ADD CONSTRAINT do_zakupienia_pk PRIMARY KEY ( kasy_biletowe_id_kasy,
                                                  biletomaty_id_biletomatu,
                                                  id_biletu );

CREATE TABLE kasy_biletowe (
    id_kasy                         INTEGER NOT NULL,
    godzina_otwarcia                DATE NOT NULL,
    godzina_zamkniecia              DATE NOT NULL,
    przystanki_id_przystanku        INTEGER,
    przystanki_miasta_nazwa_miasta  VARCHAR(30),
    przystanki_strefy_typ_strefy    ENUM('A', 'B', 'C') NOT NULL
);

ALTER TABLE kasy_biletowe ADD CONSTRAINT kasa_biletowa_pk PRIMARY KEY ( id_kasy );

CREATE TABLE kierowcy (
    pesel                   VARCHAR(11) NOT NULL,
    imie                    VARCHAR(20) NOT NULL,
    nazwisko                VARCHAR(30) NOT NULL,
    plec                    ENUM('k', 'm')     NOT NULL,
    uprawnienia_autobusowe  ENUM('t', 'n'),
    uprawnienia_tramwajowe  ENUM('t', 'n'),
    placa                   FLOAT NOT NULL,
    data_zatrudnienia       DATE,
    stan_cywilny            ENUM('zonaty', 'zamezna', 'wdowiec', 'wdowa', 'panna', 'kawaler', 'rozwiedziony', 'rozwiedziona', 'w separacji')
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
    typ_linii  ENUM('autobusowa', 'tramwajowa') NOT NULL
);

ALTER TABLE linie ADD CONSTRAINT linia_pk PRIMARY KEY ( id_linii );

CREATE TABLE miasta (
    nazwa_miasta        VARCHAR(30) NOT NULL,
    status              VARCHAR(10),
    liczba_mieszkancow  INTEGER,
    powierzchnia        FLOAT
);

ALTER TABLE miasta ADD CONSTRAINT miasto_pk PRIMARY KEY ( nazwa_miasta );

CREATE TABLE modele_pojazdow (
    id_modelu                 INTEGER NOT NULL,
    nazwa_modelu              VARCHAR(30) NOT NULL,
    typ_pojazdu               VARCHAR(10) NOT NULL,
    czy_niskopodlogowy        ENUM('t', 'n'),
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
    pwl_przyst_strefy_typ_strefy  ENUM('A', 'B', 'C') NOT NULL
);

ALTER TABLE przyjazdy ADD CONSTRAINT przyjazd_pk PRIMARY KEY ( id_przyjazdu );

CREATE TABLE przystanki (
    id_przystanku             INTEGER NOT NULL,
    nazwa_przystanku          VARCHAR(30) NOT NULL,
    adres                     VARCHAR(30) NOT NULL,
    miasta_nazwa_miasta       VARCHAR(30) NOT NULL,
    czy_zajezdnia             ENUM('t', 'n'),
    biletomaty_id_biletomatu  INTEGER NOT NULL,
    strefy_typ_strefy         ENUM('A', 'B', 'C') NOT NULL
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
    przystanki_strefy_typ_strefy    ENUM('A', 'B', 'C') NOT NULL
);

ALTER TABLE przystanki_w_linii
    ADD CONSTRAINT przystanek_w_linii_pk PRIMARY KEY ( kolejnosc,
                                                       linie_id_linii,
                                                       przystanki_id_przystanku,
                                                       przystanki_miasta_nazwa_miasta,
                                                       przystanki_strefy_typ_strefy );

CREATE TABLE strefy (
    typ_strefy ENUM('A', 'B', 'C') NOT NULL
);

ALTER TABLE strefy ADD CONSTRAINT strefa_pk PRIMARY KEY ( typ_strefy );

ALTER TABLE do_zakupienia
    ADD CONSTRAINT do_zakupienia_biletomat_fk FOREIGN KEY ( biletomaty_id_biletomatu )
        REFERENCES biletomaty ( id_biletomatu );

ALTER TABLE do_zakupienia
    ADD CONSTRAINT do_zakupienia_kasa_biletowa_fk FOREIGN KEY ( kasy_biletowe_id_kasy )
        REFERENCES kasy_biletowe ( id_kasy );

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

ALTER TABLE bilety_i_strefy
    ADD CONSTRAINT relation_20_bilet_fk FOREIGN KEY ( bilet_id_typu_biletu,
                                                      bilet_czas_przejazdu1 )
        REFERENCES bilety ( id_typu_biletu,
                            czas_przejazdu );

ALTER TABLE bilety_i_strefy
    ADD CONSTRAINT relation_20_strefa_fk FOREIGN KEY ( strefa_typ_strefy )
        REFERENCES strefy ( typ_strefy );
