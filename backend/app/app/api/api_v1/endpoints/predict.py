import csv
import os
from io import StringIO

import pandas
from datetime import date
from tempfile import NamedTemporaryFile
from typing import Any

from fastapi import APIRouter, Depends, UploadFile
from fastapi.params import File
from sqlalchemy.orm import Session

from starlette.responses import StreamingResponse, Response

from app import crud, schemas
from app.api import deps
from collections import ChainMap

from app.service.prediction_service import filter_b_company

from app.service.prediction_service import rl_agent

router = APIRouter()


@router.post("/", response_model=schemas.Predict)
def predict_offer(
        *,
        predict_in: schemas.PredictCreate,
) -> Any:
    """
    Create new prediction.
    """
    response = {'best_offers': dict(ChainMap(*rl_agent(predict_in.states, predict_in.offers))),
                'customer_id': predict_in.customer_id,
                'response_date': str(date.today())}
    return response


@router.post("/batch", responses={
    200: {
        "content": {"text/csv": {}}
    },
},
             response_class=Response)
async def batch(file: UploadFile = File(...)):
    """
    batch upload for company B csv which will process and return csv file
    """
    contents = await file.read()
    data = []
    file_copy = NamedTemporaryFile(delete=False)
    try:
        with file_copy as f:  # The 'with' block ensures that the file closes and data are stored
            f.write(contents)
        with open(file_copy.name, 'r') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                data.append(row)
        output_data = filter_b_company(data)
        df = pandas.DataFrame(output_data)
        response = StreamingResponse(StringIO(df.to_csv(index=False, sep=";")), media_type="text/csv")
        return response
    finally:
        file_copy.close()  # Remember to close any file instances before removing the temp file
        os.unlink(file_copy.name)  # delete the file


@router.post("/v2", response_model=schemas.Predict)
def predict_products(
        *,
        predict_in: schemas.PredictCreate,
        db: Session = Depends(deps.get_db)
) -> Any:
    """
    v2 version of predictions which will give the product names if available
    """
    offers_predict = rl_agent(predict_in.states, predict_in.offers)
    new_predict = []
    for offer_predict in offers_predict:
        for k, v in offer_predict.items():
            product_from_db = crud.product.get_by_key(db=db, column_name="offer_id",
                                                      value=k.replace('OFFER_', 'OFFERS_'))
            if product_from_db:
                new_predict.append({k: product_from_db.product_name})
            else:
                new_predict.append(offer_predict)
    response = {'best_offers': dict(ChainMap(*new_predict)),
                'customer_id': predict_in.customer_id,
                'response_date': str(date.today())}
    return response
