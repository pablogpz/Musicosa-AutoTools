param (
	# Program or script path
	[Parameter(Position = 0, Mandatory = $true)]
    [string]$Program,
	
	# Optional arguments for the program
	[Parameter(Position = 1)]
    [string[]]$Arguments,
	
	# (Optional) Execute program in a new window
	[switch]$NewWindow = $false
)

$peakMemory = 0
$startProcessParams = @{
    FilePath = $Program
    PassThru = $true
	NoNewWindow = -not $NewWindow
}
if ($Arguments) {
    $startProcessParams.ArgumentList = $Arguments
}

# Start the process
$startTime = Get-Date
$process = Start-Process @startProcessParams

# Monitor memory usage while the process is running
do {
	# Get current memory usage of the process (Working Set Peak)
	$currentMemory = $process.PeakWorkingSet64

	if ($currentMemory -gt $peakMemory) {
		$peakMemory = $currentMemory
	}
	
	if (-not $process.HasExited) {
		# Adjust sampling interval as needed
		Start-Sleep -Milliseconds 500
	}
} while (-not $process.HasExited)

$endTime = Get-Date
$executionTime = $endTime - $startTime

$Color = @{Foreground = "blue"}

Write-Host "`n"
Write-Host @Color "==== Benchmark Results ==================================="
Write-Host @Color "$([math]::Round($executionTime.TotalMilliseconds, 2)) ms | $([math]::Round(($peakMemory / 1MB), 2)) MB"
Write-Host @Color "=========================================================="
