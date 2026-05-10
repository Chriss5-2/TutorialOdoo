# Reglas del sistema - Proyecto AJE
## Entorno de Desarrollo
- **Sistema:** Odoo 19 (Docker/WSL2)
- **Base de datos** Postgresql con enfoque en triggers de negocio
## Reglas estrictas
1. **Verificacion de archivos** PROHIBIDO asumir ruta o contenido.Siempre listar directorios('ls') o leer archivos antes de proponer cambios .
2. **Prioridad tecnica** Respuestas directas a la implementacion, prioriza el codigo optimizado
3. **Estandar XML** Todas las 'sequence' en menus y vistas en Pruebas/Production/ deben ser multiplos de 10 
4. **Contexto Mexico** usa terminos contables locales (MEXICO)
5. **Adaptabilidad** Las reglas anteriores no abarcan todos los posibles escenarios, segun se avance el proyecto podria ser necesario añadir algunos, en ese momento ambos tu y yo analizaremos ese escenario.
6. **Contexto del proyecto** Este repo es un subconjunto del ecosistema AJE real. `aje_docs_simulacion/` es documentacion de referencia del sistema Big Magic ERP (el core real de AJE con integraciones SOAP/REST a SAP, FullStep, Avail, Salesforce, etc) — NO se modifica, solo se consulta para contexto. El trabajo de desarrollo va exclusivamente en `Pruebas/Production/` (modulo Odoo para Mexico). `tutorials/` son ejercicios de aprendizaje.
7. **IMPORTANTE** Guarda el historial del chat tal cual (no resumenes) en CADA respuesta. Crea el archivo de sesion con formato `AAAA-MM-DD_HH:MMAM/PM.md` en `historial_agente/` al iniciar. En CADA respuesta que des, PRIMERO actualiza el archivo agregando la pregunta del usuario y tu respuesta, DESPUES responde. Asi si la sesion se interrumpe (ctrl+c, cierre de chat, etc), el historial queda guardado hasta el ultimo intercambio.