## Analisis del BM-CTL-Produccion_Mexico.xlsx y Produccion_arbol_funciones.html

### Jerarquia de menus
Un menu no es mas que una direccion postal. No contiene datos, solo sirve para clasificar y agrupas
1. Menu raiz(el modulo): Es el contenedor* mas grande (ej Mantenimiento) .En odoo , esto suele aparecer como un icono en el tablero principal-
2. Sub-Menu (categoria): Agrupa funciones similares(Clasificadores o configuraciones).Su funcion es puramente organizativa para que el usuario no vea 50 opciones de golpe, por ejemplo
3. Menu de accion (el acceso): Es el nivel más bajo (el circulo azul ej Turnos)

### los programas(la unidad funcional)
En el sistema antiguo, un programa es una pieza de codigo cerrada.En odoo , un "programa" se traduce tecnicamente en una **accion de ventana**(ir.actions.act_window)<br>

Un programa tiene :
1. EL modelo (la tabla): Si el programa es **Turnos**, el modelo es la tabla en PostgreSQL que guarda el nombre del turno, hora de inicio y fin.
2. La vista(La intefaz): Es el diseño de la pantalla(formulario para editar, lista para ver todos)
3. La logica (python/triggers): Es lo que ocurre cuando se guarda.Aqui nos conectamos con AJE.Por ejemplo , si un programa de "produccion" registra una cantidad, la logica dispara el Recalculo Total que se trabaja en la base datos.
### Analisis del arbol: El semaforo de mexico
1. Circulo Azul solido: Programa operativo y necesario.Requiere un archivo xml con su **menuitem** , su **action** y su modelo de base de datos asociado.
2. Circulo con borde rojo: Son las ramas muertas
    - Tipo de carton o parametro para Max y Min
    - Se tachan porque en mexico ya tiene otra forma de resolverlo o porque la funcionalidad sera absorbido por un proceso estandar de Odoo.
Ejemplo
```bash
+-----------------------+--------------------------+------------------------------+

| Concepto en el Árbol  | Tipo de Objeto en Odoo   | Archivo sugerido en VS Code  |
+-----------------------+--------------------------+------------------------------+

| Mantenimiento         | menuitem (Raíz)          | principal_menu.xml           |
| Clasificadores        | menuitem (Padre)         | mantenimiento_menu.xml       |
| Turnos                | menuitem + act_window    | mantenimiento_menu.xml       |
+-----------------------+--------------------------+------------------------------+

```
### Modulos funcionales
Se ven modulos funcionales , en odoo seran los menus que organizan el trabajo de la planta.
 
#### Mantenimiento 
Es el mantenimiento de los datos maestros.Aqui se crean los turnos , se configuran las lineas de produccion y las etiquetas.
- Qué hace : Aqui se definen los parametros base: los turnos de trabajo, las lineas de produccion (llenadoras , etiquetadoras) los motivos de por que se detiene una máquina y como deben ser las etiquetas.
- En mexico : Es vital , se usa para configurar todo el entorno antes de empezar a fabricar 
<p align="center">
    <img src="imagenes/Mantenimiento.png" width="85%">
</p>

1. Nivel 1: Menu Raiz (El modulo)
    - Nombre: Mantenimiento
    - Archivo: principal_menu.xml
    - Funcion: Es el punto de entrada desde el tablero de Odoo
2. Nivel 2: Los pilares organizativos
    Aqui es donde se divide el trabajo
        - Clasificadores: Para datos maestros binarios (turnos , paradas)
        - Configuraciones: Para reglas de negocio complejos.
        - Consulta: Para visualizacion de datos
        - Reportes: Para salidas de informacion y KPIs
3.  Nivel 3: Agrupadores Especificas
    Dentro de configuraciones , existe un nivel intermedio
        - Codigo de barras: Este es el "padre" de todas las funciones de etiquetado
            - Programas (SI) : Tipo de tarima , Tipo de Etiqueta, Configuracion Etiqueta, Configuracion de Tarima /Palet, configuracion LINEA, Vida Util por SKU, Autorizacion de Eliminacion.
4.  Nivel 4: El programa (accion final)
    Aqui el usuario hace clic para trabajar(circulo azul)
    - Ejemplo: En el codigo de barras tenemos Tipo de Tarima  o configuracion Etiqueta.

si estuvieramos viendo la ruta "migas de pan" (breadcrumbs) en odoo para configurar una etiqueta en Mexico, se veria del siguiente modo(ej):

