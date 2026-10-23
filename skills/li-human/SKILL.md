---
name: li-human
description: >-
  Quita la huella de la máquina de cualquier borrador en español o en inglés
  (rayas largas, palabras de relleno típicas de la IA, caracteres invisibles
  de marca de agua) y lo puntúa con un panel de detección de cinco chequeos antes de que salga.
  Úsala siempre que un texto tenga que sonar humano, cuando el usuario diga
  "humanízalo", "¿esto suena a IA?", "quita las rayas largas", "sácale el
  relleno", "¿esto lo van a marcar?", o antes de mostrarle al usuario
  cualquier post, comentario, respuesta o DM de LinkedIn.
---

# li-human

En esta carpeta hay dos herramientas, y las dos funcionan de verdad. Úsalas.
No lo hagas a ojo.

```bash
python3 humanize.py draft.txt --report        # lo limpia y muestra qué cambió
python3 detect.py draft.txt                    # lo puntúa, cinco chequeos
python3 detect.py before.txt after.txt         # demuestra la diferencia
```

Las dos leen `slop.json`, que es el léxico: 168 palabras y frases hechas en
español y 113 en inglés, cada una con su reemplazo simple, 17 clases de
caracteres invisibles, 11 sustituciones tipográficas y 11 patrones delatores
por idioma. Está hecho para editarse. Si el usuario tiene una palabra que
siempre usa y el léxico la quita, sácala del archivo. Las entradas en español
llevan `"lang": "es"`; las que no lo llevan son las del inglés.

## Español e inglés

Los dos scripts detectan el idioma de cada texto y usan solo el léxico y los
patrones de ese idioma. El reporte y el panel dicen cuál usaron ("texto en
español"), y en `--json` está en el campo `language`. Si la
detección se equivoca, por ejemplo con un post en español lleno de citas en
inglés, fija el idioma con `--lang es` o `--lang en`.

Con un texto en español:

- Los reemplazos respetan el género y el número ("robusta" pasa a "sólida"),
  ajustan la "y" o la "e" de delante ("sólido e innovador" pasa a "sólido y
  nuevo") y, si se borra una apertura ("Cabe destacar que el plan..."), la
  oración vuelve a empezar con mayúscula ("El plan...").
- VOZ cuenta los pronombres y posesivos de primera y segunda persona y los
  verbos en primera persona ("perdí", "mandamos", "tengo"), porque el español
  no usa contracciones y suele omitir el sujeto.
- Las palabras con tilde o ñ cuentan como una sola palabra, y los nombres
  propios con tilde ("Bogotá") cuentan como datos concretos.

Con un texto en inglés, los resultados son los mismos del proyecto original.

## Lo que se arregla solo

**1. Caracteres invisibles.** Espacios y uniones de ancho cero, uniones de
palabras, guiones suaves, marcas de orden de bytes (BOM), caracteres de
etiqueta Unicode, espacios sin salto y estrechos. Un teclado no los produce.
Sobreviven al copiar y pegar, son invisibles en cualquier editor y son lo más
mecánico de un texto generado. `humanize.py` los borra todos, incluido
cualquier otro carácter Unicode de formato que no tenga nombrado.

**2. Tipografía.** Raya larga a coma, raya media a guion, comillas curvas a
rectas, puntos suspensivos a tres puntos, viñeta a guion. La pasada de la raya
larga (U+2014) es la que importa: la convierte, con sus espacios, en `, ` y
luego limpia la puntuación doble que eso deja.

**3. El léxico de relleno.** En español: "en el mundo actual", "cabe destacar
que", "es fundamental", potenciar, apalancar, sinergia, robusto, innovador,
"un testimonio de", asimismo, "sin más preámbulos" y el resto. En inglés:
delve, leverage, robust, seamless, crucial, tapestry, testament to, moreover,
"in today's fast-paced world", "let that sink in" y el resto. Cada una se
cambia por una palabra simple, o se borra, respetando las mayúsculas y sin
tocar las URL.

## Lo que NO se arregla solo

Los patrones delatores se **marcan, no se reescriben**, porque cambiar la forma
de una oración requiere criterio:

- "No es solo X, es Y", "no solo X sino también Y" y "no se trata de X, se
  trata de Y" ("It's not just X, it's Y", "not only X but also Y", "it isn't
  about X, it's about Y")
- "Esto es lo que aprendí" ("Here's what I learned")
- Tríadas de tres elementos
- Líneas con una pregunta retórica suelta: "¿El resultado?" ("The result?")
- Emoji de cohete, fuego, foco, destellos y diana
- Muros de hashtags
- El modelo hablando de sí mismo ("Como IA, ...") y aperturas de conclusión
  de ensayo ("En resumen, ...")
- Cebo de interacción reflejo: "¿Qué opinan?", "¿Están de acuerdo?",
  "¿Alguien más?" ("Thoughts?", "Agree?", "Who else?")
- Oraciones del mismo largo y viñetas del mismo largo

Esa lista es tu trabajo. Reescribe a mano cada línea marcada, manteniendo el
sentido, y vuelve a correr `detect.py`. Es la parte que lleva el puntaje de
REVISAR a APROBADO, y es la parte que un script no puede hacer.

## Los cinco chequeos

`detect.py` puntúa cinco señales de 0 a 100; más alto es más humano:

| chequeo | qué mide | así se ve la máquina |
| --- | --- | --- |
| RITMO | la variación del largo de las oraciones | todas las oraciones del mismo largo |
| CONCRECIÓN | números, nombres y datos concretos cada 100 palabras | sustantivos abstractos, sin cifras |
| RELLENO | coincidencias con el léxico cada 100 palabras | vocabulario de frases hechas |
| HUELLA | caracteres invisibles, rayas largas y comillas curvas cada 1000 caracteres | tipografía perfecta |
| VOZ | primera y segunda persona, patrones delatores y, en inglés, contracciones | sin persona, revelaciones montadas |

El veredicto pondera el promedio al 60% y el **chequeo más débil** al 40%,
porque a un detector le basta una señal para dispararse. APROBADO necesita un
total de 70 o más, sin ningún chequeo debajo de 55. En la salida `--json`, los
chequeos y el veredicto conservan sus nombres en inglés (BURSTINESS,
SPECIFICITY, SLOP DENSITY, FINGERPRINT, VOICE; PASS, REVIEW, FLAGGED), y el
idioma usado va en `language` (`es` o `en`).

## Dilo con honestidad

Son cinco heurísticas locales basadas en las señales que miran los detectores
públicos. Corren por completo en el equipo del usuario y no se sube
nada. **No** son GPTZero, Originality, Copyleaks, Winston ni Turnitin, no
llaman a esas APIs y no pueden prometer sus veredictos. Arreglar lo que miden
suele mover esos números, porque miden las mismas cosas de fondo. Esa es la
afirmación. No hagas una más grande en nombre del usuario, y no le digas a un
usuario que su texto es indetectable.

## Orden de los pasos

1. `humanize.py draft.txt -o clean.txt --report`
2. Lee los patrones marcados. Reescribe tú esas líneas.
3. `detect.py draft.txt clean.txt` para mostrar el antes y el después.
4. Si el veredicto no es APROBADO, arregla el chequeo más débil que nombra la
   salida y vuelve a intentar. Dos rondas es lo normal. Cinco significa que el
   borrador se escribió con fórmula, y la solución es otro borrador, no más
   pasadas.
5. Muéstrale al usuario el texto limpio y el puntaje. Nunca el puntaje solo.
