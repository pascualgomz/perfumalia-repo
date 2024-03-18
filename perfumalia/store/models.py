from django.db import models

class User(models.Model):
    userID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    cellphoneNumber = models.CharField(max_length=20)
    dateOfBirth = models.DateField()


class Perfume(models.Model):
    productID = models.CharField(primary_key = True, max_length=100)
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.IntegerField()
    inventoryQuantity = models.IntegerField()
    details = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class ShoppingCart(models.Model):
    userID = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    items = models.JSONField(blank=True, default=list) # Puede que no necesitemos esto ya que tenemos la tabla CartItem
    # quantity = models.JSONField(blank=True, default=list)  Puede que no necesitemos esto ya que tenemos la tabla CartItem
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    savedForLater = models.JSONField(blank=True, default=list)

    def __str__(self):
        return str(self.userID)
    
class Recommendations(models.Model):
    userID = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    purchaseHistory = models.JSONField(blank=True, default=list)
    browsingHistory = models.JSONField(blank=True, default=list)
    recommendationList = models.JSONField(blank=True, default=list)

    def __str__(self):
        return str(self.userID)
    
    def add_to_purchase_history(self, perfume):
        """Agrega detalles de un perfume al historial de compras."""
        history = self.purchaseHistory or []
        perfume_details = {
            'name': perfume.name,
            'details': perfume.details,
            'category': perfume.category,
            'brand': perfume.brand,
            'author': perfume.author
        }
        history.insert(0, perfume_details)
        self.purchaseHistory = history
        self.save()

    def add_to_browsing_history(self, perfume):
        """Agrega detalles de un perfume al historial de navegación."""
        history = self.browsingHistory or []
        perfume_details = {
            'name': perfume.name,
            'details': perfume.details,
            'category': perfume.category,
            'brand': perfume.brand,
            'author': perfume.author
        }
        history.insert(0, perfume_details)
        self.browsingHistory = history
        self.save()
    
    def update_recommendation_list(self, new_recommendations):
        """Fusiona una nueva lista de recomendaciones con la antigua."""
        existing_recommendations = self.recommendationList or []
        existing_dict = {rec['name']: rec for rec in existing_recommendations} # Crea un diccionario para verificación rápida

        for new_rec in new_recommendations: # Agrega solo las recomendaciones que no estén ya en la lista
            if new_rec['name'] not in existing_dict:
                existing_recommendations.append(new_rec)
                existing_dict[new_rec['name']] = new_rec  # Actualiza el diccionario para futuras verificaciones

        self.recommendationList = existing_recommendations
        self.save()



class CartItem(models.Model):
    product = models.ForeignKey(Perfume, on_delete=models.CASCADE)
    shoppingCart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.product)
    
