<#
.SYNOPSIS
    Validates the JSON Structure: Semantic and Reference-System Annotations samples.

.DESCRIPTION
    Runs five checks:

      1. The extension meta-schema (semantic-annotations-v0.json) is a conforming
         JSON Structure schema document. Skipped unless the json-structure/meta
         repository is checked out beside this one, because the meta-schema
         imports the Extended meta-schema.
      2. Every sample schema conforms to JSON Structure Core and the extensions
         it declares in $uses.
      3. Every example.json instance conforms to the schema beside it.
      4. Every annotation in every sample schema conforms to the
         extension meta-schema.
      5. Every schema-unannotated.struct.json companion is a conforming schema,
         accepts the instance beside it, and is up to date with respect to the
         annotated schema it is derived from.

    Steps 1 to 3 use the JSON Structure Python SDK. Install it with
    'pip install json-structure'. Step 4 uses check-annotations.py and step 5
    uses make-unannotated.py, both of which read the meta-schema directly.

.EXAMPLE
    ./validate-samples.ps1
#>

[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'

$samplesRoot = $PSScriptRoot
$repoRoot = Split-Path -Parent $samplesRoot
$metaSchema = Join-Path $repoRoot 'semantic-annotations-v0.json'
$extendedMeta = Join-Path (Split-Path -Parent $repoRoot) 'meta/extended/v0/index.json'
$coreMeta = Join-Path (Split-Path -Parent $repoRoot) 'meta/core/v0/index.json'

$failures = 0

function Write-Result {
    param([bool]$Ok, [string]$Label, [string[]]$Detail)

    if ($Ok) {
        Write-Host "  [ok]   $Label" -ForegroundColor Green
    }
    else {
        Write-Host "  [fail] $Label" -ForegroundColor Red
        foreach ($line in $Detail) { Write-Host "         $line" -ForegroundColor Red }
        $script:failures++
    }
}

Write-Host 'Extension meta-schema' -ForegroundColor Cyan
if ((Test-Path $extendedMeta) -and (Test-Path $coreMeta)) {
    $output = & json-structure-check --metaschema --extended --allowimport `
        -m "https://json-structure.org/meta/extended/v0/#=$extendedMeta" `
        -m "https://json-structure.org/meta/core/v0/#=$coreMeta" `
        --quiet $metaSchema 2>&1
    Write-Result ($LASTEXITCODE -eq 0) 'semantic-annotations-v0.json' $output
}
else {
    Write-Host '  [skip] semantic-annotations-v0.json (json-structure/meta not checked out beside this repository)' -ForegroundColor Yellow
}

$schemas = Get-ChildItem -Path $samplesRoot -Recurse -Filter 'schema.struct.json' | Sort-Object FullName

Write-Host 'Sample schemas' -ForegroundColor Cyan
foreach ($schema in $schemas) {
    $output = & json-structure-check --extended --allowimport --quiet $schema.FullName 2>&1
    Write-Result ($LASTEXITCODE -eq 0) $schema.Directory.Name $output
}

Write-Host 'Sample instances' -ForegroundColor Cyan
foreach ($schema in $schemas) {
    $instance = Join-Path $schema.Directory.FullName 'example.json'
    if (-not (Test-Path $instance)) {
        Write-Result $false $schema.Directory.Name @('example.json is missing')
        continue
    }
    $output = & json-structure-validate --extended --allowimport --quiet $instance $schema.FullName 2>&1
    Write-Result ($LASTEXITCODE -eq 0) $schema.Directory.Name $output
}

Write-Host 'Characteristics annotations' -ForegroundColor Cyan
$checker = Join-Path $samplesRoot 'check-annotations.py'
$python = @('py', 'python3', 'python') |
    Where-Object { Get-Command $_ -ErrorAction SilentlyContinue } |
    Select-Object -First 1
if (-not $python) {
    Write-Host '  [skip] no Python interpreter on PATH' -ForegroundColor Yellow
}
else {
    foreach ($schema in $schemas) {
        $output = & $python $checker $metaSchema $schema.FullName 2>&1
        Write-Result ($LASTEXITCODE -eq 0) $schema.Directory.Name ($output | Select-Object -Skip 1)
    }
}

Write-Host 'Unannotated companions' -ForegroundColor Cyan
$companions = Get-ChildItem -Path $samplesRoot -Recurse -Filter 'schema-unannotated.struct.json' |
    Sort-Object FullName
foreach ($companion in $companions) {
    $output = & json-structure-check --extended --allowimport --quiet $companion.FullName 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Result $false $companion.Directory.Name $output
        continue
    }
    $instance = Join-Path $companion.Directory.FullName 'example.json'
    $output = & json-structure-validate --extended --allowimport --quiet $instance $companion.FullName 2>&1
    Write-Result ($LASTEXITCODE -eq 0) $companion.Directory.Name $output
}
if (-not $python) {
    Write-Host '  [skip] up-to-date check (no Python interpreter on PATH)' -ForegroundColor Yellow
}
else {
    $output = & $python (Join-Path $samplesRoot 'make-unannotated.py') --check 2>&1
    Write-Result ($LASTEXITCODE -eq 0) 'derived from the annotated schemas' $output
}

Write-Host ''
if ($failures -eq 0) {
    Write-Host 'All checks passed.' -ForegroundColor Green
    exit 0
}

Write-Host "$failures check(s) failed." -ForegroundColor Red
exit 1
