import pandas as pd


profiles_data = pd.DataFrame(
            pd.read_csv('./data/profiles.csv'),
            columns=[
                'photo', 'cover_photo', 'about',
                'birth_date', 'country', 'public',
                'web_site', 'social_link'
            ]
        )

print(len(profiles_data.itertuples()))