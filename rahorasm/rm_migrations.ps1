Get-ChildItem -Directory | ForEach-Object {
    $parentDir = $_.FullName
    $migrationsDir = Join-Path $parentDir 'migrations'

    # Check if the "migrations" directory exists within the current directory
    if (Test-Path $migrationsDir) {
        # Get all files within the "migrations" directory, excluding __init__.py files
        Get-ChildItem -Path $migrationsDir -File  | ForEach-Object {
            # Remove each file
            Remove-Item -Path $_.FullName -Force
        }
        New-Item (Join-Path $migrationsDir '__init__.py')
    }
}