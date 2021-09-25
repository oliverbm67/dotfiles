" Vim plug plugins
call plug#begin('~/.vim/plugged')
" vim easy align
Plug 'junegunn/vim-easy-align'
" onedark theme
Plug 'joshdick/onedark.vim'
" ALE asynchronous lint engine
Plug 'dense-analysis/ale'
" Lightline
Plug 'itchyny/lightline.vim'
" Initialize plugin system
call plug#end()


" Standard VIM settings
set tabstop=4
set shiftwidth=4
" Replace tab with spaces
set expandtab
" Remove 4 spaces when possible
set softtabstop=4
" Add number line
set number
" Ignore case for search
set ic
" search with upper case are case sensitive
set smartcase
" Search highlighting
set hlsearch
" activate syntax highlighting
syntax on
" Auto indentation
set autoindent
" Set a visual help for which line is selected
set cursorline
" Activate the menu at the bottom of the interface (used for file name display)
set wildmenu
" Always working backspace
set backspace=indent,eol,start
" Name of the file in the editor
set laststatus=2
set statusline+=%F
" Activate mouse support
set mouse=a

"External packages
packadd! onedark.vim

" Color theme
colorscheme onedark
let g:lightline = {
    \ 'colorscheme': 'onedark',
    \ }

" ALE settings
" Activate auto-completion
let g:ale_completion_enabled = 1
" Sign gutter always open
let g:ale_sign_column_always = 1
" Display error in status bar
let g:airline#extensions#ale#enabled = 1
" Use vhdl 93 when linting VHDL code
let g:ale_vhdl_ghdl_options = '--std=93'

" easy align settings
" Start interactive EasyAlign in visual mode (e.g. vipga)
xmap ga <Plug>(EasyAlign)

" Start interactive EasyAlign for a motion/text object (e.g. gaip)
nmap ga <Plug>(EasyAlign)
