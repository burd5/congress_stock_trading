import requests
from settings import API_KEY
from backend.api.lib.db import add_congress_image, cursor, conn
import psycopg2
import pandas as pd


def get_bioguide_ids():
    csv_file_path = '/Users/austinburdette/Downloads/legislators-current.csv'  #
    df = pd.read_csv(csv_file_path)
    bioguideid_list = df['bioguide_id'].tolist()
    return bioguideid_list

# Function to loop through list of bioguideids and update the database
def update_image_urls(bioguideids):
    # Loop through each bioguideid in the list
    for bioguideid in bioguideids:
        # Construct the API URL for the current bioguideid
        api_member_string = f'https://api.congress.gov/v3/member/{bioguideid}?api_key={API_KEY}'

        # Make the API request
        response = requests.get(api_member_string)
        
        # Check if the response is successful
        if response.status_code == 200:
            # Parse the JSON data
            data = response.json()
            # Extract the first and last names from the dictionary
            first_name = data['member']['firstName']
            last_name = data['member']['lastName']
            
            # Combine first and last names to create the full name
            full_name = f'{first_name} {last_name}'
            
            # Extract the image URL from the dictionary
            try:
                image_url = data['member']['depiction']['imageUrl']
            except:
                print('No image')
            
            # Search for the full name in the PostgreSQL database
            # Note: Adjust the SQL query and table/column names as needed
            cursor.execute(
                'SELECT id FROM politicians WHERE name = %s',
                (full_name,)
            )
            
            # Fetch the result of the query
            result = cursor.fetchone()
            
            # If a match is found in the database
            if result:
                # Get the id of the matching record
                record_id = result[0]
                
                # Update the image_url column of the matching record
                cursor.execute(
                    'UPDATE politicians SET image_url = %s WHERE id = %s',
                    (image_url, record_id)
                )
                
                # Commit the changes
                conn.commit()
        
        # Handle any API request failure
        else:
            print(f'API request failed for bioguideid: {bioguideid}, status code: {response.status_code}')
    
    # Close the cursor and connection
    cursor.close()
    conn.close()


# Call the function to update image URLs in the database
bioguideids = get_bioguide_ids()
update_image_urls(bioguideids)
