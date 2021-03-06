
from salle_activite.models import Activity
from salle_activite.models import Salle
from .models import AbonnementClient, Abonnement
from rest_framework import serializers
from datetime import datetime, timedelta, date
from salle_activite.serializers import ActivitySerialiser, SalleSerialiser
from transaction.models import Paiement
from client.models import Client
import datetime

class PaiementClientSerializer(serializers.ModelSerializer):
    class Meta:
            model = Paiement
            fields= '__all__'

class AbonnementTestSerializer(serializers.ModelSerializer):
    class Meta:
            model = Abonnement
            fields= '__all__'

class ClientDropSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = '__all__'


class AbonnementClientDetailUpdateSerialiser(serializers.ModelSerializer):
    activity = serializers.SerializerMethodField('get_activity', read_only=True)
    type_abonnement = serializers.SerializerMethodField('get_abon_name', read_only=True)
    class Meta:
        model = AbonnementClient
        read_only_fields = ('client',)
        fields= ('id','start_date','end_date', 'client', 'type_abonnement', 'presence_quantity', 'creneaux', 'activity', 'reste')
        # depth= 4

    def get_activity(self, obj):
        abonnement_id = obj.type_abonnement.id
        abonnement = Abonnement.objects.get(id = abonnement_id)
        salles = abonnement.salles.all() #ERRRRREEEEEEUUUUUUURRRRR
        activitesOfSalles=[] 
        for i in salles:
            print('ACTIVTIEES => ', i)
            act = Activity.objects.filter(salle_id = i)
            for j in act:
                lenght=len(activitesOfSalles)
                activitesOfSalles.insert(lenght,j)               
        print('---------------',activitesOfSalles)
            # actis= Salle.activites.all()
            # for j in actis:
            #     activitesOfSalles.insert(i)
            #     print(' ---------------------',j)
          
        return SalleSerialiser(activitesOfSalles, many=True).data
    def get_abon_name(self, obj):
        return obj.type_abonnement.name

