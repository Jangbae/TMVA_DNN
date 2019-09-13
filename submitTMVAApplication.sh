#!/bin/bash

echo 'NOMINAL'
python -u doCondorApplication.py nominal
 
sleep 5

# echo "JECUP"
# python -u doCondorApplication.py JECup
# 
# sleep 5
# 
# echo "JECDOWN"
# python -u doCondorApplication.py JECdown
# 
# sleep 5
# 
# echo "JERUP"
# python -u doCondorApplication.py JERup
# 
# sleep 5
# 
# echo "JERDOWN"
# python -u doCondorApplication.py JERdown

echo "DONE"
