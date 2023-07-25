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
    ## Add a git prompt
    if [ -f ~/dotfiles/git-prompt.sh ]; then
        ## Activate staged and unstaged indicator
        GIT_PS1_SHOWDIRTYSTATE=1
        source ~/dotfiles/git-prompt.sh
        PS1_GIT='$(__git_ps1)'
    else
        PS1_GIT=""
    fi
    ## Add a python venv prompt
    if [ -f ~/dotfiles/detect_venv.py ]; then
        PS1_PY_VENV=$(python ~/dotfiles/detect_venv.py 2>&1)
    else
        PS1_PY_VENV=""
    fi
    ## Add colors in the terminal
    if [ -f ~/dotfiles/prompt_colors.sh ]; then
        source ~/dotfiles/prompt_colors.sh
        bash_prompt $PS1_GIT $PS1_PY_VENV
    fi
    
    ## Add all the aliases
    if [ -f ~/dotfiles/.bash_aliases ]; then
        source ~/dotfiles/.bash_aliases
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
fi

