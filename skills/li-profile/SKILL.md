---
name: li-profile
description: >-
  Puntúa un perfil de LinkedIn sobre 100 con una rúbrica de 12 partes y
  reescribe las partes que pierden puntos: titular, acerca de, experiencia,
  destacados, portada. Úsala cuando el usuario diga "optimiza mi perfil",
  "puntúa mi LinkedIn", "reescribe mi titular", "arregla mi acerca de", o
  pegue su perfil y pregunte cómo se lee.
---

# li-profile

Un perfil no es un currículum. Un currículum responde "qué has hecho". Un
perfil responde "¿le escribo a esta persona?", y lo responde en unos cuatro
segundos, con el titular y las dos primeras líneas del acerca de.

## Entrada

Pídele al usuario que pegue: el titular, la sección acerca de, el cargo actual
y las dos últimas experiencias, y si tiene portada y sección de destacados.
Una captura de la tarjeta superior alcanza para la primera pasada. No inicies
sesión en LinkedIn en su nombre.

## Puntúalo

Lee `rubric.json` en esta carpeta. Doce elementos, 100 puntos, cada uno con
cómo se ve el puntaje completo. Puntúa cada elemento, muestra la tabla y da el
total. Sé honesto: la mayoría de los perfiles quedan entre 30 y 49 en la
primera pasada, y un puntaje generoso no le sirve a nadie.

```
PUNTAJE DEL PERFIL  41/100

  titular                       3/12   solo el cargo, sin resultado, sin público
  acerca de, 2 primeras líneas  2/10   empieza con "apasionado por"
  acerca de, cuerpo             4/10   historia, no oferta
  destacados                    0/8    vacío
  portada                       0/6    el azul por defecto
  ...
```

## Luego reescribe, en este orden

Arregla en orden de más a menos puntos perdidos. No reescribas todo de una vez:
el usuario tiene que pegar cada una de estas partes.

**1. Titular (220 caracteres).** La fórmula que funciona:
`{qué haces y para quién} | {prueba} | {cómo empezar}`. No tu cargo. No
"Ayudo a X a lograr Y" como primeras palabras, que es como empieza uno de cada
dos perfiles ahora. Da tres opciones.

**2. Acerca de, las dos primeras líneas.** Todo lo que viene después de la
línea 2 queda detrás de "ver más" en el teléfono, así que esas dos líneas son
toda la sección para la mayoría de los lectores. Tienen que decir a quién
ayudas y qué cambia. Nada de "apasionado", nada de "orientado a resultados",
nada de biografía en tercera persona, nada de empezar con tu propio nombre.

**3. Acerca de, el cuerpo.** Escrito para un solo lector, en segunda persona.
Estructura: el problema que tiene, lo que tú haces al respecto, una prueba con
un número, qué hacer a continuación. Menos de 1400 caracteres, aunque el
límite es 2600.

**4. Destacados.** Tres elementos: el mejor post, la prueba, y la forma de
contactarte. Una sección de destacados vacía son ocho puntos, y es el único
lugar del perfil que controlas por completo.

**5. Experiencia.** Cada cargo lleva una línea de alcance y dos o tres viñetas
que son resultados con números, no tareas. Recorta todo lo de hace más de diez
años a una sola línea.

**6. Portada.** Una oración de posicionamiento y una forma de contactarte. El
degradado azul por defecto es la señal más clara de la página de que no hay
nadie en casa.

## Resultado

La tabla de puntajes, y luego las reescrituras como bloques listos para copiar,
en el orden de lo que hay que arreglar primero, cada una ya pasada por
`/li-human`. Vuelve a puntuar al final y muestra la diferencia con honestidad:
si la reescritura llega a 88 y no a 98, di 88, y di qué necesitan los puntos
que faltan (por lo general recomendaciones, una portada real e historial de
publicaciones, y nada de eso lo puede crear una reescritura).

Esta skill no guarda nada en LinkedIn. El usuario pega cada sección.
