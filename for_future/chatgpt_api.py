import os
import sys
from openai import OpenAI
import json

#cd validator , python3 validate_json_files.py
#python3 chatgpt_api.py article.txt >output.txt
OPENAI_API_KEY = ""
client = OpenAI(api_key=OPENAI_API_KEY)
def extract_main_points(article_text):

    # Prepare the prompt
    prompt = (
        "[base prompt] I will provide you a text and json file template. Read the article,"+
        "and then fill the relevant information into the json attribute in the provided json files." +
        "If the information is not there, leave the json attribute as it is (empty). " +
        "In case atleast one information was extracted, dont output anything but the json file." +
        "If it is not possible to extract any information, output only 'No information was extracted'." +
        "for context, the purpose is to extract information about startups and their funding." +
        "Make sure that the filled information is definitely correct - in case of doubt, dont fill it." +
        "IMPORTANT: Fill the information to the json attributes only in English language" +
        "[json template]: " +
        """
        [
            {
            "startup_name": "",
            "founded_date": "",
            "industry": [], 
            "founders": "",
            "funding_round": "",
            "amount_raised": "",
            "date_of_funding": "",
            "tags": "",
            "website": "",
            "country": "",
            "investors": [],
            }
        ] 
        """+
        "[the text]: " + article_text)

    # Call the OpenAI API
    response = client.chat.completions.create(model="gpt-4-turbo",
    messages=[
        {
            "role": "system",
            "content": "You are an assistant that extracts key information from news articles."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    max_tokens=4000,
    temperature=0)

    # Extract the assistant's reply
    assistant_reply = response.choices[0].message.content.strip()
    print(assistant_reply)
    print(len(article_text))
    # Try to parse the assistant's reply as JSON
    try:
        main_points = json.loads(assistant_reply)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse the assistant's reply as JSON. Error: {e}")

    return main_points

def main():
    # Read the article text from a file or standard input
    if len(sys.argv) > 1:
        # Read from file
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            article_text = f.read()
    else:
        # Read from standard input
        print("Please paste the news article text, followed by Ctrl+D (Unix) or Ctrl+Z (Windows):")
        article_text = sys.stdin.read()

    # Extract main points
    main_points = extract_main_points(article_text)

    # Write the output to a JSON file
    output_filename = "main_points.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(main_points, f, ensure_ascii=False, indent=2)

    print(f"Main points have been written to {output_filename}")

if __name__ == "__main__":
    main()
