"""Tests for skills/li-human: humanize.py and detect.py. Standard library only.

    python3 -m unittest discover -s tests -v
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
HUMAN = os.path.join(REPO, "skills", "li-human")
EM_DASH, EN_DASH, ZWSP = chr(0x2014), chr(0x2013), chr(0x200B)   # code points keep this file clean

SLOPPY = ("In today" + chr(0x2019) + "s fast-paced world, we need to delve into leverage " + EM_DASH
          + " it" + chr(0x2019) + "s not just a tool, it" + chr(0x2019) + "s a mindset." + ZWSP + "\n\n"
          "Moreover, this robust approach is a testament to innovation, growth, and impact.\n\n"
          "The result?\n\n"
          "I spent 5 hours on proposals at Acme until March. See https://example.com/robust-delve today. Thoughts?\n\n"
          "#ai #growth #leadership #mindset #success #future\n")

HUMAN_TEXT = (
    "I lost a $9,000 deal in March because my proposal was 14 pages long.\n\n"
    "Ouch, right?\n\n"
    "The client told me later, over coffee in Denver, that she'd read page one, skimmed page two, got "
    "bored somewhere around the pricing table and simply stopped, which meant I'd spent a whole weekend "
    "writing twelve pages nobody would ever see.\n\n"
    "So I cut it. Now it's one page, a price and a date. We've sent 31 of them since April and closed 12.\n\n"
    "Nobody has asked for the long version. Not once in six months, and I've stopped expecting them to.\n\n"
    "If you're writing proposals your buyer won't finish, what would you cut first?\n")


def run(script, *args, stdin=None):
    return subprocess.run([sys.executable, os.path.join(HUMAN, script)] + list(args),
                          input=stdin, capture_output=True, text=True, encoding="utf-8")


class TempFiles(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def file(self, name, text):
        path = os.path.join(self.tmp.name, name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        return path


class Humanize(TempFiles):
    def test_cleans_the_fingerprint_and_the_lexicon(self):
        r = run("humanize.py", self.file("d.txt", SLOPPY))
        self.assertEqual(r.returncode, 0, r.stderr)
        out = r.stdout
        self.assertNotIn(EM_DASH, out)
        self.assertNotIn(ZWSP, out)
        self.assertNotIn(chr(0x2019), out)
        self.assertNotIn("delve", out.lower().replace("robust-delve", ""))
        self.assertIn("https://example.com/robust-delve", out, "URLs are left untouched")

    def test_report_is_in_spanish(self):
        r = run("humanize.py", self.file("d.txt", SLOPPY), "--report")
        report = r.stderr
        for line in ("REPORTE DEL HUMANIZADOR", "1. CARACTERES INVISIBLES", "ESPACIO DE ANCHO CERO  -> borrar",
                     "2. TIPOGRAFÍA", "RAYA LARGA", "3. LÉXICO DE RELLENO", "[verbos]",
                     "4. PATRONES DELATORES", "Muro de hashtags (5 o más)"):
            self.assertIn(line, report)

    def test_json_keeps_its_keys(self):
        r = run("humanize.py", self.file("d.txt", SLOPPY), "--json")
        data = json.loads(r.stdout)
        self.assertEqual(sorted(data), ["language", "report", "text"])
        self.assertEqual(data["language"], "en")
        self.assertEqual(sorted(data["report"]), ["invisible", "lexical", "structures", "typographic"])
        self.assertEqual({h["action"] for h in data["report"]["invisible"]}, {"delete"})

    def test_out_file(self):
        out = os.path.join(self.tmp.name, "clean.txt")
        r = run("humanize.py", self.file("d.txt", SLOPPY), "-o", out)
        self.assertIn("listo: %s" % out, r.stderr)
        self.assertTrue(os.path.isfile(out))


class Detect(TempFiles):
    def test_sloppy_draft_is_flagged_in_spanish(self):
        r = run("detect.py", self.file("d.txt", SLOPPY))
        self.assertEqual(r.returncode, 1)
        for label in ("PANEL DE DETECCIÓN DE IA", "RITMO", "CONCRECIÓN", "RELLENO", "HUELLA", "VOZ",
                      "PUNTAJE HUMANO", "MARCADO", "Señal más débil:"):
            self.assertIn(label, r.stdout)

    def test_human_draft_passes(self):
        r = run("detect.py", self.file("h.txt", HUMAN_TEXT))
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("APROBADO", r.stdout)

    def test_json_keeps_english_keys_and_verdicts(self):
        r = run("detect.py", self.file("d.txt", SLOPPY), "--json")
        data = json.loads(r.stdout)
        self.assertEqual(sorted(data["checks"]),
                         sorted(["BURSTINESS", "SPECIFICITY", "SLOP DENSITY", "FINGERPRINT", "VOICE"]))
        self.assertIn(data["verdict"], ("PASS", "REVIEW", "FLAGGED"))

    def test_cleaning_raises_the_score(self):
        before = self.file("before.txt", SLOPPY)
        clean = run("humanize.py", before).stdout
        after = self.file("after.txt", clean)
        r = run("detect.py", before, after)
        self.assertIn("->", r.stdout)
        b = json.loads(run("detect.py", before, "--json").stdout)["human_score"]
        a = json.loads(run("detect.py", after, "--json").stdout)["human_score"]
        self.assertGreater(a, b)

    def test_reads_stdin(self):
        r = run("detect.py", "-", stdin=HUMAN_TEXT)
        self.assertEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
