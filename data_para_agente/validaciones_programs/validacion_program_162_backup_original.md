### SECCIÓN: AUDITORÍA TÉCNICA DE ESTRUCTURAS DE DATOS, NIVELES DE AUTORIZACIÓN Y TRAZABILIDAD DE FÓRMULAS: 
Validar la integridad de los diccionarios de datos (`tformula_`), verificar los parámetros de configuración de niveles de aprobación (`maprob1f`, `maprobniv`) y extraer la evidencia de trazabilidad técnica (triggers y tablas temporales) para asegurar la compatibilidad con el nuevo flujo en Odoo 19.

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
\d tformula_
\d tmp_aprob_ped
\d maprob1f
\d maprobniv
\d taprob1f
\d taprob2f
\d taprob3f
\d taprob4f
SELECT * FROM tformula_ LIMIT 10;
SELECT * FROM tmp_aprob_ped LIMIT 10;
SELECT * FROM maprobniv;
SELECT * FROM maprob1f LIMIT 10;
SELECT table_name, column_name, data_type FROM information_schema.columns WHERE table_name IN ('tformula_', 'tmp_aprob_ped', 'maprob1f', 'maprobniv', 'taprob1f') AND (column_name LIKE '%aprob%' OR column_name LIKE '%estado%' OR column_name LIKE '%status%' OR column_name LIKE '%firma%') ORDER BY table_name, ordinal_position;
SELECT trigger_name, event_manipulation, event_object_table, action_statement FROM information_schema.triggers WHERE event_object_table LIKE '%formula%' OR event_object_table LIKE '%aprob%';
\d sku_excel_formulas
SELECT * FROM sku_excel_formulas LIMIT 10;
\d av_ibomi_result
SELECT * FROM av_ibomi_result LIMIT 10;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local" >> ~/TutorialOdoo/data_para_agente/validacion_162.md
```
```text
                   Table "public.tformula_"
  Column  |       Type       | Collation | Nullable | Default 
----------+------------------+-----------+----------+---------
 compania | text             |           |          | 
 sucursal | text             |           |          | 
 articulo | double precision |           |          | 
 desc_sku | text             |           |          | 
 estado   | text             |           |          | 
 tamlote  | double precision |           |          | 
 nrosecu  | double precision |           |          | 
 material | double precision |           |          | 
 porcent  | double precision |           |          | 
 factconv | double precision |           |          | 
 cantidad | double precision |           |          | 

              Table "public.tmp_aprob_ped"
    Column    |  Type   | Collation | Nullable | Default 
--------------+---------+-----------+----------+---------
 compania     | text    |           |          | 
 sucursal     | text    |           |          | 
 emisor       | text    |           |          | 
 docupedido   | text    |           |          | 
 nropedido    | integer |           |          | 
 cliente      | integer |           |          | 
 ordcompra    | text    |           |          | 
 usuario      | text    |           |          | 
 seleccionado | bytea   |           |          | 

                Table "public.maprob1f"
   Column   |  Type   | Collation | Nullable | Default 
------------+---------+-----------+----------+---------
 compania   | text    |           | not null | 
 nivel      | text    |           | not null | 
 descripniv | text    |           | not null | 
 estado     | text    |           | not null | 
 feccrea    | integer |           | not null | 
 horcrea    | text    |           | not null | 
 usucrea    | text    |           | not null | 
 fecultmod  | integer |           | not null | 
 horultimod | text    |           | not null | 
 ultusumod  | text    |           | not null | 
 orden      | integer |           |          | 
 nivaprob   | text    |           |          | 
Indexes:
    "idx_168066_maprob1l1" UNIQUE, btree (compania, nivel)
    "idx_168066_maprob1l2" btree (compania, descripniv)

               Table "public.maprobniv"
   Column   |  Type   | Collation | Nullable | Default 
------------+---------+-----------+----------+---------
 compania   | text    |           | not null | 
 modulo     | text    |           | not null | 
 opcion     | text    |           | not null | 
 transaccio | text    |           | not null | 
 nivel      | text    |           | not null | 
 estado     | text    |           | not null | 
 feccrea    | integer |           | not null | 
 horcrea    | text    |           | not null | 
 usucrea    | text    |           | not null | 
 fecultmod  | integer |           | not null | 
 horultmod  | text    |           | not null | 
 ultusumod  | text    |           | not null | 
 tipoaprob  | text    |           |          | 
Indexes:
    "idx_168200_maprobnil1" UNIQUE, btree (compania, modulo, opcion, transaccio, nivel)

                Table "public.taprob1f"
   Column   |   Type   | Collation | Nullable | Default 
------------+----------+-----------+----------+---------
 compania   | text     |           | not null | 
 sucursal   | text     |           | not null | 
 area       | text     |           | not null | 
 caja       | smallint |           | not null | 
 transaccio | text     |           | not null | 
 nroserie   | text     |           |          | 
 nrodoc     | text     |           | not null | 
 persona    | integer  |           | not null | 
 nivel      | text     |           | not null | 
 corrautori | smallint |           | not null | 
 empleautor | integer  |           | not null | 
 fecautoriz | integer  |           | not null | 
 horautoriz | text     |           | not null | 
 flgaprodes | bytea    |           | not null | 
 observac   | text     |           | not null | 
 estado     | text     |           | not null | 
 feccrea    | integer  |           | not null | 
 horcrea    | text     |           | not null | 
 usucrea    | text     |           | not null | 
 fecultmod  | integer  |           | not null | 
 horultimod | text     |           | not null | 
 ultusumod  | text     |           | not null | 
 comprador  | integer  |           | not null | 
Indexes:
    "idx_173731_taprob1l1" UNIQUE, btree (compania, sucursal, area, caja, transaccio, nroserie, nrodoc, persona, nivel, corrautori)
    "idx_173731_taprob1l2" btree (compania, sucursal, area, caja, transaccio, nroserie, nrodoc, persona, nivel, empleautor)
    "idx_173731_taprob1l3" btree (compania, sucursal, persona)
    "idx_173731_taprob1l4" btree (compania, sucursal, empleautor)

                Table "public.taprob2f"
   Column   |   Type   | Collation | Nullable | Default 
------------+----------+-----------+----------+---------
 compania   | text     |           | not null | 
 sucursal   | text     |           | not null | 
 transaccio | text     |           | not null | 
 nroserie   | text     |           |          | 
 nrodoc     | text     |           | not null | 
 persona    | integer  |           | not null | 
 orden      | smallint |           | not null | 
 descrip    | text     |           | not null | 
 actualiza  | integer  |           | not null | 
 estado     | text     |           | not null | 
 feccrea    | integer  |           | not null | 
 horcrea    | text     |           | not null | 
 usucrea    | text     |           | not null | 
 fecultmod  | integer  |           | not null | 
 horultimod | text     |           | not null | 
 ultusumod  | text     |           | not null | 
Indexes:
    "idx_173736_taprob2l1" UNIQUE, btree (compania, sucursal, transaccio, nroserie, nrodoc, persona, orden)

                    Table "public.taprob3f"
   Column   |       Type       | Collation | Nullable | Default 
------------+------------------+-----------+----------+---------
 compania   | text             |           | not null | 
 sucursal   | text             |           | not null | 
 area       | text             |           | not null | 
 caja       | smallint         |           | not null | 
 transaccio | text             |           | not null | 
 serie      | text             |           | not null | 
 nrodoc     | text             |           | not null | 
 proveedor  | integer          |           | not null | 
 fecha      | integer          |           | not null | 
 total      | double precision |           | not null | 
 moneda     | text             |           | not null | 
 preparadop | integer          |           | not null | 
 ordautoriz | smallint         |           | not null | 

                Table "public.taprob4f"
   Column   |  Type   | Collation | Nullable | Default 
------------+---------+-----------+----------+---------
 compania   | text    |           | not null | 
 sucursal   | text    |           | not null | 
 transaccio | text    |           | not null | 
 nrodoc     | text    |           | not null | 
 tcompra    | integer |           | not null | 
 nivel      | integer |           | not null | 
 empleautor | integer |           | not null | 
 fecautoriz | integer |           | not null | 
 observac   | text    |           | not null | 
 estado     | text    |           | not null | 
 feccrea    | integer |           | not null | 
 horcrea    | text    |           | not null | 
 usucrea    | text    |           | not null | 
 fecultmod  | integer |           | not null | 
 horultimod | text    |           | not null | 
 ultusumod  | text    |           | not null | 
Indexes:
    "idx_173746_taprob4f_idx1" btree (compania, sucursal, transaccio, nrodoc)

 compania | sucursal | articulo |               desc_sku               | estado | tamlote | nrosecu | material | porcent | factconv  |  cantidad  
----------+----------+----------+--------------------------------------+--------+---------+---------+----------+---------+-----------+------------
 0002     | 29       |   500195 | BIG COLA PET NO RETORNABLE 3300 ML 6 | A      |     698 |       7 |   300677 |     100 | 3.0669803 | 2140.75225
 0002     | 29       |   500264 | BIG COLA PET NO RETORNABLE 500 ML 12 | A      |    2304 |       1 |     1854 |     100 |  0.049896 |   97.02144
 0002     | 29       |   500264 | BIG COLA PET NO RETORNABLE 500 ML 12 | A      |    2304 |       2 |     3242 |     100 |   5.07105 | 11683.6992
 0002     | 29       |   500264 | BIG COLA PET NO RETORNABLE 500 ML 12 | A      |    2304 |       3 |    30462 |     100 |        12 |      27648
 0002     | 29       |   500264 | BIG COLA PET NO RETORNABLE 500 ML 12 | A      |    2304 |       4 |    38153 |     100 |     0.024 |     55.296
 0002     | 29       |   500264 | BIG COLA PET NO RETORNABLE 500 ML 12 | A      |    2304 |       5 |    41282 |     100 |        12 |      27648
 0002     | 29       |   500264 | BIG COLA PET NO RETORNABLE 500 ML 12 | A      |    2304 |       6 |    41300 |     100 |        12 |      27648
 0002     | 29       |   500264 | BIG COLA PET NO RETORNABLE 500 ML 12 | A      |    2304 |       7 |   300745 |     100 |  0.929387 | 2141.30765
 0002     | 29       |   500269 | BIG COLA PET NO RETORNABLE 3300 ML 4 | A      |    1047 |       1 |     1854 |     100 | 0.1097712 |   96.98361
 0002     | 29       |   500269 | BIG COLA PET NO RETORNABLE 3300 ML 4 | A      |    1047 |       2 |     3242 |     100 |   11.1563 | 11680.6461
