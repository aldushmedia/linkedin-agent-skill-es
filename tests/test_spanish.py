"""Tests for the Spanish support in skills/li-human, and proof that English results
did not change. Standard library only.

    python3 -m unittest discover -s tests -v
"""
import hashlib
import importlib.util
import json
import os
import re
import sys
import unittest

from test_humanizer import EM_DASH, HUMAN, HUMAN_TEXT, SLOPPY, ZWSP, TempFiles, run


def load(name):
    sys.dont_write_bytecode = True   # keep the skill folder clean
    spec = importlib.util.spec_from_file_location(name, os.path.join(HUMAN, name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


detect, humanize = load("detect"), load("humanize")
LEX = humanize.load_lexicon()

# The draft the README scores, with its curly quotes and ellipsis as code points.
QUOTE, ELLIPSIS = chr(0x2019), chr(0x2026)
README_SAMPLE = (
    "In today" + QUOTE + "s fast-paced world, we need to delve into the tapestry of leverage " + EM_DASH
    + " it" + QUOTE + "s not just a tool, it" + QUOTE + "s a mindset." + ZWSP + "\n\n"
    "Moreover, this robust and seamless approach is a testament to innovation, growth, and impact.\n\n"
    "The result?\n\n"
    "Let that sink in" + ELLIPSIS + " I spent 5 hours on proposals at Acme until March. Now it takes 20 "
    "minutes. Thoughts?\n\n"
    "#ai #growth #leadership #mindset #success #future\n")

SLOPPY_ES = (
    "En el mundo actual, es fundamental potenciar tu marca personal " + EM_DASH
    + " no es solo una herramienta, es una mentalidad." + ZWSP + "\n\n"
    "Asimismo, este enfoque robusto e innovador es un testimonio de innovación, crecimiento y compromiso.\n\n"
    "¿El resultado?\n\n"
    "Cabe destacar que pasé 5 horas con propuestas en Acme hasta marzo. "
    "Mira https://example.com/potenciar-robusto hoy. ¿Qué opinan?\n\n"
    "#ia #crecimiento #liderazgo #mentalidad #éxito #futuro\n")

HUMAN_ES = (
    "Perdí un trato de 9.000 dólares en marzo porque mi propuesta tenía 14 páginas.\n\n"
    "Duele, ¿no?\n\n"
    "Meses después, tomando un café en Bogotá, la clienta me contó que había leído la primera página, "
    "hojeado la segunda, se había aburrido más o menos en la tabla de precios y simplemente había dejado "
    "de leer, o sea que pasé un fin de semana entero escribiendo doce páginas que nadie iba a ver.\n\n"
    "Así que la recorté. Ahora es una página, un precio y una fecha. Mandamos 31 desde abril y cerramos 12.\n\n"
    "Nadie nos pidió la versión larga. Ni una vez en seis meses, y ya dejé de esperar que lo hagan.\n\n"
    "Si escribes propuestas que tu cliente no termina, ¿qué recortarías primero?\n")

# What the original project's scripts return for the English drafts, recorded before the
# Spanish support was added: the scores and a hash of the cleaned text.
ORIGINAL = {
    "SLOPPY": (SLOPPY, {"BURSTINESS": 37.7, "SPECIFICITY": 83.4, "SLOP DENSITY": 0.0,
                        "FINGERPRINT": 0.0, "VOICE": 15.5}, 16.4, "FLAGGED",
               "92f1545ba454cbb579da7550df3111b1bfa39690a34ed36e42fff04f06a3b482"),
    "HUMAN_TEXT": (HUMAN_TEXT, {"BURSTINESS": 100.0, "SPECIFICITY": 100.0, "SLOP DENSITY": 100.0,
                                "FINGERPRINT": 100.0, "VOICE": 100.0}, 100.0, "PASS",
                   "d64f8db687a732d8840cbd40f32dbcbdaf25648b0942fbdb4d97e68a3f9a27b8"),
    "README_SAMPLE": (README_SAMPLE, {"BURSTINESS": 60.2, "SPECIFICITY": 100.0, "SLOP DENSITY": 0.0,
                                      "FINGERPRINT": 0.0, "VOICE": 14.0}, 20.9, "FLAGGED",
                      "d2b664cdad8fa903881160ddc124a23ace1a24d43f6997b936b6921f867f73b6"),
}

# One sentence per Spanish structure that it has to flag.
STRUCTURE_EXAMPLES = {
    "no-es-solo": "No es solo una herramienta, es una forma de trabajar.",
    "no-solo-sino": "No solo ahorra tiempo sino también dinero.",
    "no-se-trata": "No se trata de vender más. Se trata de vender mejor.",
    "el-resultado": "Probamos una sola página.\n¿El resultado?\nCerramos 12.",
    "esto-aprendi": "Esto es lo que aprendí después de 31 propuestas.",
    "triada": "Hablamos de innovación, crecimiento y compromiso.",
    "cohete": "Lanzamos la versión nueva " + chr(0x1F680),
    "muro-de-hashtags": "#ventas #propuestas #clientes #negocios #marketing",
    "como-ia": "Como IA, no tengo opiniones propias.",
    "en-resumen": "En resumen, la propuesta corta gana.",
    "cebo": "Cerramos 12 de 31.\n¿Qué opinan?",
}


def scores(payload):
    return {k: v["score"] for k, v in payload["checks"].items()}


class EnglishIsUnchanged(TempFiles):
    def test_scores_and_clean_text_match_the_original_project(self):
        for name, (text, checks, overall, verdict, digest) in ORIGINAL.items():
            path = self.file("d.txt", text)
            data = json.loads(run("detect.py", path, "--json").stdout)
            self.assertEqual(scores(data), checks, name)
            self.assertEqual((data["human_score"], data["verdict"], data["language"]),
                             (overall, verdict, "en"), name)
            clean = run("humanize.py", path).stdout
            self.assertEqual(hashlib.sha256(clean.encode("utf-8")).hexdigest(), digest, name)

    def test_readme_before_and_after(self):
        before = self.file("before.txt", README_SAMPLE)
        after = self.file("after.txt", run("humanize.py", before).stdout)
        self.assertIn("20.9 MARCADO  ->  69.6 REVISAR   (+48.7)", run("detect.py", before, after).stdout)

    def test_forcing_english_gives_the_same_result(self):
        path = self.file("d.txt", SLOPPY)
        self.assertEqual(run("detect.py", path, "--json").stdout,
                         run("detect.py", path, "--json", "--lang", "en").stdout)
        self.assertEqual(run("humanize.py", path).stdout, run("humanize.py", path, "--lang", "en").stdout)

    def test_spanish_entries_are_not_used_on_english_text(self):
        text = "The panorama from our office is vital, and the team is robust."
        clean, report = humanize.humanize(text, LEX)
        self.assertIn("panorama", clean)
        self.assertEqual({h["find"] for h in report["lexical"]}, {"vital", "robust"})


class Language(TempFiles):
    def test_detects_each_language(self):
        for text in (SLOPPY, HUMAN_TEXT, README_SAMPLE):
            self.assertEqual(humanize.language(text), "en")
            self.assertEqual(detect.language(text), "en")
        for text in (SLOPPY_ES, HUMAN_ES):
            self.assertEqual(humanize.language(text), "es")
            self.assertEqual(detect.language(text), "es")
        self.assertEqual(detect.language(""), "en", "a tie stays English")

    def test_both_scripts_use_the_same_word_lists(self):
        self.assertEqual(humanize.FUNCTION_WORDS, detect.FUNCTION_WORDS)

    def test_json_and_panel_say_the_language(self):
        path = self.file("d.txt", SLOPPY_ES)
        self.assertEqual(json.loads(run("detect.py", path, "--json").stdout)["language"], "es")
        self.assertEqual(json.loads(run("humanize.py", path, "--json").stdout)["language"], "es")
        self.assertIn("texto en español", run("detect.py", path).stdout)
        self.assertIn("texto en español", run("humanize.py", path, "--report").stderr)
        self.assertIn("texto en inglés", run("detect.py", path, "--lang", "en").stdout)

    def test_rejects_an_unknown_language(self):
        r = run("detect.py", self.file("d.txt", SLOPPY_ES), "--lang", "fr")
        self.assertEqual(r.returncode, 2)


class SpanishLexicon(unittest.TestCase):
    def test_entries_are_well_formed(self):
        families = {e["family"] for e in LEX["words"] + LEX["phrases"] if "lang" not in e}
        spanish = [e for e in LEX["words"] + LEX["phrases"] if "lang" in e]
        self.assertTrue(spanish)
        for e in spanish:
            self.assertEqual(sorted(e), ["family", "find", "lang", "replace"], e)
            self.assertEqual(e["lang"], "es")
            self.assertIn(e["family"], families, e)
            self.assertEqual(e["find"], e["find"].lower().strip(), e)
            self.assertNotRegex(e["find"], r"[¿?¡!]", "a pattern with \\b cannot start or end there")
        finds = [e["find"] for e in spanish]
        self.assertEqual(len(finds), len(set(finds)))

    def test_structures_are_well_formed(self):
        ids = [s["id"] for s in LEX["structures"]]
        self.assertEqual(len(ids), len(set(ids)))
        spanish = [s for s in LEX["structures"] if "lang" in s]
        self.assertEqual(sorted(s["id"] for s in spanish), sorted(STRUCTURE_EXAMPLES))
        for s in spanish:
            self.assertEqual(sorted(s), ["fix", "id", "lang", "name", "regex"], s)
            re.compile(s["regex"], re.MULTILINE)

    def test_each_spanish_structure_flags_its_example(self):
        regex = {s["id"]: s["regex"] for s in LEX["structures"]}
        for sid, example in STRUCTURE_EXAMPLES.items():
            self.assertRegex(example, re.compile(regex[sid], re.MULTILINE), sid)
            names = {f["name"] for f in humanize.scan_structures(example, LEX, "es")}
            self.assertIn(next(s["name"] for s in LEX["structures"] if s["id"] == sid), names, sid)

    def test_human_spanish_draft_has_no_tells(self):
        self.assertEqual(humanize.scan_structures(HUMAN_ES, LEX, "es"), [])
        _, report = humanize.humanize(HUMAN_ES, LEX)
        self.assertEqual(report["lexical"], [])

    def test_english_structures_are_not_used_on_spanish_text(self):
        text = "Agree?\nEsto lo escribimos en español para el equipo de ventas de la empresa."
        self.assertEqual(humanize.scan_structures(text, LEX, "es"), [])
        self.assertTrue(humanize.scan_structures(text, LEX, "en"))


class HumanizeSpanish(TempFiles):
    def clean(self, text):
        return humanize.humanize(text, LEX)[0].strip()

    def test_cleans_the_spanish_draft(self):
        r = run("humanize.py", self.file("d.txt", SLOPPY_ES), "--report")
        self.assertEqual(r.returncode, 0, r.stderr)
        out = r.stdout
        for gone in (EM_DASH, ZWSP, "En el mundo actual", "potenciar tu", "Asimismo", "Cabe destacar"):
            self.assertNotIn(gone, out)
        for kept in ("Hoy, es clave mejorar tu marca personal", "este enfoque sólido y nuevo",
                     "es una prueba de innovación", "Pasé 5 horas",
                     "https://example.com/potenciar-robusto"):
            self.assertIn(kept, out)
        for line in ("texto en español", "en el mundo actual  -> hoy   [aperturas]",
                     "cabe destacar que  -> (borrado)   [conectores]", '"No es solo X, es Y"',
                     "Cebo de interacción reflejo", "Muro de hashtags (5 o más)"):
            self.assertIn(line, r.stderr)

    def test_replacements_keep_gender_number_and_case(self):
        self.assertEqual(self.clean("Es una estrategia robusta para el equipo y para la empresa."),
                         "Es una estrategia sólida para el equipo y para la empresa.")
        self.assertEqual(self.clean("Son procesos robustos e innovadores para la empresa y el equipo."),
                         "Son procesos sólidos y nuevos para la empresa y el equipo.")
        self.assertEqual(self.clean("Es un plan ROBUSTO para la empresa y para el equipo de ventas."),
                         "Es un plan SÓLIDO para la empresa y para el equipo de ventas.")
        self.assertEqual(self.clean("A la hora de vender, lo que importa es el precio para el cliente."),
                         "Al vender, lo que importa es el precio para el cliente.")

    def test_y_and_e_agree_with_the_replacement(self):
        self.assertEqual(self.clean("Tenemos un proceso seguro y crucial para el equipo y los clientes."),
                         "Tenemos un proceso seguro e importante para el equipo y los clientes.")

    def test_a_deleted_opener_leaves_a_capital(self):
        cases = {
            "Seamos honestos: la mayoría de las propuestas no se leen en la empresa.":
                "La mayoría de las propuestas no se leen en la empresa.",
            "Cerramos 12 en marzo. Léelo otra vez. Nadie más lo hizo en la empresa.":
                "Cerramos 12 en marzo. Nadie más lo hizo en la empresa.",
            "¡Sin más preámbulos, empecemos con la lista de lo que funciona para el equipo!":
                "¡Empecemos con la lista de lo que funciona para el equipo!",
            "Tuve la oportunidad de hablar con el equipo y la realidad es que nadie lee las propuestas.":
                "Pude hablar con el equipo y nadie lee las propuestas.",
        }
        for text, want in cases.items():
            self.assertEqual(self.clean(text), want)

    def test_english_words_in_spanish_text_are_left_alone(self):
        text = "Este enfoque es robust y no lo vamos a cambiar por nada que tenemos en la empresa."
        self.assertEqual(self.clean(text), text)

    def test_forcing_english_skips_the_spanish_lexicon(self):
        path = self.file("d.txt", SLOPPY_ES)
        self.assertIn("En el mundo actual", run("humanize.py", path, "--lang", "en").stdout)


class DetectSpanish(TempFiles):
    def test_sloppy_spanish_draft_is_flagged(self):
        r = run("detect.py", self.file("d.txt", SLOPPY_ES))
        self.assertEqual(r.returncode, 1)
        data = json.loads(run("detect.py", self.file("d.txt", SLOPPY_ES), "--json").stdout)
        self.assertEqual(data["verdict"], "FLAGGED")
        self.assertEqual(data["checks"]["SLOP DENSITY"]["score"], 0.0)
        self.assertIn("cabe destacar que", data["checks"]["SLOP DENSITY"]["detail"])

    def test_human_spanish_draft_passes(self):
        r = run("detect.py", self.file("h.txt", HUMAN_ES))
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("APROBADO", r.stdout)
        self.assertIn("marcas de primera y segunda persona", r.stdout)

    def test_english_calibration_could_not_pass_it(self):
        path = self.file("h.txt", HUMAN_ES)
        es = json.loads(run("detect.py", path, "--json").stdout)
        en = json.loads(run("detect.py", path, "--json", "--lang", "en").stdout)
        self.assertEqual(es["checks"]["VOICE"]["score"], 100.0)
        self.assertLess(en["checks"]["VOICE"]["score"], 55)
        self.assertNotEqual(en["verdict"], "PASS")

    def test_cleaning_raises_the_spanish_score(self):
        before = self.file("before.txt", SLOPPY_ES)
        after = self.file("after.txt", run("humanize.py", before).stdout)
        b = json.loads(run("detect.py", before, "--json").stdout)["human_score"]
        a = json.loads(run("detect.py", after, "--json").stdout)["human_score"]
        self.assertGreater(a, b)

    def test_accents_and_enye_stay_inside_the_word(self):
        text = "La concreción de un año pequeño"
        self.assertEqual(detect.words(text, "es"), ["La", "concreción", "de", "un", "año", "pequeño"])
        self.assertEqual(len(detect.words(text)), 9, "the English count is the original one")

    def test_proper_nouns_with_accents(self):
        found = set(detect.PROPER_ES.findall("Viajé a Bogotá con Ángela. ¿Quién paga? Nadie, dijo Íñigo."))
        self.assertEqual(found, {"Bogotá", "Ángela", "Íñigo"})

    def test_counts_first_and_second_person(self):
        self.assertEqual(detect.person_es("Perdí el trato, mandamos otra propuesta y tu cliente me escribió."), 4)
        self.assertEqual(detect.person_es("Un café aquí, los últimos gramos, los préstamos así."), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
