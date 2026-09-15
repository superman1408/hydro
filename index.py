import math
import matplotlib.pyplot as plt

# Define constants ------------------------------------------------------------------------------------
constant = {
    "g": 9.81,  # Acceleration due to gravity (m/s^2)
    "p0": 101325,  # Atmospheric pressure at sea level (Pa)
    "rho_water": 1000,  # Density of water (kg/m^3)
    "rho_air": 1.225,  # Density of air (kg/m^3)
    "rho_ice": 917,  # Density of ice (kg/m^3)
    "rho_seawater": 1025,  # Density of seawater (kg/m^3)
}



# ----------------Checks-------------------------------------------------------------------------------------------

def connection_check():
    try:
        import math
        import matplotlib.pyplot as plt
        print("All required libraries are installed and imported successfully.")
    except ImportError as e:
        print(f"An error occurred while importing libraries: {e}")
        raise ImportError("Please ensure that all required libraries are installed.")


# def wave_number_with_circular_frequency_check(circular_Frequency_omega, wave_Number_k):
#     if (circular_Frequency_omega ** 2 / constant["g"] == wave_Number_k * math.tanh(wave_Number_k * average_Water_Depth_h)):
#         print("The wave number and circular frequency satisfy the dispersion relation.")
#     else:
#         print("The wave number and circular frequency do not satisfy the dispersion relation.")
#         # raise ValueError("Please check the values of wave number and circular frequency.")
        


def wave_number_with_circular_frequency_check(circular_Frequency_omega, wave_Number_k, average_Water_Depth_h):

    left_side = (
        circular_Frequency_omega ** 2
        / constant["g"]
    )

    right_side = (
        wave_Number_k
        * math.tanh(
            wave_Number_k * average_Water_Depth_h
        )
    )

    tolerance = 1e-6

    if abs(left_side - right_side) < tolerance:

        print(
            "The wave number and circular frequency "
            "satisfy the dispersion relation."
        )

    else:

        print(
            "The wave number and circular frequency "
            "do not satisfy the dispersion relation."
        )

    print("Left side  (ω²/g):", left_side)
    print("Right side (k tanh(kh)):", right_side)
    print("Difference:", abs(left_side - right_side))


# def wave_length_with_wave_period_check(wave_Length_lamda, wave_Period_T, circular_Frequency_omega, wave_Number_k):
#     if (wave_Length_lamda == constant["g"] / 2 * math.pi * wave_Period_T ** 2 * math.tanh(2 * math.pi * average_Water_Depth_h / wave_Length_lamda)):
#         print("The wave length and wave period satisfy the dispersion relation.")
#     else:
#         print("The wave length and wave period do not satisfy the dispersion relation.")
#         # raise ValueError("Please check the values of wave length and wave period.")



def wave_length_with_wave_period_check(wave_Length_lamda, wave_Period_T, average_Water_Depth_h):
    left_side = wave_Length_lamda

    right_side = (
        constant["g"]
        * wave_Period_T ** 2
        / (2 * math.pi)
        * math.tanh(
            2 * math.pi
            * average_Water_Depth_h
            / wave_Length_lamda
        )
    )

    tolerance = 1e-6

    if abs(left_side - right_side) < tolerance:

        print(
            "The wave length and wave period "
            "satisfy the dispersion relation."
        )

    else:

        print(
            "The wave length and wave period "
            "do not satisfy the dispersion relation."
        )

    print("Left side  (λ):", left_side)
    print("Right side:", right_side)
    print("Difference:", abs(left_side - right_side))




# Wave profile calculation
x_values = []
eta_values = []


# All functions are defined here -----------------------------------------------------------------------

