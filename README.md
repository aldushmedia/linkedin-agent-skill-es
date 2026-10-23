# La skill de agente de LinkedIn

Once skills para Claude que gestionan una cuenta de LinkedIn. Gratis, MIT, sin
registro, sin API key, nada que conectar.

Una escribe tus posts a partir de 21 fórmulas de ganchos. Otra comenta en los
posts de otras personas. Otra gestiona las respuestas debajo de los tuyos. Otra
puntúa tu perfil sobre 100 y reescribe lo que perdió puntos. Otra planea la
semana: qué publicar, cuándo y con quién interactuar.

Y una es el humanizador, que es la razón por la que las demás sirven. Le quita
a un borrador las rayas largas, el vocabulario de relleno y los caracteres
invisibles de marca de agua, y luego puntúa lo que queda con un panel de
detección de cinco chequeos antes de que tú lo veas. Funciona con textos en
español y en inglés.

**No se publica nada hasta que digas que sí.** Estas skills escriben. Tú
publicas.

## Instalación

Pega esto en Claude:

```
https://github.com/aldushmedia/linkedin-agent-skill-es

Instala esta skill y luego confirma que /li-post funciona.
```

O hazlo tú mismo, en Claude Code:

```bash
git clone https://github.com/aldushmedia/linkedin-agent-skill-es.git
cp -r linkedin-agent-skill-es/skills/li-* ~/.claude/skills/
```

O como plugin:

```
/plugin marketplace add aldushmedia/linkedin-agent-skill-es
/plugin install linkedin-agent-skill-es@linkedin-agent-skill-es
```

Instaladas como plugin, Claude Code agrupa las skills bajo el nombre del
plugin, así que aparecen como `/linkedin-agent-skill-es:li-post` y así con las
demás. Si prefieres el `/li-post` simple, copia las carpetas. Para un solo
proyecto en lugar de global: copia esas mismas carpetas en el `.claude/skills/`
de tu repo. ¿No usas Claude Code? Pega cualquier `SKILL.md` al inicio de un
chat y funciona como un modo. Pierdes las dos herramientas de Python, que son
la mayor parte del valor de `/li-human`, pero el resto funciona.

Después, dedícale diez minutos a `templates/voice.md`. Cópialo a
`~/.claude/linkedin/voice.md` y llénalo, o pega tres de tus posts en Claude y
di "escribe mi voice.md a partir de estos". Todas las skills leen ese archivo.
Si te lo saltas, todo sale sonando como todos los demás.

## Las once

| comando | qué hace |
| --- | --- |
| `/li-post` | Una idea convertida en post. Tres opciones de gancho a partir de [21 fórmulas](skills/li-post/hooks.json), un borrador completo, humanizado antes de que lo veas. |
| `/li-comment` | Comentarios en los posts de otras personas. Nueve tipos, elegidos según lo que el post es de verdad. Nunca "¡Gran post!". |
| `/li-reply` | El hilo debajo de tu propio post. Ordena cada comentario en posible cliente / aporte / colega / apoyo / ruido, y luego escribe en ese orden. |
| `/li-profile` | Puntúa tu perfil sobre 100 con una [rúbrica de 12 partes](skills/li-profile/rubric.json) y luego reescribe empezando por lo que más puntos pierde. |
| `/li-plan` | La semana. Qué publicar, cuándo publicarlo y las 10 personas con las que interactuar. Escribe `~/.claude/linkedin/plan.md`. |
| `/li-human` | El humanizador. Dos scripts que funcionan de verdad. Mira abajo. |
| `/li-carousel` | Posts de documento. El texto diapositiva por diapositiva, la portada que se gana el deslizamiento y el PDF para subir. |
| `/li-repurpose` | Un video, un boletín o una transcripción convertidos en una semana de posts que se sostienen solos. |
| `/li-dm` | La nota de invitación de 200 caracteres, el primer mensaje y los dos seguimientos. Dos. |
| `/li-inbox` | Ordena la bandeja en posible cliente / reclutador / colega / pedido / spam, y te dice qué detalle delató cada secuencia automática. |
| `/li-audit` | Análisis de lo que ya publicaste. Ordena por tasa de interacción y múltiplo de alcance, no por impresiones. |

## El humanizador

`/li-human` trae dos scripts de Python sin dependencias. Corren en tu equipo,
sobre tu texto, y no se sube nada. Detectan si el texto está en español o en
inglés y usan el léxico y la calibración de ese idioma. Si quieres fijar el
idioma, agrega `--lang es` o `--lang en`.

```bash
python3 humanize.py draft.txt --report      # lo limpia y muestra cada cambio
python3 detect.py draft.txt                  # lo puntúa, cinco chequeos
python3 detect.py before.txt after.txt       # demuestra la diferencia
```

**Lo que se quita solo:**

- **Caracteres invisibles.** Espacios y uniones de ancho cero, uniones de
  palabras, guiones suaves, marcas de orden de bytes, caracteres de etiqueta
  Unicode, espacios sin salto y estrechos. Tu teclado no los produce.
  Sobreviven al copiar y pegar y son invisibles en cualquier editor que tengas.
- **Tipografía.** Raya larga a coma, raya media a guion, comillas curvas a
  rectas, puntos suspensivos a tres puntos.
- **El léxico.** 168 palabras y frases hechas en español ("en el mundo
  actual", "cabe destacar que", potenciar, sinergia, robusto, "un testimonio
  de", "sin más preámbulos") y 113 en inglés (delve, leverage, robust,
  seamless, "in today's fast-paced world", "let that sink in"), cada una con
  un reemplazo simple, respetando las mayúsculas y sin tocar las URL. En
  español, los reemplazos respetan el género y el número ("robusta" pasa a
  "sólida"), la "y" o la "e" de delante se ajusta ("sólido e innovador" pasa a
  "sólido y nuevo") y, si se borra una apertura, la oración vuelve a empezar
  con mayúscula. Está en [`slop.json`](skills/li-human/slop.json) y está hecho
  para editarse.

