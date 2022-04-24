#!/usr/bin/env pwsh
# CA1 checks file
# Robert Murphy D00228588

$Files = @( "description.txt", "template.json", "setup.ps1", "demo.ps1", "teardown.ps1" )

Write-Host "CA1 checks" -ForegroundColor Yellow
Foreach ( $File in $Files ) {
    Write-Host "checking for $File ..." -NoNewline
    If ( ! (Test-Path $File) ) {
	Write-Host "not found" -ForegroundColor Red
	return
    }
    Write-Host "found" -ForegroundColor Green    
}

Write-Host "all required files present - ready to submit!" -ForegroundColor Green

