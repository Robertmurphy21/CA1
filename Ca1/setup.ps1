$StackName='KFC'

# import the Get-StackOutput function 
. ./stack_output_function.ps1

Write-Host 'requesting stack creation ... ' -NoNewline
aws cloudformation create-stack --stack-name $StackName --template-body file://KFC.json

#wait for the stack to complete creation
Write-Host 'waiting for stack to complete creating ... ' -NoNewline
aws cloudformation wait stack-create-complete --stack-name $StackName
Write-Host "OK" -ForegroundColor Yellow

# upload Specials to bucket
$BucketName = Get-StackOutput $StackName "menubucketname"
aws s3 cp deals.json s3://$BucketName/deals.json

Write-Host "KFC Takeaway System is now ready!" -ForegroundColor Yellow