# velocity potential for finite depth
def velocity_Potential_finiteDepth(wave_Amplitude_zita, wave_Number_k, circular_Frequency_omega, vertical_coordinate_z, average_Water_Depth_h, direction_of_Wave_Propagation, horizontal_coordinate_x=0, time_t=0):
    try:
        if direction_of_Wave_Propagation == "x":
            velocity_Potential_phi = (wave_Amplitude_zita * constant["g"] / circular_Frequency_omega) * math.cosh(wave_Number_k * (vertical_coordinate_z + average_Water_Depth_h)) / math.cosh(wave_Number_k * average_Water_Depth_h) * math.cos(circular_Frequency_omega * time_t - wave_Number_k * horizontal_coordinate_x)
        elif direction_of_Wave_Propagation == "y":
            velocity_Potential_phi = (wave_Amplitude_zita * constant["g"] / circular_Frequency_omega) * math.cosh(wave_Number_k * (vertical_coordinate_z + average_Water_Depth_h)) / math.cosh(wave_Number_k * average_Water_Depth_h) * math.cos(circular_Frequency_omega * time_t - wave_Number_k * horizontal_coordinate_x)
    except Exception as e:
        print(f"An error occurred: {e}")
        raise ValueError("Invalid direction of wave propagation. Please enter 'x' or 'y'.")
    return velocity_Potential_phi

# velocity potential for deep water waves 
def velocity_Potential_deepWater(wave_Amplitude_zita, wave_Number_k, circular_Frequency_omega, vertical_coordinate_z, average_Water_Depth_h, direction_of_Wave_Propagation, horizontal_coordinate_x=0, time_t=0):
    try :
        if direction_of_Wave_Propagation == "x":
            velocity_Potential_phi = (wave_Amplitude_zita * constant["g"] / circular_Frequency_omega) * math.exp(wave_Number_k * vertical_coordinate_z) * math.cos(circular_Frequency_omega * time_t - wave_Number_k * horizontal_coordinate_x)
        elif direction_of_Wave_Propagation == "y":
            velocity_Potential_phi = (wave_Amplitude_zita * constant["g"] / circular_Frequency_omega) * math.exp(wave_Number_k * vertical_coordinate_z) * math.cos(circular_Frequency_omega * time_t - wave_Number_k * horizontal_coordinate_x)
        else:
            raise ValueError("Invalid direction of wave propagation. Please enter 'x' or 'y'.")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise ValueError("Invalid direction of wave propagation. Please enter 'x' or 'y'.")
    return velocity_Potential_phi

# Calculate angular frequency and wave number
def angular_Frequency(wave_Period_T):
    circular_Frequency_omega = (2 * math.pi) / wave_Period_T
    return circular_Frequency_omega

# Calculate wave number 
def wave_Number(wave_Length_lamda):
    wave_Number_k = (2 * math.pi) / wave_Length_lamda
    return wave_Number_k

# Determine the vertical coordinate movement direction
def vertical_coordinate_movement_direction(vertical_coordinate_z, average_Water_Depth_h):
    match vertical_coordinate_z:
        case z if z < 0:
            return "below mean water surface / sea level"
        case z if z == 0:
            return "water surface/sea level"
        case z if z > 0:
            return "above mean water surface / sea level"
        case _:
            return "unknown"
        


# calculate wave profile
def wave_Profile(wave_Amplitude_zita, wave_Number_k, circular_Frequency_omega, horizontal_coordinate_x, time_t):
    wave_Profile_eta = wave_Amplitude_zita * math.sin(circular_Frequency_omega * time_t - wave_Number_k * horizontal_coordinate_x)
    return wave_Profile_eta



def calculate_wave_profile(wave_Amplitude_zita, wave_Number_k, circular_Frequency_omega, time_t, wavelength):
    x_values = []
    eta_values = []

    for x in range(0, int(wavelength) + 1):
        eta = wave_Profile(
            wave_Amplitude_zita,
            wave_Number_k,
            circular_Frequency_omega,
            x,
            time_t
        )

        x_values.append(x)
        eta_values.append(eta)

    return x_values, eta_values



def dynamic_Pressure_finiteDepth(fluid_density_rho, wave_Amplitude_zita, wave_Number_k, circular_Frequency_omega, vertical_coordinate_z, average_Water_Depth_h, horizontal_coordinate_x,time_t):
    dynamic_Pressure_finiteDepth = (
        fluid_density_rho
        * constant["g"]
        * wave_Amplitude_zita
        * math.cosh(
            wave_Number_k * (vertical_coordinate_z + average_Water_Depth_h)
        )
        / math.cosh(
            wave_Number_k * average_Water_Depth_h
        )
        * math.sin(
            circular_Frequency_omega * time_t
            - wave_Number_k * horizontal_coordinate_x
        )
    )

    return dynamic_Pressure_finiteDepth



