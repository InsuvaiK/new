import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import PIL
from PIL import Image

st.set_page_config(page_title="Moody's chart",layout='wide')
st.sidebar.title('Contents')
options=st.sidebar.radio('Select one of the following',['Introduction','Calculation of Reynolds number and Friction factor','Plot', 'About the author','Books and references'])

def Intro():
  st.title('Introduction')
  st.markdown('The fluids can be classified into different types based on the variation of the fluid characteristics like velocity, density etc. Depending on the type of flow, the analysis method varies in fluid mechanics. The different types of fluid flow are Steady and Unsteady Flow;Uniform and Non-Uniform Flow;Laminar and Turbulent Flow;Compressible and Incompressible Flow;Rotational and Irrotational Flow;One, Two and Three -dimensional Flow.Of this, we consider Laminar,transition and turbulent flow as the classification of fluid with respect to the flow.')
  st.image('https://i0.wp.com/theconstructor.org/wp-content/uploads/2020/02/laminar-and-turbulent-flow.jpg?resize=345%2C380&ssl=1', caption='Laminar and Turbulent flow')
  st.markdown('Laminar flow is defined as a type of flow in which the fluid particles move along a well-defined streamline or paths, such that all the streamlines are straight and parallel to each other. In a laminar flow, fluid particles move in laminas. The layers in laminar flow glide smoothly over the adjacent layer. The flow is laminar when the Reynolds number is more than 4000.')
  st.markdown('Turbulent flow is a type of flow in which the fluid particles move in a zig-zag manner. The movement in zig-zag manner results in high turbulence and eddies are formed. This results in high energy loss. The flow is turbulent when the Reynolds number is greater than 4000.')
  st.markdown('A fluid flow in a pipe, that has a Reynolds number between 2000 and 4000 is said to be in transition state.')
  st.title("Reynold's Number")
  st.markdown("Reynold's Number is a dimensionless number that determines the type of fluid using the quantities like Velocity,Viscosity,Density and the hydraulic diameter of the pipe. It is the ratio of inertial forces to viscous forces within a fluid that is subjected to relative internal movement due to different fluid velocities.")
  st.image('https://www.gstatic.com/education/formulas2/553212783/en/reynolds_number.svg', caption="Reynold's Number")
  st.title("Friction Factor")
  st.markdown("The friction factor represents the loss of pressure of a fluid in a pipe due to the interactions in between the fluid and the pipe. Friction factor can be Atkinson firction factor(measure of the resistance to airflow of a duct), Darcy friction factor(Fluid dynamics), Fanning friction factor(a dimensionless number used as a local parameter in continuum mechanics).")
  st.image("https://wikimedia.org/api/rest_v1/media/math/render/svg/ab2a101263ff230b3af61e45dddf0610e81a4111", caption = "Friction factor for laminar flow")
  st.image("https://wikimedia.org/api/rest_v1/media/math/render/svg/9c38aa3d81ef35174a961a6fc13a060fec4d2d87", caption = "Friction factor for turbulent flow")

#text input
def Calculation():
  st.title('Calculation of Reynolds number and Friction factor')
  Viscosity = st.number_input("Viscosity of the fluid(Pa.s)",format='%.5f',value=0.001)
  Density = st.number_input("Density(kg/m^3)",format='%.5f',value=997)
  Velocity = st.number_input("Velocity/flow speed(m/s)",format='%.5f',value=1)
  Diameter = st.number_input("Pipe Diameter/Length(m)",format='%.5f',value=0.1)

  Reynolds_number = (Velocity*Density*Diameter)/Viscosity
  st.success(f"The Reynold's number is {Reynolds_number}")

  if Reynolds_number<2000:
     st.write("Laminar flow regime")
  if Reynolds_number>4000:
     st.write("Turbulent flow regime")
  if 2000<Reynolds_number<4000:
     st.write("Transition state/flow regime")
    
  if Reynolds_number<2000:
     Friction_factor = 64/Reynolds_number
  if Reynolds_number>4000:
     Friction_factor = 0.316/((Reynolds_number)**0.25)
  if 2000<Reynolds_number<4000:
     Friction_factor = "uncertain"
  st.success(f"The Friction factor of the flow is {Friction_factor}")

def plots():
  x = Reynolds_number
  y = Friction_factor
  plt.xlabel('Reynolds number')
  plt.ylabel('Friction factor')
  plt.title('Friction factor vs Reynolds Number')
  plt.plot(x, y, marker='o', color="red")
  plt.show()

def Author():
  st.title('About the author')
  st.markdown("I'm Insuvai K, a final year chemical engineering student of Alagappa College of Technology,Anna University. This is my summer break 2023 project on the topic 'Plot between Friction factor and Reynold's number'.")
  st.markdown("Contact: insuvaikumar03@gmail.com")
  st.markdown("LinkedIn Profile: https://www.linkedin.com/in/insuvai-kumar-00b2351b9")
  
def References():
  st.title('References:')
  st.write('1.https://en.wikipedia.org/wiki/Moody_chart#/media/File:Moody_EN.svg')
  st.write('2.https://i0.wp.com/theconstructor.org/wp-content/uploads/2020/02/laminar-and-turbulent-flow.jpg?resize=345%2C380&ssl=1')
  st.write('3.https://theconstructor.org/fluid-mechanics/types-fluid-flow-pipe/38078/')
  st.write('4.https://en.wikipedia.org/wiki/Moody_chart')
  st.write('5.https://en.wikipedia.org/wiki/Reynolds_number')
  st.write('6.https://en.wikipedia.org/wiki/Friction_factor')
           
if options=='Introduction':
   Intro()
if options=='Calculation of Reynolds number and Friction factor':
   Calculation()
if options=='Plots':
   plots()
if options=='About the author':
   Author()
if options=='Books and references':
   References()