(10 rows)

 compania | sucursal | emisor | docupedido | nropedido | cliente | ordcompra |  usuario  | seleccionado 
----------+----------+--------+------------+-----------+---------+-----------+-----------+--------------
 0030     | 0001     | 02     | 300        |     38679 | 1748604 |           | TAROSALIA | \x46
 0030     | 0001     | 02     | 300        |     38680 | 1748609 |           | TAROSALIA | \x46
 0030     | 0001     | 02     | 300        |     38682 | 1748611 |           | TAROSALIA | \x46
 0030     | 0001     | 02     | 300        |     38683 | 1748611 |           | TAROSALIA | \x46
 0030     | 0001     | 02     | 300        |     38684 | 1748611 |           | TAROSALIA | \x46
 0030     | 0001     | 02     | 300        |     38685 | 1748612 |           | TAROSALIA | \x46
 0030     | 0001     | 02     | 300        |     38686 | 1748612 |           | TAROSALIA | \x46
 0030     | 0001     | 02     | 300        |     38687 | 1748612 |           | TAROSALIA | \x46
 0030     | 0001     | 02     | 300        |     38688 | 1748612 |           | TAROSALIA | \x46
 0030     | 0001     | 02     | 300        |     38689 | 1748612 |           | TAROSALIA | \x46
(10 rows)

 compania | modulo | opcion | transaccio | nivel | estado | feccrea | horcrea | usucrea  | fecultmod | horultmod | ultusumod | tipoaprob 
----------+--------+--------+------------+-------+--------+---------+---------+----------+-----------+-----------+-----------+-----------
 0002     | COL    | LG040  | OCO        | A     | A      |  735800 | 235843  | AOLIVERA |    735800 | 235905    | AOLIVERA  | L
 1000     | COL    | LG040  | OCO        | A     | A      |  736990 | 141818  | SYSTEM   |    736990 | 141818    | SYSTEM    | L
 0002     | COL    | LG040  | OCO        | C     | A      |  735800 | 235915  | AOLIVERA |    735800 | 235926    | AOLIVERA  | I
 1000     | COL    | LG040  | OCO        | C     | A      |  736990 | 141818  | SYSTEM   |    736990 | 141818    | SYSTEM    | I
 0100     | COL    | LG040  | OCO        |       | A      |  737286 | 184402  | MMENDOZA |    737286 | 184404    | MMENDOZA  | 
 4000     | COL    | LG040  | OCO        | A     | A      |  737452 | 101220  | SYSTEM   |    737452 | 101220    | SYSTEM    | L
 4000     | COL    | LG040  | OCO        | C     | A      |  737452 | 101220  | SYSTEM   |    737452 | 101220    | SYSTEM    | I
 3000     | COL    | LG040  | OCO        | A     | A      |  737452 | 101351  | SYSTEM   |    737452 | 101351    | SYSTEM    | L
 3000     | COL    | LG040  | OCO        | C     | A      |  737452 | 101351  | SYSTEM   |    737452 | 101351    | SYSTEM    | I
 2000     | COL    | LG040  | OCO        | A     | A      |  737452 | 101416  | SYSTEM   |    737452 | 101416    | SYSTEM    | L
 2000     | COL    | LG040  | OCO        | C     | A      |  737452 | 101416  | SYSTEM   |    737452 | 101416    | SYSTEM    | I
 0003     | COL    | LG040  | OCO        | A     | A      |  737538 | 230305  | SYSTEM   |    737538 | 230305    | SYSTEM    | L
 0003     | COL    | LG040  | OCO        | C     | A      |  737538 | 230305  | SYSTEM   |    737538 | 230305    | SYSTEM    | I
 5000     | COL    | LG040  | OCO        | A     | A      |  737544 | 160659  | SYSTEM   |    737544 | 160659    | SYSTEM    | L
 5000     | COL    | LG040  | OCO        | C     | A      |  737544 | 160659  | SYSTEM   |    737544 | 160659    | SYSTEM    | I
 0030     | COL    | LG040  | OCO        | A     | A      |  737615 | 125323  | SYSTEM   |    737615 | 125323    | SYSTEM    | L
 0030     | COL    | LG040  | OCO        | C     | A      |  737615 | 125323  | SYSTEM   |    737615 | 125323    | SYSTEM    | I
 0025     | COL    | LG040  | OCO        | A     | A      |  737704 | 142525  | SYSTEM   |    737704 | 142525    | SYSTEM    | L
 0025     | COL    | LG040  | OCO        | C     | A      |  737704 | 142525  | SYSTEM   |    737704 | 142525    | SYSTEM    | I
 0035     | COL    | LG040  | OCO        |       | A      |  737777 | 122550  | JAVIERRR |    737777 | 122554    | JAVIERRR  | 
 0033     | COL    | LG040  | OCO        |       | A      |  737788 | 103753  | JAVIERRR |    737788 | 103755    | JAVIERRR  | 
 0060     | COL    | LG040  | OCO        |       | A      |  737788 | 103852  | JAVIERRR |    737788 | 103856    | JAVIERRR  | 
 0032     | COL    | LG040  | OCO        |       | A      |  738055 | 185211  | DDIAZL   |    738055 | 185215    | DDIAZL    | 
 0036     | COL    | LG040  | OCO        | A     | A      |  738888 | 161028  | OREAJ    |    738888 | 161028    | OREAJ     | L
 0036     | COL    | LG040  | OCO        | C     | A      |  738888 | 161028  | OREAJ    |    738888 | 161028    | OREAJ     | I
(25 rows)

 compania | nivel |   descripniv   | estado | feccrea | horcrea | usucrea | fecultmod | horultimod | ultusumod | orden | nivaprob 
----------+-------+----------------+--------+---------+---------+---------+-----------+------------+-----------+-------+----------
 0032     | 01    | JEFATURA       | 1      |  734377 | 213440  | MVEGA   |    734377 | 213440     | MVEGA     |     0 | 
 0032     | 02    | GERENCIA       | 2      |  734377 | 213440  | MVEGA   |    734377 | 213440     | MVEGA     |     0 | 
 0032     | 03    | DIRECCION      | 3      |  734377 | 213441  | MVEGA   |    734377 | 213441     | MVEGA     |     0 | 
 0032     | A     | COMPRAS NV.1   | 1      |  734377 | 213441  | MVEGA   |    734377 | 213441     | MVEGA     |     0 | 
 0032     | B     | COMPRAS NV.2   | 2      |  734377 | 213442  | MVEGA   |    734377 | 213442     | MVEGA     |     0 | 
 0032     | C     | COMPRAS NV.3   | 3      |  734377 | 213442  | MVEGA   |    734377 | 213442     | MVEGA     |     0 | 
 0032     | E     | PRE-APROBACION | 1      |  734377 | 213442  | MVEGA   |    734377 | 213442     | MVEGA     |     0 | 
 0032     | F     | APROBACION DCO | 3      |  734377 | 213443  | MVEGA   |    734377 | 213443     | MVEGA     |     0 | 
 0032     | N1    | VISTO          | 1      |  734377 | 213443  | MVEGA   |    734377 | 213443     | MVEGA     |     0 | 
 0032     | N2    | APROBACION     | 2      |  734377 | 213444  | MVEGA   |    734377 | 213444     | MVEGA     |     0 | 
(10 rows)

 table_name | column_name | data_type 
------------+-------------+-----------
 maprob1f   | estado      | text
 maprob1f   | nivaprob    | text
 maprobniv  | estado      | text
 maprobniv  | tipoaprob   | text
 taprob1f   | estado      | text
 tformula_  | estado      | text
(6 rows)

  trigger_name | event_manipulation | event_object_table | action_statement 
 --------------+--------------------+--------------------+------------------
 (0 rows)
 ```
 **Comentario de Hallazgo:**
 Se confirma que `tformula_` solo maneja un campo `estado` genérico (sin campos de aprobación propios). La configuración multinivel existe en `maprob1f`/`maprobniv` con niveles como JEFATURA, GERENCIA, DIRECCION, COMPRAS NV.1-3. No existen triggers en ninguna tabla de fórmulas/aprobación — toda la lógica de aprobación reside en la capa de aplicación, no en la base de datos.

 ### SECCIÓN: AUDITORÍA ESTRUCTURAL DE LÓGICA DE NEGOCIO, PROCEDIMIENTOS ALMACENADOS Y TRAZABILIDAD DINÁMICA: 
 Analizar la distribución de estados de fórmulas, identificar dependencias en el esquema mediante muestreo de columnas de autorización (`aprob`, `autoriz`, `firm`) y auditar rutinas/funciones internas que procesan los cálculos de aprobación en Odoo 19.


```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
-- 1 y 5. Estados y conteo
SELECT estado, COUNT(*) FROM tformula_ GROUP BY estado;

-- 2. Tablas relacionadas (Fórmula/FML)
SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND (tablename ILIKE '%formula%' OR tablename ILIKE '%fml%');

-- 3. Columnas de aprobación en TODO el esquema public (Muestreo inteligente)
SELECT table_name, column_name 
FROM information_schema.columns 
WHERE (column_name ILIKE '%aprob%' OR column_name ILIKE '%autoriz%' OR column_name ILIKE '%visto%' OR column_name ILIKE '%firm%') 
AND table_schema = 'public' 
ORDER BY table_name;

