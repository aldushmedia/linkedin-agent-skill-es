---
name: li-audit
description: >-
  Análisis de lo que el usuario ya publicó: qué posts funcionaron de verdad,
  por qué, y qué dejar de hacer. Úsala cuando el usuario pegue sus analíticas
  de LinkedIn o sus posts anteriores y pregunte "qué está funcionando", "por
  qué no funcionó este", "lee mis analíticas", "audita mi contenido", o quiera
  saber en qué redoblar la apuesta.
---

# li-audit

La única fuente honesta de lo que funciona para una cuenta es esa cuenta. Cada
regla de cada guía de LinkedIn, incluidas las de este paquete, es una
suposición previa. Los últimos 30 posts del propio usuario son la evidencia.

## Entrada

Pide lo que el usuario tenga:

- La exportación de las analíticas de sus posts, desde la sección de
  analíticas de contenido de LinkedIn. Un CSV.
- O una captura por post con impresiones, reacciones, comentarios y
  republicaciones.
- O solo los posts y sus conteos de reacciones, que alcanza para una primera
  pasada.

Lee también `~/.claude/linkedin/log.md` si existe, porque ahí está qué fórmula
de gancho usó cada post.

## Qué medir de verdad

Las impresiones en bruto son el número menos útil de la página, porque dependen
sobre todo de cuánta gente ya sigue al usuario. Calcula estos en su lugar, y
muestra las cuentas:

| métrica | cómo | qué te dice |
| --- | --- | --- |
| **Tasa de interacción** | (reacciones + comentarios + republicaciones) / impresiones | si el post se ganó su alcance |
| **Proporción de comentarios** | comentarios / reacciones | si empezó algo o solo recibió un gesto de aprobación |
| **Múltiplo de alcance** | impresiones / seguidores | si viajó más allá de la audiencia que ya existía |
| **Tasa de guardados y envíos** | si está disponible | el mejor predictor por sí solo del alcance futuro |

Ordena por tasa de interacción y múltiplo de alcance, no por impresiones. Un
post con 900 impresiones y 40 comentarios le ganó al de 12 000 impresiones y 6.

## Luego encuentra el patrón

Con los 5 mejores y los 5 peores lado a lado, busca qué los separa de verdad, y
anímate a concluir algo que al usuario no le va a gustar:

- La fórmula de gancho. ¿Qué números de `hooks.json` están entre los 5
  mejores?
- El formato. Texto, documento, imagen, video.
- La extensión.
- El tema.
- El día y la hora: revisa esto **al final**, y solo si los otros cuatro no
  muestran nada. Casi nunca es la causa, y es donde la gente quiere que esté.
- Los comentarios de la primera hora. Posts en los que el usuario respondió
  dentro de la primera hora frente a los que no.

Plantea el hallazgo como una afirmación con la evidencia al lado, y di qué tan
seguro es. Con 30 posts se puede ver un patrón; con 6 no, y tienes que decir
eso en lugar de inventar uno.

## Resultado

```
AUDITORÍA  ·  31 posts  ·  12 jun - 5 sep

LOS 5 MEJORES POR TASA DE INTERACCIÓN
  8.1%  #3  Confesión de un error  "18 000 dólares es lo que me costó no tener contrato"   1940 imp.
  6.4%  #20 Lo que dejé ir         "Despedí a mi cliente que mejor pagaba"                  2210 imp.
  ...

LOS 5 PEORES
  0.4%  #5  La lista prometida     "7 herramientas que todo fundador necesita"             11 400 imp.
  ...

LO QUE DICEN LOS DATOS
1. Los posts en los que tú quedaste mal: promedio de 6.2% contra 1.1% del
   resto. n=6. Es tu señal más fuerte, y no está ni cerca.
2. Las listas de herramientas consiguen impresiones y nada más. Mucho alcance,
   sin comentarios, sin posibles clientes. Tres de tus cinco peores.
3. El día de la semana no muestra nada. Tu promedio del martes y el del viernes
   están dentro del ruido. Deja de optimizarlo.

DEJA DE HACER: listas de herramientas.
HAZ MÁS: los que tienen un costo que pagaste, y un número.
```

Luego pásale las conclusiones a `/li-plan` para que el plan de la semana que
viene se arme con la evidencia del propio usuario y no con los valores por
defecto.
