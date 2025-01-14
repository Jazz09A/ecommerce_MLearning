# import pandas as pd
# from db.base import SessionLocal
# from app.models.interaction import Interaction


# def load_interaction_data():
#     db = SessionLocal()
#     try:
#         interactions = db.query(Interaction).all()
#     finally:
#         db.close()

#     # Convertir las interacciones a un DataFrame
#     data = pd.DataFrame([{
#         "user_id": i.user_id,
#         "product_id": i.product_id,
#         "rating": i.rating or 0  # Si no hay calificación, usar 0
#     } for i in interactions])
#     return data

# data = load_interaction_data()
# print(data)
