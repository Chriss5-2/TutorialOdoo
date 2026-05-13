
### Probando program # 132 en la UI Odoo

#### 1. Catalogo de Turnos (Turno Definicion)

> **Que es:** La definicion base de los turnos globales. Equivale a la tabla legacy `bturno1f`.
> **Donde:** `Mantenimiento → Clasificadores → Turnos → Catalogo de Turnos` (lista editable)

| Campo | Formato | Ejemplo | Nota |
|---|---|---|---|
| Codigo Turno | Numero entero | `1`, `2`, `3` | ID unico del turno |
| Descripcion | Texto | `PRIMER TURNO` | Nombre legible |
| Secuencia | Numero entero | `10`, `20`, `30` | Orden visual (multiplos de 10) |
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

