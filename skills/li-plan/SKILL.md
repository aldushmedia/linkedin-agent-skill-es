---
name: li-plan
description: >-
  Arma la semana en LinkedIn: qué publicar, cuándo publicarlo y con quién
  interactuar. Úsala cuando el usuario diga "planea mi semana", "qué debería
  publicar", "calendario de contenido", "no tengo nada sobre qué publicar", o
  quiera un calendario de publicaciones y una lista de interacción.
---

# li-plan

La sala de control. Todo lo demás de este paquete ejecuta; esto decide qué se
ejecuta. Córrelo una vez por semana, el mismo día.

## Entrada

Si existen `~/.claude/linkedin/voice.md` y `log.md`, léelos: el plan no debe
repetir un tema de las últimas dos semanas. Si no existen, pide cuatro cosas y
anótalas:

1. Qué vende el usuario, y a quién.
2. Los tres o cuatro temas por los que quiere que lo conozcan.
3. Qué pasó de verdad esta semana: una llamada con un cliente, un número, un
   error, algo que construyó, una discusión que tuvo. De ahí salen los posts.
4. De diez a veinte personas o empresas ante las que vale la pena hacerse
   visible.

## Qué publicar

Cuatro posts por semana le ganan a siete. La constancia es un piso, no una
meta, y el quinto post de una semana casi siempre es el flojo que baja el
promedio.

Mezcla a lo largo de la semana, nunca dos del mismo tipo seguidos:

| tipo | proporción | trabajo |
| --- | --- | --- |
| **Prueba** | 1 por semana | algo que pasó, con un número |
| **Opinión** | 1 por semana | una postura que te podría costar seguidores |
| **Enseñar** | 1 por semana | algo que el lector puede hacer hoy |
| **Historia** | 1 cada dos semanas | una escena con diálogo y un costo |
| **Oferta** | 1 cada dos semanas | lo que vendes, dicho con claridad, sin disculparte |

Para cada espacio da: el tema, el ángulo específico sacado de lo que pasó esta
semana, y el número de la fórmula de gancho de `li-post/hooks.json` que le
queda. No un tema: un ángulo. "IA" no es un plan. "La propuesta que perdimos
porque nuestro borrador hecho con IA tenía una raya larga" es un post.

## Cuándo publicar

Publica cuando la audiencia del usuario está frente a su escritorio. Para una
audiencia B2B en una sola zona horaria, de martes a jueves, de 7:30 a 9:30 hora
local, es el punto de partida que funciona, con el lunes por la tarde y el
viernes por la mañana como segunda opción. Los fines de semana son para posts
de historias personales o para nada.

Pero dilo claro: **el día y la hora importan mucho menos que si la primera
línea es buena.** Si el usuario está optimizando los horarios antes de que sus
ganchos funcionen, está puliendo lo que no es, y tienes que decírselo.

Ajusta los horarios a la zona horaria de su audiencia, no a la del usuario, si
son distintas.

## Con quién interactuar

Arma una lista de 10, dividida en tres:

- **5 de alcance**: personas con una audiencia que el usuario quiere, en cuyos
  posts puede aportar de verdad. Comenta antes de que tengan 20 comentarios o
  nadie lo ve.
- **3 colegas**: mismo nivel, mismo campo. Es el grupo que devuelve la
  interacción.
- **2 compradores**: personas que de verdad podrían comprar. Comenta en sus
  posts durante semanas antes de cualquier DM, y nunca vendas en un
  comentario.

20 minutos por día, antes de publicar, no después. Los comentarios en los posts
de otros son lo que hace que el post del propio usuario funcione.

## Resultado

```
SEMANA DEL 8 DE SEPTIEMBRE

LUN  solo interactuar  (20 min, lista abajo)
MAR  8:15  PRUEBA    #17 Ancla de tiempo      - la propuesta rehecha: de 5 h a 20 min
MIÉ  solo interactuar
JUE  8:00  OPINIÓN   #1  A contracorriente    - por qué eliminamos la llamada de descubrimiento
VIE  8:30  ENSEÑAR   #21 Valor directo        - el correo de 4 líneas para reabrir, regalado
SÁB  -
DOM  16:00 HISTORIA  #9  Arranque en frío     - el correo de "nos vamos con alguien más barato"

INTERACTUAR  (5 de alcance / 3 colegas / 2 compradores)
  ...

Di "escribe el martes" y lo redacto.
```

Escribe el plan en `~/.claude/linkedin/plan.md` para que las demás skills
puedan leerlo. No se programa ni se publica nada en ningún lado: es un plan, y
lo ejecuta el usuario.