**Lo que se marca en lugar de arreglarse:** "No es solo X, es Y", "no solo X
sino también Y", "no se trata de X, se trata de Y", tríadas de tres elementos,
preguntas retóricas sueltas ("¿El resultado?"), muros de hashtags, cebo de
interacción reflejo ("¿Qué opinan?"), oraciones del mismo largo, y sus
equivalentes en inglés. Cambiar la forma de una oración requiere criterio, así
que eso se devuelve para reescribir en lugar de destrozarlo con una expresión
regular.

**Los cinco chequeos**, puntuados de 0 a 100, más alto es más humano:

| chequeo | qué mide |
| --- | --- |
| RITMO | la variación del largo de las oraciones. Los modelos escriben parejo. |
| CONCRECIÓN | números, nombres y datos concretos cada 100 palabras |
| RELLENO | coincidencias con el léxico cada 100 palabras |
| HUELLA | caracteres invisibles, rayas largas y comillas curvas cada 1000 caracteres |
| VOZ | primera y segunda persona, patrones delatores y, en inglés, contracciones |

El veredicto pondera el promedio al 60% y el **chequeo más débil** al 40%,
porque a un detector le basta una señal para dispararse.

El español no usa contracciones y suele omitir el sujeto, así que con un texto
en español VOZ cuenta pronombres y posesivos de primera y segunda persona y
verbos en primera persona ("perdí", "mandamos", "tengo"). La cuenta de palabras
respeta las tildes y la ñ, y los nombres propios con tilde ("Bogotá") cuentan
como datos concretos. Un post humano en español puede llegar a APROBADO igual
que uno en inglés.

Con un borrador de prueba en inglés, malo a propósito:

```
  RITMO           ##############..........  60.2
  CONCRECIÓN      ######################## 100.0
  RELLENO         ........................   0.0
                  10 términos de relleno, 15.4 cada 100 palabras
  HUELLA          ........................   0.0
                  1 invisibles, 1 rayas largas, 3 comillas curvas, 1 puntos suspensivos, 0 espacios duros
  VOZ             ###.....................  14.0
                  4 patrón(es) delator(es)
--------------------------------------------------------------
  PUNTAJE HUMANO  #####...................  20.9   MARCADO
```

Después de `humanize.py`, con los patrones marcados todavía sin reescribir:

```
  20.9 MARCADO  ->  69.6 REVISAR   (+48.7)
```

El último tramo hasta APROBADO es la parte que el script te deja a ti a
propósito.

## La letra pequeña, que es la parte honesta

**Estas skills no publican en LinkedIn, y no deberían.** No hay una API
oficial para publicar en un perfil personal sin una app de un socio aprobado,
y automatizar el sitio con un navegador o con una herramienta de terceros viola
el [Acuerdo de Usuario de LinkedIn](https://www.linkedin.com/legal/user-agreement)
y hace que restrinjan las cuentas. Por eso todas las skills de aquí terminan
igual: un bloque listo para copiar, y lo pegas tú. No es una limitación que se
agregó después: es el diseño. También es la razón por la que la aprobación es
real y no una opción de configuración.

**Los cinco chequeos son heurísticas locales, no APIs de detectores.** Están
basados en las señales que miran los detectores públicos y corren por completo
en tu equipo. No son GPTZero, Originality, Copyleaks, Winston ni Turnitin, no
llaman a esos servicios y no pueden prometer sus veredictos. Arreglar lo que
miden suele mover esos números, porque miden las mismas cosas de fondo. Esa es
toda la afirmación. Nadie te puede vender con honestidad algo "indetectable", y
quien lo hace te está vendiendo otra cosa.

**La pasada de caracteres invisibles es real y es acotada.** Quita los
caracteres de ancho cero y de formato que terminan en el texto generado y
sobreviven al copiar y pegar. Es una huella genuina y verificable. No es una
afirmación sobre romper un esquema criptográfico de marca de agua, y este repo
no hace esa afirmación.

**Aquí no se inventa nada.** Ni métricas, ni clientes, ni resultados
inventados con tu nombre. Si un borrador necesita un número que no diste,
vuelve con `{{tu número}}` y una marca, siempre.

## Archivos

```
skills/li-post/hooks.json        21 fórmulas de ganchos: plantilla, ejemplo, para qué sirve, cómo se arruina
skills/li-human/slop.json        el léxico: 168 términos en español y 113 en inglés, 17 clases de invisibles, 11 patrones delatores por idioma
skills/li-human/humanize.py      las tres pasadas de limpieza
skills/li-human/detect.py        el panel de cinco chequeos
skills/li-profile/rubric.json    el puntaje del perfil, sobre 100
templates/voice.md               tu perfil de voz. Llénalo primero.
```

Los scripts son los del proyecto original, con los mensajes traducidos al
español y una adaptación para textos en español: la detección del idioma, el
léxico y los patrones en español, la cuenta de palabras con tildes y el chequeo
VOZ en español. Con textos en inglés, los puntajes y el texto limpio son los
mismos del original, y los tests lo comprueban. En la salida `--json`, los
nombres de los chequeos y del veredicto siguen en inglés, y el campo
`language` dice qué idioma se usó.

## Créditos

Traducción y adaptación al español por Aldush Media. Basada en un proyecto
original con licencia MIT; su aviso de copyright se conserva en `LICENSE`.

## Licencia

MIT. Tómala, cámbiala, publícala. Ver `LICENSE`.
