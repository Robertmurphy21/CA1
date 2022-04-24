#!/usr/bin/env pwsh

#Robert Murphy D00228588

$StackName = "KFC"

# import the Get-StackOutput function 
. ./stack_output_function.ps1

Write-Host "emptying bucket..."
$BucketName = Get-StackOutput $StackName "menubucketname"
aws s3 rm s3://$BucketName --recursive

Write-Host "deleting stack... " -NoNewline
aws cloudformation delete-stack --stack-name $StackName
Write-Host "OK" -ForegroundColor Yellow
