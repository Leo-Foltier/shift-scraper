
# Work Schedule and Tips scraper

## Description

My first ever attempt at shift scraping using python requests. This program was made to scrape my schedule and tips earned from each of my shifts at my previous job and add them to a mysql database. 

The program uses my company login  and webpage information to gather the nessecary cookies and info to access my shifts information and then process the information and update my database.



## Installation

- Install required packages using 'requirements.txt' in the program folder with:

    ```bash
    pip install -r requirements.txt
    ```

- Make sure to update 'config.yml' with required data. e.g. database login, correct website urls, etc

- Setup a MySql database (see https://dev.mysql.com/doc/mysql-getting-started/en/ if unsure) and create the following tables:

    - Schedule

        | week_beginning | day_ | sm_start | sm_end | w_start | w_end | holiday |
        |:---:|:---:|:---:||:---:|:---:|:---:|:---:|
        |##-##-##|'day'|##:##|##:##|##:##|##:##|true/false|

    - Hours

        | week_beginning | sm_hours | w_hours |
        |:---:|:---:|:---:|
        |##-##-##|##.##|##.##|

    - Tips

        | week_beginning | week_tips |
        |:---:|:---:|
        |##-##-##|##.##|

    *Note: Both Hours and Tips tables can be combined into one if desired.*


## Usage

After all steps of installation are complete simply run the main.py.
## Authors

- [Leo Foltier](https://github.com/Leo-Foltier)

