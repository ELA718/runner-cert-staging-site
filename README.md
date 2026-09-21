# runner-cert-staging-site
Public staging deployment target for operational role certification.
Holds only staging artifacts (index.html, version.json) and the deployment workflow.

The staging deployment workflow supports explicitly selected Linux or macOS
operational slots and uses the `staging-deploy` environment. Admission must bind
its exact workflow revision and the shared `runner-cert/staging` resource scope.
It updates existing artifacts using their current GitHub blob SHA, then verifies
the public site serves the requested release. The release identifier must match
the migration and independent validation runs in ELA718/runner-certification.

Run `python3 -B -m unittest discover -s tests` for the focused fixture checks.
These mocked checks do not replace an admitted live deployment and cleanup proof.
