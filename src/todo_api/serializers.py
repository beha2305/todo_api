from rest_framework import serializers
from .models import Todo, Movie
import re
class TodoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['task', 'completed', 'timestamp', 'user', "updated"]


def is_rating(value):
   if value < 1 or value > 10:
       raise serializers.ValidationError("rating 1 va 10 orasida bolishi kerak")


class MovieSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(validators=[is_rating])
    class Meta:
        model = Movie
        fields = '__all__'

    def validate(self, attrs):
        if attrs['uzb_gross'] > attrs['world_gross']:
            raise serializers.ValidationError("Uzb gross kichkina bolishi kerak")
        return attrs

    def validate_phone_number(self, phone_number):

        number_format = re.compile(r'^\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$')

        if not number_format.match(phone_number):
            raise serializers.ValidationError("Phone number formati xato")
        return phone_number