External libraries:

spacy.io: https://spacy.io/

NLTK: https://www.nltk.org/ 

Our program takes around 4 seconds to run input_file with one story

Our program takes around 3 minutes to run input_file with 74 stories

Contributions of team members: (2nd checkpoint)
Sushmita:


Paarth:
Mainly focussed on

Contributions of team members: (1st checkpoint)

Sushmita:
1. Processed Question files
2. Handled rules and answer extraction for: WHY, WHERE, HOW, WHAT type questions

Paarth:
1. Processed story files
2. Handled rules and answer extraction for: WHO, WHEN, WHOSE, WHOM type questions

Sushmita and Paarth:
Created the infra for applying rules to the sentences depending on the question

Github profile: https://github.com/paarthlakhani/Question_Answering_System
Paper reference: https://www.cs.utah.edu/~riloff/pdfs/quarc.pdf

Instructions to run the file:
1. Untar and go to the program folder
 	tar -xvf Question_Answering_System.tar.gz
	cd Question_Answering_System/scoring_program
2. Install dependent libraries: run below command
	./QA_package_installer.txt

3. To run QA system with inputfile
	./QA-script.txt

4. To collect above command output, pipe it to a new file
	./QA-script.txt > result.txt

5. To compare with the gold standard given in the assignement and to get Fscore.
	cat ../developset-v2/*.answers > ALL.txt
	perl score-answers.pl result.txt ALL.txt