def dynamic_Pressure_deepWater(fluid_density_rho, wave_Amplitude_zita, wave_Number_k, circular_Frequency_omega, vertical_coordinate_z, average_Water_Depth_h, horizontal_coordinate_x,time_t):
    dynamic_Pressure_deepWater = (
        fluid_density_rho
        * constant["g"]
        * wave_Amplitude_zita
        * math.exp(wave_Number_k * vertical_coordinate_z)
        * math.sin(
            circular_Frequency_omega * time_t
            - wave_Number_k * horizontal_coordinate_x
        )
    )

    return dynamic_Pressure_deepWater



# -------------------------Calculate velocity components for finite depth waves---------------------------------------------------------------


def calculate_finiteDepth_velocity_components_x(velocity_Potential_phi, wave_Number_k, circular_Frequency_omega, direction_of_Wave_Propagation):
    if direction_of_Wave_Propagation == "x":
        u = (wave_Amplitude_zita * circular_Frequency_omega) * math.cosh(wave_Number_k * (vertical_coordinate_z + average_Water_Depth_h)) / math.sinh(wave_Number_k * average_Water_Depth_h) * math.sin(circular_Frequency_omega * time_t - wave_Number_k * horizontal_coordinate_x)
        v = 0
    elif direction_of_Wave_Propagation == "y":
        u = 0
        v = (wave_Amplitude_zita * circular_Frequency_omega) * math.cosh(wave_Number_k * (vertical_coordinate_z + average_Water_Depth_h)) / math.sinh(wave_Number_k * average_Water_Depth_h) * math.sin(circular_Frequency_omega * time_t - wave_Number_k * horizontal_coordinate_x)
    else:
        raise ValueError("Invalid direction of wave propagation. Please enter 'x' or 'y'.")

    return u, v



def calculate_finiteDepth_velocity_components_z(velocity_Potential_phi, wave_Number_k, circular_Frequency_omega, direction_of_Wave_Propagation):
    if direction_of_Wave_Propagation == "x":
        u = (wave_Amplitude_zita * circular_Frequency_omega) * math.sinh(wave_Number_k * (vertical_coordinate_z + average_Water_Depth_h)) / math.sinh(wave_Number_k * average_Water_Depth_h) * math.cos(circular_Frequency_omega * time_t - wave_Number_k * horizontal_coordinate_x)
        v = 0
    elif direction_of_Wave_Propagation == "y":
        u = 0
        v = (wave_Amplitude_zita * circular_Frequency_omega) * math.sinh(wave_Number_k * (vertical_coordinate_z + average_Water_Depth_h)) / math.sinh(wave_Number_k * average_Water_Depth_h) * math.cos(circular_Frequency_omega * time_t - wave_Number_k * horizontal_coordinate_x)
    else:
        raise ValueError("Invalid direction of wave propagation. Please enter 'x' or 'y'.")

    return u, v



def calculate_deepWater_velocity_components_x(velocity_Potential_phi, wave_Number_k, circular_Frequency_omega, direction_of_Wave_Propagation):
    if direction_of_Wave_Propagation == "x":
        u = (wave_Amplitude_zita * circular_Frequency_omega) * math.exp(wave_Number_k * vertical_coordinate_z) * math.sin(circular_Frequency_omega * time_t - wave_Number_k * horizontal_coordinate_x)
        v = 0
    elif direction_of_Wave_Propagation == "y":
        u = 0
        v = (wave_Amplitude_zita * circular_Frequency_omega) * math.exp(wave_Number_k * vertical_coordinate_z) * math.sin(circular_Frequency_omega * time_t - wave_Number_k * horizontal_coordinate_x)
    else:
        raise ValueError("Invalid direction of wave propagation. Please enter 'x' or 'y'.")

    return u, v