class AbonnementClientSerialiser(serializers.ModelSerializer):
    # creneaux = serializers.PrimaryKeyRelatedField(many=True, queryset= Creneau.objects.all())
    # creneaux = CreneauSerialiser(many=True)
    type_abonnement_name = serializers.SerializerMethodField('get_abon_name', read_only=True)
    
    class Meta:
        model = AbonnementClient
        read_only_fields = ('presence_quantity',)
        fields= ('id','start_date', 'client', 'type_abonnement', 'presence_quantity', 'creneaux', 'type_abonnement_name')


    def get_abon_name(self, obj):
        return obj.type_abonnement.name

    def get_day_index(self, day):
        if day == 'DI':
            return 6
        elif day == 'LU':
            return 0
        elif day == 'MA':
            return 1
        elif day == 'ME':
            return 2
        elif day == 'JE':
            return 3
        elif day == 'VE':
            return 4
        elif day == 'SA':
            return 5
        else:
            return False
    def get_next_date(self, given_start_date, day):
        today = datetime.date.today()
        weekday = given_start_date.weekday()
        print('TODAY DE TODAY', day)
        the_next_day = given_start_date + datetime.timedelta((day-weekday) % 7)
        return the_next_day
    def create(self, validated_data):
        print('VALIDATED DATA', validated_data)
        client = validated_data['client']
        creneaux = validated_data['creneaux']
        type_ab = validated_data['type_abonnement']
        start_date = validated_data['start_date']

        duree = type_ab.number_of_days
        duree_semaine = (duree // 7) - 1 
        # print('le client',client)
        # print('l" abonnement ',type_ab)
        selected_creneau= [cre.id for cre in creneaux ]
        
        print('l" start_date ',selected_creneau)
        dates_array = []
        for creneau in creneaux :
            jour = self.get_day_index(creneau.day)
            next_date = self.get_next_date(start_date, jour)
            print(f'le prochain {creneau.day} in: {jour} est le {next_date}')
            dates_array.append(next_date)
        print('la MAX : ', max(dates_array))
        maxed_date = max(dates_array)
        if type_ab.systeme_cochage:
            calculated_end_date = start_date + datetime.timedelta(days =duree)
        else:
            calculated_end_date = maxed_date + datetime.timedelta(weeks=duree_semaine)
        print('la calculated_end_date : ', calculated_end_date)
        abc_instance = AbonnementClient.objects.create(client= client, start_date= start_date ,end_date= calculated_end_date, type_abonnement = type_ab)
        for cren in selected_creneau:
            abc_instance.creneaux.add(cren)    
        abc_instance.save()
        return abc_instance 

        # for date in dates_array:
        #     print('date inividuelle : ', date)
            
    # def create(self, validated_data):
    #     print('validated_data =====>', validated_data)
    #     # return AbonnementClient.objects.create(**validated_data)
    #     abon = validated_data['type_abonnement']
    #     number = Abonnement.objects.get(id = abon.id).number_of_days
    #     delta = timedelta(days = number)
    #     end_date = datetime.now().date() + delta
    #     presence_quantity = Abonnement.objects.get(id = abon.id).seances_quantity

    #     abonnement_client = AbonnementClient.objects.create(end_date=end_date,presence_quantity=presence_quantity, **validated_data)
    #     return abonnement_client





        # abonnement_client.creneaux.create()
        # for creneau in creneaux:
        #     Creneau.objects.create(abonnements=abonnement_client, **creneaux)
        # for creneau in creneaux:
        #     Creneau.objects.create()
        
        
        # creneaux = validated_data['creneau']
        # client = validated_data['client']
        # abon = validated_data['type_abonnement']
        # print('presennnce =====>', presence_quantity)
        # return AbonnementClient.objects.create(end_date=end_date,presence_quantity=presence_quantity**validated_data)
class AbonnementClientDetailSerializer(serializers.ModelSerializer):
    type_abonnement_name = serializers.SerializerMethodField('get_type_abonnement_name', read_only=True)
    cochage       = serializers.CharField(source='type_abonnement.systeme_cochage', read_only=True)
    price       = serializers.CharField(source='type_abonnement.price', read_only=True)

    class Meta:
        model = AbonnementClient
        fields =('id', 'start_date','end_date', 'type_abonnement' , 'type_abonnement_name','presence_quantity', 'creneaux', 'cochage', 'reste', 'price')
    def get_type_abonnement_name(self, obj):
        return obj.type_abonnement.name

class AbonnementSerialiser(serializers.ModelSerializer):
    clients_number = serializers.SerializerMethodField('get_clients_number', read_only=True)
    salle_name = serializers.CharField(source='salles.name', read_only=True)
    class Meta:
        model = Abonnement
        read_only_fields = ('clients_number','salle_name')
        fields= ('id', 'name', 'price', 'number_of_days', 'seances_quantity', 'salles', 'clients_number','salle_name', 'systeme_cochage', 'actif')

    def get_clients_number(self, obj):
        try:
            queryset = Abonnement.objects.get(id = obj.id)
            number = queryset.type_abonnement_client.count()
            return number 
        except:
            return False
    
    # def get_activity_name(self, obj):
    #     try:
    #         return obj.activity.name
    #     except:
    #         return False

    # def create(self, validate_data):
    #     abon = Abonnement.objects.create(**validate_data)
    #     return True


class AbonnementClientTransactionsSerializer(serializers.ModelSerializer):
    transactions = serializers.SerializerMethodField('get_transactions', read_only=True)

    class Meta:
        model= AbonnementClient
        fields= ('client','type_abonnement','reste', 'transactions')
    def get_transactions(self, obj):
        trans = obj.transactions.all()
        return PaiementClientSerializer(trans, many=True).data

class ABCCreneauSerializer(serializers.ModelSerializer):
    abonnement = serializers.CharField(source='type_abonnement.name')
    client_data = serializers.SerializerMethodField('get_client_name', read_only=True)
    class Meta:
        model = AbonnementClient
        fields = ('id',  'client_data', 'start_date', 'end_date', 'reste', 'abonnement')
        # fields = '__all__'
    
    def get_client_name(self, obj):
        client= obj.client
        return ClientDropSerializer(client).data


    # def get_abonnement(self, obj):
    #     creneau = self.context['creneau']
    #     abonnement = AbonnementClient.objects.filter(id=obj.abonnement_client,creneaux=creneau)
    #     print('LA REQuETRTE',creneau)
    #     return AbonnementClientSerialiser(abonnement).data
