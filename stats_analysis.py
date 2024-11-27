import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats

data = pd.read_csv('/Users/ritikabatte02/09-second-exam-ritikabatte/ms_data.csv')   

# Analyze walking speed: Multiple regression with education and age, Account for repeated measures, Test for significant trend
# Fit a linear mixed-effects model
model = smf.mixedlm("walking_speed ~ education_level + age", data, groups=data['patient_id'])
result = model.fit()
print(result.summary())

# Test for a significant trend in walking speed with age
trend = smf.ols("walking_speed ~ age", data).fit()
print(trend.summary())

# Test for a significant difference in walking speed between education levels
anova = smf.ols("walking_speed ~ education_level", data).fit()
print(anova.summary())

# Test for a significant difference in walking speed between education levels, accounting for age
anova = smf.ols("walking_speed ~ education_level + age", data).fit()
print(anova.summary())

# Analyze costs: Simple analysis of insurance type effect, Box plots and basic statistics, Calculate effect sizes

# define cost per visit for each insurance type
insurance_costs = {
    'Basic': 80,
    'Premium': 130,
    'Platinum': 210
}

file_path = "/Users/ritikabatte02/09-second-exam-ritikabatte/insurance.lst"  
insurance_data = pd.read_csv(file_path, sep="\t") 

insurance_data['insurance_cost'] = insurance_data['insurance_type'].map(insurance_costs)

# statistics for each insurance type
basic_stats = insurance_data.groupby('insurance_type')['insurance_cost'].agg(
    mean_cost=np.mean,
    median_cost=np.median,
    std_dev=np.std,
    count='count'
).reset_index()

print("Basic Statistics by Insurance Type:")
print(basic_stats)

# ANOVA to test the effect of insurance type on costs
anova = smf.ols("insurance_cost ~ insurance_type", insurance_data).fit()
print(anova.summary())

# Visualize the distribution of costs by insurance type
plt.figure(figsize=(8, 6))
sns.boxplot(x='insurance_type', y='insurance_cost', data=insurance_data)
plt.xlabel('Insurance Type')
plt.ylabel('Cost per Visit')
plt.title('Distribution of Costs by Insurance Type')
plt.show()

# Advanced analysis: Education age interaction effects on walking speed, Control for relevant confounders, Report key statistics and p-values
# Fit a linear regression model with interaction term
model = smf.ols("walking_speed ~ education_level * age", data).fit()
print(model.summary())

# Test for a significant interaction effect
interaction = smf.ols("walking_speed ~ education_level * age", data).fit()
print(interaction.summary())
