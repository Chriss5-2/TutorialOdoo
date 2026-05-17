
### Probando program # 132 en la UI Odoo

#### 1. Catalogo de Turnos (Turno Definicion)

> **Que es:** La definicion base de los turnos globales. Equivale a la tabla legacy `bturno1f`.
> **Donde:** `Mantenimiento → Clasificadores → Turnos → Catalogo de Turnos` (lista editable)

| Campo | Formato | Ejemplo | Nota |
|---|---|---|---|
| Secuencia | Numero entero | `10`, `20`, `30` | Orden visual (multiplos de 10) |
| Codigo Turno | Numero entero | `1`, `2`, `3` | ID unico del turno |
| Descripcion | Texto | `PRIMER TURNO` | Nombre legible |
| Hora Inicio | Texto `HHMMSS` | `063000` | Hora 24h sin separadores |
| Hora Fin | Texto `HHMMSS` | `143000` | Si es menor que inicio = turno nocturno |

**Datos reales de la BD legacy (compania 0030):**

| Turno | Descripcion | Horario | Nocturno |
|---|---|---|---|
| 001 | PRIMER TURNO | 06:30 - 14:30 (`063000` - `143000`) | No |
| 002 | SEGUNDO TURNO | 14:30 - 22:00 (`143000` - `220000`) | No |
| 003 | TERCER TURNO | 22:00 - 06:30 (`220000` - `063000`) | Si (cruza dia) |

- El campo `Es Nocturno` se calcula solo: si `Hora Inicio > Hora Fin` → `True`
- Los campos de auditoria (Fecha Creacion, Hora Creacion, Usuario) se llenan automaticamente

---

#### 2. Horarios por Sucursal (Turno Horario)

> **Que es:** Asigna cada turno a una sucursal/planta especifica con sus horarios. Equivale a la tabla legacy `turno`.
> **Donde:** `Mantenimiento → Clasificadores → Turnos → Horarios por Sucursal` (lista editable)

| Campo | Formato | Ejemplo | Nota |
|---|---|---|---|
| Sucursal | Texto (codigo) | `0001`, `0068` | Codigo de planta/sucursal |
| Turno | Many2one (selector) | Seleccionar de lista | Referencia al turno del paso 1 |

**Campos automaticos** (se llenan desde el turno seleccionado via `related`): Codigo Turno, Hora Inicio, Hora Fin, Es Nocturno

**Datos reales de la BD legacy:**

| Sucursal | T1 | T2 | T3 |
|---|---|---|---|
| 0001 (Puebla) | 06:30-14:30 | 14:30-22:00 | 22:00-06:30 |
| 0068 (Monterrey) | 06:30-14:30 | 14:30-22:00 | 22:00-06:30 |
| 0108 | 06:30-14:30 | 14:30-22:00 | 22:00-06:30 |
| 0009 (otra cmp) | 07:00-15:00 | 15:00-23:00 | 23:00-07:00 |

Cada sucursal puede tener horarios distintos para el mismo turno.

---

#### 3. Configuracion Global (Produccion Config)

> **Que es:** Parametros generales de produccion por compania.
> **Donde:** `Mantenimiento → Clasificadores → Turnos → Configuracion Global` (lista editable)

| Campo | Formato | Ejemplo | Nota |
|---|---|---|---|
| Compania | Texto | `0030` | Codigo de compania (default `0030`) |
| Fecha Inicial | Numero juliano | `739812` | Fecha desde la cual se consideran datos |
| Turno por Defecto | Many2one (selector) | Seleccionar turno | Turno default para nuevas OP |

**Fecha juliana:** Se calcula como `(dias_desde_1_ene_del_anio) + 730000`. El campo `Fecha Inicial` (Date) se muestra automaticamente para referencia.

**Uso tipico:** Crear UN registro por compania con la fecha desde la cual quieres empezar a trabajar en el nuevo sistema.

---

#### Orden recomendado de ingreso

1. **Primero:** Crear los 3 turnos base en **Catalogo de Turnos** (T1, T2, T3)
2. **Segundo:** En **Horarios por Sucursal**, crear un registro por cada combinacion sucursal+turno que necesites
3. **Tercero:** En **Configuracion Global**, crear el registro de compania con fecha inicial y turno default

---

### Probando program # 162 en la UI Odoo

#### 1. Aprobacion de Formulas (Solicitud)

> **Que es:** Solicitud de activacion/modificacion de formulas de fabricacion con flujo de aprobacion multinivel. Equivale a las tablas legacy `csolactfor` (header) + `dsolactfor` (lineas).
> **Donde:** `Mantenimiento → Aprobacion de Formulas → Aprobacion de Formulas`

| Campo | Formato | Ejemplo | Nota |
|---|---|---|---|
| Numero Documento | Texto (auto) | `AFOR/00001` | Secuencia automatica |
| Compania | Texto | `0030` | Codigo de compania (default `0030`) |
| Transaccion | Texto | `AFOR` | Tipo de transaccion (default `AFOR`) |
| Fecha | Numero juliano | `739812` | Fecha de la solicitud |
| Solicitante | Numero (ID Empleado) | `1708248` | ID del empleado que solicita |
| Nivel Aprobacion | Numero entero | `1`, `2`, `3` | Nivel actual del flujo |
| Aprobador Actual | Numero (ID Empleado) | `6881` | Quien debe aprobar en este nivel |
| Status Aprobacion | Seleccion | `P` (Pendiente) | `P`=Pendiente, `A`=Aprobado, `R`=Rechazado, `C`=En Curso |
| Estado | Seleccion (statusbar) | `Borrador` | `draft` → `pending` → `approved`/`rejected`/`cancelled` |

