import re
import random

from django import template
from utils import jalali
from utils import city_province
from collections import Counter
from account.models import User
from content.models import Collection, WatchedContent, ContentOrder
from quiz.models import UserExamAnsewrHistory
from team.models import StartUpTeam
from subject.models import Subject, Topic
from quiz.models import PreRegisterTaskResponse

register = template.Library()

@register.filter()
def get_state_name(state_code):
    try:
        state_code = str(state_code)
        res = city_province.all_state[state_code]
        return res
    except:
        return "404"
    

@register.filter()
def get_city_name(city_code):
    try:
        city_code = str(city_code)
        res = city_province.city_list[city_code]
        return res
    except:
        return "404"


@register.filter()
def is_user_answer_to_question(question, user):
    try:
        result = PreRegisterTaskResponse.objects.filter(user=user, question=question)
        return result.last().text
    except:
        return ""


@register.filter()
def plus_one(value):
    try:
        value = int(value)
        return value + 1
    except:
        return False


@register.filter()
def to_jalali(value):
    try:
        return jalali.Gregorian(
            f"{value.year}-{value.month}-{value.day}"
        ).persian_string()
    except:
        return "خالی"
    

@register.simple_tag
def is_collection_done(user_id: int, collection_uid: str) -> bool:
    user_instance = User.objects.get(pk=user_id)
    collection_instance = Collection.objects.get(uuid=collection_uid)
    exam = collection_instance.exam
    
    # Retrieve content UUIDs from ContentOrder related to the specified collection
    content_uuids = ContentOrder.objects.filter(collection=collection_instance).values_list('content__uuid', flat=True)
    # Fetch the watched content UUIDs for the user
    watched_content_uuids_for_user = WatchedContent.objects.filter(user=user_instance, content__uuid__in=content_uuids).values_list('content__uuid', flat=True)    
    # Check if all content UUIDs related to the collection have been watched by the user
    is_content_done = set(content_uuids).issubset(watched_content_uuids_for_user)

    if exam:
        num_questions = exam.questions.count()
        num_answers = UserExamAnsewrHistory.objects.filter(user=user_instance, exam=exam).count()
        is_exam_done = num_questions == num_answers
        return bool(is_content_done and is_exam_done)
    else:
        return is_content_done


@register.simple_tag
def is_exam_done(user_id:int, collection_uid:str) -> bool:
    user_instance = User.objects.get(pk=user_id)
    collection_instance = Collection.objects.get(uuid=collection_uid)
    exam = collection_instance.exam

    num_questions = exam.questions.count()
    num_answers = UserExamAnsewrHistory.objects.filter(user=user_instance, exam=exam).count()
    is_exam_done = num_questions == num_answers
    return is_exam_done


@register.filter()
def remain_content_count(value, user) -> int:
    """
    Count how many content remain that user not watched.
    - value: count of watched content.
    - user: an instance user.
    """
    # Store remain content count
    remain_count = 0

    # Check if user is a member of a StartUp team.
    if not user.members_of_team.first():
        return None
    
    try:
        # user > team > center(accelerator) > road > CollectionOrder objects
        collection_orders = user.members_of_team.first().team_of_center.first().accelerator_of_road.first().road_of_collection_order.all()
    except:
        return None

    for order_obj in collection_orders:
        remain_count += order_obj.collection.collection_of_content_order.count()

    return remain_count - value


@register.simple_tag
def all_content_count(user:int) -> bool:
    count = 0
    for collection in user.collections.all():
        count += collection.collection_of_content_order.all().count()
    return count


@register.simple_tag
def get_topics_and_counts(uuid):
    team = StartUpTeam.objects.get(uuid=uuid)
    # Get all topics
    all_topics = Topic.objects.all()

    # Get all users in the team
    team_users = team.team_members.all()

    # Get all abilities of all users in the team
    abilities = Subject.objects.filter(abilities_of_user__in=team_users)

    # Count repetitions of each topic
    topic_counts = Counter(abilities.values_list('topic__name', flat=True))

    # Initialize counts for all topics, with 0 if the topic is not in abilities
    all_topic_counts = {topic.name: topic_counts.get(topic.name, 0) for topic in all_topics}

    if not all_topic_counts:
        return False

    return [list(all_topic_counts.keys()), list(all_topic_counts.values())]


@register.simple_tag
def get_topics_and_counts(uuid):
    team = StartUpTeam.objects.get(uuid=uuid)
    # Get all topics
    all_topics = Topic.objects.all()

    # Get all users in the team
    team_users = team.team_members.all()

    # Get all abilities of all users in the team
    abilities = Subject.objects.filter(abilities_of_user__in=team_users)

    # Count repetitions of each topic
    topic_counts = Counter(abilities.values_list('topic__name', flat=True))

    # Initialize counts for all topics, with 0 if the topic is not in abilities
    all_topic_counts = {topic.name: topic_counts.get(topic.name, 0) for topic in all_topics}

    if not all_topic_counts:
        return False

    return [list(all_topic_counts.keys()), list(all_topic_counts.values())]


@register.filter()
def not_zero(value) -> int:
    if value <= 0:
        return "رایگان"
    return value


@register.filter(is_safe=True)
def intcomma(value):
    if isinstance(value, int) and value <= 0:
        return "رایگان"

    orig = str(value)
    return re.sub(r"^(-?\d+)(\d{3})", r"\g<1>,\g<2>", orig)


@register.simple_tag
def random_fund_amount() -> int:
    res = random.randint(1000, 100000)
    rounded_res = round(res / 1000) * 1000
    return rounded_res
