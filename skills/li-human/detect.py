#!/usr/bin/env python3
"""
detect.py: un panel de cinco chequeos que puntúa qué tan escrito a máquina se ve un borrador.

Qué es:  cinco heurísticas locales basadas en las señales que de verdad miden los
detectores de IA públicos: la variación del largo de las oraciones, lo concreto,
el vocabulario de frases hechas, la huella tipográfica y la voz. Cada puntaje se
calcula en tu equipo, solo a partir del texto. No se sube nada.

Qué NO es:  GPTZero, Originality, Copyleaks, Winston ni Turnitin. No llama a sus
APIs y no puede prometer su veredicto. Detecta lo que todos ellos miran, y por eso
arreglarlo suele mover también sus números, pero la única afirmación honesta es la
de esta línea.

Funciona con textos en inglés y en español. Detecta el idioma de cada texto y
usa la calibración de ese idioma: el léxico y los patrones delatores de ese
idioma, y una forma de contar las palabras que respeta las tildes y la ñ. En
inglés, VOZ cuenta contracciones y pronombres, igual que el proyecto original.
En español, que no usa contracciones y suele omitir el sujeto, VOZ cuenta los
pronombres y posesivos de primera y segunda persona y los verbos en primera
persona ("perdí", "mandamos", "tengo"). Con textos en inglés, los puntajes son
los mismos del proyecto original.

Cada chequeo devuelve un puntaje HUMANO de 0 a 100. Más alto es mejor.

Uso
  python3 detect.py draft.txt
  pbpaste | python3 detect.py -
  python3 detect.py draft.txt --json
  python3 detect.py before.txt after.txt      # compara dos borradores
  python3 detect.py draft.txt --lang es       # fuerza el idioma en lugar de detectarlo
"""

import argparse
import json
import os
import re
import statistics
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "slop.json")

SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")
WORD_RE = re.compile(r"[A-Za-z']+")
CONTRACTIONS = re.compile(r"\b\w+'(?:s|t|re|ve|ll|d|m)\b", re.IGNORECASE)
PRONOUNS = re.compile(r"\b(i|me|my|mine|we|us|our|you|your)\b", re.IGNORECASE)
NUMBERS = re.compile(r"\b\d[\d,.]*%?\b|\$\d")
PROPER = re.compile(r"(?<![.!?]\s)(?<!^)\b[A-Z][a-z]{2,}\b", re.MULTILINE)

# Spanish. The English constants above stay as they are, so English scores do not change.
WORD_RE_ES = re.compile(r"[^\W\d_]+")
PROPER_ES = re.compile(r"(?<![.!?]\s)(?<![.!?]\s[¿¡])(?<!^)(?<!^[¿¡])\b[A-ZÁÉÍÓÚÑÜ][a-záéíóúñü]{2,}\b",
                       re.MULTILINE)
# First and second person pronouns and possessives, and first person verbs that
# the endings below miss. Spanish has no contractions and drops the subject.
PERSON_ES = re.compile(
    r"\b(?:yo|me|mi|mis|mí|conmigo|nosotros|nosotras|nos|nuestro|nuestra|nuestros|nuestras"
    r"|tú|te|ti|tu|tus|contigo|tuyo|tuya|tuyos|tuyas|usted|ustedes"
    r"|vos|vosotros|vosotras|os|vuestro|vuestra|vuestros|vuestras"
    r"|soy|estoy|tengo|hago|digo|voy|doy|veo|creo|pienso|quiero|puedo|somos"
    r"|fui|hice|tuve|dije|estuve|pude|quise|vine|supe|puse|vi)\b", re.IGNORECASE)
# First person verbs by their ending: "perdí", "mandé", "mandamos", "tenemos", "fuimos".
VERB_ES = re.compile(r"\b[^\W\d_]+(?:[éí]|amos|emos|imos)\b", re.IGNORECASE)
NOT_VERB_ES = {
    "qué", "porqué", "café", "bebé", "comité", "josé", "cliché", "puré", "bufé", "carné", "canapé",
    "consomé", "parqué", "té", "mí", "sí", "aquí", "allí", "ahí", "así", "frenesí", "maní", "rubí",
    "esquí", "colibrí", "jabalí", "israelí", "marroquí", "iraquí", "paquistaní", "bisturí", "ají",
    "alhelí", "últimos", "penúltimos", "próximos", "mínimos", "máximos", "óptimos", "íntimos",
    "legítimos", "ínfimos", "pésimos", "décimos", "centésimos", "milésimos", "primos", "ánimos",
    "anónimos", "sinónimos", "racimos", "amos", "ramos", "tramos", "préstamos", "reclamos", "gramos",
    "kilogramos", "miligramos", "extremos", "supremos", "remos",
}

# Words that only one of the two languages uses a lot. Ambiguous ones ("a", "no", "me") are left out.
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


