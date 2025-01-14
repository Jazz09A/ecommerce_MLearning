# from fastapi import APIRouter, Depends, HTTPException
# from app.ml.data_loader import load_interaction_data
# from app.ml.recommendation_engine import recommend_for_user

# router = APIRouter()

# @router.get("/recommendations/{user_id}")
# async def get_recommendations(user_id: int):
#     try:
#         data = load_interaction_data()
#         recommendations = recommend_for_user(user_id, data)

#         if not recommendations:
#             raise HTTPException(status_code=404, detail="No recommendations found.")
        
#         return {"user_id": user_id, "recommendations": recommendations}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
