

NIST will run ROUGE-1.5.5 to compute ROUGE-2 and ROUGE-SU4, with stemming and keeping stopwords. Jackknifing will be implemented so that human and system scores can be compared. ROUGE-1.5.5 will be run with the following parameters:

ROUGE-1.5.5.pl -n 2 -x -m -2 4 -u -c 95 -r 1000 -f A -p 0.5 -t 0 -d

    -n 2 	compute ROUGE-1 and ROUGE-2
    -x 	do not calculate ROUGE-L
    -m 	apply Porter stemmer on both models and peers
    -2 4 	compute Skip Bigram (ROUGE-S) with a maximum skip distance of 4
    -u 	include unigram in Skip Bigram (ROUGE-S)
    -c 95 	use 95% confidence interval
    -r 1000 	bootstrap resample 1000 times to estimate the 95% confidence interval
    -f A 	scores are averaged over multiple models
    -p 0.5 	compute F-measure with alpha = 0.5
    -t 0 	use model unit as the counting unit
    -d 	print per-evaluation scores

NIST will calculate overlap in Basic Elements (BE) between automatic and manual summaries. Summaries will be parsed with Minipar, and BE-F will be extracted. These BEs will be matched using the Head-Modifier criterion.

    ROUGE-1.5.5.pl -3 HM -d 

Groups may participate in an optional manual evaluation of summary content using the pyramid method, which will be carried out cooperatively by DUC participants. 