**Botones del flujo (aparecen segun el estado):**

| Boton | Visible cuando | Accion |
|---|---|---|
| Enviar a Aprobacion | `state = draft` | Cambia a `pending`, inicia flujo |
| Aprobar | `state = pending` | Cambia a `approved`, registra fecha/hora |
| Rechazar | `state = pending` | Cambia a `rejected` |
| Cancelar | `state = draft` o `pending` | Anula la solicitud |
| Reiniciar a Borrador | `state = rejected` o `cancelled` | Vuelve a `draft` |

**Pestana "Lineas de Formula" (editable inline):**

| Campo | Formato | Ejemplo | Nota |
|---|---|---|---|
| Sucursal Formula | Texto | `0001` | Planta donde se aplica |
| Articulo (SKU) | Numero decimal | `524121.0` | Producto terminado |
| Insumo (Material) | Numero decimal | `7177.0` | Material de la formula |
| Linea | Texto | `L1` | Linea de produccion |
| Factor Conversion | Numero decimal | `18.8` | Factor de conversion |
| Accion | Seleccion | `N`, `M`, `E` | `N`=Nuevo, `M`=Modificar, `E`=Eliminar |
| Nivel Aprobacion | Numero entero | `1` | Nivel requerido |

**Pestana "Firmas de Aprobacion" (solo lectura):**
Muestra el historial de aprobaciones por nivel. Se llena automaticamente al aprobar/rechazar.

**Datos reales de la BD legacy (`forfab`):**

| Articulo | Material | Aprobador | Fecha Aprob | Hora Aprob |
|---|---|---|---|---|
| 524121 | 7177 | 1724308 | 0 | 000000 |
| 517262 | 8 | 1724308 | 739632 | 101951 |
| 81388 | 71741 | 29750 | 739458 | 112102 |

- En el legacy, muchas aprobaciones tienen fecha/hora vacias (solo se registra el ID del aprobador)
- En Odoo 19, al hacer clic en "Aprobar", se registra automaticamente fecha juliana y hora

---

#### 2. Configuracion de Aprobadores

> **Que es:** Define quien puede aprobar en cada nivel del flujo. Equivale a la tabla legacy `aprfor1f`.
> **Donde:** `Mantenimiento → Aprobacion de Formulas → Aprobadores` (lista editable)

| Campo | Formato | Ejemplo | Nota |
|---|---|---|---|
| Compania | Texto | `0030` | Codigo de compania (default `0030`) |
| Transaccion | Texto | `AFOR` | Tipo de transaccion (default `AFOR`) |
| Nivel | Numero entero | `1`, `2`, `3` | Nivel de aprobacion |
| Tipo Aprobacion | Seleccion | `L` (Lineal), `P` (Paralelo) | `L`=secuencial, `P`=simultaneo |
| Aprobador | Numero (ID Empleado) | `1708248` | ID del empleado aprobador |
| Estado | Seleccion | `A` (Activo), `I` (Inactivo) | Estado del configuracion |

**Tipos de aprobacion:**
- **Lineal (L):** Los niveles se aprueban en secuencia (1 → 2 → 3). Cada nivel debe aprobar antes de pasar al siguiente.
- **Paralelo (P):** Los niveles pueden aprobar simultaneamente. No hay orden obligatorio.

**Datos reales de la BD legacy (`aprfor1f`):**

| Compania | Transaccio | Nivel | Tipaprob | Aprobador | Estado |
|---|---|---|---|---|---|
| 0030 | AFOR | 1 | L | 1708248 | A |
| 0030 | AFOR | 2 | L | 6881 | A |
| 0030 | AFOR | 3 | L | 29750 | A |

---

#### 3. Historial de Firmas

> **Que es:** Trazabilidad completa de todas las aprobaciones/rechazos. Equivale a la tabla legacy `taprform1f`.
> **Donde:** `Mantenimiento → Aprobacion de Formulas → Historial de Firmas`

| Campo | Formato | Ejemplo | Nota |
|---|---|---|---|
| Numero Documento | Texto | `AFOR/00001` | Referencia a la solicitud |
| Nivel Aprobacion | Numero entero | `1`, `2`, `3` | Nivel donde se firmo |
| Empleado Autorizador | Numero (ID Empleado) | `1708248` | Quien firmo |
| Fecha Autorizacion | Numero juliano | `739812` | Fecha de la firma |
| Hora Autorizacion | Texto `HHMMSS` | `143000` | Hora de la firma |
| Status Aprobacion | Seleccion | `A`, `R`, `P` | `A`=Aprobado, `R`=Rechazado, `P`=Pendiente |
| Observaciones | Texto | `Formula correcta` | Comentarios del aprobador |

**Nota:** Esta vista es de solo lectura. Los registros se crean automaticamente cuando se aprueba/rechaza una solicitud desde la vista de "Aprobacion de Formulas".

---

#### Orden recomendado de uso

1. **Primero:** Configurar los aprobadores en **Configuracion de Aprobadores** (quien aprueba en cada nivel)
2. **Segundo:** Crear una nueva solicitud en **Aprobacion de Formulas**
   - Llenar datos generales (compania, fecha, solicitante)
   - Agregar lineas de formula en la pestana "Lineas de Formula"
3. **Tercero:** Enviar a aprobacion con el boton "Enviar a Aprobacion"
4. **Cuarto:** El aprobador correspondiente abre la solicitud y hace clic en "Aprobar" o "Rechazar"
5. **Quinto:** Consultar el **Historial de Firmas** para ver la trazabilidad completa

---

#### Flujo de estados visual

```
[Borrador] → (Enviar a Aprobacion) → [En Aprobacion] → (Aprobar) → [Aprobado]
                                                    → (Rechazar) → [Rechazado]
                                                    → (Cancelar) → [Cancelado]

[Rechazado] → (Reiniciar a Borrador) → [Borrador]
[Cancelado] → (Reiniciar a Borrador) → [Borrador]
```

**Colores en la lista de solicitudes:**
- **Azul claro:** Borrador (`draft`)
- **Amarillo:** En Aprobacion (`pending`)
- **Verde:** Aprobado (`approved`)
- **Rojo:** Rechazado o Cancelado (`rejected`, `cancelled`)

---

### Probando program # 133 en la UI Odoo

#### 1. Tipos de Paradas (Parada Definicion)

> **Que es:** Catalogo de tipos de paradas de produccion para registro de tiempos muertos y calculo de OEE.
> **Donde:** `Mantenimiento → Clasificadores → Paradas` (lista editable)

| Campo | Formato | Ejemplo | Nota |
|---|---|---|---|
| Codigo | Texto | `MEC001`, `ELE001` | ID unico del tipo de parada |
| Descripcion | Texto | `Falla de banda transportadora` | Descripcion legible |
| Categoria Global | Seleccion | `MEC` | `MEC`=Mecanica, `ELE`=Electrica, `OPE`=Operativa, `CAL`=Calidad, `MAT`=Falta Material, `MAN`=Mantenimiento, `OTR`=Otros |
| Codigo Detalle | Texto | `BANDA`, `MOTOR` | Subclasificacion opcional |
| Activo | Boolean | `True` | Estado del tipo de parada |
| Tiempo Estimado (min) | Numero decimal | `30.0` | Duracion estimada en minutos |
| Afecta OEE | Boolean | `True` | Si impacta el calculo de OEE |

**Datos iniciales sugeridos (17 tipos estandarizados):**

| Codigo | Descripcion | Categoria | Detalle |
|---|---|---|---|
| MEC001 | Falla de banda | MEC | BANDA |
| MEC002 | Falla de motor | MEC | MOTOR |
| MEC003 | Falla de sensor | MEC | SENSOR |
| MEC004 | Falla de valvula | MEC | VALVULA |
| ELE001 | Falla de PLC | ELE | PLC |
| ELE002 | Falla de tablero | ELE | TABLERO |
| OPE001 | Cambio de formato | OPE | FORMATO |
| OPE002 | Limpieza | OPE | LIMPIEZA |
| OPE003 | Ajuste de maquina | OPE | AJUSTE |
| CAL001 | Rechazo de producto | CAL | RECHAZO |
| CAL002 | Ajuste de calidad | CAL | AJUSTE |
| MAT001 | Falta de jarabe | MAT | JARABE |
| MAT002 | Falta de envases | MAT | ENVASES |
| MAT003 | Falta de etiquetas | MAT | ETIQUETAS |
| MAN001 | Mantenimiento preventivo | MAN | PREVENTIVO |
| MAN002 | Mantenimiento correctivo | MAN | CORRECTIVO |
| OTR001 | Otros | OTR | - |

**Campos automaticos:**
- `Nombre`: Se calcula como `{codigo} - {descripcion}`
- `Fecha/Hora/Usuario Creacion`: Se llenan automaticamente al crear
- `Fecha/Hora/Usuario Ultima Mod.`: Se actualizan automaticamente al editar

---

#### Orden recomendado de uso

1. **Primero:** Crear los tipos de paradas base en **Tipos de Paradas** (usar los 17 sugeridos o crear personalizados)
2. **Segundo:** Este catalogo sera la base para el registro real de paradas en lineas de produccion (futuro modulo)
3. **Tercero:** Se vinculara con lineas de produccion para analisis de eficiencia por linea y calculo de OEE

---

#### Notas tecnicas

- **Origen:** Creado desde cero en Odoo 19. Las tablas legacy (`agrparoee`, `agrupoe`, `agrupoe1`) estaban vacias (0 registros).
- **Menu:** Secuencia 20 bajo `mantenimiento_clasificadores` (despues de Turnos secuencia 10).
- **Vista:** Lista editable (`editable="bottom"`) para creacion rapida inline.
- **Integracion futura:** Este modelo sera el insumo principal para el calculo de OEE y registro de tiempos muertos en Odoo 19.

---

### Probando program # 137 en la UI Odoo

#### 1. Categorias de Lineas de Produccion (Catalogo)

> **Que es:** Catalogo de categorias de lineas de produccion para clasificar lineas fisicas y agruparlas en reportes de capacidad, eficiencia y costos. Equivale a la tabla legacy `mfameq1f`.
> **Donde:** `Mantenimiento → Clasificadores → Categorias de Lineas de Produccion` (seq 40). Tambien accesible desde `Costos → Costo SemiVariable → Variables de Produccion → Categoria Linea de Produccion` (seq 10). **Ambas rutas abren el mismo catalogo** — misma lista, mismos datos, misma funcionalidad. La duplicacion es intencional (igual que en el sistema legacy).

| Campo | Formato | Ejemplo | Nota |
|---|---|---|---|
| Codigo | Texto | `001`, `025` | Codigo de la familia de equipos (heredado del legacy) |
| Descripcion | Texto | `EQUIPOS DE ENVASADO` | Nombre legible de la categoria |
| Area Funcional | Texto | `027`, `025` | Codigo de area funcional (18 valores documentados) |
| Factor | Seleccion | `B` (Botella), `N` (No Botella) | Clasifica tipo de produccion. B=lineas de envasado/soplado/jarabes. N=etiquetas/termoencogible |
| Funcion | Seleccion | `N` (Normal), `G` (Global) | G=transversal a todas las plantas (solo etiquetas y termoencogible) |
| Almacen de Proceso | Texto | `83`, `85`, `53` | Codigo de almacen asociado (83=Produccion, 85=Bases, 86=Maquila, 53=Empaque) |
| Activo | Boolean | `True`/`False` | Estado de la categoria |

