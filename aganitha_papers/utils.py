
from typing import List, Dict 
import pandas as pd
def save_to_csv(data: List[Dict], filename: str): 
    df = pd.DataFrame(data) 
    df.to_csv(filename, index=False)