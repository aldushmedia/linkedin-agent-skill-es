"""Tests for the package: manifests, skills, data files and cross-references. Standard library only.

    python3 -m unittest discover -s tests -v
"""
import json
import os
import re
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
NAME = "linkedin-agent-skill-es"
URL = "https://github.com/aldushmedia/" + NAME
SKILLS = ["li-audit", "li-carousel", "li-comment", "li-dm", "li-human", "li-inbox", "li-plan",
          "li-post", "li-profile", "li-reply", "li-repurpose"]
ALDUSH = "Copyright (c) 2026 Aldush Media (traducción y adaptación al español)"


def read(*parts):
    with open(os.path.join(REPO, *parts), encoding="utf-8") as fh:
        return fh.read()


def every_file():
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        for name in files:
            path = os.path.join(root, name)
            with open(path, encoding="utf-8", errors="ignore") as fh:
                yield os.path.relpath(path, REPO), fh.read()


class Package(unittest.TestCase):
    def test_plugin_and_marketplace(self):
        plugin = json.loads(read(".claude-plugin", "plugin.json"))
        self.assertEqual(plugin["name"], NAME)
        self.assertEqual((plugin["homepage"], plugin["repository"]), (URL, URL))
        self.assertEqual(plugin["author"]["name"], "Aldush Media")
        market = json.loads(read(".claude-plugin", "marketplace.json"))
        self.assertEqual(market["name"], NAME)
        self.assertEqual(market["plugins"][0]["name"], NAME)

    def test_readme_installs_from_aldushmedia(self):
        readme = read("README.md")
        for line in ("git clone %s.git" % URL,
                     "cp -r %s/skills/li-* ~/.claude/skills/" % NAME,
                     "/plugin marketplace add aldushmedia/" + NAME,
                     "/plugin install %s@%s" % (NAME, NAME)):
            self.assertIn(line, readme)
        for s in SKILLS:
            self.assertIn("`/%s`" % s, readme)

    def test_license_keeps_the_original_and_adds_aldush_media(self):
        lines = read("LICENSE").rstrip("\n").split("\n")
        self.assertEqual(lines[0], "MIT License")
        self.assertTrue(lines[2].startswith("Copyright (c) 2026 ") and "Aldush" not in lines[2])
        self.assertEqual(lines[-1], ALDUSH)

    def test_no_links_to_the_original_author_outside_license(self):
        bad = [rel for rel, text in every_file()
               if rel != "LICENSE" and re.search(r"opus" + "jake|Jake" + "schincariol", text)]
        self.assertEqual(bad, [])

    def test_no_em_dashes_anywhere(self):
        bad = [rel for rel, text in every_file() if chr(0x2014) in text]
        self.assertEqual(bad, [])


class Skills(unittest.TestCase):
    def test_eleven_skills_with_their_names(self):
        found = sorted(d for d in os.listdir(os.path.join(REPO, "skills"))
                       if os.path.isfile(os.path.join(REPO, "skills", d, "SKILL.md")))
        self.assertEqual(found, SKILLS)
        for s in SKILLS:
            text = read("skills", s, "SKILL.md")
            fm = re.match(r"^---\n(.*?)\n---\n", text, re.S).group(1)
            self.assertIn("name: %s\n" % s, fm + "\n", s)
            self.assertRegex(fm, r"description: ", s)

    def test_hook_names_match_hooks_json(self):
        hooks = {h["id"]: h["name"] for h in json.loads(read("skills", "li-post", "hooks.json"))["hooks"]}
        self.assertEqual(sorted(hooks), list(range(1, 22)))
        seen = 0
        for s in SKILLS:
            for num, rest in re.findall(r"#(\d{1,2}) +([^\s#].*)", read("skills", s, "SKILL.md")):
                name = hooks.get(int(num))
                if name is None:
                    continue
                self.assertTrue(rest.startswith(name), "%s: #%s %s... is not '%s'" % (s, num, rest[:30], name))
                seen += 1
        self.assertGreater(seen, 8)

    def test_rubric_adds_up_to_100(self):
        rubric = json.loads(read("skills", "li-profile", "rubric.json"))
        self.assertEqual(rubric["total"], 100)
        self.assertEqual(sum(i["points"] for i in rubric["items"]), 100)
        self.assertEqual(len(rubric["items"]), 12)

    def test_lexicon_matches_what_the_readme_says(self):
        lex = json.loads(read("skills", "li-human", "slop.json"))
        terms = lex["words"] + lex["phrases"]
        self.assertEqual(len([e for e in terms if "lang" not in e]), 113)
        self.assertEqual(len([e for e in terms if e.get("lang") == "es"]), 168)
        self.assertEqual(len(lex["invisible"]), 17)
        self.assertEqual(len(lex["typographic"]), 11)
        self.assertEqual(len([s for s in lex["structures"] if "lang" not in s]), 11)
        self.assertEqual(len([s for s in lex["structures"] if s.get("lang") == "es"]), 11)
        for s in lex["structures"]:
            re.compile(s["regex"], re.MULTILINE)
        readme = read("README.md")
        for count in ("168 palabras y frases hechas en español", "y 113 en inglés",
                      "168 términos en español y 113 en inglés, 17 clases de invisibles, "
                      "11 patrones delatores por idioma"):
            self.assertIn(count, re.sub(r"\s+", " ", readme))

    def test_voice_template_is_where_the_readme_says(self):
        self.assertIn("~/.claude/linkedin/voice.md", read("templates", "voice.md"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
