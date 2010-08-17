#!/bin/bash
export PYTHONPATH='.'
for test in tests/*tests.py
do
	echo "running $test"
    python $test
done
