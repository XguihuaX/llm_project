import pandas as pd


class data:
    def __init__(self):
        pass

    def load_data(self, url):
        try:
            df = pd.read_csv(url)
            return df
        except Exception as e:
            print(f"load data failed:{e}")
            return None

    def clean_data(self,df):
        df = df.replace('\n','').replace('\r',' ')
        #df =''.join(df.split())
        return df.lower()

    def clean_data2(self,df):
        for column in ['description','transcription']:
            df[column] = df[column].astype(str).apply(self.clean_data)
        return df

    def save_data(self,clean_df,url,):
        new_file_name = 'mtsamples_cleaned.csv'
        new_file_path = url.rsplit('\\', 1)[0] + '\\' + new_file_name
        clean_df.to_csv(new_file_path, index=False)

    def create_save(self):
        file_path = r'C:\Users\Administrator\Desktop\st\mtsamples.csv'
        text = self.load_data(file_path)
        clean_text = self.clean_data2(text)
        #self.save_data(clean_text, file_path)
        return clean_text

