$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:PYTHONPATH = if ($env:PYTHONPATH) { "$ScriptDir;$env:PYTHONPATH" } else { $ScriptDir }
python -m leh @args
