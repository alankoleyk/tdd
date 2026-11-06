countries = ["Brazil", "Indonesia", "Australia", "Canada", "Mexico"]

rule all:
    input:
        expand("results/plots/{country}.png", country=countries)

rule make_tables:
    input:
        co2="data/Agrofood_co2_emission.csv",
        gdp="data/IMF_GDP.csv"
    output:
        "results/tables/{country}.tsv"
    shell:
        """
        python src/fire_gdp.py \
            --co2_file {input.co2} \
            --gdp_file {input.gdp} \
            --country {wildcards.country} \
            --out_file {output}
        """

rule make_plots:
    input:
        co2="data/Agrofood_co2_emission.csv",
        gdp="data/IMF_GDP.csv"
    output:
        "results/plots/{country}.png"
    shell:
        """
        python src/plot_fire_gdp.py \
            --co2_file {input.co2} \
            --gdp_file {input.gdp} \
            --countries {wildcards.country} \
            --out {output}
        """