-- 4. Vistas y Funciones (Aquí puede estar el cálculo)
SELECT routine_name, routine_type 
FROM information_schema.routines 
WHERE routine_schema = 'public' AND (routine_name ILIKE '%formula%' OR routine_name ILIKE '%aprob%');

-- 6. Auditoría y Logs
SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND (tablename ILIKE '%log%' OR tablename ILIKE '%hist%');
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local" 
```
```text
 estado | count 
--------+-------
 A      |  5087
(1 row)

     tablename      
--------------------
 tformula_
 sku_excel_formulas
(2 rows)

         table_name         |     column_name      
----------------------------+----------------------
 aprfor1f                   | aprobador
 aprfor1f                   | tipaprob
 aprinv1f                   | aprobador
 aprinv2f                   | stsaprob
 aprinv2f                   | horautoriz
 aprinv2f                   | fecautoriz
 auditlote                  | aprobadop
 auditlote                  | fecaprob
 auditlote                  | horaprob
 bcktordco1f_11022021       | fecaprobac
 bcktordco1f_11022021       | desaprobp
 bcktordco1f_11022021       | ordautoriz
 bcktordco1f_11022021       | aprobadop
 bcktordco1f_11022021       | horaprobac
 bcktordco2f_11022021       | cantidad_aprobada_cc
 bcnftr1                    | flgaprobxniv
 bcnftr1                    | aprobot
 cabpenv1f                  | aprobadop
 cabpenv1f                  | horaprob
 cabpenv1f                  | flgaprob
 cabpenv1f                  | fecaprob
 cabsce1f                   | horaprob
 cabsce1f                   | fecaprob
 comdocum1f                 | nroaprob
 csolactfor                 | aprobador
 csolactfor                 | stsaprobac
 csolactfor                 | fecaprobac
 csolactfor                 | horaprobac
 csolapop                   | fecaprobac
 csolapop                   | aprobador
 csolapop                   | horaprobac
 csolaptoma                 | aprobador
 csolaptoma                 | fecaprobac
 csolaptoma                 | horaprobac
 detimprsf                  | flgaprobado
 detimprsf                  | usuaprob
 detimprsf                  | fecaprob
 detimprsf                  | horaprob
 detpenv2f                  | qautorizada
 dsolactfor                 | horaprob
 dsolactfor                 | nivaprob
 dsolactfor                 | stsaprobac
 dsolactfor                 | fecaprob
 dsolactfor                 | aprobadop
 dsolactfor                 | flgaprob
 factprvta                  | confirmado
 forfab                     | aprobadop
 forfab                     | horaprobadop
 forfab                     | fecaprobadop
 forfab_20022020            | aprobadop
 forfab_29122019            | aprobadop
 forfab_bkp_160419          | aprobadop
 forfabmes                  | horaprobadop
 forfabmes                  | aprobadop
 forfabmes                  | fecaprobadop
 forfabstd                  | aprobadop
 inv_useraprtoma            | aprobador
 inv_useraprtoma            | stsaprob
 inv_useraprtoma_niveles    | aprobador
 inv_useraprtoma_niveles    | nivel_aprob
 lote                       | fecaprob
 mactfj13f                  | vtautoriza
 mactfj1fx                  | vtautoriza
 mapro10f                   | aprobador
 maprob1f                   | nivaprob
 maprob2f                   | cantaprob
 maprob3f                   | nivaprob
 maprob3f                   | qautoriza
 maprob3f                   | tipaprob
 maprob3f                   | flgaprobac
 maprobniv                  | tipoaprob
 marticmf                   | autorizado
 mclien9f                   | credaprob
 mclienh9f                  | credaprob
 mcomdep1f                  | flgconfirma
 mcompa1f                   | aprobreq
 mcompa1f                   | aproboco
 mcret7f                    | flgautorizada
 mdocum10f                  | anioaprob
 mdocum10f                  | nroaprob
 mfirmas2f                  | aprobado
 mfletjclf                  | aprobpor
 mfletjclf                  | fecaproba
 mfletjclf                  | flgaprobado
 mfletjclf                  | horaprobac
 mlote                      | fecaprob
 mlpbse1f                   | useraprob
 mlpbse1f                   | horaprob
 mlpbse1f                   | fecaprob
 mlpbse2f                   | fecaprob
 mlpbse2f                   | useraprob
 mlpbse2f                   | horaprob
 mlpbse3f                   | fecaprob
 mlpbse3f                   | horaprob
 mlpbse3f                   | useraprob
 mlpvta1f                   | horaprobac
 mlpvta1f                   | aprobadop
 mlpvta1f                   | fecaprobac
 mlpvta5f                   | horaprobac
 mlpvta5f                   | fecaprobac
 mlpvta5f                   | aprobadop
 mlpvta6f                   | horaprobac
 mlpvta6f                   | fecaprobac
 mlpvta6f                   | aprobadop
 movlote                    | cantaprob
 movstage                   | cantaprob
 mpadis1f                   | epaprob
 mpadis1f                   | aprobpedat
 mparam2f                   | flgtipaprob
 mparam2f                   | autorizape
 mparam2f_bck_27122020      | flgtipaprob
 mparam2f_bck_27122020      | autorizape
 mparam2f_bkp08122019       | autorizape
 mpersoef                   | flgautoriz
 parprod                    | aprobot
 parsubcic                  | flgaprobado
 pass                       | autorizado
 pdlpenv                    | flgaprob
 planviaje_orden_pago       | fecha_autorizacion
 presreg5f                  | horaprobac
 presreg5f                  | ordautoriz
 presreg5f                  | fecaprobac
 prodinp                    | qaprobada
 pv_tmp_factura_compra      | desaprobp
 pv_tmp_factura_compra      | horaprobac
 pv_tmp_factura_compra      | fecaprobac
 pv_tmp_factura_compra      | aprobadop
 pv_tmp_factura_compra      | ordautoriz
 pv_tmp_provee_cargo        | flgaprobad
 pv_tmp_rend_gastos_det     | aprobadop
 pvordpag1f                 | fecha_autorizacion
 reqdesm1f                  | fecaprobac
 reqdesm1f                  | desaprobp
 reqdesm1f                  | ordautoriz
 reqdesm1f                  | horaprobac
 reqdesm1f                  | aprobadop
 reqdesm2f                  | qaprobada
 rpmclientecuenta           | credaprob
 rpmfacturadistrib          | aprobado_por
 rpmfacturadistrib          | aprobado
 rpmfacturadistrib          | desaprob_por
 rpmfacturadistrib          | orden_autoriz
 rpmfacturadistribbck       | orden_autoriz
 rpmfacturadistribbck       | aprobado
 rpmfacturadistribbck       | aprobado_por
 rpmfacturadistribbck       | desaprob_por
 solnconf                   | fecaprob
 solnconf                   | flgaprobado
 solnconf                   | horaprob
 tactfj1f                   | fecaprobac
 tactfj1f                   | aprobadop
 tactfj1f                   | horaprobac
 tactfj1f                   | desaprobp
 taprform1f                 | fecautoriz
 taprform1f                 | horautoriz
 taprform1f                 | stsaprobac
 taprinv1f                  | fecautoriz
 taprinv1f                  | horautoriz
 taprob1f                   | horautoriz
 taprob1f                   | fecautoriz
 taprob3f                   | ordautoriz
 taprob4f                   | fecautoriz
 taprpro1f                  | fecautoriz
 taprpro1f                  | horautoriz
 tartsa2f                   | fecaprobac
 tartsacb2f                 | fecaprobac
 tbajaenv1f                 | horaprob
 tbajaenv1f                 | aprobadop
 tbajaenv1f                 | fecaprob
 tbanco1f                   | aprobadop
 tbanco1f                   | horaprobac
 tbanco1f                   | desaprobp
 tbanco1f                   | flgconfirma
 tbanco1f                   | ordautoriz
 tbanco1f                   | fecaprobac
 tbanco21f                  | horaprobac
 tbanco21f                  | fecaprobac
 tbanco21f                  | aprobadop
 tbanco21f                  | ordautoriz
 tbanco21f                  | desaprobp
 tbusuario                  | autoriza
 tcctep1f                   | aprobadop
 tcctep1f                   | faprobac
 tcctep1f                   | desaprobp
 tcctep1f                   | horaaprob
 tcctep1f                   | aprobpago
 tcdade1f                   | horaprobac
 tcdade1f                   | desaprobp
 tcdade1f                   | ordautoriz
 tcdade1f                   | aprobadop
 tcdade1f                   | fecaprobac
 tcdcje1f                   | fecaprobac
 tcdcje1f                   | desaprobp
 tcdcje1f                   | ordautoriz
 tcdcje1f                   | horaprobac
 tcdcje1f                   | aprobadop
 tcdliq3f                   | flgconfirmad
 tcdliq5f                   | flgconfirmad
 tcdpre1f                   | desaprobp
 tcdpre1f                   | horaprobac
 tcdpre1f                   | aprobadop
 tcdpre1f                   | ordautoriz
 tcdpre1f                   | fecaprobac
 tciecontab                 | autorizape
 tcjaer1f                   | autorizap
 tcjaer1f                   | desaprobp
 tcjaer1f                   | ordautoriz
 tcjaer1f                   | horaprobac
 tcjaer1f                   | impaprobad
 tcjaer1f                   | fecaprobac
 tcjaer4f                   | aprobadop
 tclicg1f                   | flgaprobad
 tclicj1f                   | ordautoriz
 tclicj1f                   | desaprobp
 tclicj1f                   | horaprobac
 tclicj1f                   | fecaprobac
 tclicj1f                   | aprobadop
 tclilt1f                   | desaprobp
 tclilt1f                   | horaprobac
 tclilt1f                   | fecaprobac
 tclilt1f                   | aprobadop
 tclilt1f                   | ordautoriz
 tclsol1f                   | ordautoriz
 tclsol1f                   | desaprobp
 tclsol1f                   | horaprobac
 tclsol1f                   | fecaprobac
 tclsol1f                   | aprobadop
 tcoalm0f                   | flgconfirmado
 tcoalm17f                  | fecconfirm
 tcoalm17f                  | aprobado
 tcoalm17f                  | aprobapor
 tcoalm17f                  | fecaproba
 tcoalm17f                  | confirmado
 tcoalm17f                  | horconfirm
 tcoalm17f                  | confirmpor
 tcoalm20f                  | flgautorizada
 tcofis1f                   | aprobado_por
 tcofis1f                   | aprobado
 tcofis1f                   | orden_autoriz
 tcofis1f                   | desaprob_por
 tcomerr1f                  | flgaprob
 tcomerr1f                  | aprobadop
 tcomerr1f                  | fecaprobac
 tcomerr1f                  | desaprobp
 tcompag1f                  | flgautorizada
 tcompag1f                  | flgconfirm
 tcompag3f                  | flgconfirm
 tcorde1f                   | aprobado
 tcorde1f                   | fecaproba
 tcorde1f                   | aprobadop
 tcorde2f                   | confirma
 tcotiz1f                   | horaprobac
 tcotiz1f                   | fecaprobac
 tcotiz1f                   | aprobadop
 tcotiz1f                   | ordautoriz
 tcotiz1f                   | desaprobp
 tcotiz2f                   | fecaprobac
 tcotiz2f                   | horaprobac
 tcotiz2f                   | ordautoriz
 tcotiz2f                   | aprobadop
 tcotiz2f                   | desaprobp
 tcotiz4f                   | flgaprobad
 tcovta1f                   | aprobado_por
 tcovta1f                   | aprobado
 tcovta1f                   | desaprob_por
 tcovta1f                   | orden_autoriz
 tcovta1f                   | flgconfirm
 tcovta1f                   | fecconfirm
 tcovta1f                   | perconfirm
 tcovta7f                   | flgautorizabaja
 tcovta7f                   | flgautorizada
 tcovta7f_1                 | flgautorizada
 tcovta7f_1                 | flgautorizabaja
 tcovtafe                   | firma
 tdistgto3f                 | desaprobp
 tdistgto3f                 | aprobadop
 tdistgto3f                 | ordautoriz
 tenvins1f                  | aprobadop
 tenvins1f                  | desaprobp
 tenvins1f                  | horaprobac
 tenvins1f                  | fecaprobac
 tenvins1f                  | ordautoriz
 tenvins2f                  | qaprobada
 tevase1f                   | aprobadop
 tevase1f                   | desaprobp
 tevase1f                   | horaprobac
 tevase1f                   | fecaprobac
 tevase1f                   | ordautoriz
 tfacom1f                   | fecaprobac
 tfacom1f                   | horaprobac
 tfacom1f                   | desaprobp
 tfacom1f                   | ordautoriz
 tfacom1f                   | aprobadop
 tfacom1f_bkp_090321        | desaprobp
 tfacom1f_bkp_090321        | horaprobac
 tfacom1f_bkp_090321        | fecaprobac
 tfacom1f_bkp_090321        | aprobadop
 tfacom1f_bkp_090321        | ordautoriz
 tfacom25f                  | flgautorizada
 tfacom40f                  | horaprobac
 tfacom40f                  | fecaprobac
 tfacom40f                  | aprobadop
 tfacom40f                  | ordautoriz
 tfacom40f                  | desaprobp
 thpcam1f                   | desaprobp
 thpcam1f                   | fecaprobac
 thpcam1f                   | aprobadop
 thpcam1f                   | horaprobac
 thpcam2f                   | aprobacion
 thpedi1f                   | aprobadop
 thpedi1f                   | desaprobp
 thpedi1f                   | fecaprobac
 thpedi1f                   | horaprobac
 thpedi2f                   | aprobacion
 tinvar1                    | aprobpor
 tinvarcb1                  | aprobpor
 tinvciccab                 | aprobado
 tinvcr1                    | aprobpor
 tliqce1f                   | fecaprobac
 tliqce1f                   | horaprob
 tliqce1f                   | desaprobp
 tliqce1f                   | aprobadop
 tmp_bco_cab                | aprobadop
 tmp_bco_cab                | flgconfirma
 tmp_bco_cab                | desaprobp
 tmp_bco_cab                | horaprobac
 tmp_bco_cab                | fecaprobac
 tmp_bco_cab                | ordautoriz
 tmp_planviaje_orden_pago   | fecha_autorizacion
 tmp_rod                    | desaprobp
 tmp_rod                    | ordautoriz
 tmp_rod                    | aprobadop
 tmp_rod                    | fecaprobac
 tmp_rod                    | horaprobac
 tmp_tbanco1f               | flgconfirma
 tmp_tbanco1f               | ordautoriz
 tmp_tbanco1f               | aprobadop
 tmp_tbanco1f               | fecaprobac
 tmp_tbanco1f               | horaprobac
 tmp_tbanco1f               | desaprobp
 tmp_tcdliq3f               | flgconfirmad
 tmp_tcdliq5f               | flgconfirmad
 tmp_tfacom1f               | desaprobp
 tmp_tfacom1f               | aprobadop
 tmp_tfacom1f               | ordautoriz
 tmp_tfacom1f               | horaprobac
 tmp_tfacom1f               | fecaprobac
 tmp_tprofn1f               | desaprobp
 tmp_tprofn1f               | ordautoriz
 tmp_tprofn1f               | aprobadop
 tmp_tprofn1f               | fecaprobac
 tmp_tprofn1f               | horaprobac
 tmpdetfor                  | aprobadop
 tmpdetfor                  | fecaprob
 tmpdetfor                  | horaprob
 tmpdetfor                  | flgaprob
 tmpedidoades               | fecaprobac
 tmpedidoades               | desaprobp
 tmpedidoades               | aprobadop
 tmpmlpvta2f                | aprobado
 tmptvouch1f                | aprobadop
 tmpz_tcovta1f              | flgconfirm
 tmpz_tcovta1f              | fecconfirm
 tmpz_tcovta1f              | perconfirm
 tmpz_tcovta1f              | aprobado_por
 tmpz_tcovta1f              | desaprob_por
 tmpz_tcovta1f              | orden_autoriz
 tmpz_tcovta1f              | aprobado
 tobseq1f                   | aprobadop
 tobseq1f                   | desaprobp
 tobseq1f                   | horaprobac
 tobseq1f                   | fecaprobac
 tobseq1f                   | ordautoriz
 tobseq2f                   | qaprobada
 tobseq7f                   | segaprob
 tobseq7f                   | priaprob
 tobseq8f                   | ordaprob
 tordco1f                   | aprobadop
 tordco1f                   | fecaprobac
 tordco1f                   | horaprobac
 tordco1f                   | ordautoriz
 tordco1f                   | desaprobp
 tordco2f                   | cantidad_aprobada_cc
 tordgr1f                   | horaprobac
 tordgr1f                   | desaprobp
 tordgr1f                   | aprobadop
 tordgr1f                   | fecaprobac
 tordgr1f                   | ordautoriz
 tordpa1f                   | desaprobp
 tordpa1f                   | aprobadop
 tordpa1f                   | ordautoriz
 tordpa1f                   | fecaprobac
 tordpa1f                   | horaprobac
 tpasiv1f                   | flgconfirm
 tpcamb1f                   | desaprobp
 tpcamb1f                   | horaprobac
 tpcamb1f                   | fecaprobac
 tpcamb1f                   | aprobadop
 tpcamb2f                   | aprobacion
 tpedid1f                   | fecaprobac
 tpedid1f                   | aprobadop
 tpedid1f                   | desaprobp
 tpedid1f                   | horaprobac
 tpedid1fautorifail         | desaprobp
 tpedid1fautorifail         | horaprobac
 tpedid1fautorifail         | fecaprobac
 tpedid1fautorifail         | aprobadop
 tpedid2f                   | aprobacion
 tpedid4f                   | horaprobado
 tpedid4f                   | flgaprobado
 tpedid5f                   | flgaprobado
 tpedid5f                   | horaprobado
 tpedid6f                   | horaprobado
 tpedid6f                   | flgaprobado
 tpllcb1f                   | aprobadop
 tpllcb1f                   | desaprobp
 tpllcb1f                   | horaprobac
 tpllcb1f                   | fecaprobac
 tpllcb1f                   | ordautoriz
 tprgpg1f                   | flgconfirm
 tprgpg2f                   | flgconfirm
 tprgpg2f                   | flgautoriz
 tprgpmi1                   | flgconfirm
 tprgpmi1                   | flgautoriz
 tprocg1f                   | flgaprobad
 tprocj1f                   | aprobadop
 tprocj1f                   | fecaprobac
 tprocj1f                   | horaprobac
 tprocj1f                   | desaprobp
 tprocj1f                   | ordautoriz
 tprofn1f                   | aprobadop
 tprofn1f                   | ordautoriz
 tprofn1f                   | desaprobp
 tprofn1f                   | horaprobac
 tprofn1f                   | fecaprobac
 tproin1                    | qaprobada
 tproin1                    | fecaprob
 tproin1                    | aprobpor
 tproin1x                   | aprobpor
 tproin1x                   | fecaprob
 tprolt1f                   | ordautoriz
 tprolt1f                   | desaprobp
 tprolt1f                   | horaprobac
 tprolt1f                   | fecaprobac
 tprolt1f                   | aprobadop
 tprovasi1f                 | desaprobadop
 tprovasi1f                 | aprobadop
 tprovasi1f                 | ordaprob
 tprovasi1f                 | fecaprob
 treque13f                  | aprobgtoad
 treque1f                   | ordautoriz
 treque1f                   | desaprobp
 treque1f                   | horaprobac
 treque1f                   | fecaprobac
 treque1f                   | aprobadop
 treque2f                   | qaprobada
 tsolape1f                  | fecaproba
 tsolape1f                  | aprobadop
 tsolape1f                  | flgaproba
 tsolape1f                  | desaprobp
 tsolape2f                  | aprobadop
 tvouch100f                 | aprobadop
 tvouch13f                  | desaprobadop
 tvouch13f                  | ordaprob
 tvouch13f                  | fecaprob
 tvouch13f                  | aprobadop
 tvouch15f                  | aprobador
 tvouch1f                   | aprobadop
 tvouch23f                  | flgaprob
 tvouch23f                  | aprobadop
 tvouch3f                   | aprobadop
 v_ades_tiempos_pedido      | omaprobhora
 v_ades_tiempos_pedido      | horaprobac
 v_ades_tiempos_pedido      | fecaprobac
 v_ades_tiempos_pedido      | aprobadopusu
 v_ades_tiempos_pedido      | aprobadopnom
 v_ades_tiempos_pedido      | aprobadop
 v_ades_tiempos_pedido      | omaprobusu
 v_ades_tiempos_pedido      | omaprobfecha
 v_ades_tiempos_pedido_prog | fltaprobfec
 v_ades_tiempos_pedido_prog | fltaprob
 v_ades_tiempos_pedido_prog | fltaprobusu
 v_cm_oc_entregas           | nroconfirmcita
 v_mlpvta1f                 | fecaprobac
 v_mlpvta1f                 | horaprobac
 v_mlpvta1f                 | aprobadop
 v_tpedid1f_encabezado      | aprobadop
 v_tpedid1f_encabezado      | desaprobp
 v_tpedid1f_encabezado      | fecaprobac
 v_tpedid1f_encabezado      | horaprobac
 ws_customer_abc            | idaprobador
