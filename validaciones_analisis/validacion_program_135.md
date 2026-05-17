 table_name  
-------------
 mermastdmes
(1 row)

                  table_name                  
----------------------------------------------
 05022021_MARTIC1F
 aaa_saldofisico
 aaa_saldovalorado
 aaa_transportitas_produ
 aaa_valores_aji
 aaaa_transportitas
 aaarfli1f
 abasplan1
 access_alert
 access_detail_alert
 accusua1f
 accusua2f
 act
 agrlinvalor
 agrparoee
 agrupoee
 agrupoee1
 agrvalor
 aje_ec_inbox
 aje_rn_inbox
 aje_sf_error
 aje_sf_inbox
 aje_sf_inbox_tmp
 aje_sf_outbox
 aje_sf_outbox_tmp
 aje_xadis_inbox
 ajemex
 ajepermaxo
 ajmartfvta
 ajmartvig
 ajmclienv1
 ajmdist
 ajmlistpre
 ajmvende1
 ajt_import_nextel5f
 ajt_import_nextel6f
 ajt_log_importacion
 ajtartenvcli
 ajtartenvcli_ts
 ajtartfvta
 ajtartfvta_ts
 ajtartvig
 ajtartvig1
 ajtartvig_ts
 ajtcambio
 ajtcambio_ts
 ajtclienv1
 ajtclienv1_ts
 ajtclienv1b
 ajtclienv2
 ajtcuotav
 ajtdist
 ajtdist_ts
 ajtepedid5f1
 ajtlistpre
 ajtlistpre1
 ajtlistpre_ts
 ajtnovta
 ajtnovta1f
 ajtnovta_ts
 ajtobsent
 ajtobsent_ts
 ajtpedid5f
 ajtpedid5f1
 ajtpedid6f
 ajtpedid7f
 ajtrangos
 ajtsabor
 ajttransa
 ajttransa_ts
 ajtvende1
 ajtvende1_ts
 ajtvende1f
 ajtvende2f
 almcon
 alminsind
 alp
 amemiso1f
 anuayvta
 apefechf1
 aprfor0f
 aprfor1f
 aprinv0f
 aprinv1f
 aprinv2f
 aprinv3f
 aprinv4f
 areaeqcc
 art
 art1
 art_basebm
 art_usados
 artfecven
 articulos_mp9
 articulos_mty_mp9
 articulos_pue_mp9
 articulos_vhs_mp9
 artxmaca1f
                                 Table "public.mermastdmes"
           Column            |            Type             | Collation | Nullable | Default 
