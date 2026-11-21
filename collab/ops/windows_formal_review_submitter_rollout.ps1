# Windows Claude Code: apply the already-published CoWork formal-review submitter.
# No watcher/DB/task/key/signing/READY/model actions. Safe by default: -Apply is required.
[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$RepoRoot,
    [Parameter(Mandatory=$true)][string]$LiveConfig,
    [switch]$Apply
)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path -LiteralPath $RepoRoot).Path
$allowedOrigins = @(
    'https://github.com/wonhwipark/CoWork-Skill-Collab.git',
    'https://github.com/wonhwipark/CoWork-Skill-Collab',
    'git@github.com:wonhwipark/CoWork-Skill-Collab.git',
    'git@github.com:wonhwipark/CoWork-Skill-Collab',
    'ssh://git@github.com/wonhwipark/CoWork-Skill-Collab.git'
)
function Git([string[]] $GitArgs) {
    $output = & git -C $RepoRoot @GitArgs 2>&1
    if ($LASTEXITCODE -ne 0) { throw ("GIT_FAILURE: " + $GitArgs[0]) }
    return (($output | Out-String).Trim())
}
function Check([bool] $Condition, [string] $Reason) {
    if (-not $Condition) { throw $Reason }
}
try {
    Check (Test-Path -LiteralPath $LiveConfig -PathType Leaf) "LIVE_CONFIG_NOT_FOUND"
    $rootActual = Git -GitArgs @('rev-parse', '--show-toplevel')
    Check ([System.IO.Path]::GetFullPath($rootActual).TrimEnd('\') -ieq
           [System.IO.Path]::GetFullPath($RepoRoot).TrimEnd('\')) "REPO_ROOT_MISMATCH"
    Check ((Git -GitArgs @('branch', '--show-current')) -ceq 'main') "NOT_ON_MAIN"
    Check ((Git -GitArgs @('status', '--porcelain', '--untracked-files=normal')) -eq '') "DIRTY_WORKTREE"
    Check ($allowedOrigins.Contains((Git -GitArgs @('remote', 'get-url', 'origin')))) "UNTRUSTED_ORIGIN"
    $remoteLine = Git -GitArgs @('ls-remote', 'origin', 'refs/heads/main')
    $remoteHead = ($remoteLine -split '\s+')[0]
    Check ($remoteHead -match '^[0-9a-f]{40}$') "REMOTE_HEAD_NOT_VERIFIED"

    if ($Apply) {
        [void](Git -GitArgs @('fetch', '--no-tags', 'origin', 'main'))
        [void](Git -GitArgs @('merge', '--ff-only', 'origin/main'))
        Check ((Git -GitArgs @('rev-parse', 'HEAD')) -ceq $remoteHead) "POST_UPDATE_MAIN_MISMATCH"
    } else {
        Check ((Git -GitArgs @('rev-parse', 'HEAD')) -ceq $remoteHead) "STALE_CHECKOUT_PASS_APPLY"
    }
    foreach ($relative in @(
        'collab/ops/submit_review_request.py',
        'collab/ops/review_request_gate.py',
        'collab/ops/review_pin_preflight.py',
        'collab/ops/tests/test_submit_review_request.py',
        'collab/ops/tests/test_review_pin_preflight.py',
        'AGENTS.md', 'CLAUDE.md', 'collab/CONTEXT_BRIEF.md'
    )) {
        Check (Test-Path -LiteralPath (Join-Path $RepoRoot $relative) -PathType Leaf) ("FILE_MISSING:" + $relative)
    }
    Push-Location -LiteralPath $RepoRoot
    try {
        & python -m unittest discover -s collab/ops/tests -p test_submit_review_request.py -v
        Check ($LASTEXITCODE -eq 0) "SUBMITTER_REGRESSION_FAILED"
        & python -m unittest discover -s collab/ops/tests -p test_review_pin_preflight.py -v
        Check ($LASTEXITCODE -eq 0) "PIN_PREFLIGHT_REGRESSION_FAILED"
        & python collab/ops/review_request_gate.py select --live-config $LiveConfig --intent unified --required-budget-usd 3.00
        Check ($LASTEXITCODE -eq 0) "WINDOWS_LIVE_POLICY_INCOMPATIBLE"
    } finally {
        Pop-Location
    }
    [pscustomobject]@{
        status = 'WINDOWS_REPO_ROLLOUT_CHECK_PASS'
        apply_requested = [bool]$Apply
        repo_head = (Git -GitArgs @('rev-parse', 'HEAD'))
        source = 'wonhwipark/CoWork-Skill-Collab/main'
        source_preflight = 'REGRESSION_PASS'
        reviewer_config = 'POLICY_COMPATIBLE_NOT_APPROVED'
        signer_ready_model_calls = 'NOT_EXECUTED'
        watcher_hook_installed = 'NOT_CLAIMED'
        claude_session_loaded = 'NOT_VERIFIED'
    } | ConvertTo-Json -Depth 4
    exit 0
} catch {
    [Console]::Error.WriteLine(("WINDOWS_REVIEW_SUBMITTER_ROLLOUT_BLOCKED: " + $_.Exception.Message))
    exit 2
}
