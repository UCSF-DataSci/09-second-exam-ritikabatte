#!/bin/bash

# Generate dirty data (this step should create ms_data_dirty.csv)
python3 generate_dirty_data.py

# Debug: Check raw input file
echo "Raw input file (first 5 lines):"
head -n 5 ms_data_dirty.csv

# Step 1: Remove comment lines (lines starting with #) and empty lines
echo "After removing comments and empty lines (first 5 lines):"
grep -v '^#' ms_data_dirty.csv | sed '/^$/d' | head -n 5

# Step 2: Remove extra commas (if any)
echo "After removing extra commas (first 5 lines):"
grep -v '^#' ms_data_dirty.csv | sed '/^$/d' | sed 's/,,*/,/g' | head -n 5

# Step 3: Extract relevant columns (patient_id, visit_date, age, education_level, walking_speed)
echo "After extracting relevant columns (first 5 lines):"
grep -v '^#' ms_data_dirty.csv | sed '/^$/d' | sed 's/,,*/,/g' | cut -d',' -f1,2,4,5,6 | head -n 5

# Step 4: Filter walking speed values between 2.0 and 8.0
echo "After filtering walking speeds (first 5 lines):"
grep -v '^#' ms_data_dirty.csv | sed '/^$/d' | sed 's/,,*/,/g' | cut -d',' -f1,2,4,5,6 | awk -F',' 'NR==1 || ($5 >= 2.0 && $5 <= 8.0)' | head -n 5

# Final Output to ms_data.csv
grep -v '^#' ms_data_dirty.csv | sed '/^$/d' | sed 's/,,*/,/g' | cut -d',' -f1,2,4,5,6 | awk -F',' 'NR==1 || ($5 >= 2.0 && $5 <= 8.0)' > ms_data.csv

# Step 5: Create insurance.lst file
echo -e "insurance_type\nBasic\nPremium\nPlatinum" > insurance.lst

# Step 6: Display the total number of visits and the first few records
echo "Total visits:"
tail -n +2 ms_data.csv | wc -l
echo "First few records:"
head -n 5 ms_data.csv
