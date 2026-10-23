---
name: li-repurpose
description: >-
  Convierte un contenido largo (un video de YouTube, un podcast, un boletín,
  un artículo de blog, una transcripción o una llamada con un cliente) en una
  semana de posts de LinkedIn. Úsala cuando el usuario diga "reutiliza esto",
  "convierte esto en posts", "tengo un video, un boletín o una
  transcripción", o pegue un contenido largo y lo quiera en LinkedIn.
---

# li-repurpose

Un buen contenido largo contiene de cuatro a seis posts. La mayoría de la
gente saca uno y tira el resto.

## Entrada

Una transcripción, un artículo, un boletín, un guion, el resumen de una
llamada. Si el usuario da una URL de YouTube y hay una herramienta de
transcripción disponible en la sesión, úsala; si no, pídele que pegue el texto.
Lee todo antes de sacar nada.

## Extrae, no resumas

El resumen de un video no es un post. Nadie quiere el resumen. Recorre el
contenido y saca las cosas que se sostienen solas:

| qué sacar | qué es |
| --- | --- |
| **Afirmaciones** | cada oración que empezaría una discusión |
| **Números** | cada cifra, costo, duración, porcentaje |
| **Historias** | cada momento con una persona, una escena y un costo |
| **Mecanismos** | cada explicación de "así es como funciona..." |
| **Errores** | cada admisión de algo que salió mal |
| **Frases** | cada oración que ya se puede citar tal cual |

Haz la lista de lo que encontraste, con conteos, antes de escribir nada. Si el
contenido da menos de cuatro elementos, es pobre, y cuatro posts exprimidos de
ahí también lo van a ser. Dilo.

## Luego arma la semana

Cada elemento se convierte en un post, y cada post tiene que sostenerse
completamente solo: el lector no vio el video y nunca lo va a ver. Nunca
escribas "como dije en mi último video". El post es lo que importa.

Asígnale a cada uno una fórmula de gancho de `li-post/hooks.json`, y
varíalas: cinco posts de una misma fuente con la misma forma de gancho se leen
como una fábrica de contenido.

Ordénalos a lo largo de la semana para que la afirmación más fuerte vaya
primero, la historia a mitad de semana, y el post del mecanismo al final,
cuando la gente a la que le gustaron los anteriores lo está esperando.

## Resultado

```
FUENTE: "Por qué eliminamos las llamadas de descubrimiento" (18 min, 3400 palabras)

ENCONTRADO  4 afirmaciones, 6 números, 2 historias, 3 mecanismos, 1 error, 5 frases citables

SEMANA
MAR  #1  A contracorriente   Las llamadas de descubrimiento son el impuesto de un mal sitio web
MIÉ  #17 Ancla de tiempo     Recuperamos 6 horas por semana borrando un enlace de calendario
JUE  #9  Arranque en frío    "¿Podemos hacer una llamada rápida?"
VIE  #21 Valor directo       El formulario de 4 preguntas que reemplazó la llamada. Llévatelo.

Di "escribe el martes" y lo redacto.
```

Luego redacta cuando te lo pidan, uno por uno, cada uno a través de `/li-post` y
`/li-human`. No entregues cuatro posts terminados de una vez: van a sonar
todos igual, y el usuario no va a editar ninguno.
