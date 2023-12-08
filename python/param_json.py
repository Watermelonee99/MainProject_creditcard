import sys
import mysql.connector
import pandas as pd
import numpy as np
import json
sys.stdout.reconfigure(encoding='utf-8')

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'credit',
    'charset': 'utf8',
}

connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# 문자 인코딩 설정
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')

# 첫 번째 쿼리 실행
sql_query = "SELECT * FROM card_info"
cursor.execute(sql_query)
result_card_info = cursor.fetchall()

# 두 번째 쿼리 실행
sql_query2 = "SELECT * FROM transaction ORDER BY idx DESC LIMIT 1"
cursor.execute(sql_query2)
result_transaction = cursor.fetchall()

# 데이터프레임 생성
df_card_info = pd.DataFrame(result_card_info)
df_transaction = pd.DataFrame(result_transaction)

# print("Card Info:")
# print(df_card_info.head())
# print(df_card_info.info())

# print("\nTransaction:")
# print(df_transaction.head())
# print(df_transaction.info())



###################################################################
# 예시 사용

# card=df_card_info[df_card_info[2] <= df_transaction[22].min()]
# col=[4,19,21,25,27,29,30,31]
# card=card.drop(columns=col)
# # print(df_transaction)
# user = df_transaction.drop([0,1], axis=1)
# user = np.where(user * 0.05 >= 1, 1, user * 0.05)
# # print(user.shape)

# class CreditCardRecommendation:
#     def __init__(self, card_data):
#         self.card_data = card_data
#         self.benefit_matrix = np.array(self.card_data.drop([0, 1, 2, 3], axis=1).values, dtype=np.float64).T

#     def recommend_credit_cards(self, user_spending_totals, num_recommendations=10):
#         user_vector = np.array(user_spending_totals)

#         # 각 카드에 대한 혜택 점수 계산 (카드 혜택이 1인 경우에만 점수 부여)
#         benefit_scores = np.dot(user_vector, self.benefit_matrix)

#         # 가장 높은 점수를 가진 카드들 추천
#         recommended_cards_indices = np.argsort(benefit_scores)[::-1]
#         recommended_cards = list(self.card_data.iloc[recommended_cards_indices]['1'])

#         return recommended_cards[:num_recommendations]

# card_data=card
# user_spending_totals = np.array(user[:, :-1]).flatten()  # 'total' 제외
# # ranks=[31, 1, 2,3]
# # card_rank = df_card_info[ranks]

# recommendation_system = CreditCardRecommendation(card_data)
# recommended_cards = recommendation_system.recommend_credit_cards(user_spending_totals, num_recommendations=30)
# # print(recommended_cards)


# class FinalCreditCardSelection:
#     def __init__(self, recommended_cards, card_rank):
#         self.recommended_cards = recommended_cards
#         self.card_rank = card_rank

#     def final_selection(self, annual_fees_weight, previous_month_weight, card_company_weight):
#         final_recommendations = []

#         # 기존의 recommended_cards를 이용하여 해당 카드에 대한 점수 계산
#         scores = []
#         for card in self.recommended_cards:
#             card_info = self.card_rank[self.card_rank['1'] == card]

#             # 연회비, 전월실적, 카드사에 대한 가중치를 고려한 점수 계산
#             score = -card_info['2'].values[0] * previous_month_weight
#             score -= card_info['3'].values[0] * annual_fees_weight
#             score += card_info['31'].values[0] * card_company_weight
#             scores.append(score)

#         # 점수 내림차순으로 정렬하여 순위 계산
#         ranked_indices = np.argsort(scores)[::-1]

#         # 각 순위에 해당하는 카드를 final_recommendations에 추가
#         for rank, index in enumerate(ranked_indices):
#             final_recommendations.append({
#                 'Rank': rank + 1,
#                 'CreditCard': self.recommended_cards[index],
#                 'Score': scores[index]
#             })

#         return final_recommendations

