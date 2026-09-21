import io
import json
import os
from pathlib import Path
import re
import unittest
from unittest.mock import patch
import urllib.error

WORKFLOW = Path(__file__).resolve().parents[1] / '.github/workflows/staging-deploy.yml'
BLOCKS = re.findall(r"python3 - <<'PY'\n(.*?)          PY", WORKFLOW.read_text(), re.S)


def script(fragment):
    import textwrap
    return textwrap.dedent(next(block for block in BLOCKS if fragment in block))


class DeploymentTests(unittest.TestCase):
    def test_existing_artifact_updates_include_current_blob_sha(self):
        writes = []
        def response(request, **kwargs):
            if request.get_method() == 'GET':
                return io.BytesIO(b'{"sha":"existing-blob"}')
            writes.append(json.loads(request.data))
            return io.BytesIO(b'{"commit":{"sha":"new-commit"}}')
        with patch.dict(os.environ, {'GITHUB_REPOSITORY': 'ELA718/runner-cert-staging-site',
                'GITHUB_SHA': 'a'*40, 'GITHUB_RUN_ID': '123', 'RELEASE': 'release-2', 'DEPLOY_TOKEN': 'fixture'}), \
                patch('urllib.request.urlopen', response):
            exec(script('api = '), {})
        self.assertEqual(len(writes), 2)
        self.assertTrue(all(row['sha'] == 'existing-blob' for row in writes))

    def test_non_missing_read_errors_do_not_overwrite(self):
        with patch.dict(os.environ, {'GITHUB_REPOSITORY': 'ELA718/runner-cert-staging-site',
                'GITHUB_SHA': 'a'*40, 'GITHUB_RUN_ID': '123', 'RELEASE': 'release-2', 'DEPLOY_TOKEN': 'fixture'}), \
                patch('urllib.request.urlopen', side_effect=urllib.error.HTTPError('https://example.invalid',403,'denied',{},None)):
            with self.assertRaises(urllib.error.HTTPError):
                exec(script('api = '), {})

    def test_public_release_observation_uses_requested_environment(self):
        with patch.dict(os.environ, {'RELEASE': 'release-2'}), \
                patch('urllib.request.urlopen', return_value=io.BytesIO(b'{"release":"release-2"}')):
            with self.assertRaises(SystemExit) as result:
                exec(script("url = 'https://ela718"), {})
        self.assertEqual(result.exception.code, 0)


if __name__ == '__main__':
    unittest.main()
