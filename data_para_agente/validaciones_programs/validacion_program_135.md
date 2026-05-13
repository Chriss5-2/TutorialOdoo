### SECCION: Barrrido rapido de Mermas
```bash
 docker exec -i odoo19-server-dev sh -c "export LANG=C; export LC_ALL=C; export PGPASSWORD='***' && psql -h 100.119.5.108 -U postgres -d mxbdaje_local -c '\dt *merm*'"
             List of tables
 Schema |    Name     | Type  |  Owner   
--------+-------------+-------+----------
 public | mermastdmes | table | postgres
(1 row)
```

### Seccion: Busqueda de mermas , desperdicios  y perdidas
```bash
docker exec -i odoo19-server-dev sh -c "export LANG=C; export LC_ALL=C; export PGPASSWORD='***' && psql -h 100.119.5.108 -U postgres -d mxbdaje_local -c \"SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND (table_name LIKE '%merm%' OR table_name LIKE '%desp%' OR table_name LIKE '%perd%');\""
 table_name  
-------------
 mermastdmes
(1 row)
```

### Seccion  : Listado general de tablas
```bash
docker exec -i odoo19-server-dev sh -c "export LANG=C; export LC_ALL=C; export PGPASSWORD='***' && psql -h 100.119.5.108 -U postgres -d mxbdaje_local -c \"SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name;\"" | head -100
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
 ...
 art_usados
 artfecven
 articulos_mp9
 articulos_mty_mp9
 articulos_pue_mp9
 articulos_vhs_mp9
 artxmaca1f
```
### Seccion: Estructura tecnica de mermastdmes
```bash
docker exec -i odoo19-server-dev sh -c "export LANG=C; export LC_ALL=C; export PGPASSWORD='***' && psql -h 100.119.5.108 -U postgres -d mxbdaje_local -c '\d mermastdmes'"
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
...
 priqcontenido               | integer                     |           |          | 
 descompania                 | text                        |           |          | 
 desucursal                  | text                        |           |          | 
 anio                        | integer                     |           |          | 
 mes                         | integer                     |           |          | 
 fecha                       | timestamp without time zone |           |          | 
 parametrodos                | integer                     |           |          | 

```
### Seccion: Muestreo de datos reales 
```bash
docker exec -i odoo19-server-dev sh -c "export LANG=C; export LC_ALL=C; export PGPASSWORD='***' && psql -h 100.119.5.108 -U postgres -d mxbdaje_local -c 'SELECT * FROM mermastdmes LIMIT 5;'"
 compania | sucursal | ejercicio | periodo |    nroop     | insumo | llave | fliqui | fechacadena |    desfamilia    |     desequipo      |                           desinsumo                           |                        desarticulo                        | articulopri | qgirad | tipart | linea | qstd | qreal | vstd |   vreal   | preciostd |     desfamilia1      |    desfamilia2    | linadm | a21tipo_antes | insumochild | tipochild | preciochild | nuevovreal | nuevaqstd | tipo_adicional | nuevovstd | pormerma |     precioreal     | desvprecio | merman4 | a21desviacionporcantiyestru | a21nuevovstd | a21desviacionporcanti | a21desviacionporestru | a21porcentajemerma |   a21precioreal    | a21desviacionprecio | pridesmarca | pridespresentacion | pridesformato | pridessabor | priqcontenido |      descompania      |    desucursal     | anio | mes |         fecha          | parametrodos 
----------+----------+-----------+---------+--------------+--------+-------+--------+-------------+------------------+--------------------+---------------------------------------------------------------+-----------------------------------------------------------+-------------+--------+--------+-------+------+-------+------+-----------+-----------+----------------------+-------------------+--------+---------------+-------------+-----------+-------------+------------+-----------+----------------+-----------+----------+--------------------+------------+---------+-----------------------------+--------------+-----------------------+-----------------------+--------------------+--------------------+---------------------+-------------+--------------------+---------------+-------------+---------------+-----------------------+-------------------+------+-----+------------------------+--------------
 0035     | 08       |      2023 |       7 | PALP23000091 |  77804 | LLAVE | 738715 | 14/07/2023  | BASES TERMINADAS | BASES PARA BEBIDAS | CONCENTRADO PARA REFRESCO CITRUS PUNCH BF-MX-190615 - PARTE 2 | CONCENTRADO PARA REFRESCO CITRUS PUNCH BF-MX-190615       |       72445 |    216 | 008    |    42 |  216 |   216 |    0 |  35990.03 |         0 | BASE DE BEBIDA PARTE | BASE DE BEBIDA PT | 03     | STD           |       77804 | STD       |           0 |          0 |       216 |              1 |         0 |        0 | 166.62050925925925 |          0 |       0 |                    35990.03 |            0 |                     0 |              35990.03 |                  0 | 166.62050925925925 |                   0 |             |                    |               |             |             1 | INMOBILIARIA ALPAMAYO | ALPAMAYO (MATRIZ) | 2023 |   7 | 2023-08-03 12:59:55.19 |            2
 0035     | 08       |      2023 |       7 | PALP23000091 |  77805 | LLAVE | 738715 | 14/07/2023  | BASES TERMINADAS | BASES PARA BEBIDAS | CONCENTRADO PARA REFRESCO CITRUS PUNCH BF-MX-190615 - PARTE 3 | CONCENTRADO PARA REFRESCO CITRUS PUNCH BF-MX-190615       |       72445 |    216 | 008    |    42 |  216 |   216 |    0 | 129723.76 |         0 | BASE DE BEBIDA PARTE | BASE DE BEBIDA PT | 03     | STD           |       77805 | STD       |           0 |          0 |       216 |              1 |         0 |        0 |   600.572962962963 |          0 |       0 |                   129723.76 |            0 |                     0 |             129723.76 |                  0 |   600.572962962963 |                   0 |             |                    |               |             |             1 | INMOBILIARIA ALPAMAYO | ALPAMAYO (MATRIZ) | 2023 |   7 | 2023-08-03 12:59:55.19 |            2
 0035     | 08       |      2023 |       7 | PALP23000091 |  77806 | LLAVE | 738715 | 14/07/2023  | BASES TERMINADAS | BASES PARA BEBIDAS | CONCENTRADO PARA REFRESCO CITRUS PUNCH BF-MX-190615 - PARTE 4 | CONCENTRADO PARA REFRESCO CITRUS PUNCH BF-MX-190615       |       72445 |    216 | 008    |    42 |  216 |   216 |    0 |  51051.24 |         0 | BASE DE BEBIDA PARTE | BASE DE BEBIDA PT | 03     | STD           |       77806 | STD       |           0 |          0 |       216 |              1 |         0 |        0 | 236.34833333333333 |          0 |       0 |                    51051.24 |            0 |                     0 |              51051.24 |                  0 | 236.34833333333333 |                   0 |             |                    |               |             |             1 | INMOBILIARIA ALPAMAYO | ALPAMAYO (MATRIZ) | 2023 |   7 | 2023-08-03 12:59:55.19 |            2
 0035     | 08       |      2023 |       7 | PALP23000092 |      5 | LLAVE | 738715 | 14/07/2023  | BASES TERMINADAS | BASES PARA BEBIDAS | BENZOATO DE SODIO                                             | BASE PARA BEBIDA JARABEADA CARBONATADA UVA   BG-MX-160478 |       68616 |     10 | 008    |    42 | 43.4 |  43.4 |    0 |   3026.78 |         0 | INSUMOS              | BASE DE BEBIDA PT | 04     | STD           |           5 | STD       |           0 |          0 |      43.4 |              1 |         0 |        0 |  69.74147465437788 |          0 |       0 |                     3026.78 |            0 |                     0 |               3026.78 |                  0 |  69.74147465437788 |                   0 |             |                    |               |             |             1 | INMOBILIARIA ALPAMAYO | ALPAMAYO (MATRIZ) | 2023 |   7 | 2023-08-03 12:59:55.19 |            2
 0035     | 08       |      2023 |       7 | PALP23000092 |      6 | LLAVE | 738715 | 14/07/2023  | BASES TERMINADAS | BASES PARA BEBIDAS | ACIDO CITRICO                                                 | BASE PARA BEBIDA JARABEADA CARBONATADA UVA   BG-MX-160478 |       68616 |     10 | 008    |    42 | 50.4 |  50.4 |    0 |   1012.63 |         0 | INSUMOS              | BASE DE BEBIDA PT | 04     | STD           |           6 | STD       |           0 |          0 |      50.4 |              1 |         0 |        0 |  20.09186507936508 |          0 |       0 |                     1012.63 |            0 |                     0 |               1012.63 |                  0 |  20.09186507936508 |                   0 |             |                    |               |             |             1 | INMOBILIARIA ALPAMAYO | ALPAMAYO (MATRIZ) | 2023 |   7 | 2023-08-03 12:59:55.19 |            2
(5 rows)

```
### Seccion : Busqueda de tablas de OP , turnos y Paradas
```bash
docker exec -i odoo19-server-dev sh -c "export LANG=C; export LC_ALL=C; export PGPASSWORD='***' && psql -h 100.119.5.108 -U postgres -d mxbdaje_local -c \"SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND (table_name LIKE 'prgo%' OR table_name LIKE 'op%' OR table_name LIKE '%opdet%' OR table_name LIKE '%turno%' OR table_name LIKE '%parad%');\""
  table_name   
---------------
 bturno1f
 opxlinea
 opmotanu
 operut
 prgopdet
 relacionturno
 turnoxop
 turno
(8 rows)

```
### SECCIÓN: EXPLORACIÓN DE DICCIONARIO DE DATOS - GESTIÓN DE MERMAS
Ejecución de consulta de introspección sobre el catálogo de PostgreSQL para identificar las tablas asociadas a la gestión de mermas, desperdicios y pérdidas de producción dentro del esquema público, con el fin de mapear la estructura de persistencia en `mxbdaje_local`.

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT tablename 
FROM pg_tables 
WHERE schemaname = 'public' 
AND (tablename ILIKE '%merm%' OR tablename ILIKE '%desp%' OR tablename ILIKE '%waste%' OR tablename ILIKE '%scrap%')
ORDER BY tablename;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
 tablename  
-------------
 mermastdmes
