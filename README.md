# tdd

```
curl -L "https://docs.google.com/uc?export=download&id=1AsXP_OGs1O_TDeXiZjk3fYV1SrG4vwXF" -o data/Agrofood_co2_emission.csv
curl -L "https://docs.google.com/uc?export=download&id=19YEPysdnK7VCXuAe9Og9pwYkNT5CbQzr" -o data/IMF_GDP.csv
```
Expanded analysis to ["Brazil", "Indonesia", "Australia", "Canada", "Mexico"]. To run programs through snakemake: snakemake --cores 1. Snakemake has jobs to make plots and make tables of GDP and Emissions for each country per year. Plots and tables are created under results/plots and results/tables respectively. Example from Australia below.

Unfortunately, no correlation could be found within the scope of this research, and most graphs reflect stagnant GDP while emissions grow. Further expansions of the scope could include a linear regresssion test and then create a table containing the nation in which GDP and CO2 emissions have the highest correlation coefficient.

For testing to ensure robust code and usability, it seems important to run tests between the snakemake jobs to ensure that any bugs are easily found despite the workflow happening independently from the user. Such tests could include proper reading of the file, proper file formatting, and checking for file exports being created under results.


![alt text](image-1.png)

1990	4240.9972	413659.0
1991	4240.9972	416664.0
1992	4240.9972	432310.0
1993	4240.9972	455201.0
1994	4240.9972	482668.0
1995	4240.9972	512049.0
1996	6379.8273	543132.0
1997	9571.9957	573449.0
1998	7442.2955	605089.0
1999	10069.0516	637732.0
2000	3480.4142	687197.0
2001	2236.2255	730429.0
2002	4315.2736	782561.0
2003	7573.8576	830316.0
2004	757.3099	894720.0
2005	711.5768	964355.0
2006	5823.7134	1039552.0
2007	2102.9078	1133328.0
2008	471.1802	1236386.0
2009	3405.5055	1263580.0
2010	542.0101	1366000.0
2011	1083.1693	1468681.0
2012	1675.5378	1515293.0
2013	2839.5764	1568772.0
2014	2192.0506	1613230.0
2015	1358.7133	1638255.0
2016	1768.621	1699521.0
2017	1119.9392	1802283.0
2018	1815.4944	1895536.0
2019	20157.8404	1993774.0
2020	10985.2467	1972898.0