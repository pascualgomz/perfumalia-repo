from django.db import models, transaction

class User(models.Model):
    userID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    cellphoneNumber = models.CharField(max_length=20)
    dateOfBirth = models.DateField()

class Order(models.Model):
    orderID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    orderStatus = models.CharField(max_length=50)
    shippingDetails = models.JSONField()
    orderDate = models.DateField(auto_now_add=True)
    orderHistory = models.JSONField()

class Perfume(models.Model):
    productID = models.CharField(primary_key = True, max_length=100)
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventoryQuantity = models.IntegerField()
    details = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    def update_inventory(self, new_quantity):
        """Actualiza la cantidad de inventario de un perfume."""
        self.inventoryQuantity = new_quantity
        self.save()

    def view_details(self):
        """Muestra los detalles de un perfume."""
        return f"{self.name} by {self.author} is a {self.category} perfume by {self.brand}. {self.details}"
    
    
    def calculate_price(self, quantity):
        """Calcula el precio total de una cantidad de perfumes."""
        return self.price * quantity
    
    # def add_ingredient(self, ingredient):
    #     """Agrega un ingrediente a los detalles de un perfume."""
    #     self.details += f" {ingredient}"
    #     self.save()

    # def remove_ingredient(self, ingredient):
    #     """Elimina un ingrediente de los detalles de un perfume."""
    #     self.details = self.details.replace(ingredient, '')
    #     self.save()

    # def get_ingredient(self, index):
    #     """Obtiene un ingrediente de los detalles de un perfume."""
    #     return self.details.split(' ')[index]
    
    # def save_customization(self):
    #     """Guarda los detalles personalizados de un perfume."""
    #     self.customize_perfume = cus
    #     self.save()

    # def customize_perfume(self, new_details):
    #     """Personaliza los detalles de un perfume."""
    #     self.details = new_details
    #     self.save()

class OrderItem(models.Model):
    perfume = models.ForeignKey(Perfume, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    orderID = models.ForeignKey(Order, on_delete=models.CASCADE)


    
class ShoppingCart(models.Model):
    userID = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    savedForLater = models.JSONField(blank=True, default=list)

    def __str__(self):
        return str(self.userID)
    
    def update_subtotal(self):
        """Actualiza el subtotal del carrito basado en los ítems actuales."""
        self.subtotal = sum(item.calcular_total() for item in self.cartitem_set.all())
        self.save()

    def save_for_later(self, item_id):
        """Guarda un artículo para después."""
        # Mueve un artículo de 'items' a 'savedForLater'
        for item in self.items:
            if item['id'] == item_id:  
                self.items.remove(item)
                self.savedForLater.append(item)
                self.save()
                return item  # Retorna el ítem movido
        return None  # Retorna None si el ítem no se encontró
    
    def clear_cart(self):
        """Vacía el carrito."""
        self.items = []
        self.subtotal = 0
        self.save()

 
    def checkout(self):
        with transaction.atomic():
            # Crear un nuevo pedido
            new_order = Order.objects.create(
                userID=self.userID,
                orderStatus='Pending',  # O cualquier estado inicial que prefieras
                shippingDetails={},  # Asume valores predeterminados o ajusta según sea necesario
                orderHistory={}  # Asume valores predeterminados o ajusta según sea necesario
            )

            # Transferir ítems de ShoppingCart a Order
            for item in self.cartitem_set.all():
                OrderItem.objects.create(
                    perfume=item.product,  # Asume que 'product' ahora es un objeto Perfume en CartItem
                    cantidad=item.quantity,
                    orderID=new_order
                )

                # Actualizar inventario del perfume asociado
                item.product.update_inventory(item.product.inventoryQuantity - item.quantity)

                # Eliminar el CartItem ya que ha sido transferido a OrderItem
                item.delete()

            # Vaciar atributos del carrito de compras
            self.subtotal = 0
            self.savedForLater.clear()  # Asume que quieres limpiar la lista de 'guardar para más tarde'
            self.save()  # No olvides guardar cualquier cambio en el carrito

            # Devuelve el pedido para su posterior procesamiento
            return new_order
    


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
    
    def actualizar_cantidad(self, nueva_cantidad):
        """Actualiza la cantidad de un artículo en el carrito."""
        if nueva_cantidad >= 0:
            self.quantity = nueva_cantidad
            self.save()
            self.shoppingCart.update_subtotal()

    def calcular_total(self):
        """Calcula el precio total de un artículo."""
        return self.product.price * self.quantity
    
    def obtener_precio_unitario(self):
        """Obtiene el precio unitario de un artículo."""
        return self.product.price # Precio unitario
    
    def obtener_precio_total(self):
        """Obtiene el precio total de un artículo."""
        return self.calcular_total()
    
