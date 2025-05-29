#!/usr/bin/bash

# -*- coding: utf-8 -*-
# ---
# module: kill
# short_description: Kill a process by PID or name using a specified signal
# description:
#   - This module allows you to kill a process by either its PID or its name using a specified signal.
# options:
#   process:
#     description:
#       - The PID or name of the process to kill.
#     required: true
#     type: str
#   signal:
#     description:
#       - The signal to send to the process.
#     required: true
#     type: str
# author:
#   - John Freidman (@Xploit9999)
# ---

function output(){
    
    cat <<-!
    {
        "changed": ${1},
        "failed": ${2},
        "msg": "${3}"
    }
!
}

function kill_process(){

    if [[ ${process} =~ ^[0-9]+$ ]]; then

        kill -0 ${process} 2>/dev/null && {
                kill -${signal} ${process}
                output true false "Process with PID ${process} killed using signal ${signal}." 
            } || {
                output false false "No process found with PID $process."
            }

    elif [[ ${process} =~ ^[a-zA-Z]+$ ]]; then

        pgrep ${process} 1>/dev/null && {
                pkill -${signal} ${process}
                output true false "Process ${process} killed using signal ${signal}." 
            } || {
                output false false "No process named ${process} found to kill."
            }
    else

       output false true "Invalid process identifier: ${process}. Must be a PID or process name."

    fi
}

function __main__(){

    if [[ ${UID} -eq 0 ]]; then

        [[ ! -z ${process} && ! -z ${signal} ]] && {
            kill_process
        } || {
            output false true "[x] You must specify both the process and the signal." >&2; exit 1
        }

   else

      output false true "You must become as root to kill somebody." >&2; exit 1

   fi

}

source $1; __main__
