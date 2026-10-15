from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

import openai



class Inquiry(BaseModel):
    Name: str
    Phone_Number:str
    Alternate_Phone_Number:str


app= FastAPI()

while True:
 try:
    conn= psycopg2.connect(host='localhost', database='Inquiries', user= 'postgres', password='mutbuwu021@ASA', cursor_factory=RealDictCursor)
    cursor=conn.cursor()
    print("Database Connection was successful!")
    break
 except Exception as error:
    print("Connecting to database failed")
    print('Error: ', error)
    time.sleep(2)


@app.get("/")
def read_root():
    return{'message':'ITSS RANEVOO YESS!!!'}


@app.get("/posts")
def get_inquiries():
    cursor.execute(""" SELECT * FROM "Lead_Master" """)
    inquiries=cursor.fetchall()
    conn.commit()
    return {"data": inquiries}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_inquiry(inquiry: Inquiry):
    cursor.execute("""INSERT INTO "Lead_Master" (Name,Phone_Number, Alternate_Phone_Number) VALUES(%s,%s,%s) RETURNING *""", inquiry.Name,inquiry.Phone_Number, inquiry.Alternate_Phone_Number)
    inquiries=cursor.fetchone()
    return {"data": inquiries}
    

@app.get("/posts/{id}")
def get_inquiry(id: int):
    cursor.execute("""SELECT * FROM "Lead_Master" WHERE id=%s""", (str(id)))
    inquiry=cursor.fetchone()
    if not inquiry:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"inquiry_detail": inquiry}
    

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def del_inquiry(id: int):
    cursor.execute("""DELETE FROM "Lead_Master" WHERE id=%s returning *""", str(id))
    deleted_inquiry=cursor.fetchone()
    conn.commit()

    if deleted_inquiry==None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
        

def get_completion(prompt, model=openai):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, 
    )
    return response.choices[0].message["content"]

get_completion("What is 1+1")

   