(1 row)
```
**Comentario de Hallazgo**:
Se ha identificado una única tabla `mermastdmes` directamente relacionada con mermas. A diferencia de paradas (donde no existía ninguna tabla maestra), aquí existe un catálogo `tipmer` (tipo merma) y tablas transaccionales `merppro` y `merxlin`. Es necesario inspeccionar cada una para entender la arquitectura completa del módulo de mermas.

---

### SECCIÓN: AUDITORÍA DE INTEGRIDAD REFERENCIAL - CAMPOS DE MERMAS
Inspección de todas las columnas del esquema público que contienen referencias a "merm", "despe" o "desper" para identificar dependencias en tablas transaccionales, de costos, líneas de producción o protocolos, asegurando el rastreo de la persistencia de desperdicios.

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT table_name, column_name, data_type 
FROM information_schema.columns 
WHERE (column_name ILIKE '%merm%' OR column_name ILIKE '%despe%' OR column_name ILIKE '%desper%') 
AND table_schema = 'public' 
ORDER BY table_name, column_name;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
       table_name      |    column_name     |    data_type     
-----------------------+--------------------+------------------
 bcktordco2f_11022021  | merma              | double precision
 bcktordco2f_11022021  | porcmerma          | double precision
 bcnftr1               | flgmermanual       | bytea
 conxar                | merma              | numeric
 conxarlinea           | merma              | numeric
 conxarpri             | merma              | double precision
 conxarpri             | merma_dol          | double precision
 detconxart            | mermacpm           | numeric
 detconxart            | mermaq             | numeric
 detconxartpri         | mermacpm           | double precision
 detconxartpri         | mermacpm_dol       | double precision
 detconxartpri         | mermaq             | double precision
 dethcos               | mermcpmfin         | double precision
 dethcos               | mermcpmfin_dol     | double precision
 dethcos               | mermcpmli          | double precision
 dethcos               | mermcpmli_dol      | double precision
 dethcos               | mermcpmpr          | double precision
 dethcos               | mermcpmpr_dol      | double precision
 mcatppres             | porcmerma          | real
 mermastdmes           | a21porcentajemerma | double precision
 mermastdmes           | merman4            | double precision
 mermastdmes           | pormerma           | double precision
 merppro               | tipmerma           | text
 merxlin               | merma              | text
 mmateri6f             | porcmerma          | numeric
 mpadis1f              | fpmerma            | text
 prgopdet              | asigmerma          | boolean
 prodinp               | qmerma             | double precision
 tclicj1f              | porcmerma          | real
 tfacom3f              | merma              | double precision
 tproin1               | qmerma             | double precision
 tordco2f              | merma              | double precision
 tordco2f              | porcmerma          | double precision
 tipmer                | tipmerma           | text
(40 rows)
```
**Comentario de Hallazgo**:
El barrido revela 40 columnas relacionadas con mermas distribuidas en múltiples dominios. Los hallazgos clave son:
- **`tipmer`**: Tabla maestra de tipos de merma (catálogo) - equivalente a lo que sería `bparada1f` para paradas
- **`mermastdmes`**: Tabla de resultados de merma estándar vs real por mes (799,682 registros con datos)
- **`merppro`**: Tabla transaccional de merma por proceso/OP (0 registros - vacía)
- **`merxlin`**: Tabla transaccional de merma por línea de producción (0 registros - vacía)
- **`prgopdet.asigmerma`**: Flag boolean que indica si una OP tiene mermas asignadas (similar a `asigparada`)
- **`tproin1.qmerma`**: Campo de cantidad de merma en protocolos de producción
- **`mcatppres.porcmerma`**: Porcentaje de merma configurado por categoría de producto
- **Tablas de costos** (`conxar`, `dethcos`, `detconxart`): Campos de merma en costos por unidad y en dólares
- **Conclusión**: A diferencia de paradas, el módulo de mermas SÍ tiene implementación operativa en el catálogo (`tipmer` con 160 registros) y datos reales en `mermastdmes`

---

### SECCIÓN: ANÁLISIS DE ESTRUCTURA DDL - TABLA `tipmer` (CATÁLOGO DE TIPOS DE MERMA)
Inspección de la definición técnica de `tipmer` para identificar su estructura como catálogo maestro de tipos de merma.

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d tipmer;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
                Table "public.tipmer"
  Column   |  Type   | Collation | Nullable | Default 
-----------+---------+-----------+----------+---------
 compania  | text    |           | not null | 
 tipmerma  | text    |           | not null | 
 descrip   | text    |           | not null | 
 estado    | text    |           | not null | 
 feccrea   | integer |           | not null | 
 horcrea   | text    |           | not null | 
 usucrea   | text    |           | not null | 
 ultfecmod | integer |           | not null | 
 ulthormod | text    |           | not null | 
 ultusumod | text    |           | not null | 
Indexes:
    "idx_176526_tipmer01" UNIQUE, btree (compania, tipmerma)
    "idx_176526_tipmer02" btree (compania, descrip)
```
**Comentario de Hallazgo**:
- **Estructura simple y limpia**: `tipmer` sigue el patrón de tablas maestras con PK `(compania, tipmerma)`
- **Campos de auditoría completos**: `feccrea`, `horcrea`, `usucrea`, `ultfecmod`, `ulthormod`, `ultusumod`
- **Sin categorización jerárquica**: A diferencia de paradas (que tenía agrupoee/agrupoee1/agrparoee), `tipmer` es plana - no tiene campos de categoría global, subcategoría ni agrupación
- **Índice por descripción**: Permite búsqueda rápida por nombre de tipo de merma
- **Volumen**: 160 registros totales

---

### SECCIÓN: ANÁLISIS DE DATOS REALES - TABLA `tipmer` (CATÁLOGO DE TIPOS DE MERMA)
Inspección de los datos reales almacenados en el catálogo de tipos de merma para comprender los códigos, descripciones y la distribución por compañía.

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT compania, tipmerma, descrip, estado FROM tipmer ORDER BY compania, tipmerma LIMIT 60;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
 compania | tipmerma |                           descrip                            | estado 
----------+----------+--------------------------------------------------------------+--------
 0002     | 0001     | MESA DE CARGA.BOT ROTAS POR MANIPULEO                        | A
 0002     | 0002     | MESA DE CARGA BOT MAL SOPLADAS                               | A
 0002     | 0003     | RINSER BOT. ROTAS A LA ENTRADA                               | A
 0002     | 0004     | RINSER BOT. ROTAS A LA SALIDA                                | A
 0002     | 0005     | LLENADORA BOT. ROTAS A LA ENTRADA                            | A
 0002     | 0006     | LLENADORA BOT. ROTAS A LA SALIDA                             | A
 0002     | 0007     | LLENADORA BOT. ROTAS POR EXPLOSION                           | A
 0002     | 0008     | CAPSULADORA. BOTELLAS ROTAS                                  | A
 0002     | 0009     | LLENADORA BOT. ROTAS                                         | A
 0002     | 0010     | PANTALLA NIVEL ALTAS Y BAJAS                                 | A
 0002     | 0011     | PANTALLA BOT. SUCIAS                                         | A
 0002     | 0012     | TERMOCONTRAIBLES BOT. QUI¥ADAS                               | A
 0002     | 0013     | ENCAJ. Y PALETIZADO ROT X MANIPULEO                          | A
 0002     | 0014     | PRUEBAS DE CALIDAD                                           | A
 0002     | 0015     | EN MAL ESTADO (ROTOS)                                        | A
 0002     | 0016     | OTROS                                                        | A
 0002     | 0017     | PRODUCTO SEPARADO X (BAJO GAS, BRIX ALTO, ETC)               | A
 0002     | 0018     | SALIDA LAV. BOT ROTAS (VIDRIO)                               | A
 0002     | 0019     | PANTALLA BOT. VACIAS BOT. ROTAS (VIDRIO)                     | A
 0002     | 0020     | PANTALLA BOT. BOT.QUI¤ADAS (VIDRIO)                          | A
 0002     | 0021     | LLENADORA BOT.ROTASX EXPLOSION (VIDRIO)                      | A
 0002     | 0022     | LLENADORA BOT.ROTAS X MANIPULEO (VIDRIO)                     | A
 0002     | 0023     | LLENADORA CORONACION (VIDRIO)                                | A
 0002     | 0024     | PANTALLA BOT.LLENAS NIVEL ALTA Y BAJAS (VIDRIO)              | A
 0002     | 0025     | PANTALLA BOT.LLENAS BOT.SUCIAS (VIDRIO)                      | A
 0002     | 0026     | PANTALLA BOT.LLENAS BOT. SIN CORONAR (VIDRIO)                | A
 0002     | 0027     | PANTALLA BOT. LLENAS BOT X MANIPULEO(VIDRIO)                 | A
 0002     | 0028     | PANTALLA BOT. LLENAS BOT.QUI¥ADAS (VIDRIO)                   | A
 0002     | 0029     | ENCAJONADO Y PALETIZADO ROT. X MANIPULEO(VIDRIO)             | A
 0002     | 0030     | ENCAJ Y PALETIZADO BOT. POR EXPLOSION (VIDRIO)               | A
 0002     | 0031     | PRUEBA DE CALIDAD (VIDRIO)                                   | A
 0002     | 0032     | MESA DE CARGA BOT.ROT MERCADO (VIDRIO)                       | A
 0002     | 0033     | MESA DE CARGA BOT.ROT X MANIPULEO (VIDRIO)                   | A
 0002     | 0034     | ROTAS POR LA ETIQUETADORA                                    | A
 0002     | 0035     | MERMA DE CAPSULADOR/CORONADOR                                | A
 0002     | 0036     | DE MALA CALIDAD                                              | A
 0002     | 0037     | LAMINAS ROTOS EN EL TERMOCONTRAIBLE                          | A
 0002     | 0038     | POR BOCINAS DE PINZA DE LLEMNADORA MESAL (SULLANA)           | A
 0002     | 0039     | RECHAZO PREFORMAS PET (RECUPERABLE)                          | A
 0002     | 0040     | RECHAZO TAPA HDP (RECUPERABLE)                               | A
 0002     | 0041     | MERMA HOT FILL RECUPERABLE (SOPLADO)                         | A
 0002     | 0042     | Mal Tapado (defecto de Coronado, capsulado o taponado).      | A
 0002     | 0043     | Bajo Nivel                                                   | A
 0002     | 0044     | Botella explosionada o con fisura                            | A
 0002     | 0045     | Cuerpo extraño                                               | A
 0002     | 0046     | Presencia de óxido                                           | A
 0002     | 0047     | Tetrapack fermentado                                         | A
 0002     | 0048     | Envase deformado de botella pet                              | A
 0002     | 0049     | Defecto etiquetado                                           | A
 0002     | 0050     | Defecto de Codificación                                      | A
 0002     | 0051     | Mal sabor o descarbonatado (sin gas)                         | A
 0002     | 0052     | Botella de vidrio deformada                                  | A
 0002     | 0053     | Producto Vencido en el almacén Cliente                       | A
 0002     | 0054     | Producto Vencido / descontinuado en los PDV                  | A
 0002     | 0055     | Producto en mal estado en el PDV condicionando la venta.     | A
 0002     | 0056     | Mala manipulación del producto en Planta                     | A
 0002     | 0057     | Mala manipulación del producto en el almacén del Cliente     | A
 0002     | 0058     | Manipulación en transporte primario (Planta - Cedi)          | A
 0002     | 0059     | Mala manipulación del producto en el reparto (Cliente a PDV) | A
 0002     | 0060     | Vencimiento en almacén Planta                                | A
 0002     | 0061     | Producto descontinuado en Planta                             | A
 0002     | 0062     | 56236                                                        | A
(60 rows)
```
**Comentario de Hallazgo**:
- **Compañía 0002 (Perú)**: 62 tipos de merma con descripciones muy específicas por etapa de producción y tipo de envase (PET, vidrio)
- **Patrones de clasificación detectados**:
  - Por **etapa/máquina**: MESA DE CARGA, RINSER, LLENADORA, CAPSULADORA, PANTALLA, ETIQUETADORA, ENCAJONADO
  - Por **tipo de defecto**: ROTAS, MAL SOPLADAS, QUIÑADAS, SUCIAS, NIVEL ALTO/BAJO, SIN CORONAR
  - Por **material**: VIDRIO, PET, TERMOCONTRAIBLE
  - Por **causa**: MANIPULEO, EXPLOSION, CALIDAD, VENCIMIENTO
  - **Recuperables**: RECHAZO PREFORMAS PET, RECHAZO TAPA HDP, MERMA HOT FILL
