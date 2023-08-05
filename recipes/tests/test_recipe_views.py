from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeViewTest(RecipeTestBase):

    # View Home Tests

    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'No recipes yet! :(',
            response.content.decode('utf-8')
        )

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))

        content = response.content.decode('utf-8')
        self.assertIn('Recipe Title', content)

        response_context_recipes = response.context['recipes']
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        '''Test to check if do not load recipes with is_published False.'''

        # Make recipe method
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))

        self.assertIn(
            'No recipes yet! :(',
            response.content.decode('utf-8')
        )

    # View Category Tests

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category',
                       kwargs={'category_id': 1000}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        title_for_test = 'This is a category test.'
        self.make_recipe(title=title_for_test)
        response = self.client.get(reverse('recipes:category',
                                           kwargs={'category_id': 1}))

        content = response.content.decode('utf-8')
        self.assertIn(title_for_test, content)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        '''Test to check if do not load recipes with is_published False.'''

        # Make recipe method
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse(
                'recipes:category', kwargs={'category_id': recipe.category_id}
            )
        )

        self.assertEqual(response.status_code, 404)

    # View Detail Tests

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipes(self):
        title_for_test = 'This is a detail page test.'
        self.make_recipe(title=title_for_test)
        response = self.client.get(reverse('recipes:recipe',
                                           kwargs={'id': 1}))

        content = response.content.decode('utf-8')
        self.assertIn(title_for_test, content)

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        '''Test to check if do not load recipes with is_published False.'''

        # Make recipe method
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:recipe',
                                           kwargs={'id': recipe.id}))

        self.assertEqual(response.status_code, 404)

    def test_recipe_search_uses_correct_view_function(self):
        url = reverse('recipes:search')
        view = resolve(url)
        self.assertIs(view.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
