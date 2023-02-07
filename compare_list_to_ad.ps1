# File path of the CSV file containing the usernames
$filePath = "C:\Users\aa-jabreu1\Downloads\AWS_Cleanup_2023-02-07.csv"

# Get the contents of the CSV file
$contents = Import-Csv $filePath
 
# Iterate through each row in the contents
foreach ($row in $contents) {
    try {
        # Get the user object from Active Directory(future use)
        $user = Get-ADUser -Identity $row.UserName -Properties Enabled, DistinguishedName
        #$userObject = Get-ADObject -Identity $user.DistinguishedName -Properties lastLogon(future use)
  
        if ($user.Enabled -eq $true) {
            $status = "Enabled"
        }
        else {
            $status = "Disabled"
        }
  
        # Get the last logon time(future use)
        #$lastLogon = [DateTime]::FromFileTime($userObject.lastLogon)(future use)
  
        #$now = (Get-Date)(future use)
  
        #$timeSpan = New-TimeSpan -Start $lastLogon -End $now(future use)
        #$daysSinceLastLogon = [Math]::Floor($timeSpan.TotalDays)(future use)
  
        # Add the status to the current row
        $row | Add-Member -NotePropertyName "Status" -NotePropertyValue $status
    }
    catch {
        # Add the status to the current row
        $row | Add-Member -NotePropertyName "Status" -NotePropertyValue "Not in AD"
    }
}
  
# Export the contents back to the CSV file
$contents | Export-Csv -Path $filePath -NoTypeInformation