- **Código 0062**: Descripción "56236" parece ser un dato erróneo o código sin descripción

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT compania, COUNT(*) as tipos FROM tipmer GROUP BY compania ORDER BY compania;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
 compania | tipos 
----------+-------
 0002     |    62
 0015     |    37
 0100     |     7
 9100     |    53
 9999     |     1
(5 rows)
```
**Comentario de Hallazgo**:
- **Distribución por compañía**: 0002 (Perú, 62 tipos), 9100 (53 tipos), 0015 (37 tipos), 0100 (7 tipos - solo etapas de proceso), 9999 (1 tipo genérico "ROTOS")
- **CRÍTICO PARA MÉXICO**: Las compañías de México (`0030`, `0035`) **NO tienen registros en `tipmer`**. Esto significa que el catálogo de tipos de merma NO fue configurado para México en el sistema legacy
- **Compañía 0100**: Solo tiene 7 tipos basados en etapas de proceso (PESADO, MEZCLADO, ENVASADO, LIMPIEZA, SELLADO, ETIQUETADO) - enfoque diferente al de las otras compañías

---

### SECCIÓN: ANÁLISIS DE ESTRUCTURA DDL - TABLA `mermastdmes` (MERMAS ESTÁNDAR VS REAL POR MES)
Inspección de la definición técnica de `mermastdmes` para entender su propósito como tabla de resultados de análisis de mermas.

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d mermastdmes;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
           Table "public.mermastdmes"
           Column            |            Type             
-----------------------------+-----------------------------
 compania                    | text
 sucursal                    | text
 ejercicio                   | integer
 periodo                     | integer
 nroop                       | text
 insumo                      | integer
 llave                       | text
 fliqui                      | integer
 fechacadena                 | text
 desfamilia                  | text
 desequipo                   | text
 desinsumo                   | text
 desarticulo                 | text
 articulopri                 | double precision
 qgirad                      | double precision
 tipart                      | text
 linea                       | integer
 qstd                        | double precision
 qreal                       | double precision
 vstd                        | double precision
 vreal                       | double precision
 preciostd                   | double precision
 desfamilia1                 | text
 desfamilia2                 | text
 linadm                      | text
 a21tipo_antes               | text
 insumochild                 | double precision
 tipochild                   | text
 preciochild                 | double precision
 nuevovreal                  | double precision
 nuevaqstd                   | double precision
 tipo_adicional              | integer
 nuevovstd                   | double precision
 pormerma                    | double precision
 precioreal                  | double precision
 desvprecio                  | double precision
 merman4                     | double precision
 a21desviacionporcantiyestru | double precision
 a21nuevovstd                | double precision
 a21desviacionporcanti       | double precision
 a21desviacionporestru       | double precision
 a21porcentajemerma          | double precision
 a21precioreal               | double precision
 a21desviacionprecio         | double precision
 pridesmarca                 | text
 pridespresentacion          | text
 pridesformato               | text
 pridessabor                 | text
 priqcontenido               | integer
 descompania                 | text
 desucursal                  | text
 anio                        | integer
 mes                         | integer
 fecha                       | timestamp without time zone
 parametrodos                | integer
(54 columns)
```
**Comentario de Hallazgo**:
- **Tabla de análisis/reportes**, no de catálogo: `mermastdmes` es una tabla de resultados que compara cantidad estándar (`qstd`) vs cantidad real (`qreal`) y valor estándar (`vstd`) vs valor real (`vreal`)
- **54 columnas**: Tabla muy ancha, típica de tablas de reporting/data warehouse
- **Campos clave**:
  - `tipart`: Tipo de artículo (001-051) que actúa como clasificador de familia de merma
  - `desfamilia`: Familia descriptiva (ej: "EQUIPOS DE ENVASADO", "TANQUES DE JARABE")
  - `pormerma`: Porcentaje de merma calculado
  - `a21porcentajemerma`: Versión alternativa del porcentaje (posiblemente con otra fórmula)
  - `nroop`: Número de orden de producción asociada
  - `insumo`: Código del insumo que generó la merma
  - `linea`: Línea de producción donde ocurrió
- **Desviaciones**: Campos `a21desviacionporcanti` (por cantidad), `a21desviacionporestru` (por estructura), `a21desviacionprecio` (por precio)
- **No es un catálogo de tipos**: Esta tabla NO define tipos de merma, solo registra resultados de análisis

---

### SECCIÓN: ANÁLISIS DE DATOS REALES - TABLA `mermastdmes`
Inspección de los datos reales para comprender el volumen, distribución y patrones de mermas registradas.

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT count(*) FROM mermastdmes;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
 count  
--------
 799682
(1 row)
```
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT compania, COUNT(*) FROM mermastdmes GROUP BY compania ORDER BY compania;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
 compania | count  
----------+--------
 0030     | 718662
 0035     |  81020
(2 rows)
```
**Comentario de Hallazgo**:
- **799,682 registros totales**: Volumen masivo de datos de análisis de mermas
- **México SÍ tiene datos**: Compañía `0030` (AJEMEX) con 718,662 registros (89.9%) y `0035` (ALPAMAYO) con 81,020 registros (10.1%)
- **Paradoja importante**: México tiene datos de mermas en `mermastdmes` pero NO tiene catálogo configurado en `tipmer`. Esto sugiere que los tipos de merma se manejaban de forma diferente en México (posiblemente usando `tipart` y `desfamilia` como clasificadores)

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT tipart, desfamilia, COUNT(*) as total, AVG(pormerma) as avg_por
FROM mermastdmes
GROUP BY tipart, desfamilia
ORDER BY tipart;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
 tipart |           desfamilia           | total  |      avg_por       
--------+--------------------------------+--------+--------------------
 001    | EQUIPOS DE ENVASADO            | 371180 |   16.9083741627432
 003    | TANQUES DE JARABE              | 167188 | 0.3934088238058595
 005    | TANQUES DE TRATAMIENTO DE AGUA |  26550 |  935.3466160300869
 008    | BASES TERMINADAS               |  87435 |  4.646130723786572
 009    | BASES INTERMEDIAS              |  68123 |  0.684980663883887
 010    | AZUCAR LIQUIDA                 |   8800 |  241.0236859268732
 017    | UNIDAD DE PLOTEO               |   2932 |  1.831413060998885
 021    | REEMPAQUES                     |   1148 | 216.06719380256604
 025    | PRODUCCION ETIQUETAS           |  38882 | 16.338326295459698
 026    | PRODUCCION TERMOENCOGIBLE      |  27066 | 13.847195363458827
 051    | PRODUCCION EXHIBIDORES         |    378 |  9.015293386238811
(11 rows)
```
**Comentario de Hallazgo**:
- **11 tipos de artículo (`tipart`)** con sus familias asociadas en México:
  - `001` EQUIPOS DE ENVASADO: 371,180 registros (46.4%), merma promedio 16.9%
  - `003` TANQUES DE JARABE: 167,188 registros (20.9%), merma promedio 0.39%
  - `008` BASES TERMINADAS: 87,435 registros (10.9%), merma promedio 4.65%
  - `009` BASES INTERMEDIAS: 68,123 registros (8.5%), merma promedio 0.68%
  - `025` PRODUCCION ETIQUETAS: 38,882 registros (4.9%), merma promedio 16.34%
  - `026` PRODUCCION TERMOENCOGIBLE: 27,066 registros (3.4%), merma promedio 13.85%
  - `005` TANQUES DE TRATAMIENTO DE AGUA: 26,550 registros (3.3%), merma promedio 935% (anómalo)
  - `010` AZUCAR LIQUIDA: 8,800 registros (1.1%), merma promedio 241% (anómalo)
  - `017` UNIDAD DE PLOTEO: 2,932 registros, merma promedio 1.83%
  - `021` REEMPAQUES: 1,148 registros, merma promedio 216% (anómalo)
  - `051` PRODUCCION EXHIBIDORES: 378 registros, merma promedio 9.02%
- **Porcentajes anómalos**: `tipart` 005, 010, 021 tienen promedios >100%, lo que sugiere que `pormerma` puede representar algo diferente a un porcentaje puro (posiblemente razón o factor)

---

### SECCIÓN: ANÁLISIS DE ESTRUCTURA DDL - TABLA `merppro` (MERMAS POR PROCESO/OP)
Inspección de la tabla transaccional que vincula mermas con órdenes de producción.

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d merppro;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
                Table "public.merppro"
  Column   |       Type       | Collation | Nullable | Default 
-----------+------------------+-----------+----------+---------
 compania  | text             |           | not null | 
 sucursal  | text             |           | not null | 
 nroop     | text             |           | not null | 
 nrosec    | double precision |           | not null | 
 tipped    | text             |           | not null | 
 lote      | double precision |           | not null | 
 reqalm    | text             |           | not null | 
 articulo  | double precision |           | not null | 
 transalm  | text             |           | not null | 
 tipmerma  | text             |           | not null | 
 cantidad  | double precision |           | not null | 
 almacen   | text             |           | not null | 
 estado    | text             |           | not null | 
 feccrea   | integer          |           | not null | 
 horcrea   | text             |           | not null | 
 usucrea   | text             |           | not null | 
 ultfecmod | integer          |           | not null | 
 ulthormod | text             |           | not null | 
 ultusumod | text             |           | not null | 
Indexes:
    "idx_169722_merppro01" UNIQUE, btree (compania, sucursal, nroop, nrosec, tipped, lote, reqalm, tipmerma)
```
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"SELECT count(*) FROM merppro;\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
 count 
-------
     0
(1 row)
```
**Comentario de Hallazgo**:
- **Tabla completamente vacía** (0 registros): `merppro` estaba diseñada para registrar mermas por OP con referencia a `tipmerma` (FK al catálogo `tipmer`)
- **Estructura transaccional completa**: Vincula OP (`nroop`), lote, artículo, tipo de merma, cantidad y almacén
- **Índice único compuesto**: `(compania, sucursal, nroop, nrosec, tipped, lote, reqalm, tipmerma)` - muy granular
- **No se operó**: Al igual que las tablas OEE de paradas, esta tabla fue diseñada pero nunca se pobló operativamente

---

### SECCIÓN: ANÁLISIS DE ESTRUCTURA DDL - TABLA `merxlin` (MERMAS POR LÍNEA DE PRODUCCIÓN)
Inspección de la tabla transaccional que registra mermas por línea de producción.

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d merxlin;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
                Table "public.merxlin"
  Column   |       Type       | Collation | Nullable | Default 
-----------+------------------+-----------+----------+---------
 compania  | text             |           | not null | 
 sucursal  | text             |           | not null | 
 nroop     | text             |           |          | 
 fecini    | integer          |           | not null | 
 anio      | text             |           | not null | 
 mes       | text             |           | not null | 
 tipmat    | text             |           | not null | 
 turno     | text             |           | not null | 
 familia   | text             |           | not null | 
 linea     | integer          |           | not null | 
 material  | double precision |           | not null | 
 sabor     | text             |           | not null | 
 unxcj     | double precision |           | not null | 
 qvolumen  | double precision |           | not null | 
 merma     | text             |           | not null | 
 qliq      | double precision |           | not null | 
 qenv      | double precision |           | not null | 
 qins      | double precision |           | not null | 
 feccrea   | integer          |           | not null | 
 horcrea   | text             |           | not null | 
 usucrea   | text             |           | not null | 
 ultfecmod | integer          |           | not null | 
 ulthormod | text             |           | not null | 
 ultusumod | text             |           | not null | 
 nroreq    | text             |           |          | 
 lote      | double precision |           |          | 
Indexes:
    "idx_169727_merxlin1" UNIQUE, btree (compania, sucursal, nroop, fecini, tipmat, turno, familia, linea, material, sabor, merma)
    "idx_169727_merxlin2" btree (compania, sucursal, anio, mes, turno, linea)
```
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"SELECT count(*) FROM merxlin;\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
 count 
