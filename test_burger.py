import pytest
from unittest.mock import Mock
from praktikum.bun import Bun
from praktikum.ingredient import Ingredient
from praktikum.burger import Burger
from praktikum.ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING
from data import *

class TestBurger:


    @pytest.mark.parametrize("bun_list", BUNS_LIST
)
    def test_set_buns_with_bun_list_successfully(self,bun_list):
        burger = Burger()

        buns = []
        for name, price in bun_list:
            bun = Bun(name, price)
            buns.append(bun)

        burger.set_buns(buns)

        assert burger.bun == buns


    @pytest.mark.parametrize("ingredient_type, ingredient_name, ingredient_price", ADD_INGREDIENTS_DATA)
    def test_add_ingredient_type_successfully(self, ingredient_type, ingredient_name, ingredient_price):
        burger = Burger()

        ingredient = Ingredient(ingredient_type, ingredient_name, ingredient_price)

        burger.add_ingredient(ingredient)

        assert len(burger.ingredients) == 1

        added_ingredient = burger.ingredients[0]

        assert added_ingredient.get_type() == ingredient_type

    @pytest.mark.parametrize("ingredient_type, ingredient_name, ingredient_price", ADD_INGREDIENTS_DATA)
    def test_add_ingredient_name_successfully(self, ingredient_type, ingredient_name, ingredient_price):

        burger = Burger()

        ingredient = Ingredient(ingredient_type, ingredient_name, ingredient_price)

        burger.add_ingredient(ingredient)

        assert len(burger.ingredients) == 1

        added_ingredient = burger.ingredients[0]

        assert added_ingredient.get_name() == ingredient_name


    @pytest.mark.parametrize("ingredient_type, ingredient_name, ingredient_price", ADD_INGREDIENTS_DATA)
    def test_add_ingredient_price_successfully(self, ingredient_type, ingredient_name, ingredient_price):
        burger = Burger()

        ingredient = Ingredient(ingredient_type, ingredient_name, ingredient_price)

        burger.add_ingredient(ingredient)

        assert len(burger.ingredients) == 1

        added_ingredient = burger.ingredients[0]

        assert added_ingredient.get_price() == ingredient_price



    @pytest.mark.parametrize("index_to_remove, expected_count", REMOVE_TEST_DATA)
    def test_remove_ingredient_successfully(self, index_to_remove, expected_count):

        burger = Burger()

        sauce1 = Ingredient(INGREDIENT_TYPE_SAUCE, "Соус фирменный Space Sauce", 80.0)
        filling1 = Ingredient(INGREDIENT_TYPE_FILLING, "Филе Люминесцентного тетраодонтимформа", 988)
        sauce2 = Ingredient(INGREDIENT_TYPE_SAUCE, "Соус с шипами Антарианского плоскоходца", 88)

        burger.add_ingredient(sauce1)
        burger.add_ingredient(filling1)
        burger.add_ingredient(sauce2)

        assert len(burger.ingredients) == 3

        burger.remove_ingredient(index_to_remove)

        assert len(burger.ingredients) == expected_count

    def test_remove_ingredient_empty_list_error(self):

        burger = Burger()

        assert len(burger.ingredients) == 0

        with pytest.raises(IndexError):
            burger.remove_ingredient(2)

    def test_remove_large_index_from_small_list_error(self):

        burger = Burger()

        sauce1 = Ingredient(INGREDIENT_TYPE_SAUCE, "Соус фирменный Space Sauce", 80)
        filling1 = Ingredient(INGREDIENT_TYPE_FILLING, "Филе Люминесцентного тетраодонтимформа", 988)
        sauce2 = Ingredient(INGREDIENT_TYPE_SAUCE, "Соус с шипами Антарианского плоскоходца", 88)

        burger.add_ingredient(sauce1)
        burger.add_ingredient(filling1)
        burger.add_ingredient(sauce2)

        assert len(burger.ingredients) == 3

        with pytest.raises(IndexError):
            burger.remove_ingredient(7)


    @pytest.mark.parametrize(
        "index,new_index,expected_order",
        MOVE_TEST_DATA
    )
    def test_move_ingredient_successfully(self, index, new_index, expected_order):

        burger = Burger()

        sauce1 = Ingredient(INGREDIENT_TYPE_SAUCE, "Соус фирменный Space Sauce", 80)
        filling1 = Ingredient(INGREDIENT_TYPE_FILLING, "Филе Люминесцентного тетраодонтимформа", 988)
        sauce2 = Ingredient(INGREDIENT_TYPE_SAUCE, "Соус с шипами Антарианского плоскоходца", 88)

        burger.add_ingredient(sauce1)
        burger.add_ingredient(filling1)
        burger.add_ingredient(sauce2)

        original_names = [ing.name for ing in burger.ingredients]
        
        burger.move_ingredient(index, new_index)
        
        current_names = [ing.name for ing in burger.ingredients]
        
        assert len(burger.ingredients) == 3
        
        assert set(current_names) == set(original_names)
        
        expected_names = [
            "Соус фирменный Space Sauce",
            "Филе Люминесцентного тетраодонтимформа",
            "Соус с шипами Антарианского плоскоходца"
        ]
        
        for i, expected_name in enumerate(expected_order):
            assert current_names[i] == expected_names[expected_order[i]]


    @pytest.mark.parametrize(
        "index,new_index",
        INVALID_MOVE_TEST_DATA
    )
    def test_move_ingredient_with_invalid_indices_error(self, index, new_index):

        burger = Burger()

        sauce1 = Ingredient(INGREDIENT_TYPE_SAUCE, "Соус фирменный Space Sauce", 80)
        filling1 = Ingredient(INGREDIENT_TYPE_FILLING, "Филе Люминесцентного тетраодонтимформа", 988)
        sauce2 = Ingredient(INGREDIENT_TYPE_SAUCE, "Соус с шипами Антарианского плоскоходца", 88)

        burger.add_ingredient(sauce1)
        burger.add_ingredient(filling1)
        burger.add_ingredient(sauce2)

        original_names = [ing.name for ing in burger.ingredients]

        assert [ing.name for ing in burger.ingredients] == original_names


    def test_get_price_only_buns_successfully(self):

        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_price.return_value = 50.0
        burger.bun = mock_bun
        burger.ingredients = []

        price = burger.get_price()

        assert price == 100.0  
        mock_bun.get_price.assert_called_once()

    @pytest.mark.parametrize(
        "bun_price,ingredients_data,expected_price",VARIOUS_INGREDIENTS
    )
    def test_get_price_with_various_ingredients_successfully(self, bun_price, ingredients_data, expected_price):

        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_price.return_value = bun_price
        burger.bun = mock_bun

        mock_ingredients = []
        for price, name in ingredients_data:
            mock_ingredient = Mock()
            mock_ingredient.get_price.return_value = price
            mock_ingredients.append(mock_ingredient)
        burger.ingredients = mock_ingredients

        price = burger.get_price()

        assert price == expected_price

        for mock_ingredient in mock_ingredients:
            mock_ingredient.get_price.assert_called_once()

        mock_bun.get_price.assert_called_once()


    def test_get_price_negative_prices_error(self):

        burger = Burger()
        mock_bun = Mock()
        mock_bun.get_price.return_value = -20.0
        burger.bun = mock_bun

        mock_ingredient = Mock()
        mock_ingredient.get_price.return_value = -50.0
        burger.ingredients = [mock_ingredient]

        price = burger.get_price()
        assert price == -90.0  



    def test_get_price_no_bun_error(self):

        burger = Burger()
        burger.bun = None
        burger.ingredients = []

        with pytest.raises(AttributeError):
            burger.get_price()

    def test_get_receipt_empty_burger_successfully(self):
        burger = Burger()
        
        # Создаем мок для булочки
        mock_bun = Mock()
        mock_bun.get_name.return_value = "Флюоресцентная булка R2-D3"
        burger.bun = mock_bun
        
        burger.ingredients = []
        
        burger.get_price = Mock(return_value=988)
        
        receipt = burger.get_receipt()
        
        expected_receipt = (
            "(==== Флюоресцентная булка R2-D3 ====)\n"
            "(==== Флюоресцентная булка R2-D3 ====)\n"
            "\n"
            "Price: 988"
        )
        
        assert receipt == expected_receipt

    @pytest.mark.parametrize(
        "bun_name,ingredients_data,expected_price,expected_lines",
        RECEIPT_DATA
    )
    def test_get_receipt_with_ingredients_successfully(self, bun_name, ingredients_data, expected_price, expected_lines):

        burger = Burger()

        mock_bun = Mock()
        mock_bun.get_name.return_value = bun_name
        burger.bun = mock_bun

        mock_ingredients = []
        for ingredient_type, ingredient_name in ingredients_data:
            mock_ingredient = Mock()
            mock_ingredient.get_type.return_value = ingredient_type
            mock_ingredient.get_name.return_value = ingredient_name
            mock_ingredients.append(mock_ingredient)
        burger.ingredients = mock_ingredients

        burger.get_price = Mock(return_value=expected_price)

        receipt = burger.get_receipt()
        expected = "\n".join(expected_lines)

        assert receipt == expected

    def test_get_receipt_no_bun_error(self):

        burger = Burger()
        burger.bun = None
        burger.ingredients = []

        with pytest.raises(AttributeError):
            burger.get_receipt()

