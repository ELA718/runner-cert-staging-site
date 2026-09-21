# runner-cert-staging-site
Public staging deployment target for operational role certification.
Holds only staging artifacts (index.html, version.json) and the deployment workflow.

The staging deployment workflow supports explicitly selected Linux or macOS
operational slots and uses the `staging-deploy` environment. Admission must bind
its exact workflow revision and the shared `runner-cert/staging` resource scope.
It builds and uploads a Pages artifact on the admitted runner, deploys it through
the Pages API, then verifies the public site serves the requested release.
Configure Pages with `build_type=workflow`; no separate hosted build job is used. The release identifier must match
the migration and independent validation runs in ELA718/runner-certification.

Run `python3 -B -m unittest discover -s tests` for the focused fixture checks.
These mocked checks do not replace an admitted live deployment and cleanup proof.

The deployment follows [GitHub’s custom Pages workflow contract](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages), with pinned upload/deploy actions and environment-scoped OIDC authorization.