```bash
    mantenimiento → configuracion → codigo de barras → Configuracion Etiqueta
```
En los xmls se debe asegurar qu los **parent** coincidan
- En **mantenimiento_menu.xml**
    - El menu Configuracion debe tener **parent** a Mantenimiento
    - El menu codigo de barras deber tener como **parent** a configuraciones
    - El menu Tipo de Tarima debe tener como **parent** a codigo de barras

Entonces tenemos a **principal_menu.xml** es el archivo que contiene el Boton de Entrada para TODO el modulo de produccion de AJE.

- **principal_menu.xml** Nivel 1(Raiz) Menu principal "Produccion" o "Mantenimiento" (icono del tablero)
- **mantenimiento_menu.xml** Nivel 2 y 3  Menu "clasificadores" , "configuraciones" y sus hijos(turnos,paradas)
- **codigo_barras.xml** Nivel 3 y 4  El sub-menu "Codigo de barras" y sus programas (Tipos de tarima)
- **produccion_menu.xml** Nivel 2 y 3  Menu "operaciones" y sus hijos (Lanzar OP,Liquidar OP)
 
Los demas modulos siguen la misma logica

Por ejemplo para planeamiento, se tendra un **planeamiento_menu.xml**.Dentro de este, se creara el menu "Planeamiento" y se indicara que su **parent** es el ID que se define en el archivo principal.

#### Planeamiento (Estrategia)

Se decide cuándo y cuánto fabricar
- Qué hace: Gestiona la capacidad de las lineas. Si mexico necesita producir 1 millon de litros de bebida , aqui se calcula si las lineas tiene capacidad fisica para hacerlo en el tiempo esperado.
- En Mexico: Se usa para mapear sucursales y lanzar ordenes de produccion desde el sistema de planificacion (AVAIL)
 

#### Produccion (Ejecución)
Es el corazon operativa de la fabrica
- Que hace? : Aquí se pisa la planta.Se lanzan las ordenes de produccion (OP) ,se registra cuánta bebida se tiró(mermas) , cuántas horas trabajo el personal y se sacan los reportes diarios de eficiencia
- En Mexico: Es donde ocurre el mayor volumen de trasancciones diarias

#### Control de Calidad (filtro)
Asegura que el producto sea seguro para el consumo
- Que hace?: Define los planes de inspeccion .Por ejemplo "cada 30 minutos hay que medir el nivel de gas de la bebida"
- En Mexico: Se usa principalmente para el Plan de inspeccion y aprobar si un lote sale a la venta o se queda en la cuarentena.

#### Costos(El dinero)
Traduce lo anterior a terminos financieros
- Que hace?: Calcula el costo real de produccion.Suma el valor de los insumos (azucar , botellas), la mano de obra y los gastos indirectos (luz, agua) para decir cuanto costo cada unidad producida.

- En Mexico : muy importante para la simulacion de costos y control del "costo estandar"

#### Utils / Utilidades (Las herramientas de auxilio)
Para corregir errores
- Que hace: Son funciones administrativas para ajustar el sistema cuando algo sale mal en el dia a dia.
- En Mexico: Se usa para cambiar "Cambiar de Fecha OP" y corregir "Movimiento de Almacen"

### Implementacion menu Mantenimiento
En **mantenimiento_menu.xml** se establecen los contenedores o secciones principales.Se han ajustado las secuencias(sequence) para que los grupos aparezcan en el orden visual correcto.

Y los otros archivos con el prefijo **mantenimiento_ ...** de acuerdo al arbol equivalente al excel proporcionado por los lideres de equipo.



## docker start
```bash
docker service docker start
```
## OpenCode 
En el terminal 
```bash
opencode auth login # escoger opencode go  , auntenticarse
/models   #escoger Qwen3.6 similares
/context add .  # agregando el contexto actual
```

## conexion a la base de datos postgresql migrada

Para establecer la conexion se ejecuta **psql -h 100.119.5.108 -p 5432 -U postgres -d mxbdaje_local** o desde pgadmin con las mismas opciones, luego de lo cual se ingresaba la contraseña.

Para que nuestro servicio odoo se conecte a dicha base de datos modificamos 
```bash
environment:
      - HOST=100.119.5.108
      - PORT=5432
      - USER=postgres
      - PASSWORD=051002
```
Y la configuracion **odoo.conf**
```bash
db_host = 100.119.5.108
db_user = postgres
db_password = 051002
db_port = 5432
admin_passwd = pass
db_name = mxbdaje_local
```

