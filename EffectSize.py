import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
from sklearn.utils import resample


'''Python version of the analysis from "Make a difference: the alternative for p-values (
https://thenode.biologists.com/quantification-of-differences-as-alternative-for-p-values/research/)".
The script takes a dataframe containing observations of a feature measured among different samples (1 column
for each sample). Then, the values of each sample are bootstrapped and medians are calculated for each
bootstrapped sample. The difference between each set of medians is taken as a more meaningful estimate for the
effect size of the feature under investigation.'''

# The example is based on 3 samples, one is the control (no-treatment) sample and the other two represents two
# "muted" versions. To have a better graphical comparison, save the values of the control sample in a column that
# is in the middle of the other columns of the .csv file.

# --- Indicate here the index of the column containing the ctrl/wt sample
ctrl_index = 1
# Path to the .csv file
path = "Area_in_um-GEFs.csv"
df_raw = pd.read_csv(path, sep=',')
header = df_raw.columns
# Name the feature under investigation
feature = 'Area_um2'
df = pd.DataFrame()
for i in range(len(header)):
    local_df = pd.DataFrame({feature: df_raw[str(header[i])],
                       'label': str(header[i])})
    df = pd.concat([df, local_df], axis=0).dropna().reset_index(drop=True)

# Calculating p-values
for i in range(len(header)):
    if i == ctrl_index:
        continue
    # ith sample vs ctrl
    si_ctrl_pvalue = ttest_ind(df[df["label"] == str(header[i])][str(feature)].dropna().to_numpy(),
                               df[df["label"] == str(header[ctrl_index])][str(feature)].dropna().to_numpy(),
                               equal_var=False)[1]
    print("p-value for " + header[i] + " and " + header[ctrl_index] + ": ", si_ctrl_pvalue)

# Plotting
if len(header) > 3:
    palette = "viridis"
else:
    palette = ['red', 'forestgreen', 'dodgerblue']
# fig, ax = plt.subplots()
# sns.swarmplot(data=df, y="label", x=feature, hue="label", ax=ax, dodge=False, palette=palette)
# plt.show()

# Building a single Dataframe for the bootstrap medians
median_feature = "Medians_" + feature
diff_feature = "Difference_" + feature
median_df = pd.DataFrame()
median_diff_df = pd.DataFrame()
for i in range(len(header)):
    s = df[df["label"] == str(header[i])][str(feature)]
    local_df = pd.DataFrame({median_feature: [np.median(resample(s.values, replace=True)) for i in range(0, 1000)],
                       'label': str(header[i])})
    median_df = pd.concat([median_df, local_df], axis=0).reset_index(drop=True)
# Calculating the differences of the bootstrap medians
for i in range(len(header)):
    print(str(header[i]))
    diff_df = pd.DataFrame({diff_feature: median_df[median_df["label"] == str(header[i])][str(median_feature)].values -
                                          median_df[median_df["label"] == str(header[ctrl_index])][str(median_feature)].values,
                            "label": str(header[i])})
    median_diff_df = pd.concat([median_diff_df, diff_df], axis=0).dropna().reset_index(drop=True)
# Plotting
# fig, ax = plt.subplots()
# sns.violinplot(data=median_df, y="label", x=median_feature, hue="label", ax=ax, dodge=False, s=5, palette=palette)
# plt.show()

# Plotting differences
fig = plt.figure(figsize=(10, 5))
ax = fig.subplots(1, 2)
sns.stripplot(data=median_df, y="label", x=median_feature, hue="label", ax=ax[0], dodge=False, s=5, alpha=.3, palette=palette)
sns.violinplot(data=median_diff_df, y="label", x=diff_feature, ax=ax[1],
               alpha=.3, dodge=False, palette=palette, inner=None, linewidth=0, hue="label")
ax[1].vlines(x=0, ymin=0, ymax=len(header) -1, color='grey', linewidth=.5)
ax[1].scatter(0, ctrl_index, marker='o', color="grey", facecolor='forestgreen')
# Plotting 95% confidence intervals
ci_legend = ["95% C.I."]
for i in range(len(header)):
    ci_legend.append('')
    ax[1].hlines(y=i, linewidth=2.5, color='k', alpha=.7,
                 xmin=median_diff_df[median_diff_df["label"]==str(header[i])][diff_feature].quantile(0.025),
                 xmax=median_diff_df[median_diff_df["label"]==str(header[i])][diff_feature].quantile(0.975),
                 label=ci_legend[i])
ax[1].legend()
plt.tight_layout()
plt.show()

