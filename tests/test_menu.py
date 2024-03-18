import pytest
from menus._menu import Menu


def test_constructor():
    menu = Menu(["Option 1", "Option 2", "Option 3"], False)
    assert menu.options == ["Option 1", "Option 2", "Option 3", "Back", "Exit"]
    assert menu.is_leaf == False


def test_setters():
    menu = Menu(["Option 1", "Option 2", "Option 3"], False)
    menu.options = ["Option 4", "Option 5", "Option 6"]
    assert menu.options == ["Option 4", "Option 5", "Option 6"]
    menu.is_leaf = True
    assert menu.is_leaf == True


def test_map_options_to_menus():
    menu = Menu(["Option 1", "Option 2", "Option 3"], False)
    # create example sub menus to map the options list to
    sub_menu_1 = Menu(["Sub Option 1", "Sub Option 2"], True)
    sub_menu_2 = Menu(["Sub Option 3", "Sub Option 4"], True)
    sub_menu_3 = Menu(["Sub Option 5", "Sub Option 6"], True)
    sub_menu_list = [sub_menu_1, sub_menu_2, sub_menu_3]
    menu._map_options_to_menus(menu.options, sub_menu_list)
    assert menu.menus == {
        "Option 1": sub_menu_1,
        "Option 2": sub_menu_2,
        "Option 3": sub_menu_3,
    }


def test_display():
    menu = Menu(["Option 1", "Option 2", "Option 3"], False)
    display = menu.display()
    assert display == [
        "1. Option 1",
        "2. Option 2",
        "3. Option 3",
        "4. Back",
        "5. Exit",
    ]


def test_get_choice_numeric_no_leaf():
    menu = Menu(["Option 1", "Option 2", "Option 3"], False)
    choice = menu.get_choice_numeric(1)
    assert choice == 0


def test_get_choice_numeric_leaf():
    menu = Menu(["Option 1", "Option 2", "Option 3"], True)
    choice = menu.get_choice_numeric(1)
    assert choice == "Option 1"
    choice = menu.get_choice_numeric(3)
    assert choice == "Option 3"
    choice = menu.get_choice_numeric(4)
    assert choice == "Back"


def test_back():
    menu = Menu(["Option 1", "Option 2", "Option 3"], False)
    menu.parent = Menu(["Parent Option 1", "Parent Option 2"], False)
    assert menu.back().display()[0] == "1. Parent Option 1"


def test_exit():
    menu = Menu(["Option 1", "Option 2", "Option 3"], False)
    with pytest.raises(SystemExit):
        menu.exit()


def test_handle_choice_leaf():
    menu = Menu(["Option 1", "Option 2", "Option 3"], True)
    choice = menu.handle_choice(1)
    assert choice == "Option 1"


def test_handle_choice_non_leaf():
    menu = Menu(["Option 1", "Option 2", "Option 3"], False)

    sub_menu_1 = Menu(["Sub Option 1", "Sub Option 2"], True)
    sub_menu_2 = Menu(["Sub Option 3", "Sub Option 4"], True)
    sub_menu_3 = Menu(["Sub Option 5", "Sub Option 6"], True)
    sub_menu_list = [sub_menu_1, sub_menu_2, sub_menu_3]
    menu._map_options_to_menus(menu.options, sub_menu_list)

    choice = menu.handle_choice(1)
    assert choice == sub_menu_1


def test_handle_choice_exit():
    menu = Menu(["Option 1", "Option 2", "Option 3"], False)
    # assert that exit quits the program
    with pytest.raises(SystemExit):
        menu.handle_choice(5)


def test_handle_choice_back():
    menu = Menu(["Option 1", "Option 2", "Option 3"], False)
    parent = Menu(["Parent Option 1", "Parent Option 2"], False)
    menu.parent = parent
    assert menu.back().display()[0] == "1. Parent Option 1"
