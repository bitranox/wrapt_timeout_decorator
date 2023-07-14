put 3rd party stubs in this directory needed to pass mypy on Github Actions.

in the Github Actions the MYPYPATH is set to this directory.

for local testing, put the *.pyi Files into another central directory and set the mypy path accordingly.
the reason for that is, that a certain *.pyi have to be only found once by mypy, otherwise it will throw an error.

lets say, we have an external module "external_test" and we created an "external_test.pyi" stub file.

the module "external_test" is used in project_a, and project_b, and package_a imports package_b


-- projects -- stub_directory -- external_test.pyi
            |
            -- project_A ------- package_a_dir --- 3rd_party_stubs --- external_test.pyi
            |
            -- project_B ------- package_b_dir --- 3rd_party_stubs --- external_test.pyi


for travis test of project_A we need to set the MYPYPATH to .../projects/project_A/package_a_dir/3rd_party_stubs

for local tests, we need to set the MYPYPATH to .../projects/stub_directory , not to find external_test.pyi twice.
