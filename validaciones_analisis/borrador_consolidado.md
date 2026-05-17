# Consolidado de Implementación — Control de Producción AJE México
## Migración del Sistema Legacy Big Magic ERP a Odoo 19

---

## 1. ¿De qué se trata este proyecto?

AJE (Ajegroup) — una de las embotelladoras más grandes de Latinoamérica — opera plantas de producción de bebidas en México bajo un sistema ERP legacy llamado **Big Magic**. Dentro de ese sistema, el módulo **BM-CTL-Produccion** contiene la configuración maestra de producción: turnos, tipos de paradas, mermas, categorías de líneas, familias por sucursal, aprobación de fórmulas y procesos productivos.

El objetivo de este proyecto fue **migrar algunas funciones** (de momento) del sistema legacy a **Odoo 19**, una plataforma ERP moderna. Pero no se trató de una copia ciega: cada función fue **validada contra la base de datos real de producción de México** para entender qué existía realmente, qué se usaba, qué estaba roto, y tomar decisiones de arquitectura informadas.

**El resultado:** 7 programas implementados como modelos de Odoo 19 con sus vistas, menús, datos iniciales y seguridad, listos para operar en un ambiente productivo moderno.

---

## 2. La metodología: No copiar — auditar, decidir, construir

Antes de escribir una sola línea de código, cada programa pasó por un proceso de **validación y análisis** contra la base de datos real `mxbdaje_local` (PostgreSQL). Esto fue crítico porque:

- La documentación oficial del sistema legacy era escasa o inexistente para varias funciones.
- Muchas tablas existían estructuralmente pero **nunca se poblaron** con datos.
- Otras tablas tenían datos pero para **otros países** (Perú, Ecuador), no para México.
- Campos que parecían importantes resultaron ser **basura técnica** (100% vacíos, obsoletos).

### El proceso de validación consistió en 4 pasos para cada programa:

1. **Exploración de diccionario de datos** — consultas SQL para encontrar todas las tablas y columnas relacionadas con la función.
2. **Auditoría de volumetría** — contar registros, identificar qué compañías y sucursales tenían datos, distinguir datos activos de basura.
3. **Rastreo de dependencias** — buscar relaciones con otras tablas, triggers, stored procedures y vistas.
4. **Decisión de arquitectura** — con base en los hallazgos, decidir si migrar, reconstruir o crear desde cero.

### ¿Por qué esto es importante?

Porque el sistema legacy tenía **30 años de capas acumuladas**. Algunas funciones nunca se usaron. Otras se usaban de formas no documentadas. Sin esta auditoría, habríamos migrado esqueletos vacíos, campos inservibles y lógica muerta a Odoo — arrastrando deuda técnica al nuevo sistema.

---

## 3. Los  Programas 

### Program #132 — Turnos  (de produccion)
**"Dejar de usar hojas sueltas para pasarnos a un cuaderno organizado"**

| | Legacy (Big Magic) | Odoo 19 |
|---|---|---|
| **Qué existía** | 4 tablas: `bturno1f` (definiciones), `turno` (horarios por sucursal), `turnoxop` (37K registros de asignación), `relacionturno` (mapeo a sistema externo) | 3 modelos unificados: `turno.definicion`, `turno.horario`, `produccion.config` |
| **Problema** | Definiciones y horarios en tablas separadas sin relación explícita. Horarios como texto crudo (`HHMMSS`) sin validación. Sin detección de turnos nocturnos. | Modelos conectados con Many2one. Detección automática de nocturnidad (`horainicio > horafin`). Auditoría completa con fechas julianas para compatibilidad. |
| **Dato clave** | 30 definiciones base, 55 horarios por sucursal, 0 triggers — migración limpia | Catálogo de turnos (seq 10), Horarios por Sucursal (seq 20), Configuración Global (seq 30) |

