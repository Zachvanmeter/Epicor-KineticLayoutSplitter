# Epicor-KineticLayoutSplitter
This is python script utility which cuts one Epicor Homepage Layout into importable 'Sub-Tabs'. This allows for the maintance of one "All Role" Homepage Layout, where an admin makes changes to it, and can easily export it into role specific layouts.


# The Workflow

1. Export your layout, and save it in the same directory as the script.
2. Open the script, and edit both the PathToLayout variable and the AlwaysIncludedList variable.
     a. If you dont know what GroupIDs you'll need to take a peek into , just run the file and read the output, it will show you the GroupIDs like so
     > LayoutTab Title: your_layout_tab_title GroupID: ##
3. to run the script, ensure python and BeautifulSoup is installed.
     a. Get python [here](https://www.python.org/downloads/)
     b. Then install bs4 using this command
     > pip install beautifulsoup4
4. Import your files into Epicor
5. <img width="562" height="264" alt="95d84a21c30d263b313436ee440db84cb27be49f" src="https://github.com/user-attachments/assets/3f6cc33c-860d-4eb4-b422-00962facf82c" />
