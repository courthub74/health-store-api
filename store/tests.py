from rest_framework.test import APITestCase

from store.models import Product


#PRODUCT CREATE
class ProductCreateTestCase(APITestCase):
	def test_create_product(self):
		initial_product_count = Product.objects.count()  #Keep track of initial product count
		product_attrs = {  #Create new product
			'name': 'New Product',
			'description': 'Awesome product',
			'price': '123.45',
		}
		response = self.client.post('/api/v1/products/new', product_attrs) #Check response from the client
		if response.status_code != 201:  #If can't create a new product
			print(response.data) #Print the response
		self.assertEqual( #Make sure new product created 
			Product.objects.count(), #by checking the count of all products
			initial_product_count + 1, #against the initial product count
		)
		for attr, expected_value in product_attrs.items(): #Check the values set for the product
			self.assertEqual(response.data[attr], expected_value) #Check for value exactness
		self.assertEqual(response.data['is_on_sale'], False) #Check values for custom fields
		self.assertEqual( #Check values for custom fields
 			response.data['current_price'],
			float(product_attrs['price'])
			)

#PRODUCT DESTROY
class ProductDestroyTestCase(APITestCase):
	def test_delete_product(self):
		initial_product_count = Product.objects.count()
		product_id = Product.objects.first().id 
		self.client.delete('/api/v1/products/{}/'.format(product_id))
		self.assertEqual(
			Product.objects.count(),
			initial_product_count -1,
		)
		self.assertRaises(
			Product.DoesNotExist,
			Product.objects.get, id=product_id,
		)


#PRODUCT LIST
class ProductListTestCase(APITestCase):
	def test_list_products(self):
		products_count = Product.objects.count()
		response = self.client.get('/api/v1/products/')
		self.assertIsNone(response.data['next'])
		self.assertIsNone(response.data['previous'])
		self.assertEqual(response.data['count'], products_count)
		self.assertEqual(len(response.data['results']), products_count)


#UPDATE PRODUCT
class ProductUpdateTestCase(APITestCase):
	def test_update_product(self):
		product = Product.objects.first()
		response = self.client.patch(
			'/api/v1/products/'.format(product.id),
			{
				'name': 'New Product',
				'description': 'Awesome Product',
				'price': 123.45,
			},
			format='json',
		)
		updated = Product.objects.get(id=product.id)
		self.assertEqual(updated.name, 'Mineral Water Strawberry') #My v1 is actually v3 I deleted v1 doing something else