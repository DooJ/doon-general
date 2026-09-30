from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


class SkillRelationTests(unittest.TestCase):
    def read_skill(self, name: str) -> str:
        return (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")

    def test_travel_planner_bundles_every_required_provider(self) -> None:
        planner = self.read_skill("travel-planner")
        providers = (
            "travel-flight-search",
            "travel-lodging-search",
            "travel-destination-research",
            "travel-place-search",
            "travel-transport-search",
            "travel-itinerary-builder",
        )
        for provider in providers:
            with self.subTest(provider=provider):
                self.assertTrue((SKILLS / provider / "SKILL.md").is_file())
                self.assertIn(f"`{provider}`", planner)
        self.assertIn("`provider_mode: preferred|equivalent|tool_fallback`", planner)
        self.assertIn("`partial: capability_unavailable`", planner)

    def test_cross_plugin_links_define_capability_and_fallback(self) -> None:
        legal = self.read_skill("project-legal-advisor")
        self.assertIn("`codebase.fact-map`", legal)
        self.assertIn("`inline_fact_map`", legal)
        self.assertIn("`snapshot_report_handoff`", legal)
        self.assertIn("`living_doc_handoff`", legal)

        refining = self.read_skill("refining-implemented-ui")
        self.assertIn("`codebase.fact-map`", refining)
        self.assertIn("`partial: fact_map_unavailable`", refining)


if __name__ == "__main__":
    unittest.main()
