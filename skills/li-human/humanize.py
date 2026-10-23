#!/usr/bin/env python3
"""
humanize.py: quita la huella de la máquina de un borrador.

Tres pasadas, en este orden:

  1. INVISIBLES   borra o normaliza los caracteres que un teclado humano nunca
                  produce: uniones de ancho cero, uniones de palabras, guiones
                  suaves, BOM, caracteres de etiqueta Unicode, espacios sin salto y
                  estrechos. Sobreviven al copiar y pegar y son el rastro más
                  mecánico de cualquier texto generado.
  2. TIPOGRAFÍA   raya larga -> coma, raya media -> guion, comillas curvas ->
                  rectas, puntos suspensivos -> tres puntos, viñeta -> guion.
  3. LÉXICO       reemplaza el léxico de relleno de slop.json con palabras simples,
                  respetando las mayúsculas y sin tocar las URL.

Funciona con textos en inglés y en español: detecta el idioma y usa solo el
léxico y los patrones de ese idioma. En español, además, cuando borra una
apertura ("Cabe destacar que el plan...") empieza la oración con mayúscula ("El
plan..."), y ajusta la "y" o la "e" que queda delante de un reemplazo ("sólido e
innovador" pasa a "sólido y nuevo"). Con textos en inglés, el resultado es el
mismo del proyecto original.

Los patrones delatores (tríadas, "no es solo X, es Y", muros de hashtags) se
REPORTAN, nunca se reescriben solos: reescribir la forma de una oración necesita
criterio, así que es trabajo del modelo, no de una expresión regular.

Uso
  python3 humanize.py draft.txt
  python3 humanize.py draft.txt --report
  pbpaste | python3 humanize.py - --report
  python3 humanize.py draft.txt --json
  python3 humanize.py draft.txt -o clean.txt
  python3 humanize.py draft.txt --lang es     # fuerza el idioma en lugar de detectarlo
"""

import argparse
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "slop.json")

URL_RE = re.compile(r"https?://\S+|www\.\S+|\S+@\S+\.\S+")
SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")
WORD_RE_ES = re.compile(r"[^\W\d_]+")

# Words that only one of the two languages uses a lot. Same list as detect.py.
FUNCTION_WORDS = {
    "es": set("de la que el en y los las del se por con un una para es al lo como más pero sus su le "
              "este esta porque cuando muy sobre también hasta hay donde desde todo nos todos les ni "
              "otro otra eso esto ellos ellas yo mi mis tu tus te qué cómo está están fue ser tiene "
              "tienen hace ese esa estos estas mucho muchos nada algo así aquí después antes ahora "
              "siempre nunca".split()),
    "en": set("the and of to is in that it for was on are with as at be this have from or by but "
              "not what all were we when your can there an which do their if will would about been "
              "had they them then than its our you i my".split()),
}
LANG_NAME = {"es": "español", "en": "inglés"}
DELETED = "\x01"   # marks a Spanish deletion until the sentence is capitalized


def language(text):
    """'es' or 'en', by counting function words. A tie stays English, like the original."""
    tokens = WORD_RE_ES.findall(text.lower())
    es = sum(1 for t in tokens if t in FUNCTION_WORDS["es"])
    en = sum(1 for t in tokens if t in FUNCTION_WORDS["en"])
    return "es" if es > en else "en"


def for_lang(entries, lang):
    """Lexicon entries for one language. Entries without "lang" are the original English ones."""
    return [e for e in entries if e.get("lang", "en") == lang]


def load_lexicon(path=LEX):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _cp(spec):
    """'U+200B' -> '\\u200b';  'U+E0000-U+E007F' -> (start, end)."""
    if "-" in spec:
        a, b = spec.split("-")
        return (int(a[2:], 16), int(b[2:], 16))
    return int(spec[2:], 16)


def protect_urls(text):
    """Swap URLs for placeholders so no pass rewrites inside a link."""
    found = []

    def stash(m):
        found.append(m.group(0))
        return f"\x00URL{len(found) - 1}\x00"

    return URL_RE.sub(stash, text), found


def restore_urls(text, found):
    for i, url in enumerate(found):
        text = text.replace(f"\x00URL{i}\x00", url)
    return text


def pass_invisible(text, lex):
    """Delete or space-normalise invisible characters. Returns (text, hits)."""
    hits = []
    for entry in lex["invisible"]:
        cp = _cp(entry["cp"])
        if isinstance(cp, tuple):
            pattern = "[" + re.escape(chr(cp[0])) + "-" + re.escape(chr(cp[1])) + "]"
        else:
            pattern = re.escape(chr(cp))
        n = len(re.findall(pattern, text))
        if n:
            hits.append({"name": entry["cp"] + " " + entry["name"], "count": n,
                         "action": entry["action"]})
            text = re.sub(pattern, "" if entry["action"] == "delete" else " ", text)
    # Any remaining Cf (format) character is invisible by definition.
    stray = [c for c in text if unicodedata.category(c) == "Cf"]
    if stray:
        hits.append({"name": "otros caracteres invisibles de formato", "count": len(stray),
                     "action": "delete"})
        text = "".join(c for c in text if unicodedata.category(c) != "Cf")
    return text, hits


def pass_typographic(text, lex):
    hits = []
    for entry in lex["typographic"]:
        ch = entry["from"]
        n = text.count(ch)
        if not n:
            continue
        hits.append({"name": f"{ch} {entry['name']}", "count": n, "to": entry["to"].strip() or "(espacio)"})
        if ch == "\u2014":
            # " word, word " and "word,word" style: an em dash with or without spaces becomes a comma + space.
            text = re.sub(r"\s*\u2014\s*", ", ", text)
        elif ch == "\u2013":
            text = re.sub(r"\s*\u2013\s*(?=\d)", "-", text)      # 5 en dash 10 -> 5-10
            text = re.sub(r"\s+\u2013\s+", ", ", text)            # used as em dash
            text = text.replace("\u2013", "-")
        else:
            text = text.replace(ch, entry["to"])
    # A comma inserted before existing punctuation reads wrong.
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*\n", "\n", text)
    return text, hits


def _match_case(src, repl):
    if not repl:
        return repl
    if src.isupper() and len(src) > 1:
        return repl.upper()
    if src[0].isupper():
        return repl[0].upper() + repl[1:]
    return repl


def _conjunction(conj, word):
    """Spanish "y" is "e" before an i sound: "sólido e innovador" -> "sólido y nuevo"."""
    want = "e" if re.match(r"(?i)h?i(?![aeoáéó])", word) else "y"
    return want.upper() if conj.isupper() else want


def _replace_es(m, repl):
    conj, space, word = m.groups()
    new = _match_case(word, repl or DELETED)
    if conj and new != DELETED:
        conj = _conjunction(conj, new)
    return (conj or "") + (space or "") + new


def pass_lexical(text, lex, lang="en"):
    """Replace slop words and phrases. Longest first so phrases win."""
    hits = []
    entries = sorted(for_lang(lex["phrases"] + lex["words"], lang),
                     key=lambda e: len(e["find"]), reverse=True)
    for entry in entries:
        find = entry["find"]
        core = r"\b" + re.escape(find).replace(r"\ ", r"\s+") + r"\b"
        if lang == "es":
            # Take the "y" or "e" in front too, so it can agree with the replacement.
            pattern = re.compile(r"(?:\b([ye])(\s+))?(" + core + ")", re.IGNORECASE)
        else:
            pattern = re.compile(core, re.IGNORECASE)
        found = pattern.findall(text)
        if not found:
            continue
        hits.append({"find": find, "replace": entry["replace"] or "(borrado)",
                     "count": len(found), "family": entry["family"]})
        if lang == "es":
            text = pattern.sub(lambda m: _replace_es(m, entry["replace"]), text)
        else:
            text = pattern.sub(lambda m: _match_case(m.group(0), entry["replace"]), text)
    if lang == "es":
        # "Cabe destacar que el plan..." lost its opener: the sentence starts with a capital.
        text = re.sub(r"(?m)(^[ \t]*[¡¿]?|[.!?][ \t]+[¡¿]?)" + DELETED + r"[" + DELETED + r" \t,;:]*"
                      r"([¡¿]?[^\W\d_])", lambda m: m.group(1) + m.group(2).upper(), text)
        # A whole sentence deleted after another one ("Ganamos 12. Léelo otra vez. Nadie..."),
        # or an aside between commas ("Y, cabe destacar que, nadie...").
        text = re.sub(r"([.!?])[ \t]*" + DELETED + r"[ \t]*[.!?]", r"\1", text)
        text = re.sub(r"([,;:])[ \t]*" + DELETED + r"[ \t]*[,;:]", r"\1", text)
        text = text.replace(DELETED, "")
    # Clean up after deletions.
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"(?m)^[ \t]*([,.;:])\s*", "", text)
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r"(?m)^[ \t]+$", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # An em dash that became a comma, followed by a sentence connective, leaves
    # a splice ("is important, also, it's proof"). Promote it to a full stop.
    connectives = (r"también|así que|aun así|en el fondo|al final" if lang == "es"
                   else r"also|so|still|basically|in the end")
    text = re.sub(r",\s*(" + connectives + r")\s*,\s*",
                  lambda m: ". " + m.group(1)[0].upper() + m.group(1)[1:] + ", ", text)
    return text, hits


def scan_structures(text, lex, lang="en"):
    flags = []
    for s in for_lang(lex["structures"], lang):
        try:
            pattern = re.compile(s["regex"], re.MULTILINE)
        except re.error:
            continue
        found = pattern.findall(text)
        if found:
            flags.append({"name": s["name"], "count": len(found), "fix": s["fix"]})
    # Sentence-length uniformity is structural too.
    lens = [len(s.split()) for s in SENT_RE.findall(text) if len(s.split()) > 2]
    if len(lens) >= 4:
        mean = sum(lens) / len(lens)
        var = sum((n - mean) ** 2 for n in lens) / len(lens)
        cv = (var ** 0.5) / mean if mean else 0
        if cv < 0.35:
            flags.append({
                "name": f"Oraciones del mismo largo (variación {cv:.2f})",
                "count": len(lens),
                "fix": "Parte una oración en dos. Deja que otra se alargue. Las máquinas escriben parejo.",
            })
    return flags


def humanize(text, lex, lang=None):
    """lang is "es" or "en"; None detects it from the text."""
    lang = lang or language(text)
    text, urls = protect_urls(text)
    text, inv = pass_invisible(text, lex)
    text, typo = pass_typographic(text, lex)
    text, lexi = pass_lexical(text, lex, lang)
    text = restore_urls(text, urls)
    return text.strip() + "\n", {
        "invisible": inv,
        "typographic": typo,
        "lexical": lexi,
        "structures": scan_structures(text, lex, lang),
    }


ACTION = {"delete": "borrar", "space": "espacio"}


def render_report(report, out=sys.stderr, lang=None):
    def head(title):
        print(f"\n{title}\n" + "-" * len(title), file=out)

    total = sum(h["count"] for h in report["invisible"]) \
        + sum(h["count"] for h in report["typographic"]) \
        + sum(h["count"] for h in report["lexical"])

    head("REPORTE DEL HUMANIZADOR")
    print(f"{total} rastros de máquina quitados, "
          f"{len(report['structures'])} patrones delatores marcados para reescribir", file=out)
    if lang:
        print(f"texto en {LANG_NAME[lang]}", file=out)

    if report["invisible"]:
        head("1. CARACTERES INVISIBLES")
        for h in report["invisible"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {ACTION.get(h['action'], h['action'])}", file=out)
    if report["typographic"]:
        head("2. TIPOGRAFÍA")
        for h in report["typographic"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['to']}", file=out)
    if report["lexical"]:
        head("3. LÉXICO DE RELLENO")
        for h in report["lexical"]:
            print(f"  {h['count']:>3}x  {h['find']}  -> {h['replace']}   [{h['family']}]", file=out)
    if report["structures"]:
        head("4. PATRONES DELATORES  (no se arreglan solos: reescríbelos tú)")
        for h in report["structures"]:
            print(f"  {h['count']:>3}x  {h['name']}\n        {h['fix']}", file=out)
    if not any(report.values()):
        head("LIMPIO")
        print("  No hay nada que quitar.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Quita la huella de la máquina de un borrador.")
    ap.add_argument("input", nargs="?", default="-", help="archivo, o - para leer de la entrada estándar")
    ap.add_argument("-o", "--out", help="escribe aquí el texto limpio en lugar de la salida estándar")
    ap.add_argument("--report", action="store_true", help="muestra qué cambió, en la salida de errores")
    ap.add_argument("--json", action="store_true", help="imprime {text, report, language} como JSON")
    ap.add_argument("--lexicon", default=LEX, help="ruta a slop.json")
    ap.add_argument("--lang", choices=["auto", "es", "en"], default="auto",
                    help="idioma del texto: auto lo detecta (por defecto), es o en")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    lex = load_lexicon(args.lexicon)
    lang = language(raw) if args.lang == "auto" else args.lang
    clean, report = humanize(raw, lex, lang)

    if args.json:
        print(json.dumps({"text": clean, "report": report, "language": lang}, indent=2, ensure_ascii=False))
        return
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(clean)
        print(f"listo: {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(clean)
    if args.report:
        render_report(report, lang=lang)


if __name__ == "__main__":
    main()
