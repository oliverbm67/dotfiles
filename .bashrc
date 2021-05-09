# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# User specific environment
if ! [[ "$PATH" =~ "$HOME/.local/bin:$HOME/bin:" ]]
then
    PATH="$HOME/.local/bin:$HOME/bin:$PATH"
fi
export PATH

## Make sure to be in interactive shell and not login
if [[ $- == *i* ]]
then
    ## Add colors in the terminal
    if [ -f ~/dotfiles/prompt_colors.sh ]; then
        source ~/dotfiles/prompt_colors.sh
    fi
    
    ## Add all the aliases
    if [ -f ~/dotfiles/.bash_aliases ]; then
        source ~/dotfiles/.bash_aliases
    fi
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi
