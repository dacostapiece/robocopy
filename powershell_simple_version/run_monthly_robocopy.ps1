# ===================================================================
# CONFIGURATION
# ===================================================================
#Run this before schtasks as admin
#New-Item -ItemType SymbolicLink -Path "C:\Robocopy" -Target "D:\Target Folder\CONFIGURACOES\"
#My target folder had brazilian portuguese characters, spaces and it was a long path, symlink above made it all happens smoothly
#Run this before schtasks as admin

$ScriptRoot = "C:\Robocopy"
# Log file
$LogFile = Join-Path $ScriptRoot "robocopy_log.txt"

# Email settings
$To             = "user@example.com.br"
$From           = "user@example.com.br"
$SMTPServer     = "example.com.br"
$SMTPPort       = 587
$SMTPUser       = "user@example.com.br"
$SMTPPassword   = "password"

# ===================================================================
# DATE LOGIC
# ===================================================================
$Now            = Get-Date
$PreviousMonthName  = $Now.AddMonths(-1).ToString("yyyy-MM")
$CurrentMonthName   = $Now.ToString("yyyy-MM")

$PreviousMonth = Join-Path $ScriptRoot $PreviousMonthName
$CurrentMonth  = Join-Path $ScriptRoot $CurrentMonthName

# ===================================================================
# ROBOCOPY (LIVE OUTPUT + LOG + CAPTURE)
# ===================================================================

$RobocopyCmd = "robocopy `"$PreviousMonth`" `"$CurrentMonth`" /E /V /NP /MAXAGE:10"

Write-Host "Running: $RobocopyCmd" -ForegroundColor Cyan

# Create UTF-8 writer (no BOM)
$logWriter = New-Object System.IO.StreamWriter($LogFile, $false, [System.Text.UTF8Encoding]::new($false))

# Create in-memory capture buffer for email
$Capture = New-Object System.Collections.Generic.List[string]

cmd.exe /c $RobocopyCmd 2>&1 | ForEach-Object {
    Write-Host $_
    $logWriter.WriteLine($_)
    $Capture.Add($_)
}

$logWriter.Close()

# robocopy exit code
$ExitCode   = $LASTEXITCODE
$Success    = $ExitCode -ge 0 -and $ExitCode -le 7
$StatusText = if ($Success) { "SUCCESS" } else { "FAILURE" }

# For email
$OutputText = $Capture -join "`r`n"

# ===================================================================
# EMAIL REPORT
# ===================================================================

$Body = @"
Robocopy monthly job executed at $(Get-Date).

Previous Month : $PreviousMonth
Current Month  : $CurrentMonth
Exit Code      : $ExitCode
Status         : $StatusText

==============================================================
                     ROBOCOPY OUTPUT
==============================================================
$OutputText

"@

# SMTP authentication
$SecurePass = ConvertTo-SecureString $SMTPPassword -AsPlainText -Force
$Credential = New-Object System.Management.Automation.PSCredential ($SMTPUser, $SecurePass)

Send-MailMessage `
    -SmtpServer $SMTPServer `
    -Port $SMTPPort `
    -UseSSL `
    -To $To `
    -From $From `
    -Subject "Robocopy Job $StatusText - $CurrentMonth" `
    -Body $Body `
    -Credential $Credential