Lo anterior debido a que en la imagen de la conexion, el "host/address" es 100.119.5.108.Se trata de una ip de tailscale (100.x.x.x) , pgadmin esta viajando por internet para conectarse con el ssd donde reside la base de datos migrada.

Mientras que docker es tiene un alcance mas local.

Hechas las modificaciones comprobamos que existe trafico entre el contenedor en wsl , para lo cual se ejecuta
```bash
# Prueba si el motor de Docker en WSL2 puede saltar a Tailscale
docker run --rm alpine nc -zv 100.119.5.108 5432
#comprobado lo anterior, levantar el servicio 
docker compose up -d odoo
# entrando al contenedor de manera interativa y comunicando con la base de datos
docker exec -it odoo19-server-dev psql -h 100.119.5.108 -U postgres -d mxbdaje_local
```

Los comandos son exitosos, sin embargo el tiempo de conexion es infima e inestable.

Esto obliga a obtener informacion especifica para el agente.


### Para las pruebas no se usa la conexion a la base de datos  sino el servicio DB 
Con las credenciales cofigurados en odoo.conf

### Cargar program # 132 
```bash
Ahora reinicia el contenedor y actualiza el modulo:
docker compose down && docker compose up -d
Luego en la UI o por linea de comandos:
docker exec -it <container_name> odoo-bin -u Production -d <tu_base_de_datos> --stop-after-init
Si el error persiste, verifica que los archivos esten montados correctamente en el contenedor:
docker exec <container_name> ls -la /mnt/extra-addons/Production/models/
Los 3 archivos deben aparecer:
```
### Actualizar modulo de interes

enviar cambios
```bash
docker exec odoo19-server-dev odoo -u Production -d odoo_aje --stop-after-init
```

### El agente arruina la ui para aprobacion de formulas
El commit bueno
```bash
git log --oneline -n 10
d249f7a (HEAD -> features/produccion-modelos-logica) termina querys para program # 132
6c58334 completa querys solicitados por el agente
5ae7912 rastrea a data_para_agente
bf6cc96 concluye querys pra precisar la descripcion de program # 132
9ffc6ef completa y comprueba Aprobacion de formulas program # 162  ← este es el commit bueno
4f7afae agrega docu program 162
ef0dfa1 (origin/features/produccion-algunos-modelos, features/produccion-algunos-modelos) completa las vistas
f752462 (origin/prod_module, prod_module) Merge pull request #1 from FloresVillar/feature/mexico-menu-structure
6eb2034 implementa menu Mantenimiento
885d832 agrega documentacion
```
buscar diferencias

```bash
 git diff 9ffc6ef -- Pruebas/Production/views/mantenimiento_menu.xml
diff --git a/Pruebas/Production/views/mantenimiento_menu.xml b/Pruebas/Production/views/mantenimiento_menu.xml
index fc38591..e54c98b 100644
--- a/Pruebas/Production/views/mantenimiento_menu.xml
+++ b/Pruebas/Production/views/mantenimiento_menu.xml
@@ -24,9 +24,4 @@
                     name="Reportes" 
                     parent="mant_menu"
                     sequence="40"/>
-        <menuitem   id="mant_aprobacion_formulas_menu"
-                        name="Aprobacion de Formulas"
-                        parent="mant_menu"
-                        action="action_formula_solicitud"
-                        sequence="50"/>
 </odoo>
\ No newline at end of file
esau@DESKTOP-A3RPEKP:~/TutorialOdoo$ git diff 9ffc6ef -- Pruebas/Production/views/program_162_formula_aprobacion.xml
diff --git a/Pruebas/Production/views/program_162_formula_aprobacion.xml b/Pruebas/Production/views/program_162_formula_aprobacion.xml
index c464817..e1b856f 100644
--- a/Pruebas/Production/views/program_162_formula_aprobacion.xml
+++ b/Pruebas/Production/views/program_162_formula_aprobacion.xml
@@ -210,9 +210,9 @@
 
         <!-- MENU ITEMS (Configuracion bajo Mantenimiento) -->
         <menuitem id="menu_formula_config"
-                  name="Configuracion Formulas"
+                  name="Aprobacion de Formulas"
                   parent="mant_menu"
-                  sequence="60"/>
+                  sequence="50"/>
 
         <menuitem id="menu_formula_aprobador_config"
                   name="Aprobadores"
```

reestablecer esos archivos a ese commit

```bash
git checkout 9ffc6ef -- Pruebas/Production/views/mantenimiento_menu.xml
git checkout 9ffc6ef -- Pruebas/Production/views/program_162_formula_aprobacion.xml
```

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

