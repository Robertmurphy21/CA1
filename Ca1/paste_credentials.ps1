#!/usr/bin/env pwsh
# script to paste AWS Academy credentials into config dir

$AWSConfigDir = "~/.aws"

If(!(test-path $AWSConfigDir))
{
    Write-Host "creating AWS config directory $AWSConfigDir" -NoNewline
    New-Item -ItemType Directory -Force -Path $AWSConfigDir
    
}

Write-Host "using credentials from " -NoNewline
If( $IsMacOs ) {
    $Credentials = pbpaste
    Write-Host "mac clipboard"
}
Else {
    $Credentials = Get-Clipboard
    Write-Host "windows clipboard"
}

# check that credentials match pattern
#if ( $Credentials -notlike '*aws_access_key_id*' ) {
#    Write-Error "clipboard content is not aws credentials"
#    Return
#}

Write-Host "pasting into credentials file ... " -NoNewline
$Credentials | Out-File ~/.aws/credentials -Encoding ascii
Write-Host "done!" -ForegroundColor Green

Write-Host "creating config file ... " -NoNewline
"[default]
region=us-east-1" | Out-File ~/.aws/config -Encoding ascii
Write-Host "done!" -ForegroundColor Green

Write-Host "run lab_checks.ps1 to confirm correct setup" -ForegroundColor Yellow


