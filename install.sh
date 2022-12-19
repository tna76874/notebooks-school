#!/bin/bash
export SCRIPT=$(readlink -f "$0")
export DIR=$(dirname "$SCRIPT")

condaenv="info"
usage="$(basename "$0") [-h|-i|-u|-e|c]  -- simple conda environment installer for $condaenv environment

where:
    -h  show this help text
    -i	install conda environment and packages from environment.yml
    -p	install pip packages from requirement.txt
    -u  remove conda environment
    -e	create environment.xml
"

while [ "$1" != "" ]; do
    case $1 in
        -i | --install )       	conda env create -f environment.yml #&& conda activate $condaenv && pip install -r requirements.txt --user
				exit 1
                                ;;
        -p | --pip )            conda activate $condaenv && pip install -r requirements.txt --user
                                exit 1
                                ;;
        -u | --uninstall )    	conda remove -y --name $condaenv --all
				exit
                                ;;
        -e | --environment )    conda env export --from-history > environment.yml
                                exit 1
                                ;;
        * )                     echo "$usage" >&2
                                exit 1
    esac
    shift
done