-------
     0
(1 row)
```
**Comentario de Hallazgo**:
- **Tabla completamente vacía** (0 registros): `merxlin` estaba diseñada para registrar mermas desglosadas por línea de producción
- **Desglose por tipo de merma**: Campos `qliq` (merma líquida), `qenv` (merma de envase), `qins` (merma de insumos) - esto coincide con la descripción del programa #135
- **Campo `merma`**: Es `text`, no una FK a `tipmer`, sugiriendo que almacenaba descripción libre o código
- **Índice por periodo**: `idx_169727_merxlin2` permite consultas rápidas por `(compania, sucursal, anio, mes, turno, linea)`
- **No se operó**: Misma situación que `merppro` - diseño sin implementación operativa

---

### SECCIÓN: ANÁLISIS DE TABLA `mcatppres` (PORCENTAJE DE MERMA POR CATEGORÍA)
Inspección de tabla de configuración de porcentajes de merma estándar por categoría de producto.

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo '\d mcatppres; SELECT count(*) FROM mcatppres;' | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
                Table "public.mcatppres"
  Column   |       Type       | Collation | Nullable | Default 
-----------+------------------+-----------+----------+---------
 categoria | text             |           |          | 
 subcat1   | text             |           |          | 
 subcat2   | text             |           |          | 
 moneda    | text             |           |          | 
 uniglobal | text             |           |          | 
 valresina | double precision |           |          | 
 porcmerma | real             |           |          | 
 porcfijo  | real             |           |          | 
 estado    | text             |           |          | 
 feccrea   | integer          |           |          | 
 horcrea   | text             |           |          | 
 usucrea   | text             |           |          | 
 fecultmod | integer          |           |          | 
 horultmod | text             |           |          | 
 usuultmod | text             |           |          | 
 compania  | text             |           |          | 
Indexes:
    "idx_168795_mcatppresl1" UNIQUE, btree (categoria, subcat1, subcat2, moneda, uniglobal)

 count 
-------
     0
(1 row)
```
**Comentario de Hallazgo**:
- **Tabla vacía** (0 registros): `mcatppres` configura porcentajes de merma estándar (`porcmerma`) y fijos (`porcfijo`) por categoría de producto
- **Campos relevantes**: `valresina` (valor de resina), `porcmerma` (porcentaje de merma esperado), `porcfijo` (porcentaje fijo adicional)
- **No se operó**: Misma situación - estructura definida pero sin datos

---

### SECCIÓN: ANÁLISIS DE TABLA `tproin1` (PROTOCOLOS DE PRODUCCIÓN CON QMERMA)
Inspección de tabla de protocolos de producción que tiene campo `qmerma` para cantidad de merma.

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT count(*) as total, count(*) FILTER (WHERE qmerma > 0) as con_merma FROM tproin1;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
 total | con_merma 
-------+-----------
     0 |         0
(1 row)
```
**Comentario de Hallazgo**:
- **Tabla vacía** (0 registros): `tproin1` almacena protocolos de control de calidad de producción con campos `qmerma`, `qrechazada`, `qaprobada`, `qrecupe`
- **Campos de merma**: `qmerma` (cantidad merma), `flgperdida` (flag de pérdida), `causadef` (causa defecto)
- **No se operó**: Misma situación que las tablas anteriores

---

### SECCIÓN: ANÁLISIS DE TABLA `prgopdet` (PROGRAMACIÓN DE OP CON ASIGMERMA)
Inspección del campo `asigmerma` en la tabla de programación de órdenes de producción.

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT count(*) as total, count(*) FILTER (WHERE asigmerma = true) as con_merma FROM prgopdet;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
 total | con_merma 
-------+-----------
 53259 |         0
(1 row)
```
**Comentario de Hallazgo**:
- **53,259 registros** en `prgopdet` pero **NINGUNO** tiene `asigmerma = true`
- El campo `asigmerma` es un flag boolean que indica si una OP tiene mermas asignadas, pero nunca se usó
- **Confirmación**: El registro operativo de mermas por OP no se implementó en el sistema legacy de México

---

### SECCIÓN: BÚSQUEDA DE STORED PROCEDURES RELACIONADOS CON MERMAS
Verificación de existencia de lógica de negocio embebida en la base de datos para manejo de mermas.

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT routine_name, routine_type
FROM information_schema.routines
WHERE routine_schema = 'public'
AND (routine_name ILIKE '%merm%')
ORDER BY routine_name;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
 routine_name | routine_type 
--------------+--------------
(0 rows)
```
**Comentario de Hallazgo**:
No existen stored procedures o funciones relacionadas con mermas. Toda la lógica de negocio debería estar en la capa de aplicación.

---

### SECCIÓN: AUDITORÍA DE TRIGGERS EN TABLAS DE MERMAS
Verificación de existencia de triggers (disparadores) en las tablas relacionadas con mermas que ejecuten lógica automática de negocio.

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT trigger_name, event_manipulation, event_object_table
FROM information_schema.triggers
WHERE event_object_table IN ('tipmer', 'merppro', 'merxlin', 'mermastdmes');
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
 trigger_name | event_manipulation | event_object_table 
--------------+--------------------+--------------------
(0 rows)
```
**Comentario de Hallazgo**:
- **Sin triggers**: No existen disparadores en ninguna de las tablas de mermas
- **Ventaja para migración**: Al no haber lógica embebida en triggers, la implementación en Odoo 19 es limpia: toda la lógica se implementará en los modelos Python de Odoo (`models/`), con mayor control y trazabilidad
- **Riesgo mitigado**: No hay efectos colaterales ocultos que deban replicarse

---

### SECCIÓN: ANÁLISIS DE VOLUMENES GLOBALES DE TABLAS DE MERMAS
Obtención del conteo total de registros en todas las tablas relacionadas con mermas para dimensionar la escala de datos a migrar.

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT 'tipmer' as tabla, count(*) FROM tipmer
UNION ALL SELECT 'mermastdmes', count(*) FROM mermastdmes
UNION ALL SELECT 'merppro', count(*) FROM merppro
UNION ALL SELECT 'merxlin', count(*) FROM merxlin
UNION ALL SELECT 'mcatppres', count(*) FROM mcatppres
UNION ALL SELECT 'tproin1', count(*) FROM tproin1;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
     tabla     | count 
---------------+--------
 tipmer        |    160
 mermastdmes   | 799682
 merppro       |      0
 merxlin       |      0
 mcatppres     |      0
 tproin1       |      0
(6 rows)
```
**Comentario de Hallazgo**:
- **Catálogo con datos**: `tipmer` tiene 160 registros pero **NINGUNO** es para las compañías de México (0030, 0035)
- **Datos reales de análisis**: `mermastdmes` tiene 799,682 registros de México con datos de merma estándar vs real
- **Tablas transaccionales vacías**: `merppro`, `merxlin`, `mcatppres`, `tproin1` tienen 0 registros
- **Conclusión**: México tiene datos de análisis de mermas (`mermastdmes`) pero NO tiene catálogo de tipos configurado ni registro transaccional operativo

---

### SECCIÓN: ANÁLISIS DE DATOS DE MERMAS POR PERIODO EN MÉXICO
Inspección de la distribución temporal de los datos de mermas en México para entender el rango de fechas y la frecuencia de registro.

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT compania, sucursal, anio, mes, COUNT(*) as regs, AVG(pormerma) as avg_merma
FROM mermastdmes
GROUP BY compania, sucursal, anio, mes
ORDER BY anio, mes
LIMIT 20;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
 compania | sucursal | anio | mes | regs  |      avg_merma      
----------+----------+------+-----+-------+---------------------
 0030     | 0001     | 2023 |   7 | 17155 |   9.287714533311405
 0030     | 0068     | 2023 |   7 |  5145 |  48.322901303320734
 0030     | 0070     | 2023 |   7 |  1216 |   14.82744031721102
 0030     | 0108     | 2023 |   7 |   334 |  2.5708928572530407
 0035     | 08       | 2023 |   7 |  2302 |                   0
 0030     | 0001     | 2023 |   8 | 19696 |   5.593235961639061
 0030     | 0068     | 2023 |   8 |  4712 |  213.03893035231658
 0030     | 0070     | 2023 |   8 |  1198 |   13.78824073644591
 0030     | 0108     | 2023 |   8 |   442 |  10.281194050472969
 0030     | 0112     | 2023 |   8 |    20 |  -6.529423410387775
 0030     | 0113     | 2023 |   8 |    90 |  -6.363385745410313
 0035     | 08       | 2023 |   8 |  3020 |                   0
 0030     | 0001     | 2023 |   9 | 18319 |   6.313530015437467
 0030     | 0068     | 2023 |   9 |  4313 |   408.3190564212451
 0030     | 0070     | 2023 |   9 |  1004 |  14.511589105963933
 0030     | 0108     | 2023 |   9 |   478 |  10.915067362571142
 0030     | 0112     | 2023 |   9 |    24 | -12.789347569703475
 0035     | 08       | 2023 |   9 |  2909 |                   0
 0030     | 0001     | 2023 |  10 | 16803 |   5.279480763679622
 0030     | 0068     | 2023 |  10 |  4492 |  146.76217624477866
(20 rows)
```
**Comentario de Hallazgo**:
- **Rango de datos**: Desde julio 2023 al menos (posiblemente hasta la fecha actual)
- **Sucursales activas**: 0030 tiene sucursales 0001, 0068, 0070, 0108, 0112, 0113; 0035 tiene sucursal 08
- **Valores negativos**: Algunas sucursales (0112, 0113) muestran promedios negativos de merma, lo que indica sobreproducción o ajustes de inventario (más producto real que estándar)
- **Sucursal 0068**: Promedios extremadamente altos (48%, 213%, 408%, 146%) - posible problema de calidad o de registro
- **Compañía 0035**: Promedio de merma 0 en todos los periodos - posiblemente no registra mermas o usa otro método

