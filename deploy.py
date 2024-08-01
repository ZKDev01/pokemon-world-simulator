import streamlit as st

IMAGE_PATH = 'assets/{number}.gif'
TARGET = 0

def increase_counter () -> None:
  global TARGET
  TARGET += 1
  
  if 0 <= TARGET and TARGET <= 10:
    st.image(IMAGE_PATH.format( number = TARGET ))

def decrease_counter () -> None:
  global TARGET
  TARGET -= 1

  if 0 <= TARGET and TARGET <= 151:
    st.image(IMAGE_PATH.format( number = TARGET ))


st.title( "Pokemon World Simulator" )

increase_button = st.button( "Next" )
decrease_button = st.button( "Previous" )


while True:

  if increase_button:
    increase_counter()
  

  if decrease_button:
    decrease_counter()

  st.write( f"TARGET: { TARGET }" )
