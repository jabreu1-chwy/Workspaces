# File path of the text file containing the usernames
$filePath = "C:\Users\aa-jabreu1.001\Downloads\compare_users_to_AD.txt"

# Get the usernames from the text file
$usernames = Get-Content $filePath
 
# Create an array to store the results
$results = @()
 
# Iterate through each username
foreach ($username in $usernames) {
    try {
        # Get the user object from Active Directory
        $user = Get-ADUser -Identity $username -Properties Enabled, DistinguishedName
        $userObject = Get-ADObject -Identity $user.DistinguishedName -Properties lastLogon
 
        if ($user.Enabled -eq $true) {
            $status = "Enabled"
        }
        else {
            $status = "Disabled"
        }
 
        # Get the last logon time
        $lastLogon = [DateTime]::FromFileTime($userObject.lastLogon)
 
        $now = (Get-Date)
 
        $timeSpan = New-TimeSpan -Start $lastLogon -End $now
        $daysSinceLastLogon = [Math]::Floor($timeSpan.TotalDays)
 
        # Create a new object to store the result
        $result = [PSCustomObject]@{
            SamAccountName     = $username
            Status             = $status
            LastLogon          = $lastLogon
            DaysSinceLastLogon = $daysSinceLastLogon
        }
 
        # Add the object to the array
        $results += $result
    }
    catch {
        # Create a new object to store the result
        $result = [PSCustomObject]@{
            SamAccountName     = $username
            Status             = "Not in AD"
            LastLogon          = "N/A"
            DaysSinceLastLogon = "N/A"
        }
 
        # Add the object to the array
        $results += $result
    }
}
 
 
 
# Export the results to a CSV file
$results | Export-Csv -Path "C:\Users\aa-jabreu1.001\Downloads\testing_1.csv" -NoTypeInformation 
 