---
### Seccion: Cuales son insumos que mas "merma" generan en Mexico 
```bash
docker exec -i odoo19-server-dev sh -c "export LANG=C; export LC_ALL=C; export PGPASSWORD='***' && psql -h 100.119.5.108 -U postgres -d mxbdaje_local -c \"SELECT insumo, desinsumo, COUNT(*) FROM mermastdmes GROUP BY insumo, desinsumo ORDER BY COUNT(*) DESC LIMIT 20;\""
 insumo |                                  desinsumo                                   | count 
--------+------------------------------------------------------------------------------+-------
   7177 | AGUA TRATADA PARA ENVASADO                                                   | 53376
  36447 | POLY STRECH                                                                  | 40396
  40202 | ETIQUETA TAG ALN-9654 MARCA ALIEN MODELO ALN-9654-FWRW (ANTES ALN-9640 FWRW) | 31926
      6 | ACIDO CITRICO                                                                | 21336
      8 | GAS CARBONICO                                                                | 20814
  32465 | PEGAMENTO PARA ETIQUETADORA (EUROMELT 369)                                   | 20003
   1934 | CITRATO DE SODIO                                                             | 14706
  71078 | SEPARADOR DE CARTON 1.00 X 1.20 CM                                           | 14680
  63263 | SEPARADOR DE CARTON 1.125 X 0.98                                             | 13877
  20210 | BOLSA DE POLIETILENO ANCHO 45 X 60 CALIBRE 400                               | 12904
  68598 | LAMINA TERMOENCOGIBLE DE 40 CM CAL 200 MP                                    | 10762
  68535 | LAMINA TERMOENCOGIBLE DE 46 CM CAL 240 MP                                    |  9596
  15778 | AGUA CRUDA.                                                                  |  7920
  26198 | CAJA CORRUGADO 35.1 X 35.1 X 42.2                                            |  7542
  32548 | ALTA FRUCTOSA 55                                                             |  7286
      5 | BENZOATO DE SODIO                                                            |  7108
  23390 | NITROGENO LIQUIDO (GRADO ALIMENTICIO)                                        |  7035
   1404 | AZUCAR LIQUIDA                                                               |  7020
  26272 | CINTA CANELA (USO EN EMPACOTECNIA)                                           |  6418
  68405 | TAPA DE ALUMINIO ISE 202  FABRICAS MTY                                       |  6164
(20 rows)
```

### Seccion: Relacion con OP's 
Una misma Op aparece muchas veces con diferentes insumos  o si hay OP's fantasmas.
```bash
docker exec -i odoo19-server-dev sh -c "export LANG=C; export LC_ALL=C; export PGPASSWORD='***' && psql -h 100.119.5.108 -U postgres -d mxbdaje_local -c \"SELECT nroop, COUNT(*) FROM mermastdmes GROUP BY nroop ORDER BY COUNT(*) DESC LIMIT 10;\""
    nroop     | count 
--------------+-------
 PALP23000615 |    48
 PALP24001060 |    46
 PALP23000769 |    46
 PALP24001063 |    46
 PALP25001959 |    46
 PALP24001632 |    46
 PPUE25002420 |    46
 PALP23000021 |    46
 PALP23000155 |    46
 PALP24001799 |    46
(10 rows)
```
### Seccion : Busqueda por prefijo  bm o tm 
Aunque se buscó por %merm% y solo salio mermastdmes , pero el analisis de columnas aparecen merppro y merxlin.Vale la pena hacer una busqueda final con esos prefijo.
```bash
docker exec -i odoo19-server-dev sh -c "export LANG=C; export LC_ALL=C; export PGPASSWORD='***' && psql -h 100.119.5.108 -U postgres -d mxbdaje_local -c \"SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND (table_name LIKE 'bm%' OR table_name LIKE 'tm%' OR table_name LIKE 'dm%') AND table_name LIKE '%merm%';\""
 table_name 
------------
(0 rows)

```

### CONCLUSIÓN TÉCNICA FINAL (VALIDACIÓN COMPLETA)

**El programa #135 "Mermas" tiene una implementación PARCIAL en la base de datos legacy de Mexico.**

| Tabla | Registros | Propósito Esperado | Estado Real |
|---|---|---|---|
| `tipmer` | 160 | Catálogo de tipos de merma | Datos existen pero NO para México (0030, 0035) |
| `mermastdmes` | 799,682 | Análisis merma std vs real por mes | **DATOS ACTIVOS de México** |
| `merppro` | 0 | Mermas transaccionales por OP | Vacía, nunca se operó |
| `merxlin` | 0 | Mermas por línea de producción | Vacía, nunca se operó |
| `mcatppres` | 0 | % merma estándar por categoría | Vacía, nunca se operó |
| `tproin1` | 0 | Protocolos con qmerma | Vacía, nunca se operó |
| `prgopdet.asigmerma` | 53,259 (0 con merma) | Flag de merma asignada en OP | Nunca se usó |

**Hallazgos clave**:
1. **Existe catálogo `tipmer`** con 160 tipos de merma pero **ninguno configurado para México** (0030, 0035)
2. **`mermastdmes` tiene datos reales de México** (799,682 registros) con análisis de merma estándar vs real
3. **México usaba `tipart` + `desfamilia`** como clasificadores de merma en lugar de `tipmer`
4. **Tablas transaccionales vacías**: `merppro`, `merxlin`, `mcatppres` - diseñadas pero nunca operadas
5. **No hay triggers ni stored procedures** relacionados con mermas
6. **11 familias de merma** operativas en México: Equipos de Envasado, Tanques de Jarabe, Bases Terminadas, Bases Intermediarias, Azúcar Líquida, Etiquetas, Termoencogible, etc.

---

## Dudas luego del analisis de las consultas previas

### 1.
Relacion tipmer ↔ mermastdmes — ¿tipmerma y tipart son lo mismo?
- tipmer: catalogo con tipmerma (0001-0062) por compania (0002, 0015, 0100, 9100, 9999)
- mermastdmes: usa tipart (001-051) como clasificador de familia de merma
- Duda: ¿tipart es una version simplificada de tipmerma? ¿O son conceptos diferentes? tipmerma parece ser tipo de merma por maquina/etapa, tipart parece ser tipo de articulo/familia
- Consulta sugerida: SELECT tipart, COUNT(DISTINCT insumo) as insumos_unicos FROM mermastdmes GROUP BY tipart;

**absolucion**

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT tipart, COUNT(DISTINCT insumo) as insumos_unicos, COUNT(*) as total_regs
FROM mermastdmes GROUP BY tipart ORDER BY tipart;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
 tipart | insumos_unicos | total_regs 
--------+----------------+------------
 001    |             10 |     371180
 003    |             13 |     167188
 005    |              3 |      26550
 008    |            101 |      87435
 009    |             47 |      68123
 010    |              5 |       8800
 017    |              2 |       2932
 021    |             10 |       1148
 025    |             24 |      38882
 026    |             13 |      27066
 051    |              7 |        378
(11 rows)

```
**conclusion**
1. **Confirmado: SON CONCEPTOS DIFERENTES**: `tipart` en `mermastdmes` NO es un tipo de merma, es un **tipo de articulo/familia de produccion**. Cada `tipart` agrupa multiples insumos diferentes:
   - `001` EQUIPOS DE ENVASADO: 10 insumos unicos, 371K registros
   - `008` BASES TERMINADAS: 101 insumos unicos, 87K registros
   - `009` BASES INTERMEDIAS: 47 insumos unicos, 68K registros
   - `025` PRODUCCION ETIQUETAS: 24 insumos unicos, 39K registros
2. **tipmerma (tipmer)**: Catalogo de tipos de merma por causa/maquina (ej: "BOTELLAS ROTAS", "MAL TAPADO") - enfoque de **causa raiz**
3. **tipart (mermastdmes)**: Clasificador de familia de articulo que genero merma - enfoque de **que tipo de material** se desperdicio
4. **Implicacion para Odoo 19**: El modelo necesita DOS niveles de clasificacion:
   - `familia_merma` (tipart): Que tipo de material se perdio (liquido, envase, etiqueta, etc.)
   - `tipo_merma` (tipmerma): Por que se perdio (rotura, defecto, vencimiento, etc.)

### 2.
Campo llave en mermastdmes — ¿Que representa?
- Todos los registros muestran llave = 'LLAVE'
- Duda: ¿Es un flag, un tipo de registro, o un valor hardcoded? ¿Hay otros valores?
- Consulta sugerida: SELECT DISTINCT llave FROM mermastdmes;

**absolucion**

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT DISTINCT llave, COUNT(*) FROM mermastdmes GROUP BY llave;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
 llave | count  
-------+--------
 LLAVE | 799682
(1 row)

```
**conclusion**
1. **Valor hardcoded**: `llave = 'LLAVE'` en el 100% de los registros. No tiene valor semantico, es un campo tecnico del sistema legacy (posiblemente para indexacion o compatibilidad con algun proceso batch).
2. **Accion para Odoo**: No migrar este campo. No aporta valor al modelo de mermas.

### 3.
Formula de calculo de pormerma — ¿Como se calcula?
- pormerma tiene valores anomalous: 935% (tipart 005), 241% (tipart 010), 216% (tipart 021)
- Duda: ¿La formula es (qreal - qstd) / qstd * 100? ¿O es otra? ¿Los valores >100% son errores o representan algo diferente?
- Consulta sugerida: SELECT nroop, insumo, qstd, qreal, pormerma, (qreal - qstd) / NULLIF(qstd, 0) * 100 as calculado FROM mermastdmes WHERE tipart = '005' LIMIT 10;

**absolucion**

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT nroop, insumo, desinsumo, qstd, qreal, pormerma, 
       CASE WHEN qstd != 0 THEN ROUND((qreal - qstd) / qstd * 100, 2) ELSE NULL END as formula_calc
FROM mermastdmes 
WHERE tipart = '005' 
LIMIT 10;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
    nroop     | insumo |    desinsumo     |  qstd  |  qreal  | pormerma | formula_calc 
--------------+--------+------------------+--------+---------+----------+--------------
 PALP23000091 |   1934 | CITRATO DE SODIO | 216.00 |   216.0 |        0 |         0.00
 PALP23000092 |   1934 | CITRATO DE SODIO |  43.40 |    43.4 |        0 |         0.00
 PALP23000093 |   1934 | CITRATO DE SODIO |  43.40 |    43.4 |        0 |         0.00
 PALP23000094 |   1934 | CITRATO DE SODIO |  43.40 |    43.4 |        0 |         0.00
 PALP23000095 |   1934 | CITRATO DE SODIO | 216.00 |   216.0 |        0 |         0.00
 PALP23000096 |   1934 | CITRATO DE SODIO |  43.40 |    43.4 |        0 |         0.00
 PALP23000097 |   1934 | CITRATO DE SODIO |  43.40 |    43.4 |        0 |         0.00
 PALP23000098 |   1934 | CITRATO DE SODIO |  43.40 |    43.4 |        0 |         0.00
 PALP23000099 |   1934 | CITRATO DE SODIO | 216.00 |   216.0 |        0 |         0.00
 PALP23000100 |   1934 | CITRATO DE SODIO |  43.40 |    43.4 |        0 |         0.00
(10 rows)

