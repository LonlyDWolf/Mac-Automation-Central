#!/bin/bash

# This script has only been tested on macOS Sonoma 14.6.1

# Function to configure Dock preferences
configure_dock() {
    defaults write com.apple.dock tilesize -int 16
    defaults write com.apple.dock orientation -string "left"
    defaults write com.apple.dock autohide -bool true
    defaults write com.apple.dock launchanim -bool false
    defaults write com.apple.dock show-recents -bool false
    killall Dock
}

# Function to configure Finder preferences
configure_finder() {
    defaults write com.apple.finder ShowExternalHardDrivesOnDesktop -bool false
    defaults write com.apple.finder ShowHardDrivesOnDesktop -bool false
    defaults write com.apple.finder ShowMountedServersOnDesktop -bool false
    defaults write com.apple.finder ShowRemovableMediaOnDesktop -bool false
    defaults write com.apple.finder NewWindowTarget -string "PfHm"
    defaults write com.apple.finder NewWindowTargetPath -string "file://${HOME}/"
    defaults write NSGlobalDomain AppleShowAllExtensions -bool true
    defaults write com.apple.finder FXEnableExtensionChangeWarning -bool true
    defaults write com.apple.finder FXDefaultSearchScope -string "SCcf"
    killall Finder
}

# Function to configure Finder view options using AppleScript
configure_finder_view() {
    osascript <<EOD
tell application "Finder"
    activate
    tell application "System Events" to tell process "Finder"
        set frontmost to true
        click menu item "Show Status Bar" of menu "View" of menu bar 1
        click menu item "Show Path Bar" of menu "View" of menu bar 1
        click menu item "Show Tab Bar" of menu "View" of menu bar 1
    end tell
end tell
EOD
}

# Function to install Homebrew
install_homebrew() {
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" || {
        printf "Homebrew installation failed.\n" >&2
        return 1
    }
    printf "Homebrew has been installed successfully.\n"
}

# Global variables
ZPROFILE="$HOME/.zprofile"
BREW_PATH="/opt/homebrew/bin/brew"

# Function to add Homebrew to PATH via zprofile
add_brew_to_path() {
    if [[ -x "$BREW_PATH" ]]; then
        printf "\n# Add Homebrew to PATH\n" >> "$ZPROFILE"
        printf 'eval "$(%s shellenv)"\n' "$BREW_PATH" >> "$ZPROFILE"
    else
        printf "Error: Homebrew not found at %s\n" "$BREW_PATH" >&2
        return 1
    fi
}

# Function to evaluate Homebrew's shell environment
eval_brew_shellenv() {
    if ! eval "$("$BREW_PATH" shellenv)"; then
        printf "Error: Failed to evaluate Homebrew shell environment\n" >&2
        return 1
    fi
}

# Function to install Raycast using Homebrew
install_raycast() {
    if ! brew install --cask raycast; then
        printf "Raycast installation failed.\n" >&2
        return 1
    fi
    printf "Raycast has been installed successfully.\n"
}

# Function to install Rectangle
install_rectangle() {
    if ! brew install rectangle; then
        printf "Rectangle installation failed.\n" >&2
        return 1
    fi
    printf "Rectangle has been installed successfully.\n"
}

# Function to install Alt-Tab
install_alt_tab() {
    if ! brew install alt-tab; then
        printf "Alt-Tab installation failed.\n" >&2
        return 1
    fi
    printf "Alt-Tab has been installed successfully.\n"
}

# Function to install Hidden Bar
install_hiddenbar() {
    if ! brew install hiddenbar; then
        printf "Hidden Bar installation failed.\n" >&2
        return 1
    fi
    printf "Hidden Bar has been installed successfully.\n"
}

# Function to install Stats
install_stats() {
    if ! brew install stats; then
        printf "Stats installation failed.\n" >&2
        return 1
    fi
    printf "Stats has been installed successfully.\n"
}

# Main function
main() {
    configure_dock
    printf "Dock preferences have been set.\n"
    configure_finder
    configure_finder_view
    printf "Finder preferences have been set.\n"
    install_homebrew || return 1
    add_brew_to_path || return 1
    eval_brew_shellenv || return 1
    install_raycast || return 1
    install_rectangle || return 1
    install_alt_tab || return 1
    install_hiddenbar || return 1
    install_stats || return 1
}

main "$@"