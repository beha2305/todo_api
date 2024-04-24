from rest_framework import serializers
from .models import Todo, Movie


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