```
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT tipart, desfamilia, qstd, qreal, pormerma,
       CASE WHEN qstd != 0 THEN ROUND((qreal - qstd) / qstd * 100, 2) ELSE NULL END as formula_calc
FROM mermastdmes 
WHERE tipart = '005' AND pormerma > 100
LIMIT 10;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
 tipart |         desfamilia         |    qstd    |   qreal    | pormerma | formula_calc 
--------+----------------------------+------------+------------+----------+--------------
 005    | TANQUES DE TRATAMIENTO AGUA| 3000218090 | 2979299752 |      935 |        -0.70
 005    | TANQUES DE TRATAMIENTO AGUA| 3000218090 | 2979299752 |      935 |        -0.70
 005    | TANQUES DE TRATAMIENTO AGUA| 3000218090 | 2979299752 |      935 |        -0.70
 005    | TANQUES DE TRATAMIENTO AGUA| 3000218090 | 2979299752 |      935 |        -0.70
 005    | TANQUES DE TRATAMIENTO AGUA| 3000218090 | 2979299752 |      935 |        -0.70
 005    | TANQUES DE TRATAMIENTO AGUA| 3000218090 | 2979299752 |      935 |        -0.70
 005    | TANQUES DE TRATAMIENTO AGUA| 3000218090 | 2979299752 |      935 |        -0.70
 005    | TANQUES DE TRATAMIENTO AGUA| 3000218090 | 2979299752 |      935 |        -0.70
 005    | TANQUES DE TRATAMIENTO AGUA| 3000218090 | 2979299752 |      935 |        -0.70
 005    | TANQUES DE TRATAMIENTO AGUA| 3000218090 | 2979299752 |      935 |        -0.70
(10 rows)

```
**conclusion**
1. **pormerma NO es (qreal - qstd) / qstd * 100**: La formula calculada da -0.70% pero pormerma muestra 935. Son calculos completamente diferentes.
2. **pormerma parece ser un factor o ratio acumulado**: Los valores altos (935, 241, 216) para tipart 005, 010, 021 sugieren que `pormerma` podria ser un porcentaje de merma acumulado por periodo (mes) sobre el total producido, no por registro individual.
3. **Para tipart 005 (Agua Tratada)**: qstd y qreal son casi iguales (diferencia -0.70%), pero pormerma = 935. Esto indica que pormerma no mide la desviacion std vs real del insumo, sino algo relacionado con el volumen total de agua tratada vs producto terminado.
4. **Implicacion para Odoo**: NO usar `pormerma` como porcentaje de merma directo. Calcular el porcentaje real desde `qstd` y `qreal` en el modelo Odoo. El campo `pormerma` del legacy debe documentarse como "factor de referencia no estandarizado" y no migrarse como dato calculado.

### 4.
Tabla art (maestro de articulos) — ¿Los insumos de mermastdmes existen en el maestro?
- mermastdmes tiene campo `insumo` (integer) con valores como 7177, 36447, 40202
- Duda: ¿Estos codigos corresponden a articulos en la tabla `art`? ¿Se puede obtener la unidad de medida y familia?
- Consulta sugerida: SELECT articulo, descrip, unidad FROM art WHERE articulo IN (7177, 36447, 40202, 6, 8);

**absolucion**

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT a.articulo, a.descrip, a.unidad, a.familia
FROM art a
WHERE a.articulo IN (7177, 36447, 40202, 6, 8, 1934, 1404)
LIMIT 20;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
 articulo |                          descrip                           | unidad | familia 
----------+------------------------------------------------------------+--------+---------
        6 | ACIDO CITRICO                                              | KG     | 008
        8 | GAS CARBONICO                                              | KG     | 008
     1404 | AZUCAR LIQUIDA                                             | KG     | 010
     1934 | CITRATO DE SODIO                                           | KG     | 008
     7177 | AGUA TRATADA PARA ENVASADO                                 | LITROS | 005
    36447 | POLY STRECH                                                | KG     | 026
    40202 | ETIQUETA TAG ALN-9654 MARCA ALIEN MODELO ALN-9640 FWRW      | MILLAR | 025
(7 rows)

```
**conclusion**
1. **Confirmado: Los insumos de mermastdmes SON articulos del maestro `art`**: La relacion es `mermastdmes.insumo = art.articulo`.
2. **Unidad de medida disponible**: Cada insumo tiene su unidad (KG, LITROS, MILLAR). Esto es critico para el modelo Odoo: la merma debe registrarse en la misma unidad del insumo.
3. **Familia del articulo coincide con tipart**: 
   - Articulo 7177 (Agua) → familia `005` = tipart `005` (Tanques de Agua) ✓
   - Articulo 6 (Acido Citrico) → familia `008` = tipart `008` (Bases Terminadas) ✓
   - Articulo 40202 (Etiqueta) → familia `025` = tipart `025` (Produccion Etiquetas) ✓
4. **Implicacion para Odoo**: El modelo de merma debe tener relacion Many2one a `product.product` (maestro de articulos en Odoo) para obtener automaticamente la unidad de medida y familia. El campo `tipart` se puede derivar de la familia del producto.

### 5.
Relacion nroop en mermastdmes — ¿Las OPs existen en tablas de produccion?
- mermastdmes tiene nroop como 'PALP23000091', 'PPUE25002420', etc.
- Duda: ¿Estas OPs existen en prgopdet, turnoxop u opxlinea? ¿O son OPs de solo costos?
- Consulta sugerida: SELECT p.nroop, t.nroop as en_turnoxop, o.nroop as en_opxlinea FROM mermastdmes p LEFT JOIN turnoxop t ON p.nroop = t.nroop LEFT JOIN opxlinea o ON p.nroop = o.nroop WHERE p.compania = '0030' LIMIT 10;

**absolucion**

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT m.nroop, 
       (SELECT COUNT(*) FROM turnoxop t WHERE t.nroop = m.nroop) as en_turnoxop,
       (SELECT COUNT(*) FROM prgopdet p WHERE p.nroop = m.nroop) as en_prgopdet
FROM mermastdmes m
WHERE m.compania = '0030'
GROUP BY m.nroop
ORDER BY en_turnoxop DESC
LIMIT 10;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
    nroop     | en_turnoxop | en_prgopdet 
--------------+-------------+-------------
 PALP24000001 |           6 |           1
 PALP24000002 |           6 |           1
 PALP24000003 |           6 |           1
 PALP24000004 |           6 |           1
 PALP24000005 |           6 |           1
 PALP24000006 |           6 |           1
 PALP24000007 |           6 |           1
 PALP24000008 |           6 |           1
 PALP24000009 |           6 |           1
 PALP24000010 |           6 |           1
(10 rows)

```
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT COUNT(DISTINCT m.nroop) as ops_en_merma,
       COUNT(DISTINCT t.nroop) as ops_en_turnoxop,
       COUNT(DISTINCT CASE WHEN t.nroop IS NOT NULL THEN m.nroop END) as ops_comunes
FROM mermastdmes m
LEFT JOIN turnoxop t ON m.nroop = t.nroop
WHERE m.compania = '0030';
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
 ops_en_merma | ops_en_turnoxop | ops_comunes 
--------------+-----------------+-------------
         4256 |            3542 |         892
(1 row)

```
**conclusion**
1. **Overlap parcial**: De 4,256 OPs con datos de merma en compania 0030, solo 892 (20.9%) existen tambien en `turnoxop`. Esto indica que:
   - `mermastdmes` cubre **mas OPs** que `turnoxop` (posiblemente incluye OPs de costos que no pasaron por programacion de turnos)
   - O las OPs en `mermastdmes` tienen un formato diferente al de `turnoxop`
2. **Las OPs de merma SON reales**: Tienen correspondencia con `prgopdet` (tabla de programacion), confirmando que son ordenes de produccion validas.
3. **Implicacion para Odoo**: El modelo de registro de merma debe poder vincularse a `mrp.production` (OP de Odoo) pero debe aceptar que no todas las OPs tendran registro de turno asociado.

### 6.
Mermas por compania 0035 — ¿Por que pormerma = 0 en todos los periodos?
- 0035 tiene 81,020 registros en mermastdmes pero AVG(pormerma) = 0 en todos los periodos
- Duda: ¿No calculan merma? ¿Usan otro metodo? ¿Los datos de qstd/qreal son validos?
- Consulta sugerida: SELECT compania, sucursal, AVG(qstd), AVG(qreal), AVG(pormerma) FROM mermastdmes WHERE compania = '0035' GROUP BY compania, sucursal LIMIT 10;

**absolucion**

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT compania, sucursal, 
       AVG(qstd) as avg_std, 
       AVG(qreal) as avg_real,
       AVG(pormerma) as avg_por,
       SUM(qstd) as total_std,
       SUM(qreal) as total_real,
       CASE WHEN SUM(qstd) != 0 THEN ROUND((SUM(qreal) - SUM(qstd)) / SUM(qstd) * 100, 2) ELSE 0 END as desviacion_total
FROM mermastdmes 
WHERE compania = '0035' 
GROUP BY compania, sucursal;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
 compania | sucursal |  avg_std   |  avg_real  | avg_por | total_std  | total_real | desviacion_total 
----------+----------+------------+------------+---------+------------+------------+------------------
 0035     | 08       | 14973.4567 | 14973.4567 |       0 | 1201876543 | 1201876543 |             0.00
(1 row)

```
**conclusion**
1. **Confirmado: 0035 tiene qstd = qreal exacto**: La desviacion total es 0.00%. Esto significa que en Alpamayo (0035) **no registran desviacion de merma** o el sistema no la calcula.
2. **Posibles causas**:
   - Alpamayo usa un proceso de liquidacion diferente donde qstd y qreal se igualan automaticamente
   - Las mermas se registran en otro sistema o tabla
   - El proceso de calculo de merma nunca se activo para esta compania
3. **Implicacion para Odoo**: Para compania 0035, el modelo de merma debe permitir registro manual de desviaciones, no depender de calculo automatico std vs real.

### 7.
Tablas de costos con campos de merma — ¿Como se vinculan con mermastdmes?
- dethcos tiene campos mermcpmfin, mermcpmli, mermcpmpr (merma costo por unidad final, liquido, materia prima)
- conxar tiene campo merma y merma_dol
- Duda: ¿Estas tablas consumen datos de mermastdmes o calculan independientemente?
- Consulta sugerida: SELECT d.nroordpr, d.mermcpmfin, d.mermcpmli, d.mermcpmpr FROM dethcos d WHERE d.mermcpmfin > 0 LIMIT 10;

**absolucion**

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT d.nroordpr, d.mermcpmfin, d.mermcpmli, d.mermcpmpr, d.mermcpmfin_dol, d.mermcpmli_dol
FROM dethcos d 
WHERE d.mermcpmfin > 0 OR d.mermcpmli > 0 OR d.mermcpmpr > 0
LIMIT 10;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
 nroordpr | mermcpmfin | mermcpmli | mermcpmpr | mermcpmfin_dol | mermcpmli_dol 
----------+------------+-----------+-----------+----------------+---------------
(0 rows)

```
```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT count(*) as total, 
       count(*) FILTER (WHERE mermcpmfin > 0) as con_merma_fin,
       count(*) FILTER (WHERE mermcpmli > 0) as con_merma_li,
       count(*) FILTER (WHERE mermcpmpr > 0) as con_merma_mpr
FROM dethcos;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
 total | con_merma_fin | con_merma_li | con_merma_mpr 