> **Analogía:** En el legacy era como tener los nombres de los turnos en una libreta y los horarios en otra distinta, sin saber cuál correspondía a cuál. En Odoo, cada turno se define una vez y se asigna a cada sucursal con sus horarios — como un cuaderno con pestañas.

---

### Program #133 — Tipos de Paradas
**"Construir el catálogo que nunca existió"**

| | Legacy (Big Magic) | Odoo 19 |
|---|---|---|
| **Qué existía** | Tablas OEE (`agrparoee`, `agrupoe`, `agrupoe1`) con estructura pero **0 registros**. Solo un flag boolean `asigparada` en órdenes de producción que decía "hubo parada" sin decir de qué tipo ni cuánto duró. | Modelo `bm.ctl.produccion.parada` con 7 categorías globales, código, descripción, tiempo estimado y flag de impacto en OEE. |
| **Problema** | Era como un registro de asistencia que solo dice "alguien faltó" sin decir quién ni por qué. | Catálogo completo desde cero. 7 categorías: Mecánica, Eléctrica, Operativa, Calidad, Falta Material, Mantenimiento, Otros. |
| **Hallazgo** | **0 triggers, 0 stored procedures, 0 vistas** — no había lógica oculta que replicar. Oportunidad de "Clean Slate". | Vista lista editable (`editable="bottom"`). Menú: `Mantenimiento → Clasificadores → Paradas` (seq 20). |

> **Analogía:** El legacy tenía los anaqueles vacíos. Las repisas existían pero nunca se les puso nada. En Odoo construimos el catálogo completo desde cero, con cada tipo de parada documentado y listo para usarse cuando se implemente el registro de paradas en línea.

---

### Program #135 — Mermas de Producción
**"Construir lo que existía a medias"**

| | Legacy (Big Magic) | Odoo 19 |
|---|---|---|
| **Qué existía** | Catálogo `tipmer` con 160 registros pero **ninguno para México**. Tabla `mermastdmes` con 799,682 registros de análisis batch (cierre de mes) pero con campo `pormerma` anómalo (935% no es un porcentaje real). Tablas transaccionales (`merppro`, `merxlin`, `mcatppres`) **vacías**. | 2 modelos: `bm.ctl.produccion.merma` (catálogo) + `bm.ctl.produccion.merma.registro` (transaccional). |
| **Problema** | México tenía reportes mensuales de "cuánto se desperdició" pero sin poder registrar "qué se desperdició hoy y por qué". El `pormerma` era un factor misterioso sin fórmula estándar. | Catálogo con 8 categorías (Empaque, Etiquetado, Líquidos, Insumos, Calidad, Cambio Formato, Otros). Registro transaccional con cálculo automático de cantidad, porcentaje y costo. |
| **Hallazgo** | Las 11 familias de artículo (`tipart`) de `mermastdmes` sirvieron como referencia para las categorías. | Lista con decoración visual: **rojo** >10% merma, **naranja** >5%. Menú en Clasificadores (seq 30) + menú en Producción. |

> **Analogía:** El legacy era como recibir un estado de cuenta mensual del banco que dice cuánto gastaste, pero sin poder registrar cada gasto en el momento. En Odoo, cada merma se registra al instante con su tipo, cantidad y costo — como una app de gastos que sabes exactamente qué, cuándo y cuánto.

---

### Program #137 — Categorías de Líneas de Producción
**"El catálogo que existía pero nadie documentó"**

