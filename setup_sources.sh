#!/bin/bash -xe

dir='*'
[ -n "$1" ] && dir=$1

for spec in $dir/*.spec; do
  d=$(dirname $spec)
  source0=$(spectool --list-files $spec | awk '{print $2}' | head -n1)
  sourcebase=$(basename "$source0")
  [ -h $d/$sourcebase ] || continue
  git annex whereis "$d/$sourcebase" 2>/dev/null | grep -q " web" && continue
  
  if [[ $2 == '--relaxed' ]]; then
    git annex addurl --relaxed --file "$d/$sourcebase" "$source0"
  else
    git annex addurl --file "$d/$sourcebase" "$source0"
  fi
done
