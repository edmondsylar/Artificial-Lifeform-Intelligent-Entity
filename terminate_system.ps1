Get-Process | Where-Object {$_.MainWindowTitle -match "Layer 1"} | ForEach-Object { $_.CloseMainWindow() }
Get-Process | Where-Object {$_.MainWindowTitle -match "Layer 2"} | ForEach-Object { $_.CloseMainWindow() }
Get-Process | Where-Object {$_.MainWindowTitle -match "Layer 3"} | ForEach-Object { $_.CloseMainWindow() }
Get-Process | Where-Object {$_.MainWindowTitle -match "Layer 4"} | ForEach-Object { $_.CloseMainWindow() }
Get-Process | Where-Object {$_.MainWindowTitle -match "Layer 5"} | ForEach-Object { $_.CloseMainWindow() }
Get-Process | Where-Object {$_.MainWindowTitle -match "Layer 6"} | ForEach-Object { $_.CloseMainWindow() }