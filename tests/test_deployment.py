import io
import json
import os
from pathlib import Path
import re
import tarfile
import tempfile
import textwrap
import unittest
from unittest.mock import patch

WORKFLOW = Path(__file__).resolve().parents[1] / '.github/workflows/staging-deploy.yml'
BLOCKS = re.findall(r"python3 - <<'PY'\n(.*?)          PY", WORKFLOW.read_text(), re.S)


def script(fragment):
    return textwrap.dedent(next(block for block in BLOCKS if fragment in block))


class DeploymentTests(unittest.TestCase):
    def test_pages_archive_has_exact_release_and_only_regular_files(self):
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {
                'GITHUB_SHA': 'a'*40, 'GITHUB_RUN_ID': '123', 'RELEASE': 'release-2', 'RUNNER_TEMP': directory}):
            exec(script('tarfile.open'), {})
            with tarfile.open(Path(directory)/'artifact.tar') as archive:
                self.assertEqual(archive.getnames(), ['index.html', 'version.json'])
                self.assertTrue(all(member.isfile() for member in archive.getmembers()))
                version = json.load(archive.extractfile('version.json'))
                self.assertEqual(version['release'], 'release-2')
                self.assertEqual(version['commit'], 'a'*40)
                self.assertEqual(version['workflow_run'], 123)
                self.assertIn(b'release-2', archive.extractfile('index.html').read())

    def test_invalid_release_refuses_artifact_creation(self):
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {
                'GITHUB_SHA': 'a'*40, 'GITHUB_RUN_ID': '123', 'RELEASE': '../bad', 'RUNNER_TEMP': directory}):
            with self.assertRaises(AssertionError):
                exec(script('tarfile.open'), {})
            self.assertFalse((Path(directory)/'artifact.tar').exists())

    def test_public_release_observation_uses_requested_environment(self):
        with patch.dict(os.environ, {'RELEASE': 'release-2'}), \
                patch('urllib.request.urlopen', return_value=io.BytesIO(b'{"release":"release-2"}')):
            with self.assertRaises(SystemExit) as result:
                exec(script("url = 'https://ela718"), {})
        self.assertEqual(result.exception.code, 0)


if __name__ == '__main__':
    unittest.main()
