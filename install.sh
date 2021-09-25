## Go to the home folder, remove the original dotfiles and link the new ones
cd $HOME
rm .bashrc
rm .vimrc
ln -s dotfiles/.bashrc ./.bashrc
ln -s dotfiles/.vimrc ./.vimrc

# Vim plug
curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim

## vim packages
mkdir -p .vim/pack/external/opt
git clone https://github.com/joshdick/onedark.vim $HOME/.vim/pack/external/opt/onedark.vim
