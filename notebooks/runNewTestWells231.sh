#!/bin/bash

# Define an array of test wells
test_wells=('B8' 'B9' 'B10' 'B11' 'C7' 'C8' 'C9' 'C10' 'C11' 
            'D7' 'D8' 'D9' 'D10' 'D11' 'E7' 'E8' 'E9' 'E10' 'E11')

# Loop through each test well and run the command
for well in "${test_wells[@]}"; do
    python predict231Co.py --nIncrease 25 --testWell "$well"
done