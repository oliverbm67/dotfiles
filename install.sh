#!/usr/sh

## Go to the home folder, remove the original dotfiles and link the new ones
cd $HOME
rm .bashrc
rm .vimrc
ln -s dotfiles/.bashrc ./.bashrc
ln -s dotfiles/.vimrc ./.vimrc

## vim packages
mkdir -p .vim/pack/external/opt
git clone https://github.com/joshdick/onedark.vim $HOME/.vim/pack/external/opt/
mkdir -p .vim/pack/plugins/start/lightline
git clone https://github.com/itchyny/lightline.vim ~/.vim/pack/plugins/start/lightline
mkdir -p ~/.vim/autoload/lightline/colorscheme/
cp ~/.vim/pack/external/opt/onedark.vim/autoload/lightline/colorscheme/onedark.vim ~/.vim/autoload/lightline/colorscheme/
git clone --depth 1 https://github.com/dense-analysis/ale.git ~/.vim/pack/plugins/start/ale
