#!/bin/bash
save_dir="$PWD"
own_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" || exit && pwd -P)" # this gives the full path, even for sourced scripts

# shellcheck disable=SC1090
source "${own_dir}/create_secrets_bash_helpers.sh"

project_root_dir="${project_root_dir}"

install_dependencies

banner "this will encrypt the name and the value of a secret environment variable for travis.
common secrets for the PizzaCutter Python Template are:
\"CC_TEST_REPORTER_ID\" and \"PYPI_PASSWORD\""

read -rp 'variable name  :' var_name
read -rp 'variable value :' var_value

cd "${project_root_dir}"||exit
travis encrypt "${var_name}=${var_value}" --no-interactive --com > "${own_dir}/secrets/${var_name}.secret.txt"

banner "the secret for \"${var_name}\" was created and exported to:
${own_dir}/secrets/${var_name}.secret.txt.
it will be imported to travis.yml the next time You run PizzaCutter"
wait_for_enter
cd "${save_dir}" || exit
