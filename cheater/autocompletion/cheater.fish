#completion for cheat
complete -c cheater -s h -l help -f -x --description "Display help and exit"
complete -c cheater -l edit -f -x --description "Edit <cheatsheet>"
complete -c cheater -s e -f -x --description "Edit <cheatsheet>"
complete -c cheater -s l -l list -f -x --description "List all available cheatsheets"
complete -c cheater -s d -l cheat-directories -f -x --description "List all current cheat dirs"
complete -c cheater --authoritative -f
for cheatsheet in (cheater -l | cut -d' ' -f1)
    complete -c cheater -a "$cheatsheet"
    complete -c cheater -o e -a "$cheatsheet" 
    complete -c cheater -o '-edit' -a "$cheatsheet"
end
