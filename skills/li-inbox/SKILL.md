---
name: li-inbox
description: >-
  Ordena la bandeja de entrada de LinkedIn: clasifica las solicitudes de
  conexión y los DM en posibles clientes, reclutadores, colegas y spam, y
  escribe las respuestas que vale la pena mandar. Úsala cuando el usuario
  diga "mi bandeja es un desastre", "ordena mis DM", "¿le respondo a esto?",
  pegue una tanda de mensajes de LinkedIn, o esté ahogado en solicitudes de
  conexión.
---

# li-inbox

La mayoría de las bandejas de LinkedIn son 80% ruido, y el costo de ese ruido
es que el 20% queda sin respuesta durante una semana. Esta skill los separa y
luego escribe solo lo que vale la pena escribir.

## Entrada

El usuario pega los mensajes. Las capturas sirven. No inicies sesión en su
cuenta ni leas su bandeja con una herramienta de navegador.

## Clasifica en cinco

| grupo | señal | acción |
| --- | --- | --- |
| **POSIBLE CLIENTE** | describe un problema que el usuario resuelve, o pregunta por trabajar juntos | responder hoy, completo |
| **RECLUTADOR** | un puesto, una empresa, un rango salarial | responder si el puesto es real, una línea si no |
| **COLEGA** | alguien del mismo campo con algo que decir | responder esta semana, que suene humano |
| **PEDIDO** | quiere un consejo, tiempo, una presentación, un favor | responder si es barato y específico, decir que no con claridad si no |
| **SPAM** | venta de agencia, secuencia de captación, cripto, "una pregunta rápida" sin pregunta | archivar, sin respuesta |

Imprime primero los conteos. Ver "3 posibles clientes, 2 reclutadores, 41
spam" ya es la mayor parte del valor.

## Cómo detectar una secuencia

El contacto automatizado tiene una forma: una nota de invitación sin nada
específico, un mensaje que llega minutos después de aceptar, "una pregunta
rápida", "vi que trabajas en {industria}", un enlace de calendario en el
primer mensaje, y luego un recordatorio exactamente cuatro días después. Cuando
la veas, márcala como SPAM y di qué detalle la delató. El usuario no le debe
una respuesta a un script.

## Respuestas

- **POSIBLE CLIENTE**: responde la pregunta real del mensaje, completa y
  gratis. Si encaja, la oferta es una oración al final. Si no encaja, dilo y
  recomiéndale algo útil. Los dos resultados son buenos.
- **RECLUTADOR**: si el puesto de verdad interesa, pregunta las tres cosas que
  el mensaje no dijo: rango salarial, nivel y si es presencial. Si no
  interesa, una línea: no estoy buscando, con gusto recomiendo a alguien, y que
  la recomendación sea en serio.
- **PEDIDO**: si cuesta menos de diez minutos y es específico, hazlo. Si es
  "¿puedo hacerte unas preguntas?", di que no en una oración cálida y dale la
  única respuesta que le habrías dado en la llamada. Esa es la versión amable,
  y también la más útil.
- **LOS NO** son cortos, cálidos y definitivos. Nada de "lo retomamos en el
  tercer trimestre" si no va a haber tercer trimestre.

## Resultado

Agrupado por grupo, con los conteos primero, borradores solo para los grupos
que reciben respuesta, cada uno humanizado. Luego la compuerta: los manda el
usuario.

```
BANDEJA  ·  52 mensajes  ·  3 POSIBLE CLIENTE, 2 RECLUTADOR, 4 COLEGA, 2 PEDIDO, 41 SPAM

SPAM  (41): archivar. 38 son la misma secuencia: invitación sin nada
específico, "una pregunta rápida" a los 4 minutos de aceptar, enlace de
calendario en el primer mensaje.
```
