


lab2-2-eng.utah.edu
PartA :
 # python3 sentiment.py trainS.txt testS.txt words.txt 100
 # ./liblinear-1.93/train -q -s 0 -e 0.0001 trainS.txt.vector classifier
 # ./liblinear-1.93/predict testS.txt.vector classifier predictions.txt > accuracyS.txt

can also run: ./partA-grading.sh 
Make sure you have generated vectors for 100 words!

I have tested the accuracy for 50, 100, and 200. It matches the sample accuracy.
I have also checked diff for generated vector files. Test vectors don't have any issues. However, there are six differences for the generated train vector, and it is just a trailing single blank space(in sample output while I don't have trailing whitespace at the end of the line). I have attached a screenshot for your reference. 

So, part A works fine!
You can find below 4 files in partA_files folder
(a) trainS.txt.vector
(b) testS.txt.vector
(c) predictions.txt
(d) accuracy.txt

**************************************************************
Running partB:
*****IMP*** : Please clear all the output files before running. In the program if trainS/textS.txt.readable exists I will append it. If not I will create it. So, please don't forget to clear the output files!
# python3 entities.py trainE.txt testE.txt WORD
# ./liblinear-1.93/train -s 0 -e 0.0001 trainE.txt.vector EntityClassifier
 # ./liblinear-1.93/predict testE.txt.vector EntityClassifier predictions.txt>accuracy.txt

Go to folder PartB_files for :
a) trainE.txt.readable
(b) testE.txt.readable
(c) trainE.txt.vector
(d) testE.txt.vector
(e) predictions.txt
(f) accuracy.txt

entities.py runs pretty fast on my system. However, on the CADE it takes a bit longer. 

My output files might have an extra line at the end. I guess that's not going to be a problem. 
