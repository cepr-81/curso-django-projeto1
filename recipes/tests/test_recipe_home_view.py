from unittest.mock import patch

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):

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

    def test_per_page_quantity_are_correct(self):

        for i in range(0, 20):
            slug = 'slug-' + str(i)
            title = 'Titulo-' + str(i)
            writer = 'Escritor-' + str(i)
            author = {'username': writer}
            self.make_recipe(title=title, slug=slug, author_data=author)

        response = self.client.get(reverse('recipes:home'))

        page_itens = response.context['recipes'].object_list
        self.assertEqual(len(page_itens), 9)

    def test_except_value_error_on_make_pagination_function(self):

        for i in range(0, 20):
            slug = 'slug-' + str(i)
            title = 'Titulo-' + str(i)
            writer = 'Escritor-' + str(i)
            author = {'username': writer}
            self.make_recipe(title=title, slug=slug, author_data=author)

        response = self.client.get(reverse('recipes:home')+'?page=a')

        self.assertEqual(
            response.context['pagination_range']['current_page'], 1)

    def test_recipe_home_is_paginated(self):
        for i in range(8):
            kwargs = {'slug': f'r{i}', 'author_data': {'username': f'u{i}'}}
            self.make_recipe(**kwargs)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 2)