def calculate_deepWater_velocity_components_z(velocity_Potential_phi, wave_Number_k, circular_Frequency_omega, direction_of_Wave_Propagation):
    if direction_of_Wave_Propagation == "x":
        u = (wave_Amplitude_zita * circular_Frequency_omega) * math.exp(wave_Number_k * vertical_coordinate_z) * math.cos(circular_Frequency_omega * time_t - wave_Number_k * horizontal_coordinate_x)
        v = 0
    elif direction_of_Wave_Propagation == "y":
        u = 0
        v = (wave_Amplitude_zita * circular_Frequency_omega) * math.exp(wave_Number_k * vertical_coordinate_z) * math.cos(circular_Frequency_omega * time_t - wave_Number_k * horizontal_coordinate_x)
    else:
        raise ValueError("Invalid direction of wave propagation. Please enter 'x' or 'y'.")

    return u, v


# --------------------X components of acceleration for finite depth waves---------------------------------------------------------------

def calculate_finiteDepth_acceleration_components_x(velocity_Potential_phi, wave_Number_k, circular_Frequency_omega, direction_of_Wave_Propagation):
    if direction_of_Wave_Propagation == "x":
        u = (wave_Amplitude_zita * circular_Frequency_omega ** 2) * math.cosh(wave_Number_k * (vertical_coordinate_z + average_Water_Depth_h)) / math.sinh(wave_Number_k * average_Water_Depth_h) * math.cos(circular_Frequency_omega * time_t - wave_Number_k * horizontal_coordinate_x)
        v = 0
    elif direction_of_Wave_Propagation == "y":
        u = 0
        v = (wave_Amplitude_zita * circular_Frequency_omega ** 2) * math.cosh(wave_Number_k * (vertical_coordinate_z + average_Water_Depth_h)) / math.sinh(wave_Number_k * average_Water_Depth_h) * math.cos(circular_Frequency_omega * time_t - wave_Number_k * horizontal_coordinate_x)
    else:
        raise ValueError("Invalid direction of wave propagation. Please enter 'x' or 'y'.")

    return u, v



def calculate_finiteDepth_acceleration_components_z(velocity_Potential_phi, wave_Number_k, circular_Frequency_omega, direction_of_Wave_Propagation):
    if direction_of_Wave_Propagation == "x":
        u = (wave_Amplitude_zita * circular_Frequency_omega ** 2) * math.sinh(wave_Number_k * (vertical_coordinate_z + average_Water_Depth_h)) / math.sinh(wave_Number_k * average_Water_Depth_h) * math.sin(circular_Frequency_omega * time_t - wave_Number_k * horizontal_coordinate_x)
        v = 0
    elif direction_of_Wave_Propagation == "y":
        u = 0
        v = (wave_Amplitude_zita * circular_Frequency_omega ** 2) * math.sinh(wave_Number_k * (vertical_coordinate_z + average_Water_Depth_h)) / math.sinh(wave_Number_k * average_Water_Depth_h) * math.sin(circular_Frequency_omega * time_t - wave_Number_k * horizontal_coordinate_x)
    else:
        raise ValueError("Invalid direction of wave propagation. Please enter 'x' or 'y'.")

    return u, v



def calculate_deepWater_acceleration_components_x(velocity_Potential_phi, wave_Number_k, circular_Frequency_omega, direction_of_Wave_Propagation):
    if direction_of_Wave_Propagation == "x":
        u = (wave_Amplitude_zita * circular_Frequency_omega ** 2) * math.exp(wave_Number_k * vertical_coordinate_z) * math.cos(circular_Frequency_omega * time_t - wave_Number_k * horizontal_coordinate_x)
        v = 0
    elif direction_of_Wave_Propagation == "y":
        u = 0
        v = (wave_Amplitude_zita * circular_Frequency_omega ** 2) * math.exp(wave_Number_k * vertical_coordinate_z) * math.cos(circular_Frequency_omega * time_t - wave_Number_k * horizontal_coordinate_x)
    else:
        raise ValueError("Invalid direction of wave propagation. Please enter 'x' or 'y'.")

    return u, v



