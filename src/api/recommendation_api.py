import json
from BL.recommendation_service import recommend_contracts
from BL.document_duplication_check_service import WorkFlowExe
from core.helper.exception_dispatch_service import catch_exception
from config import Config
from core.models.contract_recommendation_model import ContractInputModel
from fastapi import APIRouter, Request, Response, HTTPException, Header, status as sc
from fastapi.security import HTTPBearer
from core.utils.authentication import Authentication

router = APIRouter()
auth_scheme = HTTPBearer()
auth = Authentication()

@router.post("/contract_recommendation")
async def item_recommendation(attributes: ContractInputModel,
                              request: Request,
                              ocp_apim_subscription_key: str = Header(None)):
    try:
        leo_base_url = auth.tcs.get_value("LeoAPIMExternalURL")

        req_json = json.dumps(attributes.dict())
        req_json = json.loads(req_json)

        item_name_txt = req_json["ItemName"]

        recommendation_dict = {"ItemName": item_name_txt}

        final_response = {}
        try:
            final_response = recommend_contracts(
                ocp_key=ocp_apim_subscription_key,
                leo_base_url=leo_base_url,
                payload=req_json,
                jwt_token= "Bearer " + request.state.auth.token,
            )

        except HTTPException as e:
            raise HTTPException(status_code=e.status_code,
                            detail=e.detail)
        except Exception as e:
            recommendation_dict["Recommendation"] = []

        recommendation_dict["Recommendation"] = final_response.get('Contracts') or []
        
        if req_json["ContractPayload"]:
            recommendation_dict['ContractPayload'] = final_response.get('ContractPayload')
            recommendation_dict['ContractPayloadCBR'] = final_response.get('ContractPayloadCBR')
            recommendation_dict['InvoiceESPayload'] = final_response.get('InvoiceESPayload')
        
        response = Response(content=json.dumps(recommendation_dict),
                            status_code=200, media_type="application/json")
        return response

    except AttributeError as e:
        raise HTTPException(
            status_code=sc.HTTP_417_EXPECTATION_FAILED,
            detail=str(e))

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(
            status_code=sc.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e))