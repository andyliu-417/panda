# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH

# Path to your oh-my-zsh installation.
export ZSH=/Users/andyjunxi/.oh-my-zsh

# Set name of the theme to load. Optionally, if you set this to "random"
# it'll load a random theme each time that oh-my-zsh is loaded.
# See https://github.com/robbyrussell/oh-my-zsh/wiki/Themes
ZSH_THEME="dracula"

# Set list of themes to load
# Setting this variable when ZSH_THEME=random
# cause zsh load theme from this variable instead of
# looking in ~/.oh-my-zsh/themes/
# An empty array have no effect
# ZSH_THEME_RANDOM_CANDIDATES=( "robbyrussell" "agnoster" )

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion. Case
# sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
# DISABLE_AUTO_UPDATE="true"

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# The optional three formats: "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(
  git
)

source $ZSH/oh-my-zsh.sh

# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='mvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch x86_64"

# ssh
# export SSH_KEY_PATH="~/.ssh/rsa_id"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"
alias subl='/Applications/Sublime\ Text.app/Contents/SharedSupport/bin/subl'

alias repo='cd ~;cd repos;'
alias hp='cd ~;cd repos/hitplay-care-monitoring'
alias hppull='hp&&git pull origin master'
alias care='cd ~;cd repos/hitplay-care-monitoring/packages/hitplay-care-user-dashboard'
alias admin='cd ~;cd repos/hitplay-care-monitoring/packages/hitplay-care-admin-dashboard'
alias careb='cd ~;cd repos/hitplay-care-monitoring/packages/backend-user-dashboard-api'
alias adminb='cd ~;cd repos/hitplay-care-monitoring/packages/backend-admin-dashboard-api'
alias share='cd ~;cd repos/hitplay-care-monitoring/packages/hitplay-care-shared'

alias cares='care&&npm start;'
alias admins='admin&&npm start;'
alias carebd='careb&&sls deploy;'
alias adminbd='adminb&&sls deploy;'
alias shareb='share&&npm run build;'
alias shared='share&&npm run dev;'

alias master='care&&git checkout master'

alias sprint='master&&gSprint $1'
function gSprint() {
	git pull origin master
	bName="SPRINT-"$1
	git checkout -b $bName;
	git push --set-upstream origin $bName
}

alias task='gTask $1 $2'
function gTask() {
	sName="SPRINT-"$1
	git checkout $bName;
	bName="feature/CARE-"$2
	git checkout -b $bName;
}

alias done='master&&gDone $1'
function gDone() {
	sName="SPRINT-"$1
	git branch -D $bName;
}

alias gb='gBranch $1'
function gBranch() {
	bName="feature/CARE-"$1
	git checkout $bName;
}

alias hplerna='hp&&lerna clean --yes&&find ./ -name "package-lock.json"|xargs rm -rf&&npm cache clean --force&&sleep 3&&lerna bootstrap'


alias panda='panda $1 $2 $3 $4'
function panda() {
  python3 ~/.scripts.py $(pwd) $1 $2 $3 $4
  # python3 ~/repos/panda/scripts.py $(pwd) $1 $2 $3 $4

  if [ "$1" = "new" ]; then
    git clone https://github.com/andyliu-417/$2.git
    cd $2;
    npm i
    git add .
    git commit -m "panda init"
    git push origin master
    npm start
  fi
}