**Datos iniciales cargados (27 categorias — 15 activas + 12 inactivas del legacy):**

**Categorias activas (15):**

| Codigo | Descripcion | Area | Factor | Funcion | Almacen | Lineas Configuradas (legacy) |
|---|---|---|---|---|---|---|
| 001 | EQUIPOS DE ENVASADO | 027 | B | N | 83 | 62 |
| 002 | EQUIPOS DE SOPLADO | 026 | B | N | 83 | 0 |
| 003 | TANQUES DE JARABE | 025 | B | N | 83 | 1 |
| 005 | TANQUES DE TRATAMIENTO DE AGUA | 025 | B | N | 83 | 0 |
| 008 | BASES TERMINADAS | 032 | B | N | 85 | 0 |
| 009 | BASES INTERMEDIAS | 032 | B | N | 85 | 0 |
| 010 | AZUCAR LIQUIDA | 025 | B | N | 83 | 1 |
| 017 | UNIDAD DE PLOTEO | 801 | B | N | - | 1 |
| 019 | MAQUILA | 035 | B | N | 86 | 2 |
| 021 | REEMPAQUES | 051 | B | N | - | 0 |
| 025 | PRODUCCION ETIQUETAS | 031 | N | G | 53 | 0 |
| 026 | PRODUCCION TERMOENCOGIBLE | 065 | N | G | 53 | 1 |
| 027 | PRODUCCION BOTELLA | 022 | B | N | 83 | 0 |
| 051 | PRODUCCION EXHIBIDORES | 072 | B | N | 53 | 2 |
| 054 | EXTRUIDO SNACKS | - | - | N | - | 0 |

**Categorias inactivas (12, active=False):**

| Codigo | Descripcion | Motivo probable |
|---|---|---|
| 004 | LAVADORAS | Proceso discontinuado |
| 006 | ACONDICIONADOS | Proceso discontinuado |
| 007 | INYECTORAS | Proceso discontinuado |
| 011 | COMPRESION | Proceso discontinuado |
| 012 | AGUA EMBOTELLADA | Linea descontinuada |
| 013 | ISOTONICAS | Inactiva pero con 2 lineas en caplinea (inconsistencia a validar) |
| 014 | AZUCAR LIQUIDA | Duplicada con 010, area incorrecta (101) |
| 015 | ENVASADOS JARABES TERMINADOS | Proceso discontinuado |
| 016 | NECTARES | Linea descontinuada |
| 018 | TANQUES DE JARABE SIMPLE | Proceso discontinuado |
| 020 | EQUIPOS DE HIELO | Proceso discontinuado |
| 050 | TRATAMIENTO DE AGUA CERVEZA | No aplica a Mexico bebidas |

**Campos automaticos:**
- `Nombre`: Se calcula como `{efamilia} - {descripcion}`
- `Fecha/Hora/Usuario Creacion`: Se llenan automaticamente al crear
- `Fecha/Hora/Usuario Ultima Mod.`: Se actualizan automaticamente al editar

**Filtros disponibles en el Search View:**
- **Activos:** Muestra solo categorias activas
- **Inactivos:** Muestra solo categorias inactivas
- **Group By Factor:** Agrupa por factor (Botella / No Botella)
- **Group By Funcion:** Agrupa por funcion (Normal / Global)
- **Group By Area:** Agrupa por area funcional
- **Group By Almacen:** Agrupa por almacen de proceso

---

#### Orden recomendado de uso

1. **Primero:** Revisar el catalogo pre-cargado en **Categorias de Lineas de Produccion** (`Mantenimiento → Clasificadores → Categorias de Lineas`). Ya vienen las 15 activas y 12 inactivas del legacy.
2. **Segundo:** Verificar el caso de `013 ISOTONICAS` — inactiva en el legacy pero con 2 lineas fisicas configuradas en `caplinea`. Si las lineas existen, reactivar y revisar factor (probablemente B por ser envasado).
3. **Tercero:** Verificar el caso de `014 AZUCAR LIQUIDA` (inactiva) vs `010 AZUCAR LIQUIDA` (activa) — son duplicadas. Mantener solo 010.
4. **Cuarto:** Si en el futuro se configura Inventario en Odoo, mapear los codigos `almproc` (83, 85, 86, 53) a `stock.warehouse` via External ID.
5. **Quinto:** Este catalogo sera la base para los modulos futuros de lineas de produccion, capacidad y costos semi-variables.

---

#### Notas tecnicas

