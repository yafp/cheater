#compdef cheat

declare -a cheats
cheats=$(cheater -l | cut -d' ' -f1)
_arguments "1:cheats:(${cheats})" && return 0
