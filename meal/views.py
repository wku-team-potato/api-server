from datetime import date, timedelta
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from .models import UserMeal
from .serializers import UserMealSerializer
from .serializers import StreakSerializer
from .serializers import MealSummarySerializer
from .serializers import UserMealDetailSerializer
from nutrition.models import Foods
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.utils.dateparse import parse_date
from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
from point.models import PointTransaction

from groups.models import GroupRanking, GroupMember


class GetMealByuserIdView(generics.ListAPIView):
    """
    사용자의 식단을 조회하기 위한 API 뷰
    
    
    사용자 아이디와 날짜를 받아 해당 사용자의 식단을 조회합니다.
    """
    
    serializer_class = MealSummarySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        date = self.kwargs.get('date')
        
        if date is None:
            raise ValidationError('date 필드는 필수입니다.')
        
        meals = UserMeal.objects.filter(user_id=user_id, date=parse_date(date))
        
        if not meals:
            return Response({'breakfast': {}, 'lunch': {}, 'dinner': {}, 'summary': {}})
        
        summary = {'breakfast': {}, 'lunch': {}, 'dinner': {}, 'summary': {}}
        for meal_type in ['breakfast', 'lunch', 'dinner']:
            meal_type_meals = meals.filter(meal_type=meal_type)
            summary[meal_type] = {
                'calorie': sum([(meal.food.energy * (meal.serving_size / meal.food.serving_size)) for meal in meal_type_meals]),
                'carbohydrate': sum([(meal.food.carbohydrate * (meal.serving_size / meal.food.serving_size)) for meal in meal_type_meals]),
                'protein': sum([(meal.food.protein * (meal.serving_size / meal.food.serving_size)) for meal in meal_type_meals]),
                'fat': sum([(meal.food.fat * (meal.serving_size / meal.food.serving_size)) for meal in meal_type_meals])
            }
        
        summary['summary'] = {
            'calorie': sum([(meal.food.energy * (meal.serving_size / meal.food.serving_size)) for meal in meals]),
            'carbohydrate': sum([(meal.food.carbohydrate * (meal.serving_size / meal.food.serving_size)) for meal in meals]),
            'protein': sum([(meal.food.protein * (meal.serving_size / meal.food.serving_size)) for meal in meals]),
            'fat': sum([(meal.food.fat * (meal.serving_size / meal.food.serving_size)) for meal in meals])
        }
        
        return Response(summary)
        
    

class MealCreateView(generics.CreateAPIView):
    """
    사용자의 식단을 기록하기 위한 API 뷰
    
    기록시 그 날 첫 등록이면 point를 지급  
    
    기록시 그 날 아침, 점심, 저녁 모두 등록했으면 point를 지급
    
    """
    
    queryset = UserMeal.objects.all()
    serializer_class = UserMealSerializer
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능
    
    # def create(self, request, *args, **kwargs):
    #     user = request.user
    #     profile = user.profile
    #     today = date.today()
        
    #     is_first_meal = not UserMeal.objects.filter(user=user, date=today).exists()
        
    #     if is_first_meal:
    #         user_groups = GroupMember.objects.filter(user_id=user)
    #         for group_member in user_groups:
    #             try:
    #                 group_ranking = GroupRanking.objects.get(group_id=group_member.group_id)
    #                 group_ranking.total_points += 100
    #                 group_ranking.save()
    #             except GroupRanking.DoesNotExist:
    #                 continue
        
    #     today_meals = UserMeal.objects.filter(user=user, date=today)
        
    #     response = super().create(request, *args, **kwargs)
    #     response.data['message'] = '식단이 성공적으로 기록되었습니다.'
        
    #     return response
    
    def create(self, request, *args, **kwargs):
        user = request.user
        today = date.today()
        
        print("현재 유저:", user)
        print("현재 날짜:", today)
        print("날짜 타입:", type(today))
        
        # 당일 첫 등록 체크 (날짜만 비교)
        existing_meals = UserMeal.objects.filter(
            user=user,
            created_at=today
        ).count() == 0

        print("existing_meals:", existing_meals)
        
        # 먼저 식단 저장
        response = super().create(request, *args, **kwargs)
        
        # 첫 등록인 경우에만 포인트 부여 (count가 0일때)
        if existing_meals:
            user_groups = GroupMember.objects.filter(user_id=user)
            for group_member in user_groups:
                try:
                    group_ranking = GroupRanking.objects.get(group_id=group_member.group_id)
                    group_ranking.total_points += 100
                    group_ranking.save()
                except GroupRanking.DoesNotExist:
                    continue
        
        response.data['message'] = '식단이 성공적으로 기록되었습니다.'
        return response
    

