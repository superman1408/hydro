import math

# Define constants ------------------------------------------------------------------------------------
constant = {
    "g": 9.81,  # Acceleration due to gravity (m/s^2)
    "p0": 101325,  # Atmospheric pressure at sea level (Pa)
}


# All functions are defined here -----------------------------------------------------------------------

# velocity potential for finite depth
def velocity_Potential_finiteDepth(wave_Amplitude_zita, wave_Number_k, angular_Frequency_omega, vertical_coordinate_z, average_Water_Depth_h, direction_of_Wave_Propagation):
    try:
        if direction_of_Wave_Propagation == "x":
            velocity_Potential_phi = (wave_Amplitude_zita * constant["g"] / angular_Frequency_omega) * math.cosh(wave_Number_k * (vertical_coordinate_z + average_Water_Depth_h)) / math.cosh(wave_Number_k * average_Water_Depth_h) * math.cos(wave_Number_k * 0 - angular_Frequency_omega * 0)
        elif direction_of_Wave_Propagation == "y":
            velocity_Potential_phi = (wave_Amplitude_zita * constant["g"] / angular_Frequency_omega) * math.cosh(wave_Number_k * (vertical_coordinate_z + average_Water_Depth_h)) / math.cosh(wave_Number_k * average_Water_Depth_h) * math.cos(wave_Number_k * 0 - angular_Frequency_omega * 0)
    except Exception as e:
        print(f"An error occurred: {e}")
        raise ValueError("Invalid direction of wave propagation. Please enter 'x' or 'y'.")
    return velocity_Potential_phi

# velocity potential for deep water waves 
def velocity_Potential_deepWater(wave_Amplitude_zita, wave_Number_k, angular_Frequency_omega, vertical_coordinate_z, average_Water_Depth_h, direction_of_Wave_Propagation):
    try :
        if direction_of_Wave_Propagation == "x":
            velocity_Potential_phi = (wave_Amplitude_zita * constant["g"] / angular_Frequency_omega) * math.exp(wave_Number_k * vertical_coordinate_z) * math.cos(wave_Number_k * 0 - angular_Frequency_omega * 0)
        elif direction_of_Wave_Propagation == "y":
            velocity_Potential_phi = (wave_Amplitude_zita * constant["g"] / angular_Frequency_omega) * math.exp(wave_Number_k * vertical_coordinate_z) * math.cos(wave_Number_k * 0 - angular_Frequency_omega * 0)
        else:
            raise ValueError("Invalid direction of wave propagation. Please enter 'x' or 'y'.")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise ValueError("Invalid direction of wave propagation. Please enter 'x' or 'y'.")
    return velocity_Potential_phi

# Calculate angular frequency and wave number
def angular_Frequency(wave_Period_T):
    angular_Frequency_omega = (2 * math.pi) / wave_Period_T
    return angular_Frequency_omega

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

# Print the types of the input variables ------------------------------------------------------------
print(type(wave_Length_lamda))
print(type(wave_Period_T))
print(type(wave_Amplitude_zita))
print(type(average_Water_Depth_h))
print(type(direction_of_Wave_Propagation))
print(type(vertical_coordinate_z))

# Calculate angular frequency, wave number, vertical coordinate movement direction, and velocity potential ----------------------------------
angular_Frequency_omega = angular_Frequency(wave_Period_T)
wave_Number_k = wave_Number(wave_Length_lamda)
vertical_coordinate_movement_direction_result = vertical_coordinate_movement_direction(vertical_coordinate_z, average_Water_Depth_h)
velocity_Potential_phi_deepWater = velocity_Potential_deepWater(wave_Amplitude_zita, wave_Number_k, angular_Frequency_omega, vertical_coordinate_z, average_Water_Depth_h, direction_of_Wave_Propagation)
velocity_Potential_phi_finiteDepth = velocity_Potential_finiteDepth(wave_Amplitude_zita, wave_Number_k, angular_Frequency_omega, vertical_coordinate_z, average_Water_Depth_h, direction_of_Wave_Propagation)

# Print the results ---------------------------------------------------------------------------------------------------------
print("The angular frequency of the wave is (ω): ", angular_Frequency_omega, " rad/s")
print("The wave number of the wave is (k): ", wave_Number_k, " rad/m")
print("The vertical coordinate movement direction is: ", vertical_coordinate_movement_direction_result)
print("Atmospheric pressure at sea level (p0): ", constant["p0"], "Pa")
print("Acceleration due to gravity (g): ", constant["g"], "m/s^2")
print("The velocity potential (φ) of the wave in deep water is: ", velocity_Potential_phi_deepWater, " m^2/s")
print("The velocity potential (φ) of the wave in finite depth is: ", velocity_Potential_phi_finiteDepth, " m^2/s")

