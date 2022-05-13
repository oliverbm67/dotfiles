# Installation #
Retrieve and install these dotfiles with

    git clone https://github.com/oliverbm67/dotfiles.git ~/dotfiles
    cd ~/dotfiles
    ./install.sh

# Vim plugin #
Launch vim and execute the command

    :PlugInstall

to install all the plugins

Installing pylint is required for the plugin to work

    pip install pylint

# Bugs and workarounds #
## The triangle is not displayed in the terminal ##
The powerline fonts are probably missing, you can install them on debian-based system with

    sudo apt-get install fonts-powerline

and on Fedora

    sudo dnf install powerline-fonts