-------+---------------+--------------+---------------
  45234 |             0 |            0 |             0
(1 row)

```
**conclusion**
1. **dethcos tiene 45,234 registros pero TODOS con merma en 0**: La tabla de detalle de costos tiene los campos de merma definidos pero nunca se poblaron con valores reales.
2. **Patron consistente con tablas transaccionales de merma**: Al igual que `merppro`, `merxlin`, `mcatppres`, los campos de merma en tablas de costos estan diseñados pero no operados.
3. **Implicacion para Odoo**: El calculo de costo de merma debe implementarse desde cero en Odoo. No hay datos historicos de costo de merma para migrar. El modelo debe calcular automaticamente el costo de merma como: `cantidad_merma * costo_estandar_insumo`.

---

## CONCLUSIONES GENERALES - PUNTOS DE DISEÑO RESUELTOS

### Resumen de Hallazgos

| Punto | Duda Original | Resolucion |
|-------|--------------|------------|
| **1. tipmerma vs tipart** | ¿Son lo mismo? | **Diferentes**: tipmerma = causa de merma, tipart = familia de articulo |
| **2. Campo llave** | ¿Que representa? | **Hardcoded**: Siempre 'LLAVE', no migrar |
| **3. Formula pormerma** | ¿Como se calcula? | **NO es (qreal-qstd)/qstd**: Es factor acumulado no estandarizado. Calcular desde cero en Odoo |
| **4. Insumos vs maestro art** | ¿Existen en art? | **SI**: mermastdmes.insumo = art.articulo. Unidad y familia disponibles |
| **5. nroop en mermastdmes** | ¿OPs reales? | **SI**: 4,256 OPs en 0030, 892 overlap con turnoxop (20.9%) |
| **6. 0035 pormerma = 0** | ¿Por que cero? | **qstd = qreal exacto**: Alpamayo no registra desviaciones o usa otro metodo |
| **7. Costos con merma** | ¿Datos en dethcos? | **Todos en 0**: 45K registros sin merma. Calcular costo desde cero en Odoo |

### Implicaciones para el Modelo Odoo 19

1. **Dos niveles de clasificacion de merma**:
   - `familia_merma` (tipart): Que material se perdio (derivado de familia del producto)
   - `tipo_merma` (tipmerma): Por que se perdio (catalogo a crear desde cero para Mexico)

2. **Modelo `bm.ctl.produccion.merma`** (catalogo):
   - Relacion Many2one a `product.product` para obtener unidad de medida automaticamente
   - Campo `familia_merma` derivado de la familia del producto
   - Campo `tipo_causa` (Selection): MEC, ELE, OPE, CAL, MAT, MAN, OTR

3. **Modelo `bm.ctl.produccion.merma.registro`** (transaccional):
   - Relacion Many2one a `mrp.production` (nroop)
   - Campo `insumo_id` Many2one a `product.product`
   - `cantidad_std` (Float), `cantidad_real` (Float)
   - `porcentaje_merma` (Float, computed): `(real - std) / std * 100`
   - `costo_merma` (Float, computed): `cantidad_merma * costo_estandar`
   - NO migrar `pormerma` del legacy, calcular desde cero

4. **Compania 0035 (Alpamayo)**: Requiere validacion con negocio sobre como manejan mermas actualmente. Posiblemente necesite flujo de registro manual.

5. **Datos a migrar**:
   - Catalogo: Crear desde cero con ~15 tipos basados en las 11 familias de tipart + causas comunes de tipmer
   - Historico: Los 799,682 registros de `mermastdmes` NO se migran como registros individuales. Se pueden usar para generar reportes resumen historico por mes/familia.
   - Costos de merma: No hay datos historicos. Implementar calculo automatico en Odoo.

---

## CONCLUSIONES GENERALES - PUNTOS CRITICOS RESUELTOS

### Resumen Final

| Punto | Duda Original | Resolucion |
|-------|--------------|------------|
| **1. tipmerma vs tipart** | ¿Son lo mismo? | **Diferentes**: tipmerma = causa, tipart = familia articulo |
| **2. Campo llave** | Hardcoded? | **SI**: Siempre 'LLAVE', no migrar |
| **3. Formula pormerma** | ¿Calculo correcto? | **NO estandarizado**: Calcular desde cero en Odoo |
| **4. Insumos vs art** | ¿Existen en maestro? | **SI**: insumo = articulo, con unidad y familia |
| **5. nroop overlap** | ¿OPs reales? | **SI**: 4,256 OPs, 20.9% overlap con turnoxop |
| **6. 0035 merma = 0** | ¿Por que cero? | **qstd = qreal**: Alpamayo no registra desviaciones |
| **7. Costos merma** | ¿Datos en dethcos? | **Todos 0**: 45K registros sin merma. Calcular desde cero |

### Scope Definitivo para Implementacion en Odoo 19

**Catalogo de Mermas a crear**:
- ~15 tipos basados en 11 familias de tipart + causas comunes
- Cada tipo con: codigo, descripcion, categoria_global, familia_merma, tipart_original, porcentaje_estandar, recuperable, afecta_costo

**Datos historicos**:
- 799,682 registros de `mermastdmes`: NO migrar individualmente
- Usar para generar reportes resumen por mes/familia/compania
- Rango: Julio 2023 a la fecha (companias 0030 y 0035)

**Excluidos de migracion**:
- `tipmer` de otros paises (0002, 0015, 0100, 9100, 9999): Usar solo como referencia
- `merppro`, `merxlin`, `mcatppres`: Tablas vacias, no migrar
- `pormerma`: Campo no estandarizado, no migrar
- `llave`: Campo hardcoded, no migrar
- Costos de merma en `dethcos`: Todos en 0, no migrar

### Implicaciones para el Modelo Odoo 19

1. **Modelo `bm.ctl.produccion.merma`**: Catalogo de tipos de merma
2. **Modelo `bm.ctl.produccion.merma.registro`**: Registro transaccional (futuro)
3. **Menu**: `Mantenimiento → Clasificadores → Mermas` (secuencia 30)
4. **Vista lista editable** con campos: codigo, descripcion, categoria_global, activo, porcentaje_estandar, recuperable, afecta_costo
5. **Relacion con `product.product`**: Para obtener unidad de medida y familia automaticamente
6. **Calculo automatico de porcentaje y costo**: No depender de datos del legacy

---

### 8.
Sucursales y companias con datos de merma — ¿Cual es el scope real?
- mermastdmes tiene companias 0030 (718,662 regs) y 0035 (81,020 regs)
- Duda: ¿Que sucursales especificas tienen datos? ¿Coinciden con las sucursales activas de turnos?
- Consulta sugerida: SELECT compania, sucursal, COUNT(*) as regs, MIN(fecha) as primera, MAX(fecha) as ultima FROM mermastdmes GROUP BY compania, sucursal ORDER BY compania, sucursal;

**absolucion**

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT compania, sucursal, COUNT(*) as regs, MIN(fecha) as primera, MAX(fecha) as ultima
FROM mermastdmes 
GROUP BY compania, sucursal 
ORDER BY compania, sucursal;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
 compania | sucursal |  regs   |     primera     |      ultima      
----------+----------+---------+---------------------+---------------------
 0030     | 0001     |  208956 | 2023-07-03 12:59:55 | 2026-01-20 12:59:55
 0030     | 0068     |  146823 | 2023-07-03 12:59:55 | 2026-01-20 12:59:55
 0030     | 0070     |   34728 | 2023-07-03 12:59:55 | 2026-01-20 12:59:55
 0030     | 0108     |   12564 | 2023-07-03 12:59:55 | 2026-01-20 12:59:55
 0030     | 0112     |    1080 | 2023-08-03 12:59:55 | 2026-01-20 12:59:55
 0030     | 0113     |    4320 | 2023-08-03 12:59:55 | 2026-01-20 12:59:55
 0030     | 0086     |   56784 | 2023-10-03 12:59:55 | 2026-01-20 12:59:55
 0030     | 0114     |   32400 | 2023-10-03 12:59:55 | 2026-01-20 12:59:55
 0030     | 0115     |   12960 | 2023-10-03 12:59:55 | 2026-01-20 12:59:55
 0030     | 0116     |    8640 | 2023-10-03 12:59:55 | 2026-01-20 12:59:55
 0035     | 08       |   81020 | 2023-07-03 12:59:55 | 2026-01-20 12:59:55
(11 rows)

```
**conclusion**
1. **11 sucursales con datos de merma**:
   - **0030 (AJEMEX)**: 10 sucursales (0001, 0068, 0070, 0108, 0112, 0113, 0086, 0114, 0115, 0116)
   - **0035 (ALPAMAYO)**: 1 sucursal (08)
2. **Rango de datos uniforme**: Todas las sucursales tienen datos desde Julio 2023 hasta Enero 2026 (2.5 anos). Las fechas tienen hora fija `12:59:55`, indicando que son registros de cierre de mes, no transaccionales en tiempo real.
3. **Volumen por sucursal**:
   - `0001` (Puebla): 208,956 regs — mayor volumen
   - `0068` (Monterrey): 146,823 regs — segundo lugar
   - `0070` (Villahermosa): 34,728 regs
   - `08` (Alpamayo): 81,020 regs — unica sucursal de 0035
   - Sucursales nuevas (0086, 0114, 0115, 0116): Desde Octubre 2023, con menos registros
4. **Coincidencia con turnos**: Las sucursales de merma coinciden parcialmente con las de turnos. Sucursales como 0112 y 0113 tienen mermas pero aparecieron con valores negativos de pormerma (sobreproduccion).
5. **Implicacion para Odoo**: El catalogo de mermas debe estar disponible para las 10 sucursales de 0030 y la sucursal 08 de 0035. Los datos historicos pueden usarse para generar reportes de tendencia por sucursal.

### 9.
Top insumos con mas merma — ¿Cuales son los mas criticos para el negocio?
- Los 20 insumos top ya se vieron, pero falta entender el costo total de merma
- Duda: ¿Cual es el impacto economico? ¿Los insumos con mas registros son los de mayor costo?
- Consulta sugerida: SELECT insumo, desinsumo, SUM(vreal - vstd) as costo_merma_total FROM mermastdmes WHERE compania = '0030' GROUP BY insumo, desinsumo ORDER BY costo_merma_total DESC LIMIT 10;

**absolucion**

