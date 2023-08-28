from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_without_recipes_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes yet! :(', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):

        recipes = self.make_recipe_in_batch()

        title_needed = 'This is what I need'
        recipes[0].title = title_needed
        recipes[0].save()

        # Usuário abre o navegador
        self.browser.get(self.live_server_url)

        # Vê um campo de busca com o texto "Search for a recipe"
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for a recipe..."]'
        )

        # Clica no input e digita o termo de busca

        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        content = self.browser.find_element(By.CLASS_NAME, 'main-content-list')
        self.assertIn(title_needed, content.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self):

        self.make_recipe_in_batch()

        # Usuário abre o navegador
        self.browser.get(self.live_server_url)

        # Vê a paginação e clica na página 2
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )

        page2.click()

        # Vê que tem mais 2 receias na página 2
        recipes_page = self.browser.find_elements(By.CLASS_NAME, 'recipe')
        self.assertEqual(len(recipes_page), 2)