(491 rows)

              routine_name               | routine_type 
-----------------------------------------+--------------
 fc_obtener_nivel_aprob_ajusteinv        | FUNCTION
 fc_retornacantidadasientomanualaprobado | FUNCTION
(2 rows)

       tablename        
------------------------
 ajt_log_importacion
 mopelog1f
 hh_log
 hh_log_import_to_magic
 his_log_history_alert
 logconfalm
 log_cade_queque_mrp
 log_aproaje
 log_cade_queque
 logerrorescadena
 mperhist1f
 tcovta2f_log
 mvsbipplog
 pv_log_error_mx
 qv_costo_log
 scmlogs
 temp_log_rdg
 catalogos_factura_mx
 tclie19log
 mvsbsegcliprolog
 tp_logflow
  tsegclilog
 (22 rows)
 ```
 **Comentario de Hallazgo:**
 El barrido identificó 491 columnas de aprobación distribuidas en ~150 tablas del esquema public, confirmando que el patrón de aprobación multinivel es transversal a todo el sistema (no exclusivo de fórmulas). Solo existen 2 funciones almacenadas relacionadas con aprobación y 22 tablas de log disponibles para auditoría. No hay procedimientos almacenados que calculen aprobación de fórmulas.

 ### SECCIÓN: AUDITORÍA DE DICCIONARIOS TÉCNICOS Y LOGS DE TRANSACCIONALIDAD: 
 Inspeccionar la estructura de las tablas maestras de configuración (`aprfor1f`), el registro histórico de firmas (`taprform1f`) y los logs de aprobación (`log_aproaje`) para garantizar que la persistencia de datos sea coherente con el flujo de Odoo 19.

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
\d aprfor1f
\d taprform1f
\d tmpdetfor
\d forfab
\d csolactfor
\d dsolactfor
\d log_aproaje
SELECT * FROM aprfor1f LIMIT 5;
SELECT * FROM taprform1f LIMIT 5;
SELECT * FROM log_aproaje LIMIT 5;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local" >> ~/TutorialOdoo/data_para_agente/validacion_program_162.md
```
```text
                Table "public.aprfor1f"
   Column   |  Type   | Collation | Nullable | Default 
------------+---------+-----------+----------+---------
 compania   | text    |           |          | 
 transaccio | text    |           |          | 
 nivel      | integer |           |          | 
 tipaprob   | text    |           |          | 
 aprobador  | integer |           |          | 
 estado     | text    |           |          | 
 feccrea    | integer |           |          | 
 horcrea    | text    |           |          | 
 usucrea    | text    |           |          | 
 fecultmod  | integer |           |          | 
 horultimod | text    |           |          | 
 ultusumod  | text    |           |          | 
Indexes:
     "idx_163675_aprfor1l1" UNIQUE, btree (compania, transaccio, nivel, tipaprob, aprobador)
 ```
 **Comentario de Hallazgo:**
 `aprfor1f` define quién puede aprobar por compañía, transacción, nivel y tipo de aprobador. Su índice único confirma que un mismo aprobador puede existir en múltiples niveles para una misma transacción. Las tablas `taprform1f`, `tmpdetfor`, `csolactfor` y `dsolactfor` fueron consultadas en este mismo bloque pero sus resultados se detallan en las secciones siguientes.

 ### SECCIÓN: HISTORIAL DE FIRMAS Y TRAZABILIDAD (taprform1f / tmpdetfor) Objetivo: Identificar quién autorizó, en qué fecha y qué datos temporales se usaron durante el proceso
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && psql -h 100.119.5.108 -U postgres -d mxbdaje_local -c '\d taprform1f' -c 'SELECT * FROM taprform1f LIMIT 5;' -c '\d tmpdetfor' -c 'SELECT * FROM tmpdetfor LIMIT 5;'" >> ~/TutorialOdoo/data_para_agente/validacion_program_162.md
```
```text
                    Table "public.taprform1f"
   Column    |       Type       | Collation | Nullable | Default 