def calculate_deepWater_acceleration_components_z(velocity_Potential_phi, wave_Number_k, circular_Frequency_omega, direction_of_Wave_Propagation):
    if direction_of_Wave_Propagation == "x":
        u = (wave_Amplitude_zita * circular_Frequency_omega ** 2) * math.exp(wave_Number_k * vertical_coordinate_z) * math.sin(circular_Frequency_omega * time_t - wave_Number_k * horizontal_coordinate_x)
        v = 0
    elif direction_of_Wave_Propagation == "y":
        u = 0
        v = (wave_Amplitude_zita * circular_Frequency_omega ** 2) * math.exp(wave_Number_k * vertical_coordinate_z) * math.sin(circular_Frequency_omega * time_t - wave_Number_k * horizontal_coordinate_x)
    else:
        raise ValueError("Invalid direction of wave propagation. Please enter 'x' or 'y'.")

    return u, v


# Main program ----------------------------------------------------------------------------------------------------------------
print("Welcome to the program.")
print("This program will help you calculate the Velocity Potential, Wave Profile, Dynamic Pressure, X and Y components of Velocity and acceleration of a wave.")

# Get user input ---------------------------------------------------------------------
wave_Length_lamda = float(input("What is the wavelength of the wave? "))
wave_Period_T = float(input("What is the wave period? "))
wave_Amplitude_zita = float(input("What is the wave amplitude? "))
average_Water_Depth_h = float(input("What is the average water depth? "))
direction_of_Wave_Propagation = input("What is the direction of wave propagation? (Enter 'x' or 'y'): ")
vertical_coordinate_z = float(input("What is the vertical coordinate? (Enter z): "))
horizontal_coordinate_x = float(input("What is the horizontal coordinate? (Enter x): "))
time_t = float(input("What is the time? (Enter t): "))



# Calculate angular frequency, wave number, vertical coordinate movement direction, and velocity potential ----------------------------------
circular_Frequency_omega = angular_Frequency(wave_Period_T)
wave_Number_k = wave_Number(wave_Length_lamda)
vertical_coordinate_movement_direction_result = vertical_coordinate_movement_direction(vertical_coordinate_z, average_Water_Depth_h)
velocity_Potential_phi_deepWater = velocity_Potential_deepWater(wave_Amplitude_zita, wave_Number_k, circular_Frequency_omega, vertical_coordinate_z, average_Water_Depth_h, direction_of_Wave_Propagation, horizontal_coordinate_x, time_t)
velocity_Potential_phi_finiteDepth = velocity_Potential_finiteDepth(wave_Amplitude_zita, wave_Number_k, circular_Frequency_omega, vertical_coordinate_z, average_Water_Depth_h, direction_of_Wave_Propagation, horizontal_coordinate_x, time_t)
wave_Profile_eta = wave_Profile(wave_Amplitude_zita, wave_Number_k, circular_Frequency_omega, horizontal_coordinate_x, time_t)
x_values, eta_values = calculate_wave_profile(wave_Amplitude_zita, wave_Number_k, circular_Frequency_omega, time_t, wave_Length_lamda)
dynamic_Pressure_p_finiteDepth = dynamic_Pressure_finiteDepth(constant["rho_seawater"], wave_Amplitude_zita, wave_Number_k, circular_Frequency_omega, vertical_coordinate_z, average_Water_Depth_h, horizontal_coordinate_x,time_t)
dynamic_Pressure_p_deepWater = dynamic_Pressure_deepWater(constant["rho_seawater"], wave_Amplitude_zita, wave_Number_k, circular_Frequency_omega, vertical_coordinate_z, average_Water_Depth_h, horizontal_coordinate_x,time_t)
x_components_velocity_finiteDepth = calculate_finiteDepth_velocity_components_x(velocity_Potential_phi_finiteDepth, wave_Number_k, circular_Frequency_omega, direction_of_Wave_Propagation)
z_components_velocity_finiteDepth = calculate_finiteDepth_velocity_components_z(velocity_Potential_phi_finiteDepth, wave_Number_k, circular_Frequency_omega, direction_of_Wave_Propagation)
x_components_velocity_deepWater = calculate_deepWater_velocity_components_x(velocity_Potential_phi_deepWater, wave_Number_k, circular_Frequency_omega, direction_of_Wave_Propagation)
z_components_velocity_deepWater = calculate_deepWater_velocity_components_z(velocity_Potential_phi_deepWater, wave_Number_k, circular_Frequency_omega, direction_of_Wave_Propagation)