- **Origen:** Migracion directa de la tabla legacy `mfameq1f`. 397 registros para Mexico (0030) distribuidos en 127 sucursales, pero solo 10 sucursales operativas (las demas son zombi con 1 registro). Catalogo identico compartido con Peru (0032) y Ecuador (0036).
- **Columnas excluidas:** De las 28 columnas originales, se migraron solo 10. Se excluyeron: 11 campos bytea (flags de UI del legacy, dump hex confirmo que son booleanos F/T sin uso transaccional), `codagru` (siempre vacio en 3,429 registros verificados), `nivcost` (97% en default 0), campos de auditoria `sucursal` (no se replica por sucursal en Odoo).
- **Menu principal:** Secuencia 40 bajo `mantenimiento_clasificadores` (despues de Mermas secuencia 30).
- **Menu secundario:** Secuencia 10 bajo `cost_costSeVa_varProduccion_menu` en Costos (duplicado intencional, igual que en el legacy).
- **Vista:** Lista editable (`editable="bottom"`) para creacion y edicion rapida inline.
- **Catalogo global:** No usa `company_id`. Las 27 categorias son identicas para Mexico, Peru y Ecuador. Si una compañia necesita categorias exclusivas, se agregan con company_id especifico.
- **Warning ISOTONICAS:** La categoria `013 ISOTONICAS` esta inactiva en TODAS las sucursales de 0030, pero tiene 2 lineas configuradas en `caplinea`. Validar con negocio si debe reactivarse.
- **Integracion futura:** Este modelo sera referenciado por: lineas de produccion fisica (`Many2one` futuro), capacidad de linea (`caplinea` → 553 registros), tipos de tarima (`ttarima` → 24 registros), y modulos de costos semi-variables.

### Probando program # 135 en la UI Odoo

#### 1. Tipos de Mermas (Catalogo)

> **Que es:** Catalogo de tipos de mermas o desperdicios de produccion para clasificar perdidas durante la fabricacion.
> **Donde:** `Mantenimiento → Clasificadores → Mermas` (lista editable)

| Campo | Formato | Ejemplo | Nota |
|---|---|---|---|
| Codigo | Texto | `EMP001`, `ETQ001`, `LIQ001` | ID unico del tipo de merma |
| Descripcion | Texto | `Poly Stretch`, `Etiqueta TAG RFID` | Descripcion legible |
| Categoria Global | Seleccion | `EMP` | `EMP`=Empaque, `ETQ`=Etiquetado, `LIQ`=Liquidos, `INS`=Insumos, `CAL`=Calidad, `FOR`=Cambio Formato, `OTR`=Otros |
| Tipart Original (Legacy) | Texto | `026`, `001`, `008` | Codigo tipart del sistema legacy para trazabilidad |
| Porcentaje Estandar (%) | Numero decimal | `13.85`, `16.91` | Porcentaje de merma esperado/permitido |
| Recuperable | Boolean | `True`/`False` | Si la merma es recuperable/reutilizable |
| Afecta Costo | Boolean | `True`/`False` | Si impacta el calculo de costos |
| Activo | Boolean | `True` | Estado del tipo de merma |

**Datos iniciales cargados (22 tipos basados en las 11 familias de `tipart` del legacy):**

| Codigo | Descripcion | Categoria | Tipart | % Estandar | Recuperable |
|---|---|---|---|---|---|
| EMP001 | Poly Stretch | EMP | 026 | 13.85 | No |
| EMP002 | Separador de Carton | EMP | 001 | 16.91 | No |
| EMP003 | Bolsa de Polietileno | EMP | 001 | 16.91 | No |
| EMP004 | Caja Corrugado | EMP | 001 | 16.91 | No |
| EMP005 | Cinta Canela (Empacotecnia) | EMP | 001 | 16.91 | No |
| ETQ001 | Etiqueta TAG RFID | ETQ | 025 | 16.34 | No |
| ETQ002 | Pegamento para Etiquetadora | ETQ | 025 | 16.34 | No |
| ETQ003 | Film Termoencogible 40cm | ETQ | 026 | 13.85 | No |
| ETQ004 | Film Termoencogible 46cm | ETQ | 026 | 13.85 | No |
| LIQ001 | Agua Tratada para Envasado | LIQ | 005 | 0.00 | Si |
| LIQ002 | Alta Fructosa 55 | LIQ | 010 | 241.02 | No |
| LIQ003 | Azucar Liquida | LIQ | 010 | 241.02 | No |
| LIQ004 | Merma de Jarabe | LIQ | 003 | 0.39 | No |
| LIQ005 | Merma de Base Terminada | LIQ | 008 | 4.65 | No |
| LIQ006 | Merma de Base Intermedia | LIQ | 009 | 0.68 | No |
| INS001 | Acido Citrico | INS | 008 | 4.65 | No |
| INS002 | Benzoato de Sodio | INS | 008 | 4.65 | No |
| INS003 | Citrato de Sodio | INS | 008 | 4.65 | No |
| INS004 | Gas Carbonico | INS | 008 | 4.65 | No |
| CAL001 | Merma por Pruebas de Calidad | CAL | - | 0.00 | No |
| FOR001 | Merma por Cambio de Formato | FOR | - | 0.00 | No |
| OTR001 | Otros | OTR | - | 0.00 | No |

**Campos automaticos:**
- `Nombre`: Se calcula como `{codigo} - {descripcion}`
- `Fecha/Hora/Usuario Creacion`: Se llenan automaticamente al crear
- `Fecha/Hora/Usuario Ultima Mod.`: Se actualizan automaticamente al editar

**Filtros disponibles:**
- **Activos:** Muestra solo los tipos activos
- **Recuperables:** Muestra solo los tipos marcados como recuperables
- **Group By Categoria:** Agrupa por categoria global (EMP, ETQ, LIQ, etc.)

---

#### 2. Registro de Mermas (Transaccional)

> **Que es:** Registro de mermas reales por orden de produccion con calculo automatico de cantidad, porcentaje y costo.
> **Donde:** `Producción → Ingreso de Paradas y Mermas → Ingreso de Mermas` (lista editable)

| Campo | Formato | Ejemplo | Nota |
|---|---|---|---|
| Fecha | Fecha | `2026-05-13` | Fecha del registro (default: hoy) |
| Orden de Produccion | Texto | `PALP24000001` | Numero de OP asociada |
| Tipo de Merma | Many2one (selector) | `EMP001 - Poly Stretch` | Referencia al catalogo del paso 1 |
| Codigo Insumo | Numero entero | `36447` | Codigo del insumo que genero la merma |
| Descripcion Insumo | Texto | `POLY STRECH` | Descripcion del insumo |
| Linea | Texto | `L1`, `L4` | Linea de produccion donde ocurrio |
| Turno | Texto | `T1`, `T3` | Turno donde ocurrio |
| Cantidad Estandar | Numero decimal | `1000.0` | Cantidad segun receta |
| Cantidad Real | Numero decimal | `1138.5` | Cantidad real consumida |
| Cantidad Merma | Numero (computed) | `138.5` | `Real - Estandar` (automatico) |
| Porcentaje Merma (%) | Numero (computed) | `13.85` | `(Merma / Estandar) * 100` (automatico) |
| Costo Estandar Unitario | Numero decimal | `0.50` | Costo por unidad del insumo |
| Costo Merma | Numero (computed) | `69.25` | `Cantidad Merma * Costo Estandar` (automatico) |
| Observaciones | Texto | `Desperdicio en etiquetadora` | Causa y detalles |

**Decoracion visual en la lista:**
- **Rojo:** Porcentaje de merma > 10% (desviacion critica)
- **Naranja:** Porcentaje de merma > 5% (desviacion moderada)

**Filtros disponibles:**
- **Hoy / Esta Semana / Este Mes:** Filtros temporales rapidos
- **Merma Alta (>10%):** Muestra solo registros con desviacion critica
- **Con Costo:** Muestra solo registros con costo de merma > 0
- **Group By:** Tipo de Merma, OP, Fecha

---

#### Orden recomendado de uso

1. **Primero:** Verificar los tipos de merma en **Tipos de Mermas** (`Mantenimiento → Clasificadores → Mermas`). Ya vienen 22 tipos pre-cargados. Agregar o modificar segun necesidad.
2. **Segundo:** Registrar mermas reales en **Ingreso de Mermas** (`Producción → Ingreso de Paradas y Mermas → Ingreso de Mermas`).
   - Seleccionar la OP, tipo de merma e insumo
   - Ingresar cantidad estandar (de receta) y cantidad real (consumida)
   - Odoo calcula automaticamente la merma, porcentaje y costo
3. **Tercero:** Usar los filtros y group by para analizar:
   - Que tipos de merma ocurren con mas frecuencia
   - Que OPs tienen mayor desviacion
   - Que insumos generan mas costo de merma

---

#### Notas tecnicas

- **Origen:** Creado desde cero en Odoo 19 con enfoque hibrido. El catalogo legacy `tipmer` tenia 160 registros pero NINGUNO para Mexico. La tabla `mermastdmes` tenia 799,682 registros de analisis batch pero el campo `pormerma` era un factor no estandarizado (valores anomalous como 935%, 241%). Las tablas transaccionales (`merppro`, `merxlin`, `mcatppres`, `tproin1`) estaban vacias (0 registros).
- **Menu Catalogo:** Secuencia 30 bajo `mantenimiento_clasificadores` (despues de Paradas secuencia 20).
- **Menu Registro:** Bajo `Producción → Ingreso de Paradas y Mermas` (sequence 20, despues de Ingreso de Paradas).
- **Vista:** Lista editable (`editable="bottom"`) para creacion rapida inline en ambos modelos.
- **Campos legacy:** Se mantiene `tipart_original` para trazabilidad con los datos historicos de `mermastdmes`.
- **Integracion futura:** Cuando se instalen los modulos `product` y `mrp`, los campos `insumo_codigo` y `nroop` podran reemplazarse por Many2one a `product.product` y `mrp.production` para obtener automaticamente costos y recetas.
- **Impacto economico:** Los tipos EMP y ETQ representan el mayor costo de merma historico: Poly Stretch ($45.6M), Etiquetas ($34.5M), Separadores ($23.4M).

---

### Probando program # 138 en la UI Odoo

#### 1. Familia de Produccion (Configuracion por Sucursal)

> **Que es:** Configuracion que activa o desactiva categorias de lineas de produccion por sucursal. Equivale a la tabla legacy `sucproc`. Define que tipos de produccion (Envasado, Jarabes, Maquila, Reempaques) estan operativos en cada planta. **No es** un catalogo de familias de articulo (gaseosas, jugos, agua) — eso lo maneja `mfamil1f` (inventario contable).
> **Donde:** `Mantenimiento → Configuraciones → Familia de Produccion` (seq 10 — primer item de Configuraciones)

| Campo | Formato | Ejemplo | Nota |
|---|---|---|---|
| Sucursal | Many2one (selector) | `0001 - Puebla` | Planta donde se activa/desactiva la categoria |
| Categoria Linea | Many2one (selector) | `001 - EQUIPOS DE ENVASADO` | Referencia al catalogo del Program #137 |
| Activo | Boolean | `True` / `False` | Estado de la configuracion (activo = `A`, inactivo = `I`) |

**Datos iniciales cargados (16 registros — 4 sucursales × 4 categorias del legacy `sucproc`):**

