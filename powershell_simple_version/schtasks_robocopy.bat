schtasks /Create /TN "Monthly Robocopy Job" /TR "powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File C:\Robocopy\run_monthly_robocopy.ps1" /SC MONTHLY /D 1 /ST 01:00
