from aiogram.fsm.state import State, StatesGroup

# saves regular user choice of rentals and slots
class FSMRegularUser(StatesGroup):
    choosing_rental_number = State()
    choosing_slot_page = State()
    # choosing_rental_with_record = State()