x_components_acceleration_finiteDepth = calculate_finiteDepth_acceleration_components_x(velocity_Potential_phi_finiteDepth, wave_Number_k, circular_Frequency_omega, direction_of_Wave_Propagation)
z_components_acceleration_finiteDepth = calculate_finiteDepth_acceleration_components_z(velocity_Potential_phi_finiteDepth, wave_Number_k, circular_Frequency_omega, direction_of_Wave_Propagation)
x_components_acceleration_deepWater = calculate_deepWater_acceleration_components_x(velocity_Potential_phi_deepWater, wave_Number_k, circular_Frequency_omega, direction_of_Wave_Propagation)
z_components_acceleration_deepWater = calculate_deepWater_acceleration_components_z(velocity_Potential_phi_deepWater, wave_Number_k, circular_Frequency_omega, direction_of_Wave_Propagation)

check_connection = connection_check()
check_wave_number_with_circular_frequency = wave_number_with_circular_frequency_check(circular_Frequency_omega, wave_Number_k, average_Water_Depth_h)
check_wave_length_with_wave_period = wave_length_with_wave_period_check(wave_Length_lamda, wave_Period_T, average_Water_Depth_h)


# Print the results ---------------------------------------------------------------------------------------------------------
print("The Circular frequency of the wave is (ω): ", circular_Frequency_omega, " rad/s")
print("The wave number of the wave is (k): ", wave_Number_k, " rad/m")
print("The vertical coordinate movement direction is: ", vertical_coordinate_movement_direction_result)
print("Atmospheric pressure at sea level (p0): ", constant["p0"], "Pa")
print("Acceleration due to gravity (g): ", constant["g"], "m/s^2")
print("The velocity potential (φ) of the wave in deep water is: ", velocity_Potential_phi_deepWater, " m^2/s")
print("The velocity potential (φ) of the wave in finite depth is: ", velocity_Potential_phi_finiteDepth, " m^2/s")
print("The wave profile (η) of the wave is: ", wave_Profile_eta, " m")
print("The dynamic pressure (p) of the wave in finite depth is: ", dynamic_Pressure_p_finiteDepth, " Pa")
print("The dynamic pressure (p) of the wave in deep water is: ", dynamic_Pressure_p_deepWater, " Pa")
print("The x-component of velocity in finite depth is: ", x_components_velocity_finiteDepth, " m/s")
print("The z-component of velocity in finite depth is: ", z_components_velocity_finiteDepth, " m/s")
print("The x-component of velocity in deep water is: ", x_components_velocity_deepWater, " m/s")
print("The z-component of velocity in deep water is: ", z_components_velocity_deepWater, " m/s")
print("The x-component of acceleration in finite depth is: ", x_components_acceleration_finiteDepth, " m/s^2")
print("The z-component of acceleration in finite depth is: ", z_components_acceleration_finiteDepth, " m/s^2")
print("The x-component of acceleration in deep water is: ", x_components_acceleration_deepWater, " m/s^2")
print("The z-component of acceleration in deep water is: ", z_components_acceleration_deepWater, " m/s^2")

# print(check_connection)
# print(check_wave_number_with_circular_frequency)
# print(check_wave_length_with_wave_period)
print("The program has completed successfully. Thank you for using the program.")

# Plot wave profile-----------------------------------------------------------------------------------------------------------------------
plt.plot(x_values, eta_values)

plt.xlabel("Horizontal coordinate x (m)")
plt.ylabel("Wave elevation η (m)")
plt.title("Wave Profile")

plt.axhline(0, linewidth=0.8)

plt.grid(True)
plt.show()

