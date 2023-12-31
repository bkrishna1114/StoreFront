from decimal import Decimal
from rest_framework import serializers
from store.models import Product,Collection, Review
from django.db.models.aggregates import Count

# class CollectionSerializer(serializers.Serializer):
class CollectionSerializer(serializers.ModelSerializer): #useed model serializer
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    class Meta:
        model = Collection
        fields = ['id','title','products_count']

    products_count = serializers.IntegerField(read_only=True) #it iwll prevent the post and put method
    
# class ProductSerializers(serializers.Serializer):
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','description','slug','inventory','description','unit_price','price_with_gst','collection'] #It will show only this fields
    # id = serializers.IntegerField()
    # description = serializers.CharField(max_length=255)
    # unit_price = serializers.DecimalField(max_digits=255,decimal_places=2)
    # collection = serializers.StringRelatedField()
    # collection = CollectionSerializer()  #getting another serializerin here shows all the anohte serialzer data..
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset = Collection.objects.all(),
    #     view_name='collection-detail'
    # )
    price_with_gst = serializers.SerializerMethodField(method_name='PriceWithTax')

    def PriceWithTax(self,product:Product):
        return round(product.unit_price + (product.unit_price)/ (Decimal(18)),2) #returning unit prics + gst


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='product.title',read_only=True) #get the title field
    class Meta:
        model = Review
        fields = ['id','title','date','name','description']


    #manully sending product_id to review product id here...
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id,**validated_data)
    