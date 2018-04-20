# Project : Call Data Record (CDR) analysis
### Architecture
![data type](https://github.com/myonlinecode1988/insight-project-arnab/blob/master/cdr_flow.jpg)

### Why we need streaming ?
"Telcos perform forensics on dropped calls and poor sound quality, but call detail records flow in at a rate of millions per second"- HortonWorks (provides CDR analytics for Verizon)

##### Dataset
Artificial dataset:
https://github.com/mayconbordin/cdr-gen

##### Dashboard
- Geographical heat-map (simulate earthquake) [streaming job]
- Time vs usage [daily batch job]
- Power user detection [batch job]

# Project : StackOverflow Analytics
### Architecture
![data type](https://github.com/myonlinecode1988/insight-project-arnab/blob/master/stackoverflow_flow.jpg)

##### Dataset
https://archive.org/download/stackexchange

##### Dashboard
- Critical Number of users for technology [batch jobs]
- Trends on technology
- Will your post get answered? [Yes/No classification]
- Autocomplete post
