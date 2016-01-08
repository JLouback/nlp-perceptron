#!/bin/sh
python question4.py
echo "Question 4 results:"
python eval_tagger.py tag_dev.key q4_output
python question5.py
echo "Question 5 results:"
python eval_tagger.py tag_dev.key q5_output
python question6.py
echo "Question 6 results:"
python eval_tagger.py tag_dev.key q6_output_combo1
python eval_tagger.py tag_dev.key q6_output_combo2
python eval_tagger.py tag_dev.key q6_output_combo3
python eval_tagger.py tag_dev.key q6_output_combo4