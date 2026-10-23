---
name: li-carousel
description: >-
  Arma un post de documento (carrusel) de LinkedIn: el texto diapositiva por
  diapositiva, la portada que se gana el deslizamiento y el PDF para subir.
  Úsala cuando el usuario diga "carrusel", "post de documento", "diapositivas
  para LinkedIn", "convierte esto en un carrusel", o tenga una idea en forma de
  lista que se moriría como post de texto.
---

# li-carousel

Los posts de documento son el formato con más tiempo de lectura en LinkedIn,
porque cada deslizamiento cuenta y un desplazamiento no. El formato premia una
idea dividida en pasos. Castiga un post de texto cortado en pedazos.

## Cuándo usarlo en lugar de un post de texto

Usa un carrusel cuando la idea tiene **secuencia**: pasos, una cuenta
regresiva, una progresión de antes y después, un marco con partes. Usa un post
de texto cuando la idea es una sola afirmación. Repartir una afirmación en ocho
diapositivas es la forma más común en que fallan los carruseles, y si eso es lo
que tiene el usuario, díselo y pásalo a `/li-post`.

## Estructura

De 8 a 12 diapositivas. Menos de 8 es un post de texto. Más de 12, y la tasa de
lectura completa se desploma.

```
1        PORTADA    el gancho, 6 palabras o menos, más una línea de promesa
2        LO QUE ESTÁ EN JUEGO  por qué importa, en una oración
3-N      UNA IDEA POR DIAPOSITIVA. Un titular de 3 a 7 palabras, y como mucho 25
                    palabras debajo. Si una diapositiva necesita un párrafo, son dos.
N+1      RESUMEN    todo junto como una lista, para que la captura sirva
ÚLTIMA   LLAMADO    una acción. Seguir, comentar una palabra clave o el enlace. Una.
```

## Reglas para el texto de las diapositivas

- **La diapositiva 1 es el 80% del resultado.** Seis palabras. Grandes. El
  resto no puede salvar una portada que nadie desliza.
- **Numera cada diapositiva** (3/10). Más gente llega al final cuando puede ver
  dónde termina.
- **Ninguna diapositiva es un párrafo.** Si no lo puedes decir en 25 palabras,
  divídelo.
- **La diapositiva de resumen es la que la gente captura.** Haz que se
  sostenga sola.
- **El @usuario de quien publica en cada diapositiva**, pequeño, en la esquina
  de abajo. Las capturas viajan sin ti.

## Cómo hacer el PDF

LinkedIn pide un PDF de 1080x1350 (4:5) para ocupar lo máximo del feed, de
menos de 100 MB y menos de 300 páginas. Hazlo como HTML e imprímelo a PDF:

```bash
# una página por diapositiva, 1080x1350, sin márgenes
# luego: Chrome headless --print-to-pdf, o el conversor de HTML a PDF que ya uses
```

Escribe el HTML con un `<section>` por diapositiva, `width:1080px;
height:1350px; page-break-after:always`, un solo color de acento y letra de no
menos de 28px: la gente los lee en el teléfono, en miniatura. Si el usuario
tiene una skill de marca o un sistema de diseño en este proyecto, úsalo y no
inventes una paleta.

## Resultado

Primero el texto diapositiva por diapositiva, como una lista numerada que el
usuario pueda leer en diez segundos. Luego el **texto del post** que la
acompaña: un carrusel igual necesita 2 o 3 líneas arriba, que son el gancho
real en el feed. Pasa los dos por `/li-human`. Arma el PDF solo si el usuario
aprueba el texto.

No se sube nada a LinkedIn. El usuario publica el PDF.
