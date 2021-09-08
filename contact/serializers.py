from rest_framework import serializers

from .models import ContactMessage, ContactFormPluginModel


class ContactMessageSerializer(serializers.ModelSerializer):
    plugin = serializers.PrimaryKeyRelatedField(
        queryset=ContactFormPluginModel.objects.all(),
        write_only=True,
        required=True
    )

    class Meta:
        model = ContactMessage
        fields = ['sender_name', 'sender_email', 'message', 'plugin']
        extra_kwargs = {
            'sender_name': {'read_only': False},
            'sender_email': {'read_only': False},
            'message': {'read_only': False}
        }

    def create(self, validated_data):
        plugin = validated_data.pop('plugin')
        validated_data['recipients'] = plugin.recipients.active()

        return super().create(validated_data)
