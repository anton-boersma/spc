& "$PSScriptRoot\venv\Scripts\activate.ps1"

ampy --port COM3 rmdir modules

ampy --port COM3 put "$PSScriptRoot\modules" modules

ampy --port COM3 rmdir libraries

ampy --port COM3 put "$PSScriptRoot\libraries" libraries