def language(text):
    """'es' or 'en', by counting function words. A tie stays English, like the original."""
    tokens = WORD_RE_ES.findall(text.lower())
    es = sum(1 for t in tokens if t in FUNCTION_WORDS["es"])
    en = sum(1 for t in tokens if t in FUNCTION_WORDS["en"])
    return "es" if es > en else "en"


def for_lang(entries, lang):
    """Lexicon entries for one language. Entries without "lang" are the original English ones."""
    return [e for e in entries if e.get("lang", "en") == lang]


def clamp(n):
    return max(0.0, min(100.0, n))


def scale(value, human, machine):
    """Map value onto 0-100 where `human` -> 100 and `machine` -> 0."""
    if human == machine:
        return 50.0
    return clamp((value - machine) / (human - machine) * 100)


def sentences(text):
    return [s.strip() for s in SENT_RE.findall(text) if len(s.split()) > 2]


def words(text, lang="en"):
    return (WORD_RE_ES if lang == "es" else WORD_RE).findall(text)


def check_burstiness(text):
    """Humans vary sentence length hard. Models write even."""
    lens = [len(s.split()) for s in sentences(text)]
    if len(lens) < 4:
        return 50.0, "muy corto para juzgar"
    mean = statistics.mean(lens)
    cv = statistics.pstdev(lens) / mean if mean else 0
    score = scale(cv, human=0.70, machine=0.22)
    return score, f"variación {cv:.2f} en {len(lens)} oraciones (lo ideal: 0.55 o más)"


def check_specificity(text, lang="en"):
    """Numbers, names and concrete nouns. Slop is abstract."""
    w = words(text, lang)
    if len(w) < 25:
        return 50.0, "muy corto para juzgar"
    per100 = 100 / len(w)
    proper = PROPER_ES if lang == "es" else PROPER
    hits = len(NUMBERS.findall(text)) + len(set(proper.findall(text)))
    density = hits * per100
    score = scale(density, human=6.0, machine=0.5)
    return score, f"{hits} datos concretos, {density:.1f} cada 100 palabras (lo ideal: 4 o más)"


def check_slop(text, lex, lang="en"):
    """Stock vocabulary density against the lexicon."""
    w = words(text, lang)
    if not w:
        return 50.0, "vacío"
    hits, found = 0, []
    for entry in for_lang(lex["words"] + lex["phrases"], lang):
        pattern = re.compile(r"\b" + re.escape(entry["find"]).replace(r"\ ", r"\s+") + r"\b",
                             re.IGNORECASE)
        n = len(pattern.findall(text))
        if n:
            hits += n
            found.append(entry["find"])
    density = hits * 100 / len(w)
    score = scale(density, human=0.0, machine=4.0)
    detail = f"{hits} términos de relleno, {density:.1f} cada 100 palabras"
    if found:
        detail += " (" + ", ".join(sorted(found)[:4]) + (", ..." if len(found) > 4 else "") + ")"
    return score, detail


def check_fingerprint(text):
    """Characters a phone keyboard does not produce."""
    invisible = sum(1 for c in text if unicodedata.category(c) == "Cf")
    em = text.count("\u2014")
    curly = sum(text.count(c) for c in "\u2018\u2019\u201c\u201d")
    ellip = text.count("\u2026")
    nbsp = sum(text.count(c) for c in "   ")
    total = invisible * 4 + em * 2 + curly + ellip + nbsp
    per1k = total * 1000 / max(len(text), 1)
    score = scale(per1k, human=0.0, machine=12.0)
    detail = (f"{invisible} invisibles, {em} rayas largas, {curly} comillas curvas, "
              f"{ellip} puntos suspensivos, {nbsp} espacios duros")
    return score, detail


def person_es(text):
    """Spanish first and second person: pronouns, possessives and first person verbs."""
    verbs = [v for v in VERB_ES.findall(text) if v.lower() not in NOT_VERB_ES]
    return len(PERSON_ES.findall(text)) + len(verbs)