-----------------------------+-----------------------------+-----------+----------+---------
 compania                    | text                        |           |          | 
 sucursal                    | text                        |           |          | 
 ejercicio                   | integer                     |           |          | 
 periodo                     | integer                     |           |          | 
 nroop                       | text                        |           |          | 
 insumo                      | integer                     |           |          | 
 llave                       | text                        |           |          | 
 fliqui                      | integer                     |           |          | 
 fechacadena                 | text                        |           |          | 
 desfamilia                  | text                        |           |          | 
 desequipo                   | text                        |           |          | 
 desinsumo                   | text                        |           |          | 
 desarticulo                 | text                        |           |          | 
 articulopri                 | double precision            |           |          | 
 qgirad                      | double precision            |           |          | 
 tipart                      | text                        |           |          | 
 linea                       | integer                     |           |          | 
 qstd                        | double precision            |           |          | 
 qreal                       | double precision            |           |          | 
 vstd                        | double precision            |           |          | 
 vreal                       | double precision            |           |          | 
 preciostd                   | double precision            |           |          | 
 desfamilia1                 | text                        |           |          | 
 desfamilia2                 | text                        |           |          | 
 linadm                      | text                        |           |          | 
 a21tipo_antes               | text                        |           |          | 
 insumochild                 | double precision            |           |          | 
 tipochild                   | text                        |           |          | 
 preciochild                 | double precision            |           |          | 
 nuevovreal                  | double precision            |           |          | 
 nuevaqstd                   | double precision            |           |          | 
 tipo_adicional              | integer                     |           |          | 
 nuevovstd                   | double precision            |           |          | 
 pormerma                    | double precision            |           |          | 
 precioreal                  | double precision            |           |          | 
 desvprecio                  | double precision            |           |          | 
 merman4                     | double precision            |           |          | 
 a21desviacionporcantiyestru | double precision            |           |          | 
 a21nuevovstd                | double precision            |           |          | 
 a21desviacionporcanti       | double precision            |           |          | 
 a21desviacionporestru       | double precision            |           |          | 
 a21porcentajemerma          | double precision            |           |          | 
 a21precioreal               | double precision            |           |          | 
 a21desviacionprecio         | double precision            |           |          | 
 pridesmarca                 | text                        |           |          | 
 pridespresentacion          | text                        |           |          | 
 pridesformato               | text                        |           |          | 
 pridessabor                 | text                        |           |          | 
 priqcontenido               | integer                     |           |          | 
 descompania                 | text                        |           |          | 
 desucursal                  | text                        |           |          | 
 anio                        | integer                     |           |          | 
 mes                         | integer                     |           |          | 
 fecha                       | timestamp without time zone |           |          | 
 parametrodos                | integer                     |           |          | 

 compania | sucursal | ejercicio | periodo |    nroop     | insumo | llave | fliqui | fechacadena |    desfamilia    |     desequipo      |                           desinsumo                           |                        desarticulo                        | articulopri | qgirad | tipart | linea | qstd | qreal | vstd |   vreal   | preciostd |     desfamilia1      |    desfamilia2    | linadm | a21tipo_antes | insumochild | tipochild | preciochild | nuevovreal | nuevaqstd | tipo_adicional | nuevovstd | pormerma |     precioreal     | desvprecio | merman4 | a21desviacionporcantiyestru | a21nuevovstd | a21desviacionporcanti | a21desviacionporestru | a21porcentajemerma |   a21precioreal    | a21desviacionprecio | pridesmarca | pridespresentacion | pridesformato | pridessabor | priqcontenido |      descompania      |    desucursal     | anio | mes |         fecha          | parametrodos 
