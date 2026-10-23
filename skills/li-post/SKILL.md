---
name: li-post
description: >-
  Escribe un post de LinkedIn a partir de una idea en bruto con 21 fórmulas
  de ganchos probadas, con la voz del propio usuario y humanizado para que no
  suene a IA. Úsala siempre que el usuario quiera un post de LinkedIn, un
  gancho, un borrador para el feed, "un post sobre X", "convierte esto en un
  post de LinkedIn", o pida opciones de ganchos. Entrega tres opciones de
  gancho, un borrador completo y un bloque listo para copiar que nunca se
  publica sin un sí explícito.
---

# li-post

Convierte una idea en bruto en un post de LinkedIn que suena como la persona
que lo publica.

## Antes de escribir

1. Lee `~/.claude/linkedin/voice.md` si existe. Ese archivo es el perfil de
   voz del usuario: cómo habla, lo que nunca dice, a quién le habla. Si no
   existe, pide **tres posts suyos anteriores**, deduce la voz a partir de
   ellos y escribe el archivo. No te saltes esto y no inventes una voz. Un
   post con la voz equivocada es peor que no publicar nada.
2. Lee `hooks.json` en esta carpeta. Las 21 fórmulas, con plantillas, ejemplos
   completos, para qué sirve cada una y cómo suele arruinarse.
3. Si la idea es pobre ("un post sobre IA"), no la rellenes. Haz una sola
   pregunta que lo junte todo: qué pasó, a quién, y qué costó o qué dejó. Un
   post necesita una cosa específica y verdadera. Consíguela antes de escribir.

## La forma

LinkedIn premia el tiempo de lectura, los guardados y los comentarios, en ese
orden. Así que:

```
Línea 1    el gancho. Sola. Tiene que sobrevivir al corte en unos 140 caracteres en el teléfono.
Línea 2    la recompensa de la línea 1, no la preparación de la línea 3.
Cuerpo     párrafos cortos, de 1 a 3 líneas cada uno, con una línea en blanco entre cada uno.
           Nada de muros de texto. El espacio en blanco es el formato.
El giro    una línea que replantea lo anterior.
Cierre     una pregunta específica, o una instrucción. Nunca las dos.
```

Extensión: entre 900 y 1300 caracteres es el rango que funciona para un post
de texto. Menos de 400 se lee como un pensamiento, no como un post. Más de
2000 tiene que ganarse cada línea, y la línea 2 tiene que pagar el toque en
"ver más".

## El ciclo

**1. Elige tres ganchos, no uno.** Pasa la idea por `hooks.json` y elige las
tres fórmulas que de verdad le quedan. Fórmulas distintas, no tres variaciones
de una. Muéstralas como tres líneas numeradas y di cuál publicarías y por qué,
en una oración.

**2. Escribe el post completo** con el gancho más fuerte.

**3. Humanízalo.** Pasa el borrador por `/li-human` antes de mostrarlo. Cada
post de esta skill sale humanizado. No es un paso extra opcional: es la razón
por la que vale la pena leer el borrador.

**4. Imprime el bloque.** Listo para copiar, en un bloque cercado, exactamente
como hay que pegarlo. Luego, debajo:

```
POST LISTO
gancho:       #17 Ancla de tiempo
extensión:    1140 caracteres
humanizador:  6 rastros quitados, puntaje humano 84 APROBADO
publicar:     martes 8:15 ET (según tu plan)

Responde "sí" para registrarlo, o dime qué cambiar.
```

**5. Nunca publiques.** Esta skill produce texto. El usuario lo publica. Con
un "sí", agrega el post a `~/.claude/linkedin/log.md` con la fecha, el gancho
usado y la primera línea, para que `/li-audit` tenga un historial con el que
trabajar después.

## Las reglas que hacen la diferencia

- **Una idea por post.** Si el borrador tiene dos, tienes dos posts. Dilo.
- **Números antes que adjetivos.** "4200 dólares" le gana a "mucho". Si el
  usuario no te dio un número, pídeselo en lugar de escribir alrededor del
  hueco.
- **Nada de cebo de interacción.** "¿Qué opinan?" y "¿Están de acuerdo?" están
  muertos. La pregunta del cierre tiene que ser una que solo este post podría
  hacer.
- **Tres hashtags como máximo**, al final, y solo si son categorías reales que
  alguien sigue.
- **Nada de enlaces en el cuerpo del post.** LinkedIn le resta alcance a los
  posts con enlaces externos. Pon el enlace en el primer comentario y dilo en
  el resumen.
- **Nunca inventes.** Ni métricas, ni clientes, ni cifras de ingresos ni
  resultados inventados con el nombre del usuario, ni siquiera de relleno. Si
  hace falta un número y no se sabe, deja `{{tu número}}` en el borrador y
  márcalo.

## Ejemplo

```
/li-post armamos una herramienta interna que bajó el tiempo de una propuesta de 5 horas a 20 minutos
```

```
GANCHOS
1. #17 Ancla de tiempo       Escribir una propuesta me llevaba 5 horas. Ahora me lleva 20 minutos.
2. #12 La comparación        Un redactor de propuestas de 12 000 dólares vs un fin de semana y una plantilla. Ganó el fin de semana.
3. #3  Confesión de un error Durante dos años les cobré a mis clientes horas que perdía dándole formato.

Publicaría la #17: la proporción es creíble y el número es tuyo.
```
