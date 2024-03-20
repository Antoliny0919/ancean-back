from users.tests import APIAdminUserTest, APICommonUserTest

# Create your tests here.

class AdminUserPostViewTest(APIAdminUserTest):
  
  @classmethod
  def setUpTestData(cls):
    super().setUpTestData()
    cls.endpoint = '/api/posts/'
  
  def test_user_create_post(self):
    response = self.__class__.client.post(self.endpoint, self.data, content_type="application/json")
    
    print(response.data)
  
    self.assertEqual(response.status_code, 201)
    
class CommonUserPostViewTest(APICommonUserTest):
  
  @classmethod
  def setUpTestData(cls):
    super().setUpTestData()
    cls.endpoint = '/api/posts/'
  
  def test_user_create_post(self):
    response = self.__class__.client.post(self.endpoint, self.data, content_type="application/json")
    
    print(response.data)
  
    self.assertEqual(response.status_code, 201)
    
    
    
    
    