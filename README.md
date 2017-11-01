<img src="http://2017.igem.org/wiki/images/a/ac/T--EPFL--ToeholdDesigner_V2.svg"/>

This tool allows people to easily generate toehold switches and targets for a unique virus sequence. It represents a pipeline that puts together techniques for generating this types of switches<sup>[1](#1), [2](#2)</sup> and processing algorithms<sup>[3](#3), [4](#4), [5](#5)</sup>. 

It strictly follows the Series A and B designs of the Zika virus<sup>[2](#2)</sup>, generalized for any unique RNA virus sequence. 

Thanks to the NUPACK Design <sup>[3](#3)</sup> and Analysis<sup>[4](#4)</sup> algorithms this tool analyses the  optimality of the structure of the generated sequences. Evaluates the target's availability for binding with the toehold (1), the toehold's availiability for binding with the target (2) and the sensor's complex defect (3). 

By summing up (1), (2) and (3), and assigning to each of them a different weight <sup>[1](#1)</sup> we can order the generated sequences by score from lowest up to the highest score where the sequences with lowest score have better structures than the ones with highest scores. 

It also makes use of the NUPACK Web application<sup>[3](#3)</sup> in order to generate images of the optimal secondary structure of the generated sequence. 

We can then choose the first few Series A or B toeholds and test them in the lab. 

<b>Toehold designer</b> was tested on succesfully generating a toehold switch for a hepatitis C sequence. The results can be seen [here](http://2017.igem.org/Team:EPFL/Results/Toehold#software). 


# Instalation in only 5 steps

1. Install NUPACK from [here](http://nupack.org/downloads)
2. Install Python from [here](https://www.python.org/downloads/release/python-360/)
3. Open the command line and run the following commands: 
```
python get-pip.py
pip install beautifulsoup4 Flask
```
4. Download and unzip this project
5. Place you in the root of this repository and write in the command line
```
python toehold-designer.py
```
That's it. You have the toehold designer running in your browser now! 

# How to use it? 
Take a look of [this demo](http://2017.igem.org/wiki/images/0/0d/T--EPFL--software-demo.gif)

# References 

<a name="1">[1] Green, Alexander A., et al. "Toehold switches: de-novo-designed regulators of gene expression." Cell 159.4 (2014): 925-939.</a>

<a name="2">[2] Pardee, Keith, et al. "Rapid, low-cost detection of Zika virus using programmable biomolecular components." Cell 165.5 (2016): 1255-1266.</a>

<a name="3">[3] NUPACK Web Application </a>
* J. N. Zadeh, C. D. Steenberg, J. S. Bois, B. R. Wolfe, M. B. Pierce, A. R. Khan, R. M. Dirks, N. A. Pierce. NUPACK: analysis and design of nucleic acid systems. J Comput Chem, 32:170–173, 2011. (pdf)

<a name="4">[4] NUPACK Analysis Algorithms </a>
* R. M. Dirks, J. S. Bois, J. M. Schaeffer, E. Winfree, and N. A. Pierce. Thermodynamic analysis of interacting nucleic acid strands. SIAM Rev, 49:65-88, 2007. (pdf)
* R. M. Dirks and N. A. Pierce. An algorithm for computing nucleic acid base-pairing probabilities including pseudoknots. J Comput Chem, 25:1295-1304, 2004. (pdf)
* R. M. Dirks and N. A. Pierce. A partition function algorithm for nucleic acid secondary structure including pseudoknots. J Comput Chem, 24:1664-1677, 2003. (pdf, supp info)

<a name="5">[5] NUPACK Design Algorithms</a>

* B. R. Wolfe, N. J. Porubsky, J. N. Zadeh, R. M. Dirks, and N. A. Pierce. Constrained multistate sequence design for nucleic acid reaction pathway engineering. J Am Chem Soc, 139:3134-3144, 2017. (pdf, supp info)
* B. R. Wolfe and N. A. Pierce. Sequence design for a test tube of interacting nucleic acid strands. ACS Synth Biol, 4:1086-1100, 2015. (pdf, supp info, supp tests)
* J. N. Zadeh, B. R. Wolfe, and N. A. Pierce. Nucleic acid sequence design via efficient ensemble defect optimization. J Comput Chem, 32:439–452, 2011. (pdf, supp info, supp tests)
* R. M. Dirks, M. Lin, E. Winfree, and N. A. Pierce. Paradigms for computational nucleic acid design. Nucl Acids Res, 32:1392-1403, 2004. (pdf, supp info, supp seqs)