| Sucursal | Categoria | Codigo | Descripcion Categoria |
|---|---|---|---|
| 0001 (Puebla) | 001 | 001 | EQUIPOS DE ENVASADO |
| 0001 (Puebla) | 003 | 003 | TANQUES DE JARABE |
| 0001 (Puebla) | 019 | 019 | MAQUILA |
| 0001 (Puebla) | 021 | 021 | REEMPAQUES |
| 0068 (Monterrey) | 001 | 001 | EQUIPOS DE ENVASADO |
| 0068 (Monterrey) | 003 | 003 | TANQUES DE JARABE |
| 0068 (Monterrey) | 019 | 019 | MAQUILA |
| 0068 (Monterrey) | 021 | 021 | REEMPAQUES |
| 0070 | 001 | 001 | EQUIPOS DE ENVASADO |
| 0070 | 003 | 003 | TANQUES DE JARABE |
| 0070 | 019 | 019 | MAQUILA |
| 0070 | 021 | 021 | REEMPAQUES |
| 0108 | 001 | 001 | EQUIPOS DE ENVASADO |
| 0108 | 003 | 003 | TANQUES DE JARABE |
| 0108 | 019 | 019 | MAQUILA |
| 0108 | 021 | 021 | REEMPAQUES |

**Campos automaticos:**
- `Nombre`: Se calcula como `{codigo_sucursal} / {codigo_categoria}`. Ejemplo: `0001 / 001`, `0068 / 019`
- `Fecha/Hora/Usuario Creacion`: Se llenan automaticamente al crear
- `Fecha/Hora/Usuario Ultima Mod.`: Se actualizan automaticamente al editar
- `Compania`: Se asigna automaticamente (`self.env.company`)

**Filtros disponibles en el Search View:**
- **Activos:** Muestra solo las configuraciones activas
- **Inactivos:** Muestra solo las configuraciones inactivas
- **Group By Sucursal:** Agrupa por planta (para ver que categorias tiene cada sucursal)
- **Group By Categoria:** Agrupa por categoria de linea (para ver en que sucursales esta activa cada categoria)

---

#### Orden recomendado de uso

1. **Primero:** Revisar los 16 registros pre-cargados en **Familia de Produccion** (`Mantenimiento → Configuraciones → Familia de Produccion`). Verificar que las 4 sucursales tienen las 4 categorias activas.
2. **Segundo:** Si una sucursal deja de operar temporalmente una categoria (ej: la sucursal 0070 no produce maquila este mes), desactivar el registro correspondiente con el switch `Activo`.
3. **Tercero:** Si se abre una nueva sucursal o se reactiva una categoria, crear un nuevo registro seleccionando Sucursal y Categoria Linea. El switch activo viene prendido por defecto.
4. **Cuarto:** Si se necesita agregar categorias adicionales (Soplado, Agua, Bases, Azucar, etc.), crearlas en el catalogo de **Categorias de Lineas** (Program #137) y luego activarlas por sucursal en esta pantalla.

---

#### Notas tecnicas

- **Origen:** Migracion directa de la tabla legacy `sucproc` con 16 registros para Mexico (0030). La tabla `sucproc` es minimalista: PK `(compania, sucursal, efamilia)` + campo `estado` (A/I) + auditoria. La equivalencia `efamilia` del legacy se resuelve via Many2one a `bm.ctl.produccion.categoria.linea`.
- **Relacion Program #137 ↔ #138:** El #137 es "que categorias existen" (catalogo maestro de 27 categorias). El #138 es "cuales estan prendidas en cada planta" (configuracion 16 registros). Son dos caras de la misma moneda con dos accesos distintos en el menu: Clasificadores vs Configuraciones.
- **Por que solo 4 de 27 categorias:** Las 4 categorias configuradas en `sucproc` (001 Envasado, 003 Jarabes, 019 Maquila, 021 Reempaques) son las lineas de produccion **directas** — las que transforman materia prima en producto terminado. Las otras 11 categorias activas del catalogo #137 (Soplado, Agua, Bases, Azucar, Ploteo, Etiquetas, Termoencogible, Botella, Exhibidores, Snacks) son lineas **auxiliares/intermedias** que se activan implicitamente desde otros modulos.
- **Por que solo 4 de 10 sucursales:** Solo las sucursales con produccion directa (0001, 0068, 0070, 0108) tienen configuracion en `sucproc`. Las otras 6 sucursales operativas (0086, 0112, 0113, 0114, 0115, 0116) heredan configuracion de la sucursal principal.
- **Menu:** Secuencia 10 bajo `mant_configuraciones_menu` (primer item de Configuraciones).
- **Vista:** Lista editable (`editable="bottom"`) con solo 3 columnas: Sucursal, Categoria, Activo. Minimalista e intuitiva para activar/desactivar con un clic.
- **Modelo independiente (no `_inherits`):** `sucproc` tiene su propia PK y sus propios campos de auditoria, distintos de `mfameq1f`. El modelo usa Many2one a `bm.ctl.produccion.categoria.linea` en lugar de herencia.
- **Seguridad:** Acceso total (CRUD) para `base.group_user`. Cualquier usuario autenticado puede gestionar la configuracion.
- **Integracion futura:** Este modelo servira como validacion para:
    - Creacion de lineas fisicas de produccion (validar que la combinacion sucursal-categoria este activa)
    - Planificacion de produccion (DRP) — restringir planificacion a categorias activas por sucursal
    - Reportes de capacidad instalada por sucursal (cruzar con `caplinea`)
    - Control de acceso por sucursal (restringir vistas de usuario a su planta)
    - Wizard de activacion/desactivacion masiva (copiar config de una sucursal a otra)

---

### Probando program # 574 en la UI Odoo

#### 1. Procesos Productivos (Catalogo)

> **Que es:** Catalogo de procesos productivos que componen la cadena de fabricacion de un producto. Define la secuencia de operaciones (Soplado → Jarabe → Bases → Llenado → Etiquetado → Empacado) y el area funcional asociada de cada proceso. Es la base para el plan de produccion y el calculo de tiempos estandar.
> **Donde:** `Mantenimiento → Configuraciones → Configura Procesos Productivos` (seq 20 — segundo item de Configuraciones, despues de Familia de Produccion)

| Campo | Formato | Ejemplo | Nota |
|---|---|---|---|
| Codigo | Texto (3 letras) | `SOP`, `LLE`, `ETQ` | Codigo abreviado del proceso |
| Descripcion | Texto | `Soplado`, `Llenado / Envasado` | Nombre legible del proceso |
| Secuencia | Numero entero | `10`, `20`, `40` | Orden en la cadena productiva (multiplos de 10) |
| Categoria Linea | Many2one (selector) | `002 - EQUIPOS DE SOPLADO` | Area funcional del Program #137 |
| Activo | Boolean | `True` / `False` | Estado del proceso |

**Datos iniciales cargados (6 procesos — cadena completa de bebidas):**

| Codigo | Descripcion | Secuencia | Categoria (#137) | Area |
|---|---|---|---|---|
| SOP | Soplado | 10 | 002 - EQUIPOS DE SOPLADO | 026 |
| JAR | Preparacion de Jarabe | 20 | 003 - TANQUES DE JARABE | 025 |
| BAS | Preparacion de Bases | 30 | 008 - BASES TERMINADAS | 032 |
| LLE | Llenado / Envasado | 40 | 001 - EQUIPOS DE ENVASADO | 027 |
| ETQ | Etiquetado | 50 | 025 - PRODUCCION ETIQUETAS | 031 |
| EMP | Empacado | 60 | 021 - REEMPAQUES | 051 |

**Flujo de la cadena productiva:**

```
[SOP 10] → [JAR 20] → [BAS 30] → [LLE 40] → [ETQ 50] → [EMP 60]
 Soplado    Jarabe     Bases      Llenado    Etiquetado  Empacado
 (botellas) (mezcla)   (conc.)    (envasado)  (etiquetas) (cajas/tarimas)
```

**Campos automaticos:**
- `Nombre`: Se calcula como `{codigo} - {descripcion}`. Ejemplo: `SOP - Soplado`, `LLE - Llenado / Envasado`
- `Fecha/Hora/Usuario Creacion`: Se llenan automaticamente al crear
- `Fecha/Hora/Usuario Ultima Mod.`: Se actualizan automaticamente al editar
- `Compania`: Se asigna automaticamente (`self.env.company`)

**Filtros disponibles en el Search View:**
- **Activos:** Muestra solo procesos activos
- **Inactivos:** Muestra solo procesos inactivos
- **Group By Categoria:** Agrupa por categoria de linea para ver que procesos pertenecen a cada area

---

#### Orden recomendado de uso

1. **Primero:** Revisar los 6 procesos pre-cargados en **Configura Procesos Productivos** (`Mantenimiento → Configuraciones → Configura Procesos Productivos`). Verificar que cubren la cadena productiva de la planta.
2. **Segundo:** Verificar que las categorias del Program #137 referenciadas (001, 002, 003, 008, 021, 025) esten activas en las sucursales via Program #138 (Familia de Produccion).
3. **Tercero:** Agregar procesos adicionales si la planta tiene operaciones especiales (ej: `LAV` Lavado de Botellas entre Soplado y Jarabe con secuencia 15, o `TAP` Tapado entre Llenado y Etiquetado con secuencia 45).
4. **Cuarto:** Ajustar la secuencia si el orden real de produccion difiere del estandar. Usar multiplos de 10 para facilitar inserciones futuras.

---

#### Notas tecnicas

- **Origen:** Creado desde cero en Odoo 19 ("Clean Slate"). La tabla legacy `mproprod1f` estaba completamente vacia (0 registros). Los Stored Procedures asociados (`USP_PROCESO_PRODUCCION`, `USP_PROD_PROCPROD_ELIMINAVALIDA`, `PR_ERP_FNZ_QRY_WS_CREAPROCESOFABRICACION`) no existen en `mxbdaje_local` — eran de otras bases del ecosistema Big Magic y nunca se desplegaron en Mexico. Sin datos que migrar, sin logica que replicar.
- **Relacion Program #137 → #574:** #137 cataloga las areas funcionales (Envasado, Soplado, Etiquetas...). #574 asigna cada proceso al area correcta via Many2one con `ondelete='restrict'` — no se puede borrar una categoria si tiene procesos configurados.
- **Relacion Program #138 → #574:** #138 define que categorias operan en cada sucursal. #574 hereda esa restriccion implicitamente: si la sucursal 0070 no tiene activa la categoria 001 (Envasado), no deberia poder asignar el proceso LLE (Llenado) a lineas de esa sucursal.
- **Menu:** Secuencia 20 bajo `mant_configuraciones_menu` (segundo item de Configuraciones, despues de Familia de Produccion seq 10).
- **Vista:** Lista editable (`editable="bottom"`) con 5 columnas: codigo, descripcion, secuencia, categoria, activo.
- **Secuencias en multiplos de 10:** Permite insertar procesos intermedios sin renumerar (ej: insertar `TAP` Tapado en secuencia 45 entre Llenado y Etiquetado).
- **Independencia de `mrp`:** El modelo no depende del modulo de Manufactura de Odoo. La conexion con Work Centers (`mrp.workcenter`) queda para integracion futura via el campo `categoria_linea_id`.
- **Seguridad:** Acceso total (CRUD) para `base.group_user`.
- **Integracion futura:** Este modelo sera la base para:
    - Hoja de ruta de fabricacion (secuencia de operaciones por OP)
    - Calculo de tiempos estandar por SKU (suma de tiempos por proceso)
    - Asignacion de lineas fisicas a procesos (Many2one desde `bm.ctl.produccion.linea`)
    - Mapeo a `mrp.routing.workcenter` si se adopta Manufactura de Odoo
