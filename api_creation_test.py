from fastapi import FastAPI
import requests 
from fastapi.responses import JSONResponse
import pandas as pd
from io import BytesIO
from fastapi.responses import StreamingResponse


app = FastAPI()

dataset_data = {
    "Name": ["Production végétale 2010-2022", "Cartographie des musées au Maroc", "Liste des établissements scolaires publics"],
    "Topic": ["Agriculture", "Cartographie", "Education"],
    "Link": ["https://data.gov.ma/data/fr/dataset/fb340a2e-7a78-4880-a7ff-d3eab72a4a60/resource/8c15d785-b1e6-4f11-acf9-958d34877529/download/20230714-production-vegetale-2010-2022.xlsx", 
    "https://data.gov.ma/data/fr/dataset/c4ec598a-a30d-496e-8252-4d3297395f77/resource/2a38c716-5217-46f8-b648-c26e6692149c/download/cartographie-des-musees-fnm-2022-1.docx", 
    "https://data.gov.ma/data/fr/dataset/a1704cc3-5fcb-481f-bde1-79ad2349c0f7/resource/34a1382d-ebaf-44a5-989f-86c58800a811/download/liste-des-etablissements-publics-avril-2011-men-f.xls"]
}

df = pd.DataFrame(dataset_data)

@app.get("/get-datasets-info")
def dwnld_datasets_info():
    return JSONResponse(content=df.to_dict(orient="records"))

@app.get("/get_dataset")
def get_dataset(name=None):
    # TODO: filter the dataset with more criteria
    topic_df = df[df.Name == name]
    excel_output = BytesIO()
    with pd.ExcelWriter(excel_output, engine='xlsxwriter') as writer:
            for row in topic_df.iterrows():
                if row["Link"].split(".")[-1] in ["docx"]:
                    continue
                else:
                    response = requests.get(row["Link"])
                    response.raise_for_status()
                    dataset_content = BytesIO(response.content)
                    if row["Link"].split(".")[-1] == 'csv':
                        df_topic = pd.read_csv(dataset_content, encoding='latin1')
                    if row["Link"].split(".")[-1] == 'xlsx':
                        df_topic = pd.read_excel(dataset_content)
                    df_topic.to_excel(writer, sheet_name=row["Name"], index=False)
    excel_output.seek(0)

    return StreamingResponse(excel_output, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": f"attachment;filename={name}_datasets.xlsx"})




