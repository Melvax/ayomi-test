from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from fastapi_sqlalchemy import DBSessionMiddleware, db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import csv
from fastapi.responses import FileResponse

app = FastAPI()

origins = ["*"]  # Allow all origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


### SQLAlchemy ###
app.add_middleware(DBSessionMiddleware, db_url="sqlite:///./test.db")
engine = create_engine("sqlite:///./test.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#Schema for the database
class Operation(Base):
    __tablename__ = "operations"
    id = Column(Integer, primary_key=True, index=True)
    expression = Column(String)
    result = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)
class OperationIn(BaseModel):
    expression: str

def evaluate_npi(expression: str):
    stack = []
    for token in expression.split():
        if token in ["+", "-", "*", "/"]:
            operand2 = stack.pop()
            operand1 = stack.pop()
            if token == "+":
                result = operand1 + operand2
            elif token == "-":
                result = operand1 - operand2
            elif token == "*":
                result = operand1 * operand2
            elif token == "/":
                result = operand1 / operand2
            stack.append(result)
        else:
            stack.append(float(token))
    return stack.pop()

@app.post("/calculate")
def calculate(operation: OperationIn):
    """
    This function handles POST requests at the "/calculate" endpoint.
    It takes an OperationIn object as input, which contains an expression in Reverse Polish Notation.
    The function evaluates the expression using the evaluate_npi function.
    It then creates a new Operation object with the expression and its result, and adds it to the database.
    Finally, it returns a JSON response with the result of the operation.
    """
    result = evaluate_npi(operation.expression)
    db_operation = Operation(expression=operation.expression, result=result)
    db.session.add(db_operation)
    db.session.commit()
    return {"result": result}


@app.get("/operations/csv")
def operations_csv():
    """
    This function handles GET requests at the "/operations/csv" endpoint.
    It writes all operations stored in the database to a CSV file named "operations.csv".
    Each operation is represented by a row in the CSV file, with columns for "id", "expression", "result", and "timestamp".
    After writing to the CSV file, it returns a FileResponse with the CSV file.
    """
    with open("operations.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "expression", "result", "timestamp"])
        operations = db.session.query(Operation).all()  
        for operation in operations:
            writer.writerow([operation.id, operation.expression, operation.result, operation.timestamp])
    return FileResponse("operations.csv", media_type="text/csv")
