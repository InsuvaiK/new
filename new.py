import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import PIL
from PIL import Image
from scipy.optimize import fsolve


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
laminar_line_color = 'maroon'
relative_roughness_color = 'black'
interval_arrows_color = 'deepskyblue'
transition_line_color = 'darkgrey'
trans_turbulent_color = 'deepskyblue'
fully_turbulent_color = '#804000'

# Choose which relative roughness lines to plot and the major and minor ticks for the friction factor axis
relative_roughness = [0, 0.00001, 0.00005, 0.0001, 0.0002, 0.0004, 0.0006, 0.0008, 0.001, 0.002, 0.004, 0.006, 0.008,
                      0.01, 0.015, 0.02, 0.03, 0.04, 0.05]
major_ticks = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
minor_ticks = [0.008, 0.009, 0.0125, 0.015, 0.025]

fig, ax = plt.subplots()  # You can do more with figure and axis object

# Plotting the laminar line
Re_lam = np.linspace(64/0.1, 2000, 1000)
Re_critical = np.linspace(2000, 4500, 1000)
ax.set_xscale('log')
ax.set_yscale('log')
ax.plot(Re_lam, 64/Re_lam, color=laminar_line_color)
ax.plot(Re_critical, 64/Re_critical, color=laminar_line_color, ls='--')

# Plotting the relative roughness lines
Re_turbulent = np.linspace(4500, 1e8, 100_000)
f_lamb = lambda Re_, r_: 0.3086/((np.log10(6.9/Re_ + (r_/3.7)**1.11))**2)  # Haaland Equation (p. 10)
for r in relative_roughness:
    f = f_lamb(Re_turbulent, r)
    f_trans = (1/(-1.8*np.log10((r/3.7)**1.11 + 6.9/Re_critical)))**2
    ax.plot(Re_turbulent, f, color=relative_roughness_color)
    ax.plot(Re_critical, f_trans, color=relative_roughness_color, ls='--')
    if r != 0.001:  # This is just to fix the issue with the 0.001 being too close to 0.0008
        ax.annotate(f'{r:.5f}'.rstrip('0'), (1.2e8, np.min(f)), va='center',
                    bbox=dict(facecolor='white', pad=0, edgecolor='white'))
    else:
        ax.annotate(f'{r:.5f}'.rstrip('0'), (1.2e8, np.min(f)),
                    bbox=dict(facecolor='white', pad=0, edgecolor='white'))

# Plotting the transitional line
f_T = lambda r_: 0.3086/(1.11*np.log10(r_/3.7))**2
Re_lamb = lambda Re, r_: 1.011*f_T(r_) - f_lamb(Re, r_)
Re_trans, f_values = [], []
guess = 1e7
for r in np.linspace(relative_roughness[1] - relative_roughness[1]/3, relative_roughness[-1] + relative_roughness[-1]/3,
                     100_000):
    Re_tran = fsolve(Re_lamb, np.array([guess, ]), args=(r,))[0]
    guess = Re_tran
    if Re_tran > 10**8:
        continue
    Re_trans.append(Re_tran)
    f_values.append(1.011*f_T(r))
ax.plot(Re_trans, f_values, color=transition_line_color, ls='-.')

# noinspection PyTypeChecker
ax.fill(Re_trans + [4500, 4500, max(Re_trans)], f_values + [max(f_values), 0.007, 0.007],
        facecolor=trans_turbulent_color, alpha=0.1)
ax.fill(Re_trans + [max(Re_trans), max(Re_trans)], f_values + [max(f_values), min(f_values)],
        facecolor=fully_turbulent_color, alpha=0.1)

# Make the laminar, critical, and turbulent intervals
# For more details on annotate: https://matplotlib.org/1.5.3/users/annotations_guide.html
arrow_style = dict(arrowstyle='<|-|>', connectionstyle='arc3', color=interval_arrows_color, lw=1.5,
                   shrinkB=0, shrinkA=0)  # ShrinkA and shrinkB are set to connect, meaning no space.
bbox_parameter = dict(facecolor='white', edgecolor='white', pad=0)
vertical = 0.088
ax.annotate('', xy=(64/0.1, vertical), xytext=(2000, vertical), arrowprops=arrow_style)
ax.annotate('', xy=(2000, vertical), xytext=(4500, vertical), arrowprops=arrow_style)
ax.annotate('', xy=(4500, vertical), xytext=(1e8, vertical), arrowprops=arrow_style)
ax.annotate('Laminar', xy=(np.sqrt(64/0.1*2000), vertical + 0.002), va='bottom', ha='center', size='small',
            bbox=bbox_parameter)
ax.annotate('Critical', xy=(np.sqrt(2000*4500), vertical + 0.002), va='bottom', ha='center', size='small',
            bbox=bbox_parameter)
ax.annotate('Turbulent', xy=(np.sqrt(4500*1e8), vertical + 0.002), va='bottom', ha='center', size='small',
            bbox=bbox_parameter)

# Grid and Axis Labels
# Do not need to call ax.minorticks_on() if the following gets called:
ax.set_yticks(ticks=major_ticks, labels=[str(i) for i in major_ticks])
ax.set_yticks(ticks=minor_ticks, labels=[str(i) for i in minor_ticks], minor=True)
ax.grid(which='minor', ls='--')
ax.grid(which='major')
ax.set_xlim(np.min(Re_lam), 4e8)
ax.set_ylim(0.007, 0.1)
fig.legend([ax.lines[0], ax.lines[2], ax.lines[-1], ax.patches[0], ax.patches[1]],
           [r'$f=64/Re$', r'$\epsilon/D$', r'Transition Line', 'Transitionally Turbulent', 'Fully Turbulent'], ncol=5,
           loc='upper center')
ax.set_ylabel(r'Friction Factor ($f=-\frac{\partial P}{\partial x}\frac{D}{\rho {V}^2/2}$)')
ax.set_xlabel(r"Reynold's Number ($Re=\frac{\rho VD}{\mu}$)")
ax.set_title('Moody Chart')
fig.tight_layout()

if save_pdf:
    fig.set_size_inches(8.5, 11)
    fig.savefig('vertical_moody_chart.pdf')
    fig.set_size_inches(11, 8.5)
    fig.savefig('horizontal_moody_chart.pdf')
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
