from rest_framework import serializers

from applications.feedback.models import Rating, Like, Comment, Favorite
from applications.feedback.serializers import ReviewerSerializer, FanSerializer, CommentSerializer, FavoriteSerializer


# COMMENT ##############################################################################################################
def give_comment(obj, user, comment):
    """
    пользователь ставит комментарий
    :param obj: `obj` который комментируют
    :param user: пользователь который комментирует
    :param comment: комментарий
    """
    comment_obj, is_created = Comment.objects.get_or_create(user=user, electronic=obj)
    comment_obj.comment = comment
    comment_obj.save()
    if is_created:
        return 'Комментарий создан'
    return 'Комментарий обновлен'


def del_comment(obj, user):
    """
    Удаляет комментарий
    :param obj: `obj`, комментарий которого удаляют
    :param user: пользователь, комментарий которого удаляют
    """
    try:
        Comment.objects.get(electronic=obj, user=user).delete()
    except Comment.DoesNotExist:
        pass


def is_commented(obj, user):
    """
    Оставлял ли пользователь комментарий
    :param obj: `obj`
    :param user: пользователь
    """
    try:
        return Comment.objects.filter(user=user, electronic=obj).exists()
    except TypeError:
        return False


def get_commentators(obj):
    """
    Выводит список комментаторов и комментариев к `obj`
    :param obj: `obj`, комментарии которого выводятся
    """
    commentators = Comment.objects.filter(electronic=obj)
    serializer = CommentSerializer(commentators, many=True)
    commentators = [{'user': i['user'], 'comment': i['comment']} for i in serializer.data]
    return commentators


def get_comments(user):
    """
    Выводит список комментариев пользователя
    :param user: пользователь, комментарии которого выводятся
    """
    comments = Comment.objects.filter(user=user)
    serializer = CommentSerializer(comments, many=True)
    comments = [{'electronic': i['electronic'], 'comment': i['comment']} for i in serializer.data]
    return comments

# LIKE #################################################################################################################


def like_unlike(user, obj):
    """
    Ставит и убирает лайк
    :param user: пользователь, который ставит лайк
    :param obj: `obj`, которому ставят лайк
    :return: статус: like/unlike
    """
    like_obj, is_created = Like.objects.get_or_create(user=user, electronic=obj)
    like_obj.like = not like_obj.like
    like_obj.save()
    if not like_obj.like:
        return 'unliked'
    return 'liked'


def is_fan(user, obj):
    """
    Проверяет поставил ли пользователь лайк
    :param user: пользователь, которого проверяем
    :param obj: `obj`, которому пользователь поставил лайк (или не поставил)
    """
    try:
        like = Like.objects.filter(user=user, electronic=obj)
        if like.exists() and like[0].like:
            return True
        return False
    except TypeError:
        return False


def get_fans(obj):
    """
    Выводит список пользователей, поставивших лайк
    :param obj: `obj` которому поставили лайк
    """
    fans = Like.objects.filter(electronic=obj, like=True)
    serializer = FanSerializer(fans, many=True)
    return serializer.data


# RATING
def give_rating(obj, user, rating):
    """
    Ставит рейтинг
    :param obj: `obj` которому ставят рейтинг
    :param user: пользователь который ставит рейтинг
    :param rating: рейтинг который поставил пользователь
    """
    if 0 <= int(rating) <= 5:
        rating_obj, is_created = Rating.objects.get_or_create(user=user, electronic=obj)
        rating_obj.rating = rating
        rating_obj.save()
        if not is_created:
            return 'Рейтинг обновлен!'
        return 'Рейтинг создан!'
    raise serializers.ValidationError('Неверно введен рейтинг')


def del_rating(obj, user):
    """
    Удаляет рейтинг
    :param obj: рейтинг который удаляют
    :param user: пользователь который удаляет рейтинг
    """
    try:
        Rating.objects.get(electronic=obj, user=user).delete()
    except Rating.DoesNotExist:
        pass


def is_reviewer(obj, user):
    """
    Оставлял ли пользователь рейтинг
    :param obj: `obj` на который поставили рейтинг (или не поставили)
    :param user: пользователь который поставил рейтинг
    """
    try:
        return Rating.objects.filter(user=user, electronic=obj).exists()
    except TypeError:
        return False


def get_reviewers(obj):
    """
    Выводит список пользователей, поставивших рейтинг
    :param obj: `obj` которому поставили рейтинг
    """
    users = Rating.objects.filter(electronic=obj)
    serializer = ReviewerSerializer(users, many=True)
    return serializer.data

# FAVORITES ############################################################################################################


def add_del_favorite(obj, user):
    """
    Добавляет/удаляет `obj` из избранных
    :param obj: `obj` который добавляется
    :param user: пользователь который добавляет/удаляет
    """
    fav_obj, is_created = Favorite.objects.get_or_create(electronic=obj, user=user)
    fav_obj.is_favorite = not fav_obj.is_favorite
    fav_obj.save()
    if fav_obj.is_favorite:
        return 'Добавлено в избранное'
    return 'Удалено из избранных'


def is_favorite(obj, user):
    """
    Проверяет, находится ли `obj` в избранных у пользователя
    :param obj: electronic
    :param user: пользователь
    """
    try:
        return Favorite.objects.filter(electronic=obj, user=user, is_favorite=True).exists()
    except TypeError:
        return False


def get_favorites(user):
    """
    Выводит избранных список `obj`
    :param user: пользователь который добавил в избранное
    """
    try:
        electronic = Favorite.objects.filter(user=user, is_favorite=True)
        serializer = FavoriteSerializer(electronic, many=True)
        return serializer.data
    except TypeError:
        return []