| | Legacy (Big Magic) | Odoo 19 |
|---|---|---|
| **Qué existía** | Tabla `mfameq1f` con 27 categorías (15 activas, 12 inactivas) — el catálogo real de familias de equipos compartido entre México, Perú y Ecuador. Pero **cero documentación funcional** en los archivos oficiales. 28 columnas, de las cuales 11 eran basura técnica (flags binarios de UI) y 1 estaba 100% obsoleta. | Modelo `bm.ctl.produccion.categoria.linea` con solo 10 columnas útiles migradas. |
| **Problema** | Descubierto vía consultas SQL, no por documentación. Campos como `factor` (B/N), `funcion` (Normal/Global), `almproc` (almacén de proceso) eran operativos pero nadie sabía exactamente qué hacían hasta que se validaron. | Catálogo global sin company_id (compartido). Factor como Selection con validación. Función N/G. Doble acceso: Clasificadores (seq 40) y Costos (seq 10). |
| **Hallazgo** | 10 sucursales operativas reales en México. 87 sucursales "zombi" con 1 solo registro heredado. 553 líneas físicas en `caplinea` vinculadas a 8 de las 27 categorías. | 27 registros seed (15 activos + 12 inactivos preservados). |

> **Analogía:** El legacy tenía un excel impecable con 27 categorías perfectamente organizadas, pero estaba en un cajón sin etiqueta y nadie sabía que existía. En Odoo, ese catálogo ahora es visible, documentado y trazable — con cada categoría sabiendo a qué área pertenece, si es de botella o no, y en qué almacén opera.

---

### Program #138 — Familia de Producción por Sucursal
**"Encender y apagar líneas de producción por planta"**

