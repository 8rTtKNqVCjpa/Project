import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

chemin = r"C:\Users\hp\Desktop\Projects\projet\mock_data\csvjson.json"

def load_clean_data():
    if os.path.exists(chemin):
        with open(chemin, "r", encoding="UTF-8") as file:
            try:
                data = json.load(file)
                df = pd.DataFrame(data)
                print("Valeurs manquantes:")
                print(df.isnull().sum())
                df.fillna("inexistant", inplace=True)
                print("Valeurs manquantes après nettoyage :")
                print(df.isnull().sum())
                return df
            except json.JSONDecodeError:
                print('Error detected: Invalid JSON format')
                return None
            except IOError as e:
                print(f'Error detected: {e}')
                return None
    else:
        return None  # Returning None if file does not exist

def getorderbyid(order_id):
    df = load_clean_data()
    if isinstance(df, pd.DataFrame):
        order = df[df['ORDERNUMBER'] == order_id].to_dict(orient='records')
        if order:
            return order[0]
        else:
            return None
    return None

def getorderbystatus(order_status):
    df = load_clean_data()
    if isinstance(df, pd.DataFrame):
        orders = df[df['STATUS'] == order_status].to_dict(orient='records')
        if orders:
            return orders 
        else:
            return None
    return None

def datadescription():
    df = load_clean_data()
    if isinstance(df, pd.DataFrame):
        datadescr = df.describe()
        return datadescr
    return None

def datacorrelation():
    df = load_clean_data()
    if isinstance(df, pd.DataFrame):
        sns.pairplot(df)
        plt.title("Pairplot for data analysis")
        plt.savefig('pairplot.png')
        plt.close()
        return "Pairplot for data analysis created"
    else:
        return "Error: No data available for correlation analysis"
    
def dataheatmap():
    df=load_clean_data()
    if isinstance(df, pd.DataFrame):
        numeric_df = df.select_dtypes(include=[int, float])
        if(numeric_df.empty):
            return "No numeric data"
        sns.heatmap(numeric_df.corr(), annot=True)
        plt.title("The heatmap of the data")
        plt.savefig("heatmap.png")
        plt.close()
        return "Heatmap of the data"
    else:
        return "Error: No data available for heatmap visualization"
    
def priceofeachbymsrplmplot():
    df=load_clean_data()
    if isinstance(df, pd.DataFrame):
        sns.lmplot(x="MSRP", y="PRICEEACH", data=df, scatter_kws={'alpha':0.3})
        plt.title("The lmplot for the price of each by MSRP")
        plt.savefig("Thelmplot.png")
        plt.close()
        return "The lmplot"
    else:
        return "Error: No data available for the Lmplot visualization"
    
def salesbycountryvisualisation():
    df = load_clean_data()
    if isinstance(df, pd.DataFrame):
        plt.figure()
        df.groupby("COUNTRY")["SALES"].sum().plot(kind='bar')
        plt.xlabel("Country")
        plt.ylabel("Sales")
        plt.title("Sales by Country")
        plt.savefig('sales_country.png')
        plt.close()
        return "Sales by country visualization created"
    else:
        return "Error: No data available for country visualization"

def salesbyyearvisualisation():
    df = load_clean_data()
    if isinstance(df, pd.DataFrame):
        plt.figure()
        df.groupby("YEAR_ID")["SALES"].sum().plot(kind='line')
        plt.xlabel("Year")
        plt.ylabel("Sales")
        plt.title("Sales by Year")
        plt.savefig('sales_year.png')
        plt.close()
        return "Sales by year visualization created"
    else:
        return "Error: No data available for year visualization"