def check_voice(text, lex, lang="en"):
    """Contractions, person, and the shapes models default to."""
    w = words(text, lang)
    if len(w) < 25:
        return 50.0, "muy corto para juzgar"
    per100 = 100 / len(w)
    if lang == "es":
        person = person_es(text) * per100
    else:
        contractions = len(CONTRACTIONS.findall(text)) * per100
        person = len(PRONOUNS.findall(text)) * per100
    tells = 0
    names = []
    for s in for_lang(lex["structures"], lang):
        try:
            n = len(re.compile(s["regex"], re.MULTILINE).findall(text))
        except re.error:
            continue
        if n:
            tells += n
            names.append(s["id"])
    bullets = [len(b.split()) for b in re.findall(r"(?m)^\s*[-*•]\s+(.+)$", text)]
    uniform = (len(bullets) >= 3 and statistics.pstdev(bullets) < 1.6)
    if lang == "es":
        # Without contractions, person carries their weight too.
        score = (scale(person, human=6.0, machine=1.0) * 0.70
                 + clamp(100 - tells * 22) * 0.30)
    else:
        score = (scale(contractions, human=3.0, machine=0.0) * 0.35
                 + scale(person, human=8.0, machine=1.0) * 0.35
                 + clamp(100 - tells * 22) * 0.30)
    if uniform:
        score -= 12
        names.append("uniform-bullets")
    if lang == "es":
        detail = (f"{person:.1f} marcas de primera y segunda persona cada 100 palabras, "
                  f"{tells} patrón(es) delator(es)")
    else:
        detail = (f"{contractions:.1f} contracciones, {person:.1f} pronombres personales "
                  f"cada 100 palabras, {tells} patrón(es) delator(es)")
    if names:
        detail += " [" + ", ".join(names[:4]) + "]"
    return clamp(score), detail


CHECKS = ["BURSTINESS", "SPECIFICITY", "SLOP DENSITY", "FINGERPRINT", "VOICE"]
# What the panel prints. The keys above stay as they are in --json.
LABEL = {"BURSTINESS": "RITMO", "SPECIFICITY": "CONCRECIÓN", "SLOP DENSITY": "RELLENO",
         "FINGERPRINT": "HUELLA", "VOICE": "VOZ"}
VERDICT = {"PASS": "APROBADO", "REVIEW": "REVISAR", "FLAGGED": "MARCADO"}


def run(text, lex, lang=None):
    """lang is "es" or "en"; None detects it from the text."""
    lang = lang or language(text)
    results = {}
    results["BURSTINESS"] = check_burstiness(text)
    results["SPECIFICITY"] = check_specificity(text, lang)
    results["SLOP DENSITY"] = check_slop(text, lex, lang)
    results["FINGERPRINT"] = check_fingerprint(text)
    results["VOICE"] = check_voice(text, lex, lang)
    scores = [results[c][0] for c in CHECKS]
    # The weakest check drags the verdict: a detector only needs one signal.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4
    verdict = "PASS" if overall >= 70 and min(scores) >= 55 else (
        "REVIEW" if overall >= 50 else "FLAGGED")
    return results, overall, verdict


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render(results, overall, verdict, label=None, out=sys.stdout, lang=None):
    title = "PANEL DE DETECCIÓN DE IA" + (f"  -  {label}" if label else "")
    print("\n" + title, file=out)
    print("=" * max(len(title), 62), file=out)
    if lang:
        print(f"  texto en {LANG_NAME[lang]}", file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {LABEL[name]:<15} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<15} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'PUNTAJE HUMANO':<15} {bar(overall)} {overall:5.1f}   {VERDICT[verdict]}", file=out)
    if verdict != "PASS":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Señal más débil: {LABEL[weakest]}. Arregla eso primero.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Puntúa qué tan escrito a máquina se ve un borrador.")
    ap.add_argument("input", nargs="?", default="-", help="archivo, o - para leer de la entrada estándar")
    ap.add_argument("compare", nargs="?", help="segundo archivo, para mostrar el antes y el después")
    ap.add_argument("--json", action="store_true", help="imprime JSON en lugar del panel")
    ap.add_argument("--lexicon", default=LEX, help="ruta a slop.json")
    ap.add_argument("--lang", choices=["auto", "es", "en"], default="auto",
                    help="idioma del texto: auto lo detecta (por defecto), es o en")
    args = ap.parse_args()

    lex = json.load(open(args.lexicon, encoding="utf-8"))
    read = lambda p: sys.stdin.read() if p == "-" else open(p, encoding="utf-8").read()

    targets = [(args.input, read(args.input))]
    if args.compare:
        targets.append((args.compare, read(args.compare)))

    payload = []
    for name, text in targets:
        lang = language(text) if args.lang == "auto" else args.lang
        results, overall, verdict = run(text, lex, lang)
        payload.append({
            "source": name,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "human_score": round(overall, 1),
            "verdict": verdict,
            "language": lang,
        })

    if args.json:
        print(json.dumps(payload if args.compare else payload[0], indent=2))
        return

    for (name, text), p in zip(targets, payload):
        results, overall, verdict = run(text, lex, p["language"])
        render(results, overall, verdict, label=os.path.basename(name) if args.compare else None,
               lang=p["language"])
    if args.compare:
        a, b = payload
        delta = b["human_score"] - a["human_score"]
        print(f"  {a['human_score']:.1f} {VERDICT[a['verdict']]}  ->  "
              f"{b['human_score']:.1f} {VERDICT[b['verdict']]}   ({delta:+.1f})\n")

    sys.exit(0 if payload[-1]["verdict"] == "PASS" else 1)


if __name__ == "__main__":
    main()
