from aiogram.fsm.state import State, StatesGroup

# saves rentals and slots for regular user
class FSMRegularUser(StatesGroup):
    choosing_rental_number = State()
    choosing_slot_page = State()