-------------+------------------+-----------+----------+---------
 compania    | text             |           |          | 
 transaccio  | text             |           |          | 
 nrodoc      | text             |           |          | 
 articulo    | double precision |           |          | 
 insumo      | double precision |           |          | 
 sucform     | text             |           |          | 
 lineainsumo | text             |           |          | 
 nivel       | integer          |           |          | 
 empleautor  | integer          |           |          | 
 fecautoriz  | integer          |           |          | 
 horautoriz  | text             |           |          | 
 stsaprobac  | text             |           |          | 
 observac    | text             |           |          | 
 estado      | text             |           |          | 
 feccrea     | integer          |           |          | 
 horcrea     | text             |           |          | 
 usucrea     | text             |           |          | 
 fecultmod   | integer          |           |          | 
 horultimod  | text             |           |          | 
 ultusumod   | text             |           |          | 
Indexes:
    "idx_173721_taprform1l1" UNIQUE, btree (compania, transaccio, nrodoc, articulo, insumo, sucform, nivel)

 compania | transaccio | nrodoc | articulo | insumo | sucform | lineainsumo | nivel | empleautor | fecautoriz | horautoriz | stsaprobac | observac | estado | feccrea | horcrea | usucrea | fecultmod | horultimod | ultusumod 
----------+------------+--------+----------+--------+---------+-------------+-------+------------+------------+------------+------------+----------+--------+---------+---------+---------+-----------+------------+-----------
(0 rows)

                     Table "public.tmpdetfor"
    Column    |       Type       | Collation | Nullable | Default 
--------------+------------------+-----------+----------+---------
 clave        | text             |           |          | 
 compania     | text             |           |          | 
 transaccio   | text             |           |          | 
 nrodoc       | text             |           |          | 
 sucform      | text             |           |          | 
 articulo     | double precision |           |          | 
 insumo       | double precision |           |          | 
 linea        | text             |           |          | 
 factconv     | double precision |           |          | 
 accion       | text             |           |          | 
 nivapro      | smallint         |           |          | 
 flgaprob     | boolean          |           |          | 
 aprobadop    | integer          |           |          | 
 fecaprob     | integer          |           |          | 
 horaprob     | text             |           |          | 
 stssolicitud | text             |           |          | 
 progactfor   | text             |           |          | 
 seleccion    | bytea            |           |          | 
 elimreg      | boolean          |           |          | 
Indexes:
    "idx_177299_tmpdetforl1" UNIQUE, btree (clave, compania, transaccio, nrodoc, sucform, articulo, insumo)
    "idx_177299_tmpdetforl2" btree (clave, seleccion, compania, transaccio, nrodoc, sucform, articulo, insumo)

 clave | compania | transaccio | nrodoc | sucform | articulo | insumo | linea | factconv | accion | nivapro | flgaprob | aprobadop | fecaprob | horaprob | stssolicitud | progactfor | seleccion | elimreg 
-------+----------+------------+--------+---------+----------+--------+-------+----------+--------+---------+----------+-----------+----------+----------+--------------+------------+-----------+---------
 (0 rows)
 ```
 **Comentario de Hallazgo:**
 Ambas tablas están completamente vacías (0 registros). `taprform1f` debería contener el histórico de firmas por nivel de aprobación y `tmpdetfor` los datos temporales del proceso de solicitud. Esto confirma que el flujo multinivel de aprobación de fórmulas nunca se operó en Mexico — la aprobación se ejecuta por una vía directa sin pasar por estas tablas de trámite.

 ### SECCIÓN: MAESTRO DE FÓRMULAS DE FABRICACIÓN (forfab)\n-- Objetivo: Verificar si los cambios aprobados impactan directamente en esta tabla, que es la que usa producción
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && psql -h 100.119.5.108 -U postgres -d mxbdaje_local -c '\d forfab' -c 'SELECT * FROM forfab LIMIT 5;'" >> ~/TutorialOdoo/data_para_agente/validacion_program_162.md
```