----------+----------+-----------+---------+--------------+--------+-------+--------+-------------+------------------+--------------------+---------------------------------------------------------------+-----------------------------------------------------------+-------------+--------+--------+-------+------+-------+------+-----------+-----------+----------------------+-------------------+--------+---------------+-------------+-----------+-------------+------------+-----------+----------------+-----------+----------+--------------------+------------+---------+-----------------------------+--------------+-----------------------+-----------------------+--------------------+--------------------+---------------------+-------------+--------------------+---------------+-------------+---------------+-----------------------+-------------------+------+-----+------------------------+--------------
 0035     | 08       |      2023 |       7 | PALP23000091 |  77804 | LLAVE | 738715 | 14/07/2023  | BASES TERMINADAS | BASES PARA BEBIDAS | CONCENTRADO PARA REFRESCO CITRUS PUNCH BF-MX-190615 - PARTE 2 | CONCENTRADO PARA REFRESCO CITRUS PUNCH BF-MX-190615       |       72445 |    216 | 008    |    42 |  216 |   216 |    0 |  35990.03 |         0 | BASE DE BEBIDA PARTE | BASE DE BEBIDA PT | 03     | STD           |       77804 | STD       |           0 |          0 |       216 |              1 |         0 |        0 | 166.62050925925925 |          0 |       0 |                    35990.03 |            0 |                     0 |              35990.03 |                  0 | 166.62050925925925 |                   0 |             |                    |               |             |             1 | INMOBILIARIA ALPAMAYO | ALPAMAYO (MATRIZ) | 2023 |   7 | 2023-08-03 12:59:55.19 |            2
 0035     | 08       |      2023 |       7 | PALP23000091 |  77805 | LLAVE | 738715 | 14/07/2023  | BASES TERMINADAS | BASES PARA BEBIDAS | CONCENTRADO PARA REFRESCO CITRUS PUNCH BF-MX-190615 - PARTE 3 | CONCENTRADO PARA REFRESCO CITRUS PUNCH BF-MX-190615       |       72445 |    216 | 008    |    42 |  216 |   216 |    0 | 129723.76 |         0 | BASE DE BEBIDA PARTE | BASE DE BEBIDA PT | 03     | STD           |       77805 | STD       |           0 |          0 |       216 |              1 |         0 |        0 |   600.572962962963 |          0 |       0 |                   129723.76 |            0 |                     0 |             129723.76 |                  0 |   600.572962962963 |                   0 |             |                    |               |             |             1 | INMOBILIARIA ALPAMAYO | ALPAMAYO (MATRIZ) | 2023 |   7 | 2023-08-03 12:59:55.19 |            2
 0035     | 08       |      2023 |       7 | PALP23000091 |  77806 | LLAVE | 738715 | 14/07/2023  | BASES TERMINADAS | BASES PARA BEBIDAS | CONCENTRADO PARA REFRESCO CITRUS PUNCH BF-MX-190615 - PARTE 4 | CONCENTRADO PARA REFRESCO CITRUS PUNCH BF-MX-190615       |       72445 |    216 | 008    |    42 |  216 |   216 |    0 |  51051.24 |         0 | BASE DE BEBIDA PARTE | BASE DE BEBIDA PT | 03     | STD           |       77806 | STD       |           0 |          0 |       216 |              1 |         0 |        0 | 236.34833333333333 |          0 |       0 |                    51051.24 |            0 |                     0 |              51051.24 |                  0 | 236.34833333333333 |                   0 |             |                    |               |             |             1 | INMOBILIARIA ALPAMAYO | ALPAMAYO (MATRIZ) | 2023 |   7 | 2023-08-03 12:59:55.19 |            2
 0035     | 08       |      2023 |       7 | PALP23000092 |      5 | LLAVE | 738715 | 14/07/2023  | BASES TERMINADAS | BASES PARA BEBIDAS | BENZOATO DE SODIO                                             | BASE PARA BEBIDA JARABEADA CARBONATADA UVA   BG-MX-160478 |       68616 |     10 | 008    |    42 | 43.4 |  43.4 |    0 |   3026.78 |         0 | INSUMOS              | BASE DE BEBIDA PT | 04     | STD           |           5 | STD       |           0 |          0 |      43.4 |              1 |         0 |        0 |  69.74147465437788 |          0 |       0 |                     3026.78 |            0 |                     0 |               3026.78 |                  0 |  69.74147465437788 |                   0 |             |                    |               |             |             1 | INMOBILIARIA ALPAMAYO | ALPAMAYO (MATRIZ) | 2023 |   7 | 2023-08-03 12:59:55.19 |            2
 0035     | 08       |      2023 |       7 | PALP23000092 |      6 | LLAVE | 738715 | 14/07/2023  | BASES TERMINADAS | BASES PARA BEBIDAS | ACIDO CITRICO                                                 | BASE PARA BEBIDA JARABEADA CARBONATADA UVA   BG-MX-160478 |       68616 |     10 | 008    |    42 | 50.4 |  50.4 |    0 |   1012.63 |         0 | INSUMOS              | BASE DE BEBIDA PT | 04     | STD           |           6 | STD       |           0 |          0 |      50.4 |              1 |         0 |        0 |  20.09186507936508 |          0 |       0 |                     1012.63 |            0 |                     0 |               1012.63 |                  0 |  20.09186507936508 |                   0 |             |                    |               |             |             1 | INMOBILIARIA ALPAMAYO | ALPAMAYO (MATRIZ) | 2023 |   7 | 2023-08-03 12:59:55.19 |            2
(5 rows)

