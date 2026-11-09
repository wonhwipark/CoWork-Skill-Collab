# CoWork Windows host inspection only. Does not read secrets or alter tasks.
# Usage: powershell -NoProfile -File .\WINDOWS_READONLY_AUDIT.ps1 -WatcherHome 'D:\User\whpark\skill-collab-watcher' -Output '.\host_inventory_private.json'
param(
 [Parameter(Mandatory=$true)][string]$WatcherHome,
 [Parameter(Mandatory=$true)][string]$Output
)
$ErrorActionPreference = 'Stop'
$tasks = @(Get-ScheduledTask | Where-Object { $_.TaskName -match 'SKILL-COLLAB' } | ForEach-Object {
    $info = $null
    try { $info = Get-ScheduledTaskInfo -TaskName $_.TaskName -TaskPath $_.TaskPath } catch {}
    [ordered]@{name=$_.TaskName; state=[string]$_.State; task_path=$_.TaskPath;
        last_run_time=$(if($info){[string]$info.LastRunTime}else{$null});
        last_task_result=$(if($info){$info.LastTaskResult}else{$null})}
})
$processes = @(Get-Process -Name python,pythonw,claude -ErrorAction SilentlyContinue | ForEach-Object {
    [ordered]@{pid=$_.Id;name=$_.ProcessName}
})
$files = @('pyproject.toml','requirements.txt','README.md','reviewer.config.json') | ForEach-Object {
    [ordered]@{basename=$_;exists=[bool](Test-Path -LiteralPath (Join-Path $WatcherHome $_) -PathType Leaf)}
}
$result = [ordered]@{
    schema='COWORK_WINDOWS_HOST_READONLY_V1'
    collected_at_utc=[DateTime]::UtcNow.ToString('o')
    watcher_home_exists=[bool](Test-Path -LiteralPath $WatcherHome -PathType Container)
    watcher_tasks=$tasks
    python_or_reviewer_processes=$processes
    known_file_presence=@($files)
    actual_installed_version='NOT_VERIFIED'
    github_auth='NOT_TESTED'
    inspection_script_model_calls=0
    mode='INSPECTION_ONLY'
}
$result | ConvertTo-Json -Depth 6 | Out-File -FilePath $Output -Encoding UTF8
Write-Output "Local read-only inventory saved. Review/redact before any external upload."