```text
                      Table "public.forfab"
    Column    |       Type       | Collation | Nullable | Default 
--------------+------------------+-----------+----------+---------
 compania     | text             |           | not null | 
 sucursal     | text             |           | not null | 
 articulo     | double precision |           | not null | 
 nrosecu      | smallint         |           | not null | 
 material     | double precision |           | not null | 
 porcent      | double precision |           | not null | 
 factconv     | double precision |           | not null | 
 cantidad     | double precision |           | not null | 
 stkdisp      | double precision |           | not null | 
 tipdist      | text             |           | not null | 
 fase         | integer          |           | not null | 
 corrfase     | smallint         |           | not null | 
 feccrea      | integer          |           | not null | 
 horcrea      | text             |           | not null | 
 usucrea      | text             |           | not null | 
 ultfecmod    | integer          |           | not null | 
 ulthormod    | text             |           | not null | 
 ultusumod    | text             |           | not null | 
 lanza        | bytea            |           | not null | 
 tetiqueta    | text             |           |          | 
 aprobadop    | integer          |           |          | 
 fecaprobadop | integer          |           |          | 
 horaprobadop | text             |           |          | 
Indexes:
    "idx_167195_forfab01" UNIQUE, btree (compania, sucursal, articulo, material)
    "idx_167195_forfab02" btree (compania, sucursal, material, articulo)

 compania | sucursal | articulo | nrosecu | material | porcent | factconv  | cantidad  | stkdisp | tipdist | fase | corrfase | feccrea | horcrea | usucrea  | ultfecmod | ulthormod | ultusumod | lanza | tetiqueta | aprobadop | fecaprobadop | horaprobadop 
----------+----------+----------+---------+----------+---------+-----------+-----------+---------+---------+------+----------+---------+---------+----------+-----------+-----------+-----------+-------+-----------+-----------+--------------+--------------
 0030     | 0001     |   524121 |       1 |     7177 |     100 |      18.8 |     59220 |       0 | UA      |    0 |        0 |  739494 | 070149  | MGLUNA   |    739494 | 070149    | MGLUNA    | \x54  |           |   1724308 |            0 | 000000
 0030     | 0068     |   517262 |       1 |        8 |     100 | 0.0892054 | 633.62596 |       0 | UA      |    0 |        0 |  739632 | 100252  | MGLUNA   |    739632 | 100252    | MGLUNA    | \x54  |           |   1724308 |       739632 | 101951
 0030     | 0001     |    81388 |       1 |    71741 |     100 | 0.0001968 |    0.1968 |       0 | UA      |    0 |        0 |  739458 | 110842  | AHRIVERA |    739458 | 110842    | AHRIVERA  | \x54  |           |     29750 |       739458 | 112102
 0030     | 0001     |    58173 |       1 |    47279 |     100 |      0.49 |       490 |       0 | UC      |    0 |        0 |  739447 | 093624  | AHRIVERA |    739447 | 093624    | AHRIVERA  | \x54  |           |     29750 |            0 | 000000
 0030     | 0001     |    68536 |       2 |    47279 |     100 |      0.49 |       490 |       0 | UA      |    2 |        2 |  739052 | 085732  | AHRIVERA |    739052 | 085732    | AHRIVERA  | \x54  |           |     29750 |            0 | 000000
 (5 rows)
 ```
 **Comentario de Hallazgo:**
 `forfab` contiene 70,070 fórmulas activas con IDs de aprobadores reales (ej: 1724308, 29750). Sin embargo, las columnas `fecaprobadop` y `horaprobadop` aparecen vacías o con valores cero en la mayoría de registros, evidenciando una carencia de auditoría temporal en el sistema legacy — se sabe quién aprobó pero no cuándo.

 ### SECCIÓN: SOLICITUDES DE ACTIVACIÓN DE FÓRMULAS (csolactfor / dsolactfor)\n-- Objetivo: Analizar el documento de solicitud (Cabecera/Detalle) que se crea ANTES de que la fórmula sea oficial
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && psql -h 100.119.5.108 -U postgres -d mxbdaje_local -c '\d csolactfor' -c '\d dsolactfor' -c 'SELECT * FROM csolactfor LIMIT 5;'" >> ~/TutorialOdoo/data_para_agente/validacion_program_162.md
```
```text
                 Table "public.csolactfor"
     Column     |  Type   | Collation | Nullable | Default 
----------------+---------+-----------+----------+---------
 compania       | text    |           |          | 
 transaccio     | text    |           |          | 
 nrodoc         | text    |           |          | 
 fecha          | integer |           |          | 
 solicitante    | integer |           |          | 
 qarticulos     | integer |           |          | 
 qacciones      | integer |           |          | 
 flgmailenviado | bytea   |           |          | 
 nivelapr       | integer |           |          | 
 aprobador      | integer |           |          | 
 fecaprobac     | integer |           |          | 
 horaprobac     | text    |           |          | 
 stsaprobac     | text    |           |          | 
 stsactualiza   | text    |           |          | 
 flganulado     | bytea   |           |          | 
 fecanula       | integer |           |          | 
 feccrea        | integer |           |          | 
 horcrea        | text    |           |          | 
 usucrea        | text    |           |          | 
 fecultmod      | integer |           |          | 
 horultmod      | text    |           |          | 
 ultusumod      | text    |           |          | 
Indexes:
    "idx_165818_csolactforl1" UNIQUE, btree (compania, transaccio, nrodoc)

                    Table "public.dsolactfor"
    Column    |       Type       | Collation | Nullable | Default 
--------------+------------------+-----------+----------+---------
 compania     | text             |           |          | 
 transaccio   | text             |           |          | 
 nrodoc       | text             |           |          | 
 sucform      | text             |           |          | 
 articulo     | double precision |           |          | 
 insumo       | double precision |           |          | 
 lineainsumo  | text             |           |          | 
 factconv     | double precision |           |          | 
 accion       | text             |           |          | 
 nivaprob     | integer          |           |          | 
 flgaprob     | bytea            |           |          | 
 aprobadop    | integer          |           |          | 
 fecaprob     | integer          |           |          | 
 horaprob     | text             |           |          | 
 stsaprobac   | text             |           |          | 
 stsactualiza | text             |           |          | 
 feccrea      | integer          |           |          | 
 horcrea      | text             |           |          | 
 usucrea      | text             |           |          | 
 fecultmod    | integer          |           |          | 
 horultmod    | text             |           |          | 
 ultusumod    | text             |           |          | 
Indexes:
    "idx_166686_dsolactforl1" UNIQUE, btree (compania, transaccio, nrodoc, sucform, articulo, insumo)

 compania | transaccio | nrodoc | fecha | solicitante | qarticulos | qacciones | flgmailenviado | nivelapr | aprobador | fecaprobac | horaprobac | stsaprobac | stsactualiza | flganulado | fecanula | feccrea | horcrea | usucrea | fecultmod | horultmod | ultusumod 
----------+------------+--------+-------+-------------+------------+-----------+----------------+----------+-----------+------------+------------+------------+--------------+------------+----------+---------+---------+---------+-----------+-----------+-----------
 (0 rows)
 ```
 **Comentario de Hallazgo:**
 `csolactfor` y `dsolactfor` están vacías (0 registros). Estas tablas deberían contener las solicitudes de activación de fórmulas (cabecera y detalle) antes de que sean oficiales. Su vacio confirma que en Mexico no se usa el flujo de solicitud formal — las fórmulas se crean y aprueban directamente sin pasar por este trámite.

 ### SECCIÓN: BITÁCORA DE AUDITORÍA Y CAMBIOS DE ESTADO (log_aproaje)\n-- Objetivo: Ver el rastro de quién cambió los estados de aprobación y detectar si hay reversiones o rechazos
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && psql -h 100.119.5.108 -U postgres -d mxbdaje_local -c '\d log_aproaje' -c 'SELECT * FROM log_aproaje LIMIT 5;'" >> ~/TutorialOdoo/data_para_agente/validacion_program_162.md
```
```text
                                       Table "public.log_aproaje"
  Column  |            Type             | Collation | Nullable |                 Default                 
----------+-----------------------------+-----------+----------+-----------------------------------------
 id       | bigint                      |           | not null | nextval('log_aproaje_id_seq'::regclass)
 jsonbody | text                        |           |          | 
 idapp    | integer                     |           |          | 
 response | text                        |           |          | 
 fecha    | timestamp without time zone |           |          | 
Indexes:
    "idx_167765_pk__log_apro__3214ec273bf6f9fd" PRIMARY KEY, btree (id)

 id |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           jsonbody                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | idapp |      response       |          fecha          
----+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-------+---------------------+-------------------------
  1 | {"auth":"areli.torres.mx@ajegroup.com","resume":"AJEMEX - 0001 : PLANTA PUEBLA/202506000020","detail": {"title":"AJEMEX - 0001 : PLANTA PUEBLA/202506000020","body": [{"campo":"Compania","valor":"0030 - AJEMEX"},{"campo":"Sucursal","valor":"0001 - PLANTA PUEBLA"},{"campo":"Numero Documento","valor":"202506000020"},{"campo":"Solicitante","valor":"GARCIA MINERO LUISA"},{"campo":"Fecha","valor":"27/06/2025"},{"campo":"Moneda","valor":"PES - PESOS"},{"campo":"Importe","valor":"85000.00"},{"campo":"Glosa","valor":"CANCELACION DE PROV DE GTOS DE IMPORTACION EXP 141 AJEMAYA OC 139549"},{"campo":"PRIMERA APROBACION","valor":"APROBACION"},{"campo":"Aprobador","valor":"TORRES SANCHEZ MARIA SURIARELI"}],"details_title":"DETALLE","details_header": [{"titulo":"Cuenta Contable","width":"80"},{"titulo":"Descripcion","width":"400"},{"titulo":"Dolares","width":"80"},{"titulo":"Debe","width":"80"},{"titulo":"Haber","width":"80"}],"details_rows": [{"cuenta_contable":"4891110101","descripcion":"Otras provisiones","dolares":"4,492.53","debe":"85,000.00","haber":"0.00"},{"cuenta_contable":"2811110201","descripcion":"MERCADERIAS POR RECIBIR-IMPORTADAS","dolares":"-2,148.67","debe":"0.00","haber":"40,653.45"},{"cuenta_contable":"2811110201","descripcion":"MERCADERIAS POR RECIBIR-IMPORTADAS","dolares":"-2,148.67","debe":"0.00","haber":"40,653.45"},{"cuenta_contable":"2081110101","descripcion":"Costo otras mercaderías","dolares":"-195.19","debe":"0.00","haber":"3,693.10"}]},"validity_period": "5","type": "AMA","company":"0030","nemotecnico":"AprobacionAsientoManual","data": [{"llave":"nemotecnico","valor":"AprobacionAsientoManual"},{"llave":"compania","valor":"0030"},{"llave":"sucursal","valor":"0001"},{"llave":"ejercicio","valor":"2025"},{"llave":"periodo","valor":"6"},{"llave":"asiento","valor":"16"},{"llave":"comprobant","valor":"202506000020"},{"llave":"aprobador","valor":"28885"},{"llave":"ordauto","valor":"1"},{"llave":"nivaut","valor":"N2"},{"llave":"solicitante","valor":"624582"},{"llave":"tipaprob","valor":"V"}]}                                                                                                                                                                                                                                                                                | 48516 | {"auth_id":"48516"} | 2025-06-27 14:56:01.757
  2 | {"auth":"yazmin.ramirez.mx@ajegroup.com","resume":"AJEMEX - 0001 : PLANTA PUEBLA/202506000020","detail": {"title":"AJEMEX - 0001 : PLANTA PUEBLA/202506000020","body": [{"campo":"Compania","valor":"0030 - AJEMEX"},{"campo":"Sucursal","valor":"0001 - PLANTA PUEBLA"},{"campo":"Numero Documento","valor":"202506000020"},{"campo":"Solicitante","valor":"GARCIA MINERO LUISA"},{"campo":"Fecha","valor":"27/06/2025"},{"campo":"Moneda","valor":"PES - PESOS"},{"campo":"Importe","valor":"85000.00"},{"campo":"Glosa","valor":"CANCELACION DE PROV DE GTOS DE IMPORTACION EXP 141 AJEMAYA OC 139549"},{"campo":"PRIMERA APROBACION","valor":"APROBACION"},{"campo":"Aprobador","valor":"RAMIREZ QUIROZ YAZMIN GUADALUPE"}],"details_title":"DETALLE","details_header": [{"titulo":"Cuenta Contable","width":"80"},{"titulo":"Descripcion","width":"400"},{"titulo":"Dolares","width":"80"},{"titulo":"Debe","width":"80"},{"titulo":"Haber","width":"80"}],"details_rows": [{"cuenta_contable":"4891110101","descripcion":"Otras provisiones","dolares":"4,492.53","debe":"85,000.00","haber":"0.00"},{"cuenta_contable":"2811110201","descripcion":"MERCADERIAS POR RECIBIR-IMPORTADAS","dolares":"-2,148.67","debe":"0.00","haber":"40,653.45"},{"cuenta_contable":"2811110201","descripcion":"MERCADERIAS POR RECIBIR-IMPORTADAS","dolares":"-2,148.67","debe":"0.00","haber":"40,653.45"},{"cuenta_contable":"2081110101","descripcion":"Costo otras mercaderías","dolares":"-195.19","debe":"0.00","haber":"3,693.10"}]},"validity_period": "5","type": "AMA","company":"0030","nemotecnico":"AprobacionAsientoManual","data": [{"llave":"nemotecnico","valor":"AprobacionAsientoManual"},{"llave":"compania","valor":"0030"},{"llave":"sucursal","valor":"0001"},{"llave":"ejercicio","valor":"2025"},{"llave":"periodo","valor":"6"},{"llave":"asiento","valor":"16"},{"llave":"comprobant","valor":"202506000020"},{"llave":"aprobador","valor":"1212261"},{"llave":"ordauto","valor":"1"},{"llave":"nivaut","valor":"N2"},{"llave":"solicitante","valor":"624582"},{"llave":"tipaprob","valor":"V"}]}                                                                                                                                                                                                                                                                           | 48517 | {"auth_id":"48517"} | 2025-06-27 14:56:02.93
  3 | {"auth":"areli.torres.mx@ajegroup.com","resume":"AJEMEX - 0001 : PLANTA PUEBLA/202506000021","detail": {"title":"AJEMEX - 0001 : PLANTA PUEBLA/202506000021","body": [{"campo":"Compania","valor":"0030 - AJEMEX"},{"campo":"Sucursal","valor":"0001 - PLANTA PUEBLA"},{"campo":"Numero Documento","valor":"202506000021"},{"campo":"Solicitante","valor":"GARCIA MINERO LUISA"},{"campo":"Fecha","valor":"27/06/2025"},{"campo":"Moneda","valor":"PES - PESOS"},{"campo":"Importe","valor":"81306.90"},{"campo":"Glosa","valor":"ADICION GTOS IMPORTACION EXP 141 AJEMAYA OC 139549"},{"campo":"PRIMERA APROBACION","valor":"APROBACION"},{"campo":"Aprobador","valor":"TORRES SANCHEZ MARIA SURIARELI"}],"details_title":"DETALLE","details_header": [{"titulo":"Cuenta Contable","width":"80"},{"titulo":"Descripcion","width":"400"},{"titulo":"Dolares","width":"80"},{"titulo":"Debe","width":"80"},{"titulo":"Haber","width":"80"}],"details_rows": [{"cuenta_contable":"2811110201","descripcion":"MERCADERIAS POR RECIBIR-IMPORTADAS","dolares":"-2,148.67","debe":"0.00","haber":"40,653.45"},{"cuenta_contable":"2811110201","descripcion":"MERCADERIAS POR RECIBIR-IMPORTADAS","dolares":"-2,148.67","debe":"0.00","haber":"40,653.45"},{"cuenta_contable":"2081110101","descripcion":"Costo otras mercaderías","dolares":"4,297.34","debe":"81,306.90","haber":"0.00"}]},"validity_period": "5","type": "AMA","company":"0030","nemotecnico":"AprobacionAsientoManual","data": [{"llave":"nemotecnico","valor":"AprobacionAsientoManual"},{"llave":"compania","valor":"0030"},{"llave":"sucursal","valor":"0001"},{"llave":"ejercicio","valor":"2025"},{"llave":"periodo","valor":"6"},{"llave":"asiento","valor":"16"},{"llave":"comprobant","valor":"202506000021"},{"llave":"aprobador","valor":"28885"},{"llave":"ordauto","valor":"1"},{"llave":"nivaut","valor":"N2"},{"llave":"solicitante","valor":"624582"},{"llave":"tipaprob","valor":"V"}]}                                                                                                                                                                                                                                                                                                                                                                                                                          | 48518 | {"auth_id":"48518"} | 2025-06-27 14:56:03.54
  4 | {"auth":"yazmin.ramirez.mx@ajegroup.com","resume":"AJEMEX - 0001 : PLANTA PUEBLA/202506000021","detail": {"title":"AJEMEX - 0001 : PLANTA PUEBLA/202506000021","body": [{"campo":"Compania","valor":"0030 - AJEMEX"},{"campo":"Sucursal","valor":"0001 - PLANTA PUEBLA"},{"campo":"Numero Documento","valor":"202506000021"},{"campo":"Solicitante","valor":"GARCIA MINERO LUISA"},{"campo":"Fecha","valor":"27/06/2025"},{"campo":"Moneda","valor":"PES - PESOS"},{"campo":"Importe","valor":"81306.90"},{"campo":"Glosa","valor":"ADICION GTOS IMPORTACION EXP 141 AJEMAYA OC 139549"},{"campo":"PRIMERA APROBACION","valor":"APROBACION"},{"campo":"Aprobador","valor":"RAMIREZ QUIROZ YAZMIN GUADALUPE"}],"details_title":"DETALLE","details_header": [{"titulo":"Cuenta Contable","width":"80"},{"titulo":"Descripcion","width":"400"},{"titulo":"Dolares","width":"80"},{"titulo":"Debe","width":"80"},{"titulo":"Haber","width":"80"}],"details_rows": [{"cuenta_contable":"2811110201","descripcion":"MERCADERIAS POR RECIBIR-IMPORTADAS","dolares":"-2,148.67","debe":"0.00","haber":"40,653.45"},{"cuenta_contable":"2811110201","descripcion":"MERCADERIAS POR RECIBIR-IMPORTADAS","dolares":"-2,148.67","debe":"0.00","haber":"40,653.45"},{"cuenta_contable":"2081110101","descripcion":"Costo otras mercaderías","dolares":"4,297.34","debe":"81,306.90","haber":"0.00"}]},"validity_period": "5","type": "AMA","company":"0030","nemotecnico":"AprobacionAsientoManual","data": [{"llave":"nemotecnico","valor":"AprobacionAsientoManual"},{"llave":"compania","valor":"0030"},{"llave":"sucursal","valor":"0001"},{"llave":"ejercicio","valor":"2025"},{"llave":"periodo","valor":"6"},{"llave":"asiento","valor":"16"},{"llave":"comprobant","valor":"202506000021"},{"llave":"aprobador","valor":"1212261"},{"llave":"ordauto","valor":"1"},{"llave":"nivaut","valor":"N2"},{"llave":"solicitante","valor":"624582"},{"llave":"tipaprob","valor":"V"}]}                                                                                                                                                                                                                                                                                                                                                                                                                     | 48519 | {"auth_id":"48519"} | 2025-06-27 14:56:03.947
  5 | {"auth":"areli.torres.mx@ajegroup.com","resume":"AJEMEX - 0001 : PLANTA PUEBLA/202506000021","detail": {"title":"AJEMEX - 0001 : PLANTA PUEBLA/202506000021","body": [{"campo":"Compania","valor":"0030 - AJEMEX"},{"campo":"Sucursal","valor":"0001 - PLANTA PUEBLA"},{"campo":"Numero Documento","valor":"202506000021"},{"campo":"Solicitante","valor":"GARCIA MINERO LUISA"},{"campo":"Fecha","valor":"27/06/2025"},{"campo":"Moneda","valor":"PES - PESOS"},{"campo":"Importe","valor":"162512.40"},{"campo":"Glosa","valor":"ADICION GTOS IMPORTACION EXP 141 AJEMAYA OC 139549"},{"campo":"PRIMERA APROBACION","valor":"APROBACION"},{"campo":"Aprobador","valor":"TORRES SANCHEZ MARIA SURIARELI"}],"details_title":"DETALLE","details_header": [{"titulo":"Cuenta Contable","width":"80"},{"titulo":"Descripcion","width":"400"},{"titulo":"Dolares","width":"80"},{"titulo":"Debe","width":"80"},{"titulo":"Haber","width":"80"}],"details_rows": [{"cuenta_contable":"2811110201","descripcion":"MERCADERIAS POR RECIBIR-IMPORTADAS","dolares":"-2,148.67","debe":"0.00","haber":"40,653.45"},{"cuenta_contable":"2811110201","descripcion":"MERCADERIAS POR RECIBIR-IMPORTADAS","dolares":"-2,148.67","debe":"0.00","haber":"40,653.45"},{"cuenta_contable":"2811110201","descripcion":"MERCADERIAS POR RECIBIR-IMPORTADAS","dolares":"-2,145.99","debe":"0.00","haber":"40,602.75"},{"cuenta_contable":"2811110201","descripcion":"MERCADERIAS POR RECIBIR-IMPORTADAS","dolares":"-2,145.99","debe":"0.00","haber":"40,602.75"},{"cuenta_contable":"2081110101","descripcion":"Costo otras mercaderías","dolares":"4,291.98","debe":"81,205.50","haber":"0.00"},{"cuenta_contable":"2081110101","descripcion":"Costo otras mercaderías","dolares":"4,297.34","debe":"81,306.90","haber":"0.00"}]},"validity_period": "5","type": "AMA","company":"0030","nemotecnico":"AprobacionAsientoManual","data": [{"llave":"nemotecnico","valor":"AprobacionAsientoManual"},{"llave":"compania","valor":"0030"},{"llave":"sucursal","valor":"0001"},{"llave":"ejercicio","valor":"2025"},{"llave":"periodo","valor":"6"},{"llave":"asiento","valor":"16"},{"llave":"comprobant","valor":"202506000021"},{"llave":"aprobador","valor":"28885"},{"llave":"ordauto","valor":"1"},{"llave":"nivaut","valor":"N2"},{"llave":"solicitante","valor":"624582"},{"llave":"tipaprob","valor":"V"}]} | 48623 | {"auth_id":"48623"} | 2025-06-27 15:02:25.71
 (5 rows)
 ```
 **Comentario de Hallazgo:**
 `log_aproaje` contiene registros JSON de auditoría, pero corresponden a aprobaciones de asientos contables manuales (nemotecnico: `AprobacionAsientoManual`, type: `AMA`), no a fórmulas de producción. Cada registro incluye email del aprobador, detalles del documento y campos de validación. Esta tabla es un log genérico del sistema de aprobaciones, no específico del programa#162.

 ### ANÁLISIS TÉCNICO DE REGLAS DE NEGOCIO Y CICLO DE VIDA - PROGRAMA#162 -- Objetivo: Mapear los estados (stsaprobac) para configurar el State Machine de Odoo 19 y diferenciar borradores de aprobados. -- Nota: Se analiza el ID de transacción (transaccio) para garantizar que el flujo de producción no se mezcle con compras u otros módulos. -- Dimensionamiento: Conteo de registros en csolactfor y taprform1f para prever la carga en el Chatter y el historial de firmas.
```bash
# 1. Definimos los queries para extraer el "ADN" del proceso#162
QUERIES_FINALES="
-- Mapeo de estados (stsaprobac): Determina el flujo de vida del documento
SELECT DISTINCT stsaprobac, 'En Solicitudes (csolactfor)' as procedencia FROM csolactfor;
SELECT DISTINCT stsaprobac, 'En Histórico Firmas (taprform1f)' as procedencia FROM taprform1f;

-- Identificación de Transacción: Filtro para aislar Producción de otros módulos
SELECT DISTINCT transaccio, 'ID de proceso en csolactfor' as nota FROM csolactfor;
SELECT DISTINCT tipaprob, 'Tipos de aprobadores en aprfor1f' as nota FROM aprfor1f;

-- Análisis de operación y sincronización de datos temporales
SELECT DISTINCT accion as tipo_operacion, 'Lógica de cambio en tmpdetfor' as contexto FROM tmpdetfor;
SELECT DISTINCT stssolicitud as estado_sincro, 'Estado integración tmpdetfor' as contexto FROM tmpdetfor;

-- Cuantificación de registros: Impacto en migración y Chatter de Odoo
SELECT 'Solicitudes de Activación' as objeto, COUNT(*) as total FROM csolactfor;
SELECT 'Firmas y Logs históricos' as objeto, COUNT(*) as total FROM taprform1f;
SELECT 'Fórmulas finales en producción' as objeto, COUNT(*) as total FROM forfab;"

# 2. Título y descripción con detalles particulares del negocio AJE
echo -e "\n\n### ANÁLISIS TÉCNICO DE REGLAS DE NEGOCIO Y CICLO DE VIDA - PROGRAMA#162" >> ~/TutorialOdoo/data_para_agente/validacion_program_162.md
echo -e "-- Objetivo: Mapear los estados (stsaprobac) para configurar el State Machine de Odoo 19 y diferenciar borradores de aprobados.\n-- Nota: Se analiza el ID de transacción (transaccio) para garantizar que el flujo de producción no se mezcle con compras u otros módulos.\n-- Dimensionamiento: Conteo de registros en csolactfor y taprform1f para prever la carga en el Chatter y el historial de firmas." >> ~/TutorialOdoo/data_para_agente/validacion_program_162.md

# 3. Ejecución segura  
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"$QUERIES_FINALES\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local" >> ~/TutorialOdoo/data_para_agente/validacion_program_162.md
```
```text
 stsaprobac | procedencia 
------------+-------------
(0 rows)

 stsaprobac | procedencia 
------------+-------------
(0 rows)

 transaccio | nota 
------------+------
(0 rows)

 tipaprob | nota 
----------+------
(0 rows)

 tipo_operacion | contexto 
----------------+----------
(0 rows)

 estado_sincro | contexto 
---------------+----------
(0 rows)

          objeto           | total 
---------------------------+-------
 Solicitudes de Activación |     0
(1 row)

          objeto          | total 
--------------------------+-------
 Firmas y Logs históricos |     0
(1 row)

             objeto             | total 
--------------------------------+-------
 Fórmulas finales en producción | 70070
 (1 row)

 ```
 **Comentario de Hallazgo:**
 Todas las consultas de estados, transacciones y tipos de aprobación retornan 0 rows, confirmando que las tablas de trámite (`csolactfor`, `taprform1f`, `tmpdetfor`, `aprfor1f`) no tienen datos operativos para fórmulas de producción. El único dato relevante: `forfab` tiene 70,070 fórmulas finales. No hay estados que mapear para el State Machine de Odoo desde las tablas legacy — los estados (draft → pending → approved) se definirán desde cero.


 ### ACCIÓN: INVESTIGACIÓN DE FIRMAS DIRECTAS EN MAESTRO DE PRODUCCIÓN (forfab) **Contexto:** Debido a que las tablas de trámite están vacías, se valida si la aprobación se registra directamente en el maestro mediante IDs de usuario.
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
-- Identificación de IDs de aprobadores (Tipo Integer)
SELECT DISTINCT aprobadop, 'ID Aprobador detectado' as metadato 
FROM forfab 
WHERE aprobadop IS NOT NULL AND aprobadop > 0 
LIMIT 10;

-- Muestra de trazabilidad con nombre de columna corregido (horaprobadop)
SELECT compania, articulo, material, aprobadop, fecaprobadop, horaprobadop 
FROM forfab 
WHERE aprobadop IS NOT NULL AND aprobadop > 0 
ORDER BY fecaprobadop DESC 
LIMIT 5;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local" >> ~/TutorialOdoo/data_para_agente/validaciones_programs/validacion_program_162.md
```
**Resultado de la investigación de firmas en forfab:**
```text
 aprobadop |        metadato        
-----------+------------------------
   1708248 | ID Aprobador detectado
      6881 | ID Aprobador detectado
   1683322 | ID Aprobador detectado
     29750 | ID Aprobador detectado
   1668443 | ID Aprobador detectado
   1668285 | ID Aprobador detectado
   1657091 | ID Aprobador detectado
     64435 | ID Aprobador detectado
   1779648 | ID Aprobador detectado
   1721708 | ID Aprobador detectado
(10 rows)

 compania | articulo | material | aprobadop | fecaprobadop | horaprobadop 
----------+----------+----------+-----------+--------------+--------------
 0030     |    73145 |    73147 |   1708248 |              | 
 0030     |    73145 |    73148 |   1708248 |              | 
 0030     |    73278 |    20210 |   1708248 |              | 
 0030     |    73145 |    73146 |   1708248 |              | 
 0030     |    73145 |    26198 |   1708248 |              | 
(5 rows)

```
**Comentario de Hallazgo:**
Se confirma que la aprobación se persiste directamente en el maestro de producción `forfab`. Sin embargo, las columnas `fecaprobadop` y `horaprobadop` aparecen vacías en los registros recientes, lo que sugiere que el sistema original podría estar delegando la fecha a otra tabla de logs o que el trigger de actualización no se disparó. Odoo deberá forzar el llenado de estos campos para mantener la integridad.
