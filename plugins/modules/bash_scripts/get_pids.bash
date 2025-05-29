#!/usr/bin/bash

# -*- coding: utf-8 -*-
# ---
# module: get_pids
# short_description: Retrieve the PIDs of processes by user or by process name.
# description:
#   - This module allows retrieving process IDs (PIDs) based on the user who owns the process or by the process name.
#   - It supports case-insensitive searches and can output the PIDs in JSON format.
# options:
#   by_user:
#     description:
#       - The username for which you want to retrieve the processes.
#       - If provided, this option retrieves the processes owned by the given user.
#     required: false
#     type: str
#   by_name:
#     description:
#       - The name of the process to search for.
#       - If provided, this option retrieves the PIDs of the processes matching the given name.
#     required: false
#     type: str
#   ignore_case:
#     description:
#       - Set this to C(true) to perform a case-insensitive search for process names or usernames.
#     required: false
#     type: bool
#     default: false
# author:
#   - John Freidman (@Xploit9999)
# notes:
#   - Either I(by_user) or I(by_name) must be provided. If neither is provided, the module will fail.
#   - The I(ignore_case) option defaults to C(false), meaning the search is case-sensitive unless specified otherwise.
#   - This module does not change the state of the system but retrieves process information.
# examples:
#   - name: Retrieve PIDs by username
#     get_pids:
#       by_user: "john"
#
#   - name: Retrieve PIDs by process name
#     get_pids:
#       by_name: "bash"
#
#   - name: Case-insensitive search by process name
#     get_pids:
#       by_name: "BASH"
#       ignore_case: true
#
#   - name: Retrieve PIDs by username, case-insensitive
#     get_pids:
#       by_user: "JOHN"
#       ignore_case: true


function output(){
    
    IFS='\n' read -d "" -ra arr <<< ${5}
    while read pid; do [[ ${#pid} > 0 ]] && { result+="${pid}, " ;}; done <<< ${arr[@]}
    cat <<-!
    {
    "changed": ${1},
    "failed": ${2},
    "pids": {
        "${3}": "${4}",
        "pids": [${result%%, }]
        } 
    }
!
}

function get_pids(){

    ignore_case=${ignore_case:-false}
    
    case ${ignore_case} in 
        false|False)
            [[ ! -z ${by_user} ]] && {
                pids=`ps --no-headers -U ${by_user} -o pid 2>/dev/null`
                [[ $? -eq 0 ]] && {
                    output false false "user" "${by_user}" "${pids}"
                
                } || { output false true "Error" "No process found for the user ${by_user}" "" ;}
            } || {
                [[ ! -z ${by_name} ]] && {
                    pids=`pgrep ${by_name}`
                    output false false "process" "${by_name}" "${pids}"
                } || {
                    output false true "Error" "Invalid option, this module only accept: [ 'by_name', 'by_user' ]" ""    
                }
            }
            ;;
        true|True)
            [[ ! -z ${by_user} ]] && {
                pids=`ps --no-headers -U ${by_user,,} -o pid`
                output false false "user" "${by_user}" "${pids}"
            } || {
                [[ ! -z ${by_name} ]] && {
                    pids=`pgrep -i ${by_name}`
                    output false false "process" "${by_name}" "${pids}"
                } || {
                    output false true "Error" "Invalid option, this module only accept: [ 'by_name', 'by_user' ]" ""    
                }
            }
            ;;
       esac
 
}

function __main__(){

    [[ ! -z ${by_user} || ! -z ${by_name} ]] && {
        get_pids
    } || {
        output false true "Error" "You must specify either by_user or by_name to retrieve processes." ""
        exit 1
    }

}

source $1; __main__
