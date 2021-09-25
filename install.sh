## Go to the home folder
cd $HOME
## Source the installed bashrc at the end of the original bashrc
echo "source ~/dotfiles/.bashrc" >> ~/.bashrc

## For VIM, remove existing configuration and install new one
rm .vimrc
ln -s dotfiles/.vimrc ./.vimrc

# Vim plug
curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim

## vim packages
mkdir -p .vim/pack/external/opt
git clone https://github.com/joshdick/onedark.vim $HOME/.vim/pack/external/opt/onedark.vim
