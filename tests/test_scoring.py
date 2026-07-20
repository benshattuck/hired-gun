"""Regression suite for the matching heuristics.

Every test here corresponds to a real bug or design promise — if you
change the matching logic, add a case. Run from the repo root:

    python3 -m unittest discover -s tests
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from _common import canonical_terms, phrase_hits, posting_terms, stem, substring_matches  # noqa: E402
import score_fit  # noqa: E402
import select_bullets  # noqa: E402


class TestSynonyms(unittest.TestCase):
    def test_alias_matches_canonical_in_text(self):
        self.assertIn("kubernetes", substring_matches({"kubernetes"}, "We use k8s heavily."))

    def test_canonical_matches_alias_in_text(self):
        self.assertIn("k8s", substring_matches({"k8s"}, "We use Kubernetes heavily."))

    def test_no_alias_no_false_match(self):
        self.assertNotIn("kubernetes", substring_matches({"kubernetes"}, "We use Docker heavily."))

    def test_canonical_terms_is_bidirectional(self):
        self.assertEqual(canonical_terms("k8s"), {"k8s", "kubernetes"})
        self.assertEqual(canonical_terms("kubernetes"), {"kubernetes", "k8s"})

    def test_short_alias_does_not_match_inside_other_words(self):
        # "ts" must not match "tests" or "posts" or "TypeScript" — a
        # naive substring check would false-positive on all three.
        self.assertEqual(substring_matches({"ts"}, "We write lots of tests and posts."), set())

    def test_short_alias_matches_as_a_whole_word(self):
        self.assertEqual(substring_matches({"ts"}, "Fluent in Python and TS."), {"ts"})

    def test_word_boundary_prevents_java_javascript_false_positive(self):
        # A profile listing "java" must not be credited for a posting
        # that only mentions "javascript" — different languages.
        self.assertEqual(substring_matches({"java"}, "We use JavaScript everywhere."), set())
        self.assertEqual(substring_matches({"java"}, "We use Java everywhere."), {"java"})


class TestPhraseHits(unittest.TestCase):
    """Dealbreaker / nice-to-have matching."""

    ONCALL = "On-call heavier than 1 week per month"

    def test_word_form_mismatch_still_hits(self):
        # "Requires" in the criteria, "required" in the posting.
        hits = phrase_hits(
            ["Requires security clearance"],
            "Security clearance is required for this position.",
        )
        self.assertEqual(hits, ["Requires security clearance"])

    def test_direct_negation_suppresses(self):
        # "No on-call heavier than..." is a promise kept, not a violation.
        text = "Great team. No on-call heavier than one week per month."
        self.assertEqual(phrase_hits([self.ONCALL], text), [])

    def test_distant_negation_does_not_suppress(self):
        # The "don't" belongs to a different clause than the violation.
        text = "We don't sugarcoat it: on-call is heavier than one week per month here."
        self.assertEqual(phrase_hits([self.ONCALL], text), [self.ONCALL])

    def test_plain_violation_hits(self):
        text = "On-call rotation is heavier than one week per month during launches."
        self.assertEqual(phrase_hits([self.ONCALL], text), [self.ONCALL])

    def test_hyphen_and_space_forms_match(self):
        # Criteria says "on-call", posting says "on call".
        text = "On call duty is heavier than one week per month."
        self.assertEqual(phrase_hits([self.ONCALL], text), [self.ONCALL])

    def test_absent_phrase_does_not_hit(self):
        self.assertEqual(phrase_hits([self.ONCALL], "Fully remote, no on-call at all."), [])


class TestTokenizer(unittest.TestCase):
    def test_no_trailing_periods_on_tokens(self):
        terms = posting_terms("We use Python and Kafka. Kubernetes is a big plus.")
        self.assertTrue(
            all(not t.endswith(".") for t in terms),
            f"tokens with trailing periods: {[t for t in terms if t.endswith('.')]}",
        )
        self.assertIn("kubernetes", terms)
        self.assertIn("kafka", terms)

    def test_bigrams_do_not_cross_sentence_boundaries(self):
        terms = posting_terms("We use Kafka. Kubernetes helps too.")
        self.assertNotIn("kafka kubernetes", terms)

    def test_stem_unifies_word_forms(self):
        self.assertEqual(stem("requires"), stem("required"))
        self.assertEqual(stem("mentoring"), stem("mentors"))


class TestScoreComponents(unittest.TestCase):
    def test_nice_to_have_bonus(self):
        criteria = {"nice_to_haves": ["small team", "error budget"]}
        bonus, hits = score_fit.score_nice_to_haves(
            criteria, "We are a small team with a real error budget."
        )
        self.assertEqual(bonus, 4)
        self.assertCountEqual(hits, ["small team", "error budget"])

    def test_nice_to_have_bonus_is_capped(self):
        criteria = {"nice_to_haves": ["python", "kafka", "postgres", "terraform"]}
        bonus, _ = score_fit.score_nice_to_haves(
            criteria, "Python, Kafka, Postgres, and Terraform daily."
        )
        self.assertEqual(bonus, 6)

    def test_biggest_gap_skips_terms_inside_matched_keywords(self):
        terms = ["backend", "kubernetes", "kubernetes"]
        matched = {"senior backend engineer"}
        self.assertEqual(score_fit.biggest_gap(terms, matched), "kubernetes")

    def test_biggest_gap_keeps_bare_substrings(self):
        # "java" is not covered by "javascript".
        terms = ["java", "java"]
        matched = {"javascript"}
        self.assertEqual(score_fit.biggest_gap(terms, matched), "java")

    def test_bigram_with_covered_word_is_not_a_gap(self):
        # "engineer remote" adds nothing beyond "remote", which is
        # reported on its own.
        terms = ["engineer remote", "remote"]
        matched = {"senior backend engineer"}
        self.assertEqual(score_fit.biggest_gap(terms, matched), "remote")

    def test_criteria_wants_are_not_gaps(self):
        # A posting mentioning "remote" answers the criteria; it doesn't
        # reveal a skill gap.
        criteria = {"location": {"mode": ["remote"]}}
        known = score_fit.criteria_known_wants(criteria)
        terms = ["remote", "remote", "kubernetes"]
        self.assertEqual(score_fit.biggest_gap(terms, known), "kubernetes")

    def test_dealbreaker_floors_score(self):
        criteria = {"dealbreakers": ["Requires security clearance"]}
        hits = score_fit.check_dealbreakers(
            criteria, "Top pay, remote, security clearance required."
        )
        self.assertEqual(hits, ["Requires security clearance"])


class TestSelectBullets(unittest.TestCase):
    def test_bullets_are_returned_verbatim(self):
        bullets = [{"text": "Led the Kafka migration.", "tags": ["kafka"]}]
        selected, _ = select_bullets.select_for_role(
            bullets, "We need Kafka experience.", {"kafka"}, max_per_role=1
        )
        self.assertEqual(selected, bullets)  # same objects, nothing rewritten

    def test_selects_highest_scoring_bullets_first(self):
        bullets = [
            {"text": "Wrote docs.", "tags": ["documentation"]},
            {"text": "Led the Kafka migration.", "tags": ["kafka"]},
        ]
        selected, left_out = select_bullets.select_for_role(
            bullets, "We need Kafka experience.", {"kafka"}, max_per_role=1
        )
        self.assertEqual(selected, [bullets[1]])
        self.assertEqual(left_out, [bullets[0]])

    def test_falls_back_to_original_order_when_nothing_scores(self):
        bullets = [{"text": "A.", "tags": []}, {"text": "B.", "tags": []}]
        selected, _ = select_bullets.select_for_role(
            bullets, "Totally unrelated posting.", set(), max_per_role=1
        )
        self.assertEqual(selected, [bullets[0]])  # first bullet, not empty

    def test_short_alias_reaches_skill_marking(self):
        # "TS" in the posting must mark "TypeScript" in profile.yaml, even
        # though the tokenizer drops 2-letter tokens like "ts".
        profile = {"skills": {"languages": ["TypeScript", "Python"]}}
        lines = select_bullets.format_skills_section(profile, "Fluent in TS required.")
        self.assertIn("TypeScript*", lines[0])
        self.assertNotIn("Python*", lines[0])

    def test_skill_marking_never_alters_wording(self):
        profile = {"skills": {"tools": ["PostgreSQL"]}}
        lines = select_bullets.format_skills_section(profile, "We use Postgres daily.")
        self.assertIn("PostgreSQL*", lines[0])
        self.assertNotIn("Postgres*", lines[0])  # marked, not relabeled


if __name__ == "__main__":
    unittest.main()