class MealUpdateView(generics.UpdateAPIView):
    """
    사용자의 식단을 수정하기 위한 API 뷰
    
    사용자의 식단을 수정할 수 있습니다.
    
    """
    queryset = UserMeal.objects.all()
    serializer_class = UserMealSerializer
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data['message'] = '식단이 성공적으로 수정되었습니다.'
        return response
    
class MealDeleteView(generics.DestroyAPIView):
    """
    사용자의 식단을 삭제하기 위한 API 뷰
    
    사용자의 식단을 삭제할 수 있습니다.
    """
    queryset = UserMeal.objects.all()
    serializer_class = UserMealSerializer
    permission_classes = [IsAuthenticated]
    
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        if response.data is None:
            response.data = {}
        response.data['message'] = '식단이 성공적으로 삭제되었습니다.'
        return response
    
"""
폐기: MealListView
사유 : api 문서 단순화로 인한 삭제
"""
# class MealListView(generics.ListAPIView):
#     """__sumary__
#     description:
#         사용자의 식단을 조회하기 위한 API 뷰
#     """
#     queryset = UserMeal.objects.all()
#     serializer_class = UserMealSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         date = self.kwargs.get('date')
#         if date is None:
#             raise ValidationError('date 필드는 필수입니다.')
#         return UserMeal.objects.filter(user=user, date=parse_date(date))

"""
폐기: MealListView
사유 : api 문서 단순화로 인한 삭제
"""
# class MealTypeListView(generics.ListAPIView):
#     """_summary_

#     description:
#         사용자의 식단을 MealType으로 조회하기 위한 API 뷰
#     """
#     queryset = UserMeal.objects.all()
#     serializer_class = UserMealSerializer
#     permission_classes = [IsAuthenticated]
    
#     def get_queryset(self):
#         user = self.request.user
#         date = self.kwargs.get('date')
#         meal_type = self.kwargs.get('meal_type')
        
#         if date is None:
#             raise ValidationError('date 필드는 필수입니다.')
        
#         queryset = UserMeal.objects.filter(user=user, date=parse_date(date))
        
#         if meal_type:
#             if meal_type not in ['breakfast', 'lunch', 'dinner']:
#                 raise ValidationError('meal_type은 breakfast, lunch, dinner 중 하나여야 합니다.')
#             queryset = queryset.filter(meal_type=meal_type)
            
#         return queryset

class MealTypeListView(generics.ListAPIView):
    """
        사용자의 식단을 MealType으로 조회하기 위한 API 뷰
        
        사용자의 식단을 MealType으로 조회하기 위한 API 뷰
    """
    queryset = UserMeal.objects.all()
    serializer_class = UserMealDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        date = self.kwargs.get('date')
        meal_type = self.kwargs.get('meal_type')
        
        if date is None:
            raise ValidationError('date 필드는 필수입니다.')
        
        queryset = UserMeal.objects.filter(user=user, date=parse_date(date))
        
        if meal_type:
            if meal_type not in ['breakfast', 'lunch', 'dinner']:
                raise ValidationError('meal_type은 breakfast, lunch, dinner 중 하나여야 합니다.')
            queryset = queryset.filter(meal_type=meal_type)
            
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class MealSummaryView(generics.RetrieveAPIView):
    """
        사용자의 식단을 요약하여 조회하기 위한 API 뷰
        
        사용자의 식단을 요약하여 조회합니다.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = MealSummarySerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        date = self.kwargs.get('date')
        if date is None:
            raise ValidationError('date 필드는 필수입니다.')
        
        meals = UserMeal.objects.filter(user=user, date=parse_date(date))
        
        if not meals:
            return Response({'breakfast': {}, 'lunch': {}, 'dinner': {}, 'summary': {}})
        
        summary = {'breakfast': {}, 'lunch': {}, 'dinner': {}, 'summary': {}}
        for meal_type in ['breakfast', 'lunch', 'dinner']:
            meal_type_meals = meals.filter(meal_type=meal_type)
            summary[meal_type] = {
                'calorie': sum([(meal.food.energy * (meal.serving_size / meal.food.serving_size)) for meal in meal_type_meals]),
                'carbohydrate': sum([(meal.food.carbohydrate * (meal.serving_size / meal.food.serving_size)) for meal in meal_type_meals]),
                'protein': sum([(meal.food.protein * (meal.serving_size / meal.food.serving_size)) for meal in meal_type_meals]),
                'fat': sum([(meal.food.fat * (meal.serving_size / meal.food.serving_size)) for meal in meal_type_meals])
            }
            
        summary['summary'] = {
            'calorie': sum([(meal.food.energy * (meal.serving_size / meal.food.serving_size)) for meal in meals]),
            'carbohydrate': sum([(meal.food.carbohydrate * (meal.serving_size / meal.food.serving_size)) for meal in meals]),
            'protein': sum([(meal.food.protein * (meal.serving_size / meal.food.serving_size)) for meal in meals]),
            'fat': sum([(meal.food.fat * (meal.serving_size / meal.food.serving_size)) for meal in meals])
        }
        
        return Response(summary)

class UserMealDetailView(generics.RetrieveAPIView):
    """
        사용자의 식단을 상세 조회하기 위한 API 뷰
        
        
        사용자의 식단을 상세 조회합니다.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserMealDetailSerializer
    
    def get(self, request, *args, **kwargs):
        user = request.user
        date = self.kwargs.get('date')
        
        if date is None:
            raise ValidationError('date 필드는 필수입니다.')
        
        meals = UserMeal.objects.filter(user=user, date=parse_date(date))
        
        if not meals:
            return Response([])
        
        serializer = self.get_serializer(meals, many=True)
        return Response(serializer.data)

# class MealTypeSummaryView(generics.RetrieveAPIView):
#     """__sumary__
#     description:
#         사용자의 식단을 MealType으로 요약하여 조회하기 위한 API 뷰
#     """
#     permission_classes = [IsAuthenticated]
#     serializer_class = MealSummarySerializer

#     def get(self, request, *args, **kwargs):
#         user = request.user
#         date = self.kwargs.get('date')
#         meal_type = self.kwargs.get('meal_type')
        
#         if date is None:
#             raise ValidationError('date 필드는 필수입니다.')
        
#         meals = UserMeal.objects.filter(user=user, date=parse_date(date), meal_type=meal_type)
        
#         if not meals:
#             return Response({'calorie': 0, 'carbohydrate': 0, 'protein': 0, 'fat': 0})
        
#         summary = {
#             'calorie': sum([(meal.food.energy * (meal.serving_size / meal.food.serving_size)) for meal in meals]),
#             'carbohydrate': sum([(meal.food.carbohydrate * (meal.serving_size / meal.food.serving_size)) for meal in meals]),
#             'protein': sum([(meal.food.protein * (meal.serving_size / meal.food.serving_size)) for meal in meals]),
#             'fat': sum([(meal.food.fat * (meal.serving_size / meal.food.serving_size)) for meal in meals])
#         }
        
#         return Response(summary)

class MealStreakView(generics.RetrieveAPIView):
    """
        오늘 기준으로 몇일 연속으로 식단을 등록했는지 확인하는 API 뷰
        
        
        오늘 기준으로 몇일 연속으로 식단을 등록했는지 확인합니다.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = StreakSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        meals = UserMeal.objects.filter(user=user).order_by('-date')
        if not meals:
            return Response({'streak': 0})

        streak = 0
        current_date = date.today()  # 오늘 날짜로 초기화
        meal_dates_checked = set()  # 이미 확인한 날짜들을 저장할 집합

        for meal in meals:
            meal_date = meal.date  # 날짜 필드
            created_date = meal.created_at  # created_at의 날짜 부분만 가져옴

            # 날짜가 같고, 중복되지 않은 경우에만 체크
            if meal_date == created_date and meal_date == current_date and meal_date not in meal_dates_checked:
                streak += 1
                current_date -= timedelta(days=1)
                meal_dates_checked.add(meal_date)  # 확인된 날짜를 추가
            elif meal_date < current_date:  # 연속되지 않는 날짜가 나오면 종료
                break

        return Response({'streak': streak})