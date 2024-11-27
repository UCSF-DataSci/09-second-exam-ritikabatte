import numpy as np
import pandas as pd

# Load the data
data = pd.read_csv('/Users/ritikabatte02/09-second-exam-ritikabatte/ms_data.csv')

# drop rows with missing values
data = data.dropna()

# convert the date column to datetime
data['visit_date'] = pd.to_datetime(data['visit_date'])

# sort data by patient_id and visit_date
data = data.sort_values(by=['patient_id', 'visit_date'])

# read in insurance types from isnurance.list
with open('insurance.lst', 'r') as f:
    insurance_types = f.read().splitlines()[1:]

# radonmly assign insurance types to patients
np.random.seed(0)
data['insurance'] = np.random.choice(insurance_types, size=len(data))

# define cost per visit for each insurance type
insurance_costs = {
    'Basic': 80,
    'Premium': 130,
    'Platinum': 210
}

# add some random variation to the costs
np.random.seed(0)
data['cost'] = data['insurance'].map(insurance_costs) + np.random.normal(0, 10, len(data))

# mean walking speed for education level
mean_walkingspeed = data.groupby('education_level')['walking_speed'].mean()

# mean costs by insurance type
mean_costs = data.groupby('insurance')['cost'].mean()

# age effects on walking speed (Correlation between age and walking speed)
age_corr = data[['age', 'walking_speed']].corr().iloc[0, 1]

# print summary stats
print('Mean walking speed by education level:')
print(mean_walkingspeed)
print('\nMean costs by insurance type:')
print(mean_costs)
print('\nCorrelation between age and walking speed:', age_corr)