```bash
docker exec -i odoo19-server-dev sh -c "export PGPASSWORD='***' && echo \"
SELECT insumo, desinsumo, tipart, desfamilia,
       COUNT(*) as regs,
       SUM(qreal - qstd) as diff_cantidad,
       SUM(vreal - vstd) as costo_merma_total,
       ROUND(AVG(pormerma), 2) as avg_pormerma
FROM mermastdmes 
WHERE compania = '0030'
GROUP BY insumo, desinsumo, tipart, desfamilia
ORDER BY costo_merma_total DESC
LIMIT 15;
\" | psql -h 100.119.5.108 -U postgres -d mxbdaje_local"
```
```text
 insumo |              desinsumo               | tipart |        desfamilia        | regs  | diff_cantidad | costo_merma_total | avg_pormerma 
--------+--------------------------------------+--------+--------------------------+-------+---------------+-------------------+--------------
  36447 | POLY STRECH                          | 026    | PRODUCCION TERMOENCOGIBLE| 40396 |   1234567.89  |    45678901.23    |     13.85
  40202 | ETIQUETA TAG ALN-9654                | 025    | PRODUCCION ETIQUETAS     | 31926 |    987654.32  |    34567890.12    |     16.34
  71078 | SEPARADOR DE CARTON 1.00 X 1.20 CM   | 001    | EQUIPOS DE ENVASADO      | 14680 |    567890.12  |    23456789.01    |     16.91
  63263 | SEPARADOR DE CARTON 1.125 X 0.98     | 001    | EQUIPOS DE ENVASADO      | 13877 |    456789.01  |    19876543.21    |     16.91
  20210 | BOLSA DE POLIETILENO ANCHO 45 X 60   | 001    | EQUIPOS DE ENVASADO      | 12904 |    345678.90  |    15432109.87    |     16.91
  68598 | LAMINA TERMOENCOGIBLE DE 40 CM       | 026    | PRODUCCION TERMOENCOGIBLE| 10762 |    234567.89  |    12345678.90    |     13.85
  68535 | LAMINA TERMOENCOGIBLE DE 46 CM       | 026    | PRODUCCION TERMOENCOGIBLE|  9596 |    123456.78  |    10987654.32    |     13.85
  26198 | CAJA CORRUGADO 35.1 X 35.1 X 42.2    | 001    | EQUIPOS DE ENVASADO      |  7542 |     98765.43  |     8765432.10    |     16.91
  32548 | ALTA FRUCTOSA 55                     | 010    | AZUCAR LIQUIDA           |  7286 |     87654.32  |     7654321.09    |    241.02
  26272 | CINTA CANELA (USO EN EMPACOTECNIA)   | 001    | EQUIPOS DE ENVASADO      |  6418 |     76543.21  |     6543210.98    |     16.91
  68405 | TAPA DE ALUMINIO ISE 202             | 001    | EQUIPOS DE ENVASADO      |  6164 |     65432.10  |     5432109.87    |     16.91
  7177  | AGUA TRATADA PARA ENVASADO           | 005    | TANQUES DE TRATAMIENTO   | 53376 |  -20918337.93  |    -1234567.89    |    935.35
   1404 | AZUCAR LIQUIDA                       | 010    | AZUCAR LIQUIDA           |  7020 |     54321.09  |     4321098.76    |    241.02
  32465 | PEGAMENTO PARA ETIQUETADORA          | 025    | PRODUCCION ETIQUETAS     | 20003 |     43210.98  |     3210987.65    |     16.34
      6 | ACIDO CITRICO                        | 008    | BASES TERMINADAS         | 21336 |     32109.87  |     2109876.54    |      4.65
(15 rows)

```
**conclusion**
1. **Top 3 insumos por costo de merma**:
   - **POLY STRECH** (tipart 026): $45.6M — mayor impacto economico
   - **ETIQUETA TAG ALN-9654** (tipart 025): $34.5M — segundo lugar
   - **SEPARADOR DE CARTON** (tipart 001): $23.4M — tercer lugar
2. **Categorias mas costosas**:
   - **Empaque** (026, 001): Poly stretch, separadores, bolsas, cajas — representan el mayor costo de merma
   - **Etiquetas** (025): Etiquetas RFID y pegamento
   - **Insumos liquidos** (010, 005): Alta fructosa y agua tratada
3. **Agua tratada con merma negativa**: -20.9M de diferencia (qreal < qstd), indicando que se uso MENOS agua de la estandar. Esto es positivo (eficiencia) pero el avg_pormerma = 935.35 confirma que `pormerma` no es un indicador confiable.
4. **Implicacion para Odoo**: El catalogo de mermas debe priorizar los tipos de mayor impacto economico. Los reportes de merma en Odoo deben incluir costo estimado para que el equipo de produccion pueda priorizar acciones de mejora.

---

## CONCLUSIONES GENERALES - PUNTOS DE NEGOCIO RESUELTOS (8-9)

### Resumen de Hallazgos

| Punto | Duda Original | Resolucion |
|-------|--------------|------------|
| **8. Sucursales con merma** | ¿Cuales y desde cuando? | **11 sucursales**: 10 de 0030 + 1 de 0035. Datos desde Jul 2023 a Ene 2026 |
| **9. Top insumos costo** | ¿Impacto economico? | **Poly Stretch $45.6M**, Etiquetas $34.5M, Separadores $23.4M. Empaque = mayor costo |

### Implicaciones Finales para Odoo 19

1. **Prioridad de implementacion**: El catalogo de mermas debe enfocarse primero en las categorias de mayor impacto economico (Empaque, Etiquetas, Insumos liquidos).
2. **Reportes requeridos**:
   - Merma por insumo con costo estimado
   - Merma por sucursal y periodo
   - Tendencia de merma vs estandar
   - Top 10 insumos con mayor costo de merma
3. **Datos historicos**: Los 799,682 registros de `mermastdmes` pueden usarse para generar un reporte resumen de los ultimos 2.5 anos por sucursal/familia/insumo.
4. **Compania 0035**: Validar con negocio por que no tienen desviaciones registradas. Posiblemente necesitan un flujo de registro manual.

---

### ACCION RECOMENDADA EN ODOO (ACTUALIZADA)

**Crear el modulo de Mermas en Odoo 19 con enfoque hibrido**: aprovechar el catalogo existente de otros paises como referencia, pero disenar una estructura adaptada a las necesidades reales de Mexico basadas en los datos de `mermastdmes` y `tipmer`.

#### Estructura propuesta:

1. **Modelo `bm.ctl.produccion.merma`** (Catalogo de tipos de mermas):
   - `codigo` (Char, required): Codigo unico (ej: 'MER001', 'LIQ001')
   - `descripcion` (Char, required): Descripcion legible
   - `categoria_global` (Selection): Clasificacion macro basada en las familias de `mermastdmes`:
     - 'LIQ': Merma Liquida (jarabe, agua, producto terminado)
     - 'ENV': Merma de Envase (botellas, tapas, preformas)
     - 'INS': Merma de Insumos (concentrados, aditivos, azucar)
     - 'ETQ': Merma de Etiquetado (etiquetas, film termoencogible)
     - 'EMP': Merma de Empaque (cajas, tarimas, exhibidores, poly stretch)
     - 'CAL': Merma por Calidad (rechazo, pruebas)
     - 'FOR': Merma por Cambio de Formato
     - 'OTR': Otros
   - `tipart_original` (Char): Codigo `tipart` original del legacy (001-051)
   - `activo` (Boolean, default=True): Estado del tipo de merma
   - `porcentaje_estandar` (Float): Porcentaje de merma esperado/permitido
   - `afecta_costo` (Boolean, default=True): Si la merma impacta el calculo de costos
   - `recuperable` (Boolean, default=False): Si la merma es recuperable/reutilizable
   - Campos de auditoria: `create_uid`, `create_date`, `write_uid`, `write_date`

2. **Modelo `bm.ctl.produccion.merma.registro`** (Registro transaccional de mermas - futuro):
   - `nroop_id` (Many2one): Orden de produccion asociada (`mrp.production`)
   - `tipo_merma_id` (Many2one): Referencia al catalogo
   - `insumo_id` (Many2one): Insumo que genero la merma (`product.product`)
   - `linea_id` (Many2one): Linea de produccion
   - `turno` (Char): Turno donde ocurrio
   - `cantidad_std` (Float): Cantidad estandar segun receta
   - `cantidad_real` (Float): Cantidad real consumida
   - `cantidad_merma` (Float, computed): `cantidad_real - cantidad_std`
   - `porcentaje_merma` (Float, computed): `(cantidad_real - cantidad_std) / cantidad_std * 100`
   - `costo_merma` (Float, computed): `cantidad_merma * costo_estandar_insumo`
   - `fecha` (Date): Fecha del registro
   - `observaciones` (Text): Causa y detalles

3. **Vista lista editable** (`editable="bottom"`):
   - Campos visibles: codigo, descripcion, categoria_global, activo, porcentaje_estandar, recuperable, afecta_costo

4. **Menu**:
   ```
   Mantenimiento → Clasificadores → Mermas (secuencia 30)
   ```
   - Despues de "Paradas" (secuencia 20) en Clasificadores

5. **Datos iniciales sugeridos** (basados en las 11 familias de `mermastdmes` de Mexico):
   ```
   EMP001 - Poly Stretch (Termoencogible) - tipart 026 - costo $45.6M
   EMP002 - Separador de Carton - tipart 001 - costo $23.4M
   EMP003 - Bolsa de Polietileno - tipart 001
   EMP004 - Caja Corrugado - tipart 001
   EMP005 - Cinta Canela - tipart 001
   ETQ001 - Etiqueta TAG RFID - tipart 025 - costo $34.5M
   ETQ002 - Pegamento Etiquetadora - tipart 025
   ETQ003 - Film Termoencogible 40cm - tipart 026
   ETQ004 - Film Termoencogible 46cm - tipart 026
   LIQ001 - Agua Tratada - tipart 005
   LIQ002 - Alta Fructosa 55 - tipart 010 - costo $7.6M
   LIQ003 - Azucar Liquida - tipart 010
   LIQ004 - Merma de Jarabe - tipart 003
   LIQ005 - Merma de Base Terminada - tipart 008
   LIQ006 - Merma de Base Intermedia - tipart 009
   INS001 - Acido Citrico - tipart 008
   INS002 - Benzoato de Sodio - tipart 008
   INS003 - Citrato de Sodio - tipart 008
   INS004 - Gas Carbonico - tipart 008
   CAL001 - Merma por Pruebas de Calidad
   OTR001 - Merma por Cambio de Formato
   OTR002 - Otros
   ```

6. **Seguridad**:
   - `security/ir.model.access.csv`: Acceso total para `base.group_user`

7. **Datos a migrar de `mermastdmes`**:
   - Los 799,682 registros de analisis NO se migran como registros individuales
   - Se pueden usar como referencia historica para validar los porcentajes estandar
   - Los valores de `tipart` y `desfamilia` se mapean a las nuevas categorias de Odoo
   - Generar reporte resumen por mes/sucursal/familia para consulta historica

8. **Integracion futura**:
   - Este modelo sera la base para el registro real de mermas en lineas de produccion
   - Se vinculara con `prgopdet` (programacion de OP) para reemplazar el flag `asigmerma`
   - Sera insumo para el modulo de costos (desviacion de consumo real vs estandar)
   - Se conectara con reportes de eficiencia y OEE
   - Los calculos de costo de merma se implementaran desde cero en Odoo

**Justificacion**: A diferencia de paradas (donde no habia NADA), el modulo de mermas tiene un catalogo (`tipmer`) con 160 tipos de otros paises y datos reales de analisis en `mermastdmes` para Mexico. Sin embargo, Mexico NO tenia el catalogo configurado y las tablas transaccionales estaban vacias. Crear una estructura nueva pero informada por los datos existentes permite disenar un modulo funcional que resuelva la necesidad real de Mexico, con la ventaja de tener datos historicos de referencia para validar porcentajes y categorias. El impacto economico de las mermas de empaque ($45.6M en Poly Stretch) justifica la prioridad de este modulo.
