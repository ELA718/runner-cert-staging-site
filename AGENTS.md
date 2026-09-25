# ELA718/runner-cert-staging-site agent contract

Use isolated task worktrees; preserve unrelated work and repository validation.

<!-- agentroles-delivery-policy:start -->
## Delivery without an idle agent

Canonical policy: [AgentRoles delivery](https://github.com/AgentRoles/agr-skills/blob/main/docs/agents-delivery-policy.md)
(user direction, 2026-09-25).

- Finish implementation, focused checks and review; push a task branch and open
  a ready PR to the remote default branch. Preserve required checks and reviews.
- Enable native auto-merge (or the verified repository merge queue) and confirm
  GitHub accepted it for the intended PR/head. All applicable validation must be
  enforced; auto-merge availability alone is not a validation gate.
- Record PR, full head SHA, checks and originating task/session owner. Once the
  handoff is accepted, report delivery pending and yield the active turn. Do not
  occupy an agent with CI polling, watch commands or a waiting helper agent.
- GitHub owns merging; Runners owns validation execution. Failures return to the
  originating task through its supported continuation route. If no route is
  registered, report it explicitly; never claim automatic repair is scheduled.
  Herdr monitoring stays passive; do not inject input into idle sessions.
- Verify actual merge before source-delivery completion. Deployment and native
  closeout remain owner responsibilities; preserve dirty/live/unmerged workspaces.
  Pending CI, accepted auto-merge and a clean exit are not completed delivery.
- Drafts, holds, failed/missing checks and unresolved reviews do not authorize
  merge. Keep existing outage exceptions explicit and separate from passing CI.
<!-- agentroles-delivery-policy:end -->
