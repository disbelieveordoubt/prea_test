# PREA Research Suite - Full Powerline Oh My Posh Integration for Gemini
# Merged script to combine the powerline theme with functional Nerd Font icons.

# Read JSON input from the CLI
$input = [Console]::In.ReadToEnd()

try {
    $data = $input | ConvertFrom-Json
    $modelName = "Gemini ✨"
    $currentDir = if ($data.workspace.current_dir) { $data.workspace.current_dir } else { "" }
} catch {
    $modelName = "Gemini ✨"
    $currentDir = Get-Location
}

# ANSI escape sequences
$ESC = [char]27
$RESET = "${ESC}[0m"

# Oh My Posh jandedobbeleer color scheme (RGB values from theme)
$PURPLE_BG = "${ESC}[48;2;193;156;220m"      # Purple segment
$PINK_BG = "${ESC}[48;2;238;190;190m"        # Pink segment
$GREEN_BG = "${ESC}[48;2;144;238;144m"       # Light green segment
$YELLOW_BG = "${ESC}[48;2;255;255;0m"        # Yellow segment
$BLUE_BG = "${ESC}[48;2;135;206;250m"        # Light blue segment
$GRAY_BG = "${ESC}[48;2;128;128;128m"        # Gray segment
$WHITE_FG = "${ESC}[38;2;255;255;255m"       # White text
$BLACK_FG = "${ESC}[38;2;0;0;0m"             # Black text

# Nerd Font powerline symbols
$POWERLINE_RIGHT = "\uE0B0" # nf-pl-left_hard_divider

# Nerd Font icons (from gemini-statusline.ps1)
$USER_ICON = "\uF007"      # nf-fa-user
$FOLDER_ICON = "\uF115"    # nf-fa-folder_open
$GIT_ICON = "\uF126"      # nf-fa-code_branch
$GIT_AHEAD = "\uF062"     # nf-oct-arrow_up
$GIT_BEHIND = "\uF063"    # nf-oct-arrow_down
$GIT_STAGED = "\uF067"    # nf-fa-plus
$GIT_MODIFIED = "\uF044"  # nf-fa-pencil
$GIT_UNTRACKED = "\uF059" # nf-fa-question
$GIT_DELETED = "\uF068"   # nf-fa-minus
$GIT_CONFLICT = "\uF071" # nf-fa-exclamation_triangle
$BRAIN_ICON = "\uF29A"     # nf-md-google
$TIME_ICON = "\uF017"      # nf-fa-clock_o

# Helper function to create powerline segments
function New-PowerlineSegment {
    param(
        [string]$Content,
        [string]$BackgroundColor,
        [string]$ForegroundColor,
        [string]$NextBackground = "",
        [bool]$IsLast = $false
    )

    $segment = "$BackgroundColor$ForegroundColor $Content "

    if ($IsLast) {
        $segment += "$RESET$BackgroundColor$POWERLINE_RIGHT$RESET"
    } elseif ($NextBackground) {
        # Transition to next segment
        $transitionColor = $BackgroundColor -replace "48;", "38;"  # Convert bg to fg
        $segment += "$NextBackground$transitionColor$POWERLINE_RIGHT"
    }

    return $segment
}

# Get username and directory
$username = $env:USERNAME
$dirName = if ($currentDir) { Split-Path -Leaf $currentDir } else { Split-Path -Leaf (Get-Location) }

# Git processing
$gitContent = ""
$gitBgColor = $GREEN_BG
$gitDir = if ($currentDir) { $currentDir } else { Get-Location }

$gitExe = $null
foreach ($path in @("git", "D:\Git\bin\git.exe", "C:\Program Files\Git\bin\git.exe")) {
    try { $null = & $path --version 2>$null; $gitExe = $path; break } catch { continue }
}

if ($gitExe -and (Test-Path (Join-Path $gitDir ".git"))) {
    try {
        Push-Location $gitDir
        $branch = & $gitExe branch --show-current 2>$null
        if (-not $branch) { $branch = & $gitExe rev-parse --abbrev-ref HEAD 2>$null }
        if (-not $branch) { $branch = "detached" }

        # Get git status
        $gitStatus = & $gitExe status --porcelain 2>$null
        $untracked = $modified = $deleted = $staged = $conflicts = 0

        if ($gitStatus) {
            foreach ($line in $gitStatus) {
                if ($line -match '^\?\?') { $untracked++ }
                elseif ($line -match '^[MADRC] ') { $staged++ }
                elseif ($line -match '^ ?M') { $modified++ }
                elseif ($line -match '^ ?D') { $deleted++ }
                elseif ($line -match '^UU|^AA|^DD') { $conflicts++ }
            }
        }

        # Get ahead/behind
        $ahead = $behind = 0
        try {
            $aheadBehind = & $gitExe rev-list --left-right --count HEAD@{upstream}...HEAD 2>$null
            if ($aheadBehind -and $aheadBehind -match '(\d+)\s+(\d+)') {
                $behind = [int]$matches[1]
                $ahead = [int]$matches[2]
            }
        } catch {}

        # Determine git segment color and build content
        if ($conflicts -gt 0) { $gitBgColor = "${ESC}[48;2;255;69;0m" }  # Red-orange for conflicts
        elseif ($staged -gt 0 -or $modified -gt 0 -or $untracked -gt 0 -or $deleted -gt 0) { $gitBgColor = $YELLOW_BG }
        else { $gitBgColor = $GREEN_BG }

        $gitParts = @("$GIT_ICON $branch")
        if ($ahead -gt 0) { $gitParts += "$GIT_AHEAD$ahead" }
        if ($behind -gt 0) { $gitParts += "$GIT_BEHIND$behind" }
        if ($staged -gt 0) { $gitParts += "$GIT_STAGED$staged" }
        if ($untracked -gt 0) { $gitParts += "$GIT_UNTRACKED$untracked" }
        if ($modified -gt 0) { $gitParts += "$GIT_MODIFIED$modified" }
        if ($deleted -gt 0) { $gitParts += "$GIT_DELETED$deleted" }
        if ($conflicts -gt 0) { $gitParts += "$GIT_CONFLICT$conflicts" }

        $gitContent = $gitParts -join " "
        Pop-Location
    } catch { try { Pop-Location } catch {} }
}

# Get timestamp
$timestamp = Get-Date -Format "HH:mm:ss"

# Build powerline statusline with segments
$statusLine = ""

# Username segment (purple)
$statusLine += New-PowerlineSegment -Content "$USER_ICON $username" -BackgroundColor $PURPLE_BG -ForegroundColor $WHITE_FG -NextBackground $PINK_BG

# Directory segment (pink)
$statusLine += New-PowerlineSegment -Content "$FOLDER_ICON $dirName" -BackgroundColor $PINK_BG -ForegroundColor $BLACK_FG -NextBackground $gitBgColor

# Git segment (dynamic color)
if ($gitContent) {
    $statusLine += New-PowerlineSegment -Content $gitContent -BackgroundColor $gitBgColor -ForegroundColor $BLACK_FG -NextBackground $BLUE_BG
}

# Model segment (blue)
$statusLine += New-PowerlineSegment -Content "$BRAIN_ICON $modelName" -BackgroundColor $BLUE_BG -ForegroundColor $BLACK_FG -NextBackground $GRAY_BG

# Time segment (gray) - final segment
$statusLine += New-PowerlineSegment -Content "$TIME_ICON $timestamp" -BackgroundColor $GRAY_BG -ForegroundColor $WHITE_FG -IsLast $true

Write-Output $statusLine