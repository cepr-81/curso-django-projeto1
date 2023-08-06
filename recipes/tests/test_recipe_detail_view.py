from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):

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
