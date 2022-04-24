function Get-StackOutput {

    param ($StackName,$OutputName)

    $OutputValue = ((aws cloudformation describe-stacks --stack-name "$StackName" |ConvertFrom-Json).Stacks[0].Outputs | Where-Object { $_.OutputKey -eq "$OutputName" }).OutputValue
	return $OutputValue

}
