# Alternative_to_pvalue_EffectSize

## _Motivation:_
A simple Python script reproducing the analysis by Joachim Goedhart in "_Make a difference: the alternative for p-values_"(https://thenode.biologists.com/quantification-of-differences-as-alternative-for-p-values/research/). Original data and a web-based application by Joachim Goedhart can be found here: https://zenodo.org/records/1421371, https://github.com/JoachimGoedhart/PlotsOfDifferences.

## _Description:_
The use of p-values is common in scientific publications to identify whether two conditions, such as control and treatment are statistically different. The main limitation of using p-values is the impossibility to evaluate the actual difference between the analyzed conditions. This is instead possible by determining the “effect size”, which is related to the difference between the groups. Please refer to “https://thenode.biologists.com/quantification-of-differences-as-alternative-for-p-values/research/“ for a thorough description of the problem and its solution.

## _Content:_
The repository contains _**EffectSize.py**_ which is a script that process the data contained within _**Area_in_um-GEFs.csv_** to produce the analysis of the effect size. Instructions about how to run the script with different datasets can be found in the initial lines of code in the script.
