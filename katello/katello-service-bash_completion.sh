# Opts for every command
_katelloservice_help_opts="-h --help"
_katello_action_opts="restart stop start status list"
_katello_services="mongod postgresql qpidd qdrouterd tomcat tomcat6 pulp_workers pulp_celerybeat pulp_resource_manager foreman-proxy httpd foreman-tasks"

_katello-service_exclude-only()
{
  local opts="${_katello_services}"
  COMPREPLY=($(compgen -W "${opts}" -- ${1}))
}

# Main function
_katello-service()
{
    local first second cur prev opts base line
    COMPREPLY=()
    first=${COMP_WORDS[1]}
    second=${COMP_WORDS[2]}
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    line=${COMP_LINE}

    # top-level commands and options
    if [[ $cur == -* ]]
    then
    opts="--only --exclude ${_katelloservice_help_opts}"
    else
    opts="${_katello_action_opts}"
    fi

    case "${prev}" in
        *--exclude*|*--only*)
        "_katello-service_exclude-only" "${cur}" "${prev}" "${line}"
        return 0
        ;;
    esac
    COMPREPLY=($(compgen -W "${opts}" -- ${cur}))
    return 0
}
complete -F _katello-service -o filenames katello-service words