# # 예시 사용
# final_selection_system = FinalCreditCardSelection(recommended_cards, card_rank)
# final_recommendations = final_selection_system.final_selection(annual_fees_weight=1, previous_month_weight=1, card_company_weight=0.001)

# # 출력 예시
# for recommendation in final_recommendations:
#     print(f"Rank {recommendation['Rank']}: {recommendation['CreditCard']} (Score: {recommendation['Score']})")

# print("Card Info:")
# print(df_card_info.head())
# print(df_card_info.info())

# print("\nTransaction:")
# print(df_transaction.head())
# print(df_transaction.info())

card = df_card_info[df_card_info[2] <= df_transaction[22].min()]

card_data = card.drop([4,19,21,25,27,29,30,31], axis=1)
# print(card_data)

user = df_transaction.drop([0,1], axis=1)
user = np.where(user * 0.05 >= 1, 1, user * 0.05)
# print(user.shape)

class CreditCardRecommendation:
    def __init__(self, card_data):
        self.card_data = card_data
        self.benefit_matrix = np.array(self.card_data.drop([0, 1, 2, 3], axis=1).values, dtype=np.float64).T

    def recommend_credit_cards(self, user_spending_totals, num_recommendations=10):
        user_vector = np.array(user_spending_totals)

        # 각 카드에 대한 혜택 점수 계산 (카드 혜택이 1인 경우에만 점수 부여)
        benefit_scores = np.dot(user_vector, self.benefit_matrix)

        # 가장 높은 점수를 가진 카드들 추천
        recommended_cards_indices = np.argsort(benefit_scores)[::-1]
        recommended_cards = list(self.card_data.iloc[recommended_cards_indices][1])

        return recommended_cards[:num_recommendations]

# card_data=card
user_spending_totals = np.array(user[:, :-1]).flatten()  # 'total' 제외
ranks=[31, 1, 2,3]
card_rank = df_card_info[ranks]

recommendation_system = CreditCardRecommendation(card_data)
recommended_cards = recommendation_system.recommend_credit_cards(user_spending_totals, num_recommendations=30)
# print(recommended_cards)
# print(card_rank)

class FinalCreditCardSelection:
    def __init__(self, recommended_cards, card_rank):
        self.recommended_cards = recommended_cards
        self.card_rank = card_rank

    def final_selection(self, annual_fees_weight, previous_month_weight, card_company_weight):
        final_recommendations = []

        # 기존의 recommended_cards를 이용하여 해당 카드에 대한 점수 계산
        scores = []
        for card in self.recommended_cards:
            card_info = self.card_rank[self.card_rank[1] == card]

            # 연회비, 전월실적, 카드사에 대한 가중치를 고려한 점수 계산
            score = -card_info[2].values[0] * previous_month_weight
            score -= card_info[3].values[0] * annual_fees_weight
            score += card_info[31].values[0] * card_company_weight
            scores.append(score)

        # 점수 내림차순으로 정렬하여 순위 계산
        ranked_indices = np.argsort(scores)[::-1]

        # 각 순위에 해당하는 카드를 final_recommendations에 추가
        for rank, index in enumerate(ranked_indices):
            final_recommendations.append({
                'Rank': rank + 1,
                'CreditCard': self.recommended_cards[index],
                'Score': scores[index]
            })

        return final_recommendations

# 예시 사용
final_selection_system = FinalCreditCardSelection(recommended_cards, card_rank)
final_recommendations = final_selection_system.final_selection(annual_fees_weight=1, previous_month_weight=1, card_company_weight=0.001)

# 출력 예시
# for recommendation in final_recommendations:
#     print(f"Rank {recommendation['Rank']}: {recommendation['CreditCard']} (Score: {recommendation['Score']})")
json_data = json.dumps(final_recommendations, ensure_ascii=False)

# JSON 문자열 출력
print(json_data)

# 연결 및 커서 닫기
cursor.close()
connection.close()