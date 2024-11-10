Jak spustit:

python3 App.py 
spustí se aplikace pro scrapovaní dat, která vezme z newsapi články,
udělá json file scraped_data.json, a zapíše zdroj článku a url článku do airtable

python3 remove_all_data.py 
odstraní se všechny řádky z airtable

další práce:
cd for_future
python3 json_to_airtable.py
spustí se aplikace která vloží do airtable informace z json filu ve složce json_files. V případě, že u některého json elementu je zaznamenáno, že už v airtable je, tak se změní pouze informace (nevytváří se nový řádek). Data musí být validní,
pro kontrolu:

cd validator

python3 validate_json_files.py

pokud jsou data smazána, je třeba změnit v json files record_id, jinak nepůjdou vložit do airtable
python3 

získávání informací by se dalo dělat přes chatgpt api. První verze je v chatgpt_apy.py. Spouští se:
python3 chatgpt_api.py article.txt > output.txt
Chatgpt si přečte článek article.txt a vytvoří json fily v output.txt. Dále propojené s aplikací projektu to není.
Je třeba mít chatgpt API klíč.
