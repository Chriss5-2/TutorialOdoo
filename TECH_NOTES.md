## Chatter de Odoo
Es el charlatán o panel lateral(inferior) que apareece dentro de un registro(como facturas o una solicitud) y sirve para comunicacion y el seguimiento historico.

Se divide en tres funciones:
- Logs de auditoria (Tracking) : Si el modelo tiene habilitado el rastreo, cada vez que alguien cambie un estado  (de "borrador" a "Aprobado") o modifique un campo importante, Odoo escribe automaticamente una nota ahi. "Administrador cambió de Estado de Draft a Pending"
- Notas Internas: Permite escribir mensajes que solo ven los empleados (ej: Revisar la formula porque el costo parece alto)
- Enviar mensajes: Permite enviar correos electronicos directamente al agente o proveedor de registro, y las respuestas quedan guardadas ahi mismo

### Importante para program#162
En un flujo de aprobacion de formulas, el Chatter es tu mejor prueba de cumplimiento.Ahi quedará registrado con fecha, hora y usuario exactamente quien autorizó y cuándo, de forma visual y cronológica.


