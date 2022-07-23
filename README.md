# auto_Gmail_sending
this project send email automatically to your contact list

# How to use
- sending empty massage:
  python sendingGmail.py your-email@gmail.com ./contact.csv 
- sending simple massage:
  python sendingGmail.py your-email@gmail.com ./contact.csv  --body body.txt 
- sending html massage:
  python sendingGmail.py your-email@gmail.com ./contact.csv  --html html.html 
- sending one pdf file:
  python sendingGmail.py your-email@gmail.com ./contact.csv  --attachment document.pdf 

## for setting subject you have two option:
1- write subject in a txt file and use --> --subject_file sub.txt key

2- use --subject_txt key and write subject string directly

## add Custom data for contacts
1- adding columns with arbitrary names like 'data1' or 'name' and filling every row with related data
2- In the template file, you can use the word $column-name$ for the name of each column.
for example $data1$ or $name$

# You can use -h or --help keys also