| | Legacy (Big Magic) | Odoo 19 |
|---|---|---|
| **Qué existía** | Tabla `sucproc` — 16 registros para México: 4 sucursales × 4 categorías. Una tabla minimalista con PK `(compania, sucursal, efamilia)` y solo 2 campos de negocio: sucursal, categoría y estado activo/inactivo. | Modelo `bm.ctl.produccion.familia` con Many2one a `categoria.linea` (#137) y `sucursal`. |
| **Problema** | El nombre "Familia de Producción" era engañoso — parecía referirse a familias de producto (gaseosas/jugos/agua) pero en realidad era un switch de activación de categorías de línea por planta. Se confirmó que `sucproc.efamilia` = `mfameq1f.efamilia`. | 3 campos operativos: sucursal, categoría, activo. Nombre computado automático: "0001 / 001". |
| **Hallazgo** | Solo 4 de 27 categorías están configuradas en `sucproc`: Envasado (001), Jarabes (003), Maquila (019), Reempaques (021). Las demás son líneas auxiliares. | Menú: `Mantenimiento → Configuraciones → Familia de Produccion` (seq 10). 16 datos seed. |

> **Analogía:** Si el #137 es el catálogo de todas las máquinas que existen en la empresa, el #138 es el panel de control donde cada gerente de planta decide cuáles de esas máquinas están prendidas en su sucursal este mes. En Odoo es un switch de activar/desactivar con un clic.

---

### Program #162 — Aprobación de Fórmulas
**"Dejar de usar un cuaderno viejo y desordenado para pasarnos a una aplicación moderna"**

| | Legacy (Big Magic) | Odoo 19 |
|---|---|---|
| **Qué existía** | Tablas diseñadas para flujo documental (`csolactfor`, `dsolactfor`, `aprfor1f`, `taprform1f`) pero **0 registros**. Sin embargo, `forfab` (maestro de fórmulas) tenía 70,000+ registros con IDs de empleados reales en campo `aprobadop` — pero con fechas de aprobación **vacías**. | 5 modelos: `solicitud` (cabezal), `solicitud.line` (líneas), `aprobador.config`, `firma`, `tmp.detalle`. Máquina de estados: Borrador → Pendiente → Aprobado/Rechazado. |
| **Problema** | Alguien simplemente escribía su número de empleado en una celda y ya. Sin fecha, sin hora, sin trazabilidad de quién autorizó cada paso. Era un proceso "mudo". | Odoo obliga a registrar fecha, hora y usuario en cada aprobación. El botón "Aprobar" dispara automáticamente la grabación de todos los campos de auditoría. |
| **Hallazgo** | Se detectaron IDs de empleados reales (1708248, 6881, 29750) en `forfab.aprobadop` — aprobación plana/directa sin flujo multinivel. | Flujo estructurado con niveles de aprobación configurables. Statusbar visual. Menú: `Formulas → Aprobacion de Formulas`. |

> **Analogía:** El legacy era como firmar un documento con un lápiz sin fecha — no se sabe cuándo se firmó, quién lo revisó antes, ni si pasó por las revisiones necesarias. En Odoo, cada fórmula sigue un circuito documental con firmas electrónicas fechadas — como un expediente digital con todos los vistos buenos.

---

### Program #574 — Configuración de Procesos Productivos
**"La cadena de fabricación que el legacy nunca configuró"**

| | Legacy (Big Magic) | Odoo 19 |
|---|---|---|
| **Qué existía** | Tabla `mproprod1f` — la maestra de procesos. **0 registros**. Tabla `ctm_proceso` con 6 macro-procesos (BEBIDAS, COMPRESIÓN, INYECCIÓN...) pero de costos, no de producción. 5 Stored Procedures que **ni siquiera existen** en la BD de México. | Modelo `bm.ctl.produccion.proceso` con 6 procesos individuales: SOP (Soplado), JAR (Jarabe), BAS (Bases), LLE (Llenado), ETQ (Etiquetado), EMP (Empacado). |
| **Problema** | La cadena productiva de bebidas (soplar → mezclar → llenar → etiquetar → empacar) se manejaba implícitamente vía recetas sin un catálogo explícito. | Cada proceso con código 3 letras, descripción, secuencia de ejecución  y vinculación al área funcional vía Many2one a Categoría de Línea (#137). |
| **Hallazgo** | `ctm_proceso_area` tiene 18 mapeos de áreas que coinciden con `mfameq1f` (#137) — referencia útil para asignar procesos a áreas correctas. | Menú: `Mantenimiento → Configuraciones → Configura Procesos Productivos` (seq 30). 6 datos seed. |

> **Analogía:** El legacy sabía hacer bebidas pero nunca escribió la receta de "en qué orden se hacen las cosas". Era como un chef que cocina de memoria pero nunca documentó el paso a paso. En Odoo, los 6 procesos forman una línea de tiempo explícita — como un diagrama de flujo que muestra exactamente qué va primero, qué después y en qué área se ejecuta.

---

## 4. El panorama completo: Cómo se conectan los 7 programas

Los 7 programas no son islas — forman un circuito de configuración que va de lo más general a lo más específico:

```
NIVEL 1 — CATÁLOGOS BASE
  #132 Turnos        → ¿En qué horario se trabaja? (3 turnos × sucursal)
  #133 Paradas       → ¿Por qué se detiene la línea? (7 categorías)
  #135 Mermas        → ¿Qué se desperdicia y cuánto? (8 categorías)

NIVEL 2 — CONFIGURACIÓN DE PLANTA
  #137 Cat. Líneas   → ¿Qué tipos de máquinas existen? (27 categorías)
  #138 Familia       → ¿Cuáles están activas en cada sucursal? (switch ON/OFF)

NIVEL 3 — CADENA PRODUCTIVA
  #574 Procesos      → ¿En qué orden se fabrica? (SOP→JAR→BAS→LLE→ETQ→EMP)

NIVEL 4 — CONTROL DE CALIDAD Y RECETAS
  #162 Aprob. Fórmulas → ¿Quién autoriza las recetas? (flujo documental)
```

### El circuito de configuración completo:

1. **#137** define qué áreas funcionales existen (Envasado, Soplado, Etiquetas, Jarabes...).
2. **#138** decide cuáles de esas áreas están activas en cada sucursal (ej: Planta Puebla tiene Envasado + Jarabes + Maquila + Reempaques).
3. **#574** asigna cada proceso a su área correspondiente (Llenado → Envasado, Soplado → Soplado).
4. **#132** define en qué turnos opera cada sucursal (06:30-14:30, 14:30-22:00, 22:00-06:30).
5. **#133** cataloga los tipos de paradas que pueden ocurrir en cualquier proceso (falla mecánica en llenado, falta de material en etiquetado...).
6. **#135** registra las mermas generadas en cada proceso y turno (cuánto poly stretch se desperdició en el turno 2).
7. **#162** controla el flujo de aprobación de las recetas que ejecutan estos procesos.

---

## 5. Resultados y valor del trabajo realizado

### Lo que se entregó:

| Concepto | Cantidad |
|---|---|
| **Modelos Python de Odoo 19** | 15 archivos (3 turnos + 1 paradas + 2 mermas + 1 cat. línea + 1 familia + 5 fórmulas + 1 procesos + 1 sucursal) |
| **Vistas XML** | 30 archivos (list, form, search, action, menuitem para cada modelo) |
| **Datos iniciales (seed)** | 5 archivos XML con datos extraídos y validados de la BD legacy |
| **Reglas de seguridad (ACL)** | 16 permisos de acceso en `ir.model.access.csv` |
| **Documentación de validación** | 14 archivos (7 validaciones + 7 análisis) documentando cada hallazgo y decisión |
| **Menús Odoo** | 7 menús principales en `Mantenimiento`, `Producción`, `Costos`, `Formulas` con sequences multiplos de 10 |

### Lo que NO se hizo (decisiones conscientes):

- **No se copió basura técnica:** 11 campos bytea de UI del legacy descartados. Campos 100% vacíos (`codagru`) eliminados. Tablas vacías no migradas.
- **No se heredó deuda técnica:** Donde el legacy tenía huecos (fechas vacías en aprobaciones, catálogos sin datos para México), Odoo impone reglas que los resuelven.
- **No se replicaron estructuras muertas:** Tablas OEE de paradas con 0 registros. Stored Procedures que nunca se desplegaron. Módulos de costeo inexistentes en la BD de México.
- **No se asumió nada:** Cada decisión de arquitectura está respaldada por consultas SQL contra la base de datos real de producción.

### Lo que sigue:

Estos 7 programas son la **capa de configuración maestra** del control de producción. Son los cimientos. Sobre ellos se construirán:

- **Registro transaccional de paradas en línea** (usando el catálogo #133)
- **Registro de mermas en tiempo real** (usando el modelo transaccional de #135)
- **Programación de órdenes de producción** (usando turnos #132 y procesos #574)
- **Cálculo de OEE** (Overall Equipment Effectiveness) por línea y turno
- **Integración con el módulo de Manufactura (MRP) de Odoo** (Work Centers, BOMs, Routing)

---

## 6. Lecciones aprendidas

1. **La documentación miente — la base de datos no.** Varias descripciones funcionales asumían que ciertos programas estaban operativos, pero las consultas SQL revelaron tablas vacías, campos sin uso y lógica nunca desplegada.

2. **Migrar no es copiar.** Es auditar, entender, decidir qué sirve y qué no, y construir sobre lo que realmente se usa. Si hubiéramos migrado las 28 columnas de `mfameq1f`, estaríamos arrastrando 11 campos de basura binaria a Odoo.

3. **El formato juliano importa.** Mantener compatibilidad con el offset 730000 del AS/400 permite que los reportes de Odoo puedan ser leídos por sistemas legacy durante la transición.

4. **Los catálogos compartidos entre países son un hallazgo.** México, Perú y Ecuador comparten los mismos catálogos de turnos y categorías de línea — esto permite modelos globales sin company_id que simplifican el mantenimiento.

5. **Clean Slate es mejor que parche.** Para programas como #133 (Paradas), #574 (Procesos) y partes de #135 (Mermas), donde el legacy no tenía implementación real, fue mejor construir desde cero con las mejores prácticas de Odoo que intentar migrar esqueletos vacíos.

---

*Documento generado a partir de 7 validaciones y 7 análisis técnicos realizados contra la base de datos `mxbdaje_local` de AJE México. Los archivos fuente están en `data_para_agente/validaciones_programs/`.*
