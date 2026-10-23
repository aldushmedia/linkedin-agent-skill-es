---
name: li-comment
description: >-
  Escribe comentarios en los posts de LinkedIn de otras personas que se leen
  como los de alguien con una opinión, no como los de un bot. Úsala cuando el
  usuario pegue un post y quiera un comentario, diga "comenta esto",
  "interactúa con esto", "qué digo aquí", o quiera una tanda de comentarios
  para su ronda de interacción.
---

# li-comment

Comentar es lo que más rinde en LinkedIn y lo más fácil de hacer mal. Un
comentario en un post con 400 reacciones lo ve más gente que la mayoría de tus
propios posts. Uno genérico no lo ve nadie y te cuesta credibilidad con el
autor.

## Entrada

El usuario pega el texto del post (y el nombre y el cargo del autor, si los
tiene). Si pega una captura, léela. Si te da una URL que no puedes abrir, pídele
que pegue el texto: no adivines lo que decía el post y no uses automatización
del navegador para extraer el feed.

## Los nueve tipos de comentario

Elige según lo que el post es de verdad. Nunca elijas el tipo 1 por defecto.

| # | tipo | cuándo | forma |
| --- | --- | --- | --- |
| 1 | **Aportar un dato** | el post afirma algo que puedes respaldar con un número | "Nos pasó lo mismo: el 40% de nuestros..." |
| 2 | **Aportar el caso que falta** | el post tiene razón pero está incompleto | "Esto se cumple hasta que {condición}. Ahí..." |
| 3 | **Desacuerdo respetuoso** | de verdad crees que está mal | nombra primero el acuerdo y luego dónde se separan |
| 4 | **Ampliar una línea** | una oración del post es la buena | cítala y construye a partir de ella |
| 5 | **Hacer la pregunta de verdad** | el post se saltó la parte difícil | una pregunta, específica, sin "me encantaría saber" |
| 6 | **La prueba** | hiciste lo que describen | qué pasó, en dos oraciones |
| 7 | **La corrección** | hay un error de hecho | ten razón, sé breve, sé amable, ten certeza |
| 8 | **El replanteo** | el post tiene los hechos bien y el enfoque mal | "Otra forma de leer esto:" |
| 9 | **La frase corta** | el post no necesita nada y quieres estar presente | menos de 12 palabras, tiene que ser graciosa o cierta |

## Reglas

- **De 2 a 4 oraciones.** Más largo se lee como querer adueñarse del post. Más
  corto se lee como relleno.
- **Nunca empieces con "Gran post"**, "Me encanta", "Muy cierto", "No podría
  estar más de acuerdo", "Esto resuena" ni el nombre del autor seguido de un
  signo de exclamación. Los seis son invisibles.
- **Nada de emoji al inicio.** Ni 🔥 ni 👏 como primer carácter.
- **Nunca repitas el post.** El autor sabe lo que escribió, y todos los que lo
  leen también.
- **Una idea.** Un comentario con dos puntos se lee como un intento de blog.
- **Di lo específico.** Si el comentario podría ir debajo de cualquier post
  sobre el tema, no es un comentario, es ruido.
- **El desacuerdo está permitido y funciona**, pero el acuerdo tiene que ir
  primero y ser real.

## Resultado

Da **dos opciones de tipos distintos**, con su etiqueta, y una línea con el
motivo de la que publicarías. Pasa las dos por `/li-human` primero: un
comentario con una raya larga se nota más escrito por una máquina que un post,
porque los comentarios son cortos y la gente los lee con atención.

```
OPCIONES DE COMENTARIO  (en el post de @autor sobre contratación)

[6 · La prueba]
Probamos la versión sin currículum de esto en 3 contrataciones el año pasado.
Dos fueron las mejores que hicimos. La tercera fue un desastre, y la
diferencia fue si ya habían hecho el trabajo antes, no cómo les fue en la
entrevista.

[3 · Desacuerdo respetuoso]
De acuerdo con el problema de la señal. Pero lo que nos funcionó no fue quitar
el currículum, fue darle a cada candidato la misma tarea remunerada de 90 minutos.
Mismo resultado, muchas menos discusiones internas.

Publica el primero. Son tus propios datos y reconoce un fracaso, que es la
parte a la que la gente responde.
```

## Modo tanda

Si el usuario quiere una ronda de interacción, pide los 5 a 10 posts como texto
pegado en un solo mensaje, devuelve un comentario para cada uno en un solo
bloque, y lleva en `~/.claude/linkedin/log.md` una nota de a quién ya comentó
esta semana. Comentar todos los días a las mismas tres personas se nota, y se
ve como lo que es.

## Nunca

No publiques automáticamente. No uses una herramienta de navegador para
publicar comentarios en nombre del usuario. La publicación automatizada y la
extracción de datos violan el Acuerdo de Usuario de LinkedIn y ponen en riesgo
la cuenta. Esta skill escribe el comentario. El usuario lo publica.
