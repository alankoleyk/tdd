test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

CO2=test/data/Agrofood_co2_emission.csv
GDP=test/data/IMF_GDP.csv
OUT=test_output_fire_gdp.png

run test_plot_runs python src/plot_fire_gdp.py \
    --co2_file $CO2 --gdp_file $GDP \
    --countries Albania Algeria Japan --out $OUT
assert_exit_code 0
assert_equal $OUT $( ls $OUT )
rm -f $OUT

run test_country_with_no_data python src/plot_fire_gdp.py \
    --co2_file $CO2 --gdp_file $GDP \
    --countries Albania Cuba --out $OUT
assert_exit_code 0
assert_equal $OUT $( ls $OUT )
rm -f $OUT

run test_missing_input_file python src/plot_fire_gdp.py \
    --co2_file no_such_file.csv --gdp_file $GDP --out $OUT
assert_exit_code 1

run test_bad_argument python src/plot_fire_gdp.py --not_an_option
assert_exit_code 2