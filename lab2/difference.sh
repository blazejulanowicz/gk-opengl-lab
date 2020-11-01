#/usr/bin/bash

START=$(date +%s.%N)
python3 mandelbrot.py --TEST
END=$(date +%s.%N)
DIFF1=$(echo "$END - $START" | bc)

START=$(date +%s.%N)
python3 np_mandelbrot.py --TEST
END=$(date +%s.%N)
DIFF2=$(echo "$END - $START" | bc)

echo "normal: $DIFF1, numpy: $DIFF2"