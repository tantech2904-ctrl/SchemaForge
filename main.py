from fastapi import FastAPI, Body
from routes import auth_routes
from db.executor import execute_query
from generator.table_generator import create_table
from generator.crud_generator import ( 
    get_all_rows,
    get_row_by_id,
    insert_row,
    update_row,
    delete_row
)
from db.metadata import get_all_tables
from routes import crud_routes

app = FastAPI(title="SchemaForge")
app.include_router(auth_routes.router)
app.include_router(crud_routes.router)


@app.get("/")
def root():
    return {"status": "Backend running"}

@app.get("/users")
def get_users():
    sql = "SELECT * FROM test_users"
    users = execute_query(sql, fetch=True)
    return {"data": users}

@app.post("/users")
def create_user(data: dict = Body(...)):
    sql = """
    INSERT INTO test_users (name, email)
    VALUES (%s, %s)
    """
    execute_query(sql, (data["name"], data["email"]))
    return {"message": "User created"} 

@app.post("/generate-table")
def generate_table(payload: dict = Body(...)):
    table_name = payload["table_name"]
    columns = payload["columns"]

    create_table(table_name, columns)

    return {"message": f"Table '{table_name}' created successfully"}

@app.get("/data/{table}")
def read_all(table: str):
    return {"data": get_all_rows(table)}

@app.get("/data/{table}/{row_id}")
def read_one(table: str, row_id: int):
    row = get_row_by_id(table, row_id)
    if not row:
        return {"error": "Not found"}
    return row

@app.post("/data/{table}")
def create_row(table: str, payload: dict = Body(...)):
    insert_row(table, payload)
    return {"message": "Row inserted"}

@app.put("/data/{table}/{row_id}")
def update(table: str, row_id: int, payload: dict = Body(...)):
    update_row(table, row_id, payload)
    return {"message": "Row updated"}

@app.delete("/data/{table}/{row_id}")
def delete(table: str, row_id: int):
    delete_row(table, row_id)
    return {"message": "Row deleted"}

@app.get("/tables")
def list_tables():
    return {"tables": get_all_tables()}

@app.get("/tables/{table}/columns")
def get_columns(table: str):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(f"SHOW COLUMNS FROM `{table}`")  
        rows = cursor.fetchall()
        if not rows:
            raise HTTPException(status_code=404, detail=f"No columns found for table {table}")
        columns = [{"column_name": row["Field"], "data_type": row["Type"]} for row in rows]
        return columns
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()