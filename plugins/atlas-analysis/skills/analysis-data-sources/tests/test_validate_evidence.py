"""Evidence delivery and claim-consistency regressions; no network access."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

MODULE = Path(__file__).resolve().parents[1] / "scripts/validate_evidence.py"
SPEC = importlib.util.spec_from_file_location("evidence_validator", MODULE)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.workspace = Path(self.tmp.name)
        source = self.workspace / "analysis.md"
        source.write_text("Run 3 analysis\n", encoding="utf-8")
        (self.workspace / "data-sources.md").write_text("| jet-pt | unverified |\n", encoding="utf-8")
        self.data = {"schema_version": 1,
                     "specification": {"path": "analysis.md", "sha256": hashlib.sha256(source.read_bytes()).hexdigest()},
                     "models": {"steering": "test"}, "unresolved": ["Not probed"],
                     "requirements": [{"id": "jet-pt", "status": "unverified", "probe_ids": []}],
                     "probes": []}

    def save(self):
        (self.workspace / "data-source-evidence.json").write_text(json.dumps(self.data), encoding="utf-8")

    def check(self):
        self.save()
        return validator.validate(self.workspace)

    def success(self, entries=3):
        self.data["requirements"][0].update(status="verified", probe_ids=["p1"])
        self.data["probes"] = [{"id": "p1", "status": "succeeded", "transport": "servicex",
                                "query": "Jets().Select(lambda j: j.pt()/1000)",
                                "observations": {"entries": entries, "columns": {"jet_pt": {"returned_units": "GeV"}}}}]

    def test_incomplete_analysis_can_deliver_valid_evidence(self):
        self.assertEqual(self.check()["requirements"], 1)

    def test_compact_success_needs_no_returned_probe_directory(self):
        self.success()
        self.assertEqual(self.check()["probes"], 1)
        self.assertFalse((self.workspace / "probes").exists())

    def test_nested_file_does_not_satisfy_root_deliverable(self):
        self.save()
        nested = self.workspace / "probes"
        nested.mkdir()
        (self.workspace / "data-source-evidence.json").rename(nested / "data-source-evidence.json")
        with self.assertRaisesRegex(validator.EvidenceError, "under probes"):
            validator.validate(self.workspace)

    def test_invalid_json(self):
        (self.workspace / "data-source-evidence.json").write_text("{", encoding="utf-8")
        with self.assertRaisesRegex(validator.EvidenceError, "Invalid evidence JSON"):
            validator.validate(self.workspace)

    def test_stale_input_hash(self):
        self.data["specification"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(validator.EvidenceError, "SHA-256"):
            self.check()

    def test_duplicate_requirement(self):
        self.data["requirements"].append(dict(self.data["requirements"][0]))
        with self.assertRaisesRegex(validator.EvidenceError, "Duplicate"):
            self.check()

    def test_dangling_probe(self):
        self.data["requirements"][0]["probe_ids"] = ["missing"]
        with self.assertRaisesRegex(validator.EvidenceError, "unknown probe"):
            self.check()

    def test_verified_without_success(self):
        self.data["requirements"][0]["status"] = "verified"
        with self.assertRaisesRegex(validator.EvidenceError, "lacks nonempty"):
            self.check()

    def test_empty_delivery_cannot_verify_a_requirement(self):
        self.success(entries=0)
        with self.assertRaisesRegex(validator.EvidenceError, "lacks nonempty"):
            self.check()

    def test_successful_query_must_be_returned(self):
        self.success()
        del self.data["probes"][0]["query"]
        with self.assertRaisesRegex(validator.EvidenceError, "executed query"):
            self.check()

    def test_external_metadata_cannot_verify_event_accessor(self):
        self.success()
        self.data["probes"][0]["transport"] = "external"
        with self.assertRaisesRegex(validator.EvidenceError, "lacks nonempty"):
            self.check()

    def test_unknown_backup_target(self):
        self.data["requirements"][0].update(status="backup", backup_for="missing")
        with self.assertRaisesRegex(validator.EvidenceError, "backup_for"):
            self.check()


if __name__ == "__main__":
    unittest.main()
