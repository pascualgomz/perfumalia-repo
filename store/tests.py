from django.test import TestCase
from .models import ShoppingCart, User, Perfume, OrderItem, Order, CartItem, Recommendations
from django.contrib.auth.models import User as AuthUser
from decimal import Decimal


class PerfumeModelTest(TestCase):

    def setUp(self):
        self.perfume = Perfume.objects.create(
            productID='001',
            name='Test Perfume',
            author='Test Author',
            brand='Test Brand',
            category='Test Category',
            price=100.00,
            inventoryQuantity=50,
            details='This is a test perfume'
        )

    def test_update_inventory(self):
        # Prueba el método update_inventory
        self.perfume.update_inventory(100)
        self.assertEqual(self.perfume.inventoryQuantity, 100)

    def test_view_details(self):
        # Prueba el método view_details
        expected_details = 'Test Perfume by Test Author is a Test Category perfume by Test Brand. This is a test perfume'
        self.assertEqual(self.perfume.view_details(), expected_details)

    def test_calculate_price(self):
        # Prueba el método calculate_price
        self.assertEqual(self.perfume.calculate_price(10), 1000)  # 5 * 100.00


class ShoppingCartTest(TestCase):

    def setUp(self):
        self.user = AuthUser.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.user_profile = User.objects.create(
            name='Test User', 
            address='123 Main St',
            cellphoneNumber='1234567890', 
            dateOfBirth='2000-01-01'
        )
        self.perfume = Perfume.objects.create(
            productID='001',
            name='Test Perfume',
            author='Test Author',
            brand='Test Brand',
            category='Test Category',
            price=Decimal('50.00'),
            inventoryQuantity=100,
            details='Test details'
        )
        self.cart = ShoppingCart.objects.create(
            userID=self.user_profile,
            subtotal=Decimal('0.00')
        )

    def test_add_to_cart_and_checkout(self):
        # Añade un elemento al carrito y realiza un checkout
        cart_item = CartItem.objects.create(
            product=self.perfume, 
            shoppingCart=self.cart, 
            quantity=2
        )
        self.cart.update_subtotal()  # Actualizar el subtotal después de añadir elementos

        # Verificar que el subtotal se haya actualizado correctamente
        expected_subtotal = self.perfume.price * cart_item.quantity
        self.assertEqual(self.cart.subtotal, expected_subtotal)

        # Probar el método checkout
        new_order = self.cart.checkout()
        self.assertIsNotNone(new_order)  # Verificar que se creó un nuevo pedido
        self.assertEqual(new_order.userID, self.user_profile)  # Verifica que el pedido esté asignado al usuario correcto
        self.assertEqual(new_order.orderStatus, 'Pending')  # Verifica el estado inicial del pedido
        self.assertEqual(OrderItem.objects.filter(orderID=new_order).count(), 1)  # Asegurarse de que los ítems se transfirieron
        self.assertEqual(self.cart.cartitem_set.count(), 0)  # El carrito debería estar vacío después del checkout
        self.assertEqual(self.perfume.inventoryQuantity, 100)  # Verificar la actualización del inventario
        self.assertEqual(self.cart.subtotal, Decimal('0.00'))  # El subtotal del carrito debe resetearse después del checkout

class CartItemTest(TestCase):

    def setUp(self):
        # Crear usuario
        self.user = User.objects.create(name='Test User', address='Test Address', cellphoneNumber='1234567890', dateOfBirth='2000-01-01')

        # Crear carrito de compras
        self.shoppingCart = ShoppingCart.objects.create(userID=self.user, subtotal=Decimal('0.00'))

        # Crear un perfume
        self.perfume = Perfume.objects.create(
            productID='001',
            name='Test Perfume',
            author='Test Author',
            brand='Test Brand',
            category='Test Category',
            price=Decimal('100.00'),
            inventoryQuantity=10,
            details='Test Details'
        )

        # Crear un CartItem
        self.cartItem = CartItem.objects.create(
            product=self.perfume,
            shoppingCart=self.shoppingCart,
            quantity=2
        )

    def test_actualizar_cantidad(self):
        """Prueba la actualización de la cantidad de un artículo en el carrito."""
        self.cartItem.actualizar_cantidad(3)
        self.assertEqual(self.cartItem.quantity, 3)

    def test_calcular_total(self):
        """Prueba el cálculo del precio total de un artículo en el carrito."""
        total = self.cartItem.calcular_total()
        self.assertEqual(total, Decimal('200.00'))  # 2 * 100.00

    def test_obtener_precio_unitario(self):
        """Prueba la obtención del precio unitario de un artículo."""
        precio_unitario = self.cartItem.obtener_precio_unitario()
        self.assertEqual(precio_unitario, Decimal('100.00'))

    def test_obtener_precio_total(self):
        """Prueba la obtención del precio total de un artículo."""
        precio_total = self.cartItem.obtener_precio_total()
        self.assertEqual(precio_total, Decimal('200.00'))  # 2 * 100.00

    def test_update_subtotal_on_cart(self):
        """Prueba la actualización del subtotal en el carrito de compras tras cambiar la cantidad de un artículo."""
        # Asumiendo que tienes un método para actualizar el subtotal en el ShoppingCart
        self.cartItem.actualizar_cantidad(3)
        self.cartItem.shoppingCart.update_subtotal()
        expected_subtotal = self.cartItem.calcular_total()  # 3 * 100.00
        self.assertEqual(self.shoppingCart.subtotal, expected_subtotal)

class RecommendationsTest(TestCase):

    def setUp(self):
        # Configura objetos necesarios para las pruebas
        self.user = User.objects.create(
            name='Test User', 
            address='123 Main Street', 
            cellphoneNumber='1234567890', 
            dateOfBirth='1990-01-01'
        )
        self.perfume1 = Perfume.objects.create(
            productID='001',
            name='Eau de Test',
            author='Test Author',
            brand='Test Brand',
            category='Test Category',
            price=50.00,
            inventoryQuantity=20,
            details='A test perfume'
        )
        self.perfume2 = Perfume.objects.create(
            productID='002',
            name='Sample Scent',
            author='Another Author',
            brand='Another Brand',
            category='Another Category',
            price=75.00,
            inventoryQuantity=15,
            details='Another test perfume'
        )
        self.recommendations = Recommendations.objects.create(
            userID=self.user
        )

    def test_add_to_purchase_history(self):
        # Prueba agregar un perfume al historial de compras
        self.recommendations.add_to_purchase_history(self.perfume1)
        self.assertEqual(len(self.recommendations.purchaseHistory), 1)
        self.assertEqual(self.recommendations.purchaseHistory[0]['name'], 'Eau de Test')

    def test_add_to_browsing_history(self):
        # Prueba agregar un perfume al historial de navegación
        self.recommendations.add_to_browsing_history(self.perfume2)
        self.assertEqual(len(self.recommendations.browsingHistory), 1)
        self.assertEqual(self.recommendations.browsingHistory[0]['name'], 'Sample Scent')

    def test_update_recommendation_list(self):
        # Prueba actualizar la lista de recomendaciones
        new_recommendations = [
            {'name': 'Eau de Test', 'details': 'A test perfume', 'category': 'Test Category', 'brand': 'Test Brand', 'author': 'Test Author'},
            {'name': 'New Scent', 'details': 'A new perfume', 'category': 'New Category', 'brand': 'New Brand', 'author': 'New Author'}
        ]
        self.recommendations.update_recommendation_list(new_recommendations)
        self.assertEqual(len(self.recommendations.recommendationList), 2)
        self.assertIn('New Scent', [rec['name'] for rec in self.recommendations.recommendationList])