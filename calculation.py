import math
from utils.constants import constant

# Define constantss ------------------------------------------------------------------------------------
# constants = {
#     "g": 9.81,  # Acceleration due to gravity (m/s^2)
#     "p0": 101325,  # Atmospheric pressure at sea level (Pa)
#     "rho_water": 1000,  # Density of water (kg/m^3)
#     "rho_air": 1.225,  # Density of air (kg/m^3)
#     "rho_ice": 917,  # Density of ice (kg/m^3)
#     "rho_seawater": 1025,  # Density of seawater (kg/m^3)
# }

# main calculation function

def sea_environment_calculation(frontend):
    try:


        # input data
        input_data = {

            "wave_period":frontend["wave_period"],
            "wave_amplitude":frontend["wave_amplitude"],
            "average_water_depth":frontend["average_water_depth"],
            "coordinate_x_y":frontend["coordinate_x_y"],
            "vertical_coordinate_z":frontend["vertical_coordinate_z"],
            "time_t":frontend["time_t"]

        }


        wave_period = input_data["wave_period"]
        wave_amplitude = input_data["wave_amplitude"]
        average_water_depth = input_data["average_water_depth"]
        coordinate_x_y = input_data["coordinate_x_y"]
        vertical_coordinate_z = input_data["vertical_coordinate_z"]
        time_t = input_data["time_t"]

        print(wave_period)
        print(wave_amplitude)
        print(average_water_depth)
        print(coordinate_x_y)
        print(vertical_coordinate_z)
        print(time_t)

        # ----------------Checks-------------------------------------------------------------------------------------------

        def connection_check():
            try:
                import math
                import matplotlib.pyplot as plt
                print("All required libraries are installed and imported successfully.")
            except ImportError as e:
                print(f"An error occurred while importing libraries: {e}")
                raise ImportError("Please ensure that all required libraries are installed.")
            

        def wave_number_with_circular_frequency_check(circular_frequency, wave_number_finite_k, wave_number_deep_water_k, average_water_depth):

            left_side_finite = (
                circular_frequency ** 2
                / constant["g"]
            )
            
            left_side_deep = (
                circular_frequency ** 2
                / constant["g"]
            )

            right_side_finite = (
                wave_number_finite_k
                * math.tanh(
                    wave_number_finite_k * average_water_depth
                )
            )
            
            right_side_deep = wave_number_deep_water_k

            tolerance = 1e-6
            
            #condition for deep water
            
            if abs(left_side_deep - right_side_deep) < tolerance:

                print(
                    "The wave number and circular frequency "
                    "satisfy the dispersion relation for deep water."
                )
            else:
                
                print(
                    "The wave number and circular frequency "
                    "do not satisfy the dispersion relation for deep water."
                )
                
            #condition for finite depth water

            if abs(left_side_finite - right_side_finite) < tolerance:

                print(
                    "The wave number and circular frequency "
                    "satisfy the dispersion relation."
                )

            else:

                print(
                    "The wave number and circular frequency "
                    "do not satisfy the dispersion relation."
                )

            print("Left side deep (ω²/g):", left_side_deep)
            print("Right side deep (k):", right_side_deep)
            print("Difference deep:", abs(left_side_deep - right_side_deep))
            print("Left side finite (ω²/g):", left_side_finite)
            print("Right side finite (k tanh(kh)):", right_side_finite)
            print("Difference finite:", abs(left_side_finite - right_side_finite))
            return {
                "left_side_deep": left_side_deep,
                "right_side_deep": right_side_deep,
                "difference_deep": abs(left_side_deep - right_side_deep),
                "left_side_finite": left_side_finite,
                "right_side_finite": right_side_finite,
                "difference_finite": abs(left_side_finite - right_side_finite)
            }


        # Calculation of Wave Number and Wave Length for Deep Water and Finite Depth Water----------------------------------------------------

        def circular_Frequency(wave_Period_T):
            return 2 * math.pi / wave_Period_T

        def waveNumber_infinite(circular_Frequency_omega):
            return circular_Frequency_omega ** 2 / constant["g"]

        # def waveNumber_finite(circular_Frequency_omega, average_Water_Depth_h):
        #     return circular_Frequency_omega / math.sqrt(constants["g"] * average_Water_Depth_h)



        def waveNumber_finite(circular_Frequency_omega, average_Water_Depth_h):
            # Initial guess using the deep water wave number
            k_guess = (circular_Frequency_omega ** 2) / constant["g"]
            tolerance = 1e-6
            max_iterations = 100
            
            for _ in range(max_iterations):
                tanh_kh = math.tanh(k_guess * average_Water_Depth_h)
                if tanh_kh == 0:
                    break
                
                # Fixed-point iteration step: k = ω² / (g * tanh(kh))
                k_next = (circular_Frequency_omega ** 2) / (constant["g"] * tanh_kh)
                
                if abs(k_next - k_guess) < tolerance:
                    return k_next
                    
                k_guess = k_next
                
            return k_guess


        def wave_Length_infinite(waveNumber_infinite_k):
            return 2 * math.pi / waveNumber_infinite_k


        def wave_Length_finiteDepth(waveNumber_finite_k):
            return 2 * math.pi / waveNumber_finite_k


        # -------------------------Velocity Potential and Wave Profile Calculations---------------------------------------------

        #---------------------- velocity potential for finite depth-----------------------------------------------------------------------------------
        def velocity_Potential_finiteDepth(wave_amplitude, waveNumber_finite_k, circular_frequency, vertical_coordinate_z, average_water_depth, direction_of_Wave_Propagation, coordinate_x_y=0, time_t=0):
            try:
                if direction_of_Wave_Propagation == "x":
                    velocity_Potential_phi = (wave_amplitude * constant["g"] / circular_frequency) * math.cosh(waveNumber_finite_k * (vertical_coordinate_z + average_water_depth)) / math.cosh(waveNumber_finite_k * average_water_depth) * math.cos(circular_frequency * time_t - waveNumber_finite_k * coordinate_x_y)
                elif direction_of_Wave_Propagation == "y":
                    velocity_Potential_phi = (wave_amplitude * constant["g"] / circular_frequency) * math.cosh(waveNumber_finite_k * (vertical_coordinate_z + average_water_depth)) / math.cosh(waveNumber_finite_k * average_water_depth) * math.cos(circular_frequency * time_t - waveNumber_finite_k * coordinate_x_y)
            except Exception as e:
                print(f"An error occurred: {e}")
                raise ValueError("Invalid direction of wave propagation. Please enter 'x' or 'y'.")
            return velocity_Potential_phi

        #----------- velocity potential for deep water waves-------------------------------------
        def velocity_Potential_infiniteDepth(wave_amplitude, waveNumber_infinite_k, circular_frequency, vertical_coordinate_z, direction_of_Wave_Propagation, coordinate_x_y, time_t):
            try :
                if direction_of_Wave_Propagation == "x":
                    velocity_Potential_phi = (wave_amplitude * constant["g"] / circular_frequency) * math.exp(waveNumber_infinite_k * vertical_coordinate_z) * math.cos(circular_frequency * time_t - waveNumber_infinite_k * coordinate_x_y)
                elif direction_of_Wave_Propagation == "y":
                    velocity_Potential_phi = (wave_amplitude * constant["g"] / circular_frequency) * math.exp(waveNumber_infinite_k * vertical_coordinate_z) * math.cos(circular_frequency * time_t - waveNumber_infinite_k * coordinate_x_y)
                else:
                    raise ValueError("Invalid direction of wave propagation. Please enter 'x' or 'y'.")
            except Exception as e:
                print(f"An error occurred: {e}")
                raise ValueError("Invalid direction of wave propagation. Please enter 'x' or 'y'.")
            return velocity_Potential_phi



        # -----------------------------------Wave Profile Calculation---------------------------------------------
        # calculate wave profile
        def wave_Profile(wave_amplitude, waveNumber_infinite_k, waveNumber_finite_k, circular_Frequency_omega, coordinate_x_y, time_t):
            wave_Profile_finite_zeta = wave_amplitude * math.sin(circular_Frequency_omega * time_t - waveNumber_finite_k * coordinate_x_y)
            wave_Profile_infinite_zeta = wave_amplitude * math.sin(circular_Frequency_omega * time_t - waveNumber_infinite_k * coordinate_x_y)
            return wave_Profile_finite_zeta, wave_Profile_infinite_zeta


        #------------------------------Dynamic Pressure Calculation---------------------------------------------
        def dynamic_Pressure_finiteDepth(fluid_density_rho, wave_amplitude, waveNumber_finite_k, circular_frequency, vertical_coordinate_z, average_water_depth, coordinate_x_y,time_t):
            dynamic_Pressure_finiteDepth = (
                fluid_density_rho
                * constant["g"]
                * wave_amplitude
                * math.cosh(
                    waveNumber_finite_k * (vertical_coordinate_z + average_water_depth)
                )
                / math.cosh(
                    waveNumber_finite_k * average_water_depth
                )
                * math.sin(
                    circular_frequency * time_t
                    - waveNumber_finite_k * coordinate_x_y
                )
            )

            return dynamic_Pressure_finiteDepth



        def dynamic_Pressure_deepWater(fluid_density_rho, wave_amplitude, waveNumber_infinite_k, circular_frequency, vertical_coordinate_z, coordinate_x_y,time_t):
            dynamic_Pressure_deepWater = (
                fluid_density_rho
                * constant["g"]
                * wave_amplitude
                * math.exp(waveNumber_infinite_k * vertical_coordinate_z)
                * math.sin(
                    circular_frequency * time_t
                    - waveNumber_infinite_k * coordinate_x_y
                )
            )

            return dynamic_Pressure_deepWater

        #-------------------------------X component of velocity and Acceleration for Finite Depth---------------------------------------------
        def x_component_velocity_finiteDepth(circular_frequency, wave_amplitude, waveNumber_finite_k, average_water_depth, vertical_coordinate_z, direction_of_Wave_Propagation, coordinate_x_y, time_t):
            if direction_of_Wave_Propagation == "x":
                x_velocity = (
                    circular_frequency
                    * wave_amplitude
                    * math.cosh(
                        waveNumber_finite_k * (vertical_coordinate_z + average_water_depth)
                    )
                    / math.sinh(
                        waveNumber_finite_k * average_water_depth
                    )
                    * math.sin(
                        circular_frequency * time_t
                        - waveNumber_finite_k * coordinate_x_y
                    )
                )
            elif direction_of_Wave_Propagation == "y":
                x_velocity = 0  # No x-component of velocity in y-direction propagation
            else:
                raise ValueError("Invalid direction of wave propagation. Please enter 'x' or 'y'.")
            return x_velocity


        def x_component_velocity_infiniteDepth(circular_frequency, wave_amplitude, waveNumber_infinite_k, vertical_coordinate_z, direction_of_Wave_Propagation, coordinate_x_y, time_t):
            if direction_of_Wave_Propagation == "x":
                x_velocity = (
                    circular_frequency
                    * wave_amplitude
                    * math.exp(waveNumber_infinite_k * vertical_coordinate_z)
                    * math.sin(
                        circular_frequency * time_t
                        - waveNumber_infinite_k * coordinate_x_y
                    )
                )
            elif direction_of_Wave_Propagation == "y":
                x_velocity = 0  # No x-component of velocity in y-direction propagation
            else:
                raise ValueError("Invalid direction of wave propagation. Please enter 'x' or 'y'.")
            return x_velocity



        def x_component_acceleration_finiteDepth(circular_frequency, wave_amplitude, waveNumber_finite_k, average_water_depth, vertical_coordinate_z, direction_of_Wave_Propagation, coordinate_x_y, time_t):
            if direction_of_Wave_Propagation == "x":
                x_acceleration = (
                    circular_frequency ** 2
                    * wave_amplitude
                    * math.cosh(
                        waveNumber_finite_k * (vertical_coordinate_z + average_water_depth)
                    )
                    / math.sinh(
                        waveNumber_finite_k * average_water_depth
                    )
                    * math.cos(
                        circular_frequency * time_t
                        - waveNumber_finite_k * coordinate_x_y
                    )
                )
            elif direction_of_Wave_Propagation == "y":
                x_acceleration = 0  # No x-component of acceleration in y-direction propagation
            else:
                raise ValueError("Invalid direction of wave propagation. Please enter 'x' or 'y'.")
            return x_acceleration


        def x_component_acceleration_infiniteDepth(circular_frequency, wave_amplitude, waveNumber_infinite_k, vertical_coordinate_z, direction_of_Wave_Propagation, coordinate_x_y, time_t):
            if direction_of_Wave_Propagation == "x":
                x_acceleration = (
                    circular_frequency ** 2
                    * wave_amplitude
                    * math.exp(waveNumber_infinite_k * vertical_coordinate_z)
                    * math.cos(
                        circular_frequency * time_t
                        - waveNumber_infinite_k * coordinate_x_y
                    )
                )
            elif direction_of_Wave_Propagation == "y":
                x_acceleration = 0  # No x-component of acceleration in y-direction propagation
            else:
                raise ValueError("Invalid direction of wave propagation. Please enter 'x' or 'y'.")
            return x_acceleration

        # ---------------------------------Z Component of Velocity and Acceleration for Finite Depth---------------------------------------------
        def z_component_velocity_finiteDepth(circular_frequency, wave_amplitude, waveNumber_finite_k, average_water_depth, vertical_coordinate_z, direction_of_Wave_Propagation, coordinate_x_y, time_t):
            if direction_of_Wave_Propagation == "x":
                z_velocity = (
                    circular_frequency
                    * wave_amplitude
                    * math.sinh(
                        waveNumber_finite_k * (vertical_coordinate_z + average_water_depth)
                    )
                    / math.sinh(
                        waveNumber_finite_k * average_water_depth
                    )
                    * math.cos(
                        circular_frequency * time_t
                        - waveNumber_finite_k * coordinate_x_y
                    )
                )
            elif direction_of_Wave_Propagation == "y":
                z_velocity = 0  # No z-component of velocity in y-direction propagation
            else:
                raise ValueError("Invalid direction of wave propagation. Please enter 'x' or 'y'.")
            return z_velocity


        def z_component_velocity_infiniteDepth(circular_frequency, wave_amplitude, waveNumber_infinite_k, vertical_coordinate_z, direction_of_Wave_Propagation, coordinate_x_y, time_t):
            if direction_of_Wave_Propagation == "x":
                z_velocity = (
                    circular_frequency
                    * wave_amplitude
                    * math.exp(waveNumber_infinite_k * vertical_coordinate_z)
                    * math.cos(
                        circular_frequency * time_t
                        - waveNumber_infinite_k * coordinate_x_y
                    )
                )
            elif direction_of_Wave_Propagation == "y":
                z_velocity = 0  # No z-component of velocity in y-direction propagation
            else:
                raise ValueError("Invalid direction of wave propagation. Please enter 'x' or 'y'.")
            return z_velocity



        def z_component_acceleration_finiteDepth(circular_frequency, wave_amplitude, waveNumber_finite_k, average_water_depth, vertical_coordinate_z, direction_of_Wave_Propagation, coordinate_x_y, time_t):
            if direction_of_Wave_Propagation == "x":
                z_acceleration = - (
                    circular_frequency ** 2
                    * wave_amplitude
                    * math.sinh(
                        waveNumber_finite_k * (vertical_coordinate_z + average_water_depth)
                    )
                    / math.sinh(
                        waveNumber_finite_k * average_water_depth
                    )
                    * math.sin(
                        circular_frequency * time_t
                        - waveNumber_finite_k * coordinate_x_y
                    )
                )
            elif direction_of_Wave_Propagation == "y":
                z_acceleration = 0  # No z-component of acceleration in y-direction propagation
            else:
                raise ValueError("Invalid direction of wave propagation. Please enter 'x' or 'y'.")
            return z_acceleration


        def z_component_acceleration_infiniteDepth(circular_frequency, wave_amplitude, waveNumber_infinite_k, vertical_coordinate_z, direction_of_Wave_Propagation, coordinate_x_y, time_t):
            if direction_of_Wave_Propagation == "x":
                z_acceleration = - (
                    circular_frequency ** 2
                    * wave_amplitude
                    * math.exp(waveNumber_infinite_k * vertical_coordinate_z)
                    * math.sin(
                        circular_frequency * time_t
                        - waveNumber_infinite_k * coordinate_x_y
                    )
                )
            elif direction_of_Wave_Propagation == "y":
                z_acceleration = 0  # No z-component of acceleration in y-direction propagation
            else:
                raise ValueError("Invalid direction of wave propagation. Please enter 'x' or 'y'.")
            return z_acceleration

        # Take Inputs from here-----------------------------
        # connection_check()
        # wave_period = float(input("Enter the wave period (T) in seconds: "))
        # wave_amplitude = float(input("Enter the wave amplitude (ζ) in meters: "))
        # average_water_depth = float(input("Enter the average water depth (h) in meters: "))

        # direction_of_Wave_Propagation = input("What is the direction of wave propagation? (Enter 'x' or 'y'): ").lower()
        direction_of_Wave_Propagation = "x" # changes into hard code
        # coordinate_x_y = float(input("What is the coordinate as selected earlier? (Enter x or y): "))
        # vertical_coordinate_z = - float(input("What is the vertical coordinate z (e.g., enter 5 for 5m depth): "))
        # time_t = float(input("What is the time? (Enter t): "))


        #-----------------Calculations---------------------------------------------
        circular_frequency = circular_Frequency(wave_period)
        check_wave_number_with_circular_frequency = wave_number_with_circular_frequency_check(circular_frequency, waveNumber_finite(circular_frequency, average_water_depth), waveNumber_infinite(circular_frequency), average_water_depth)
        dynamic_pressure_finiteDepth = dynamic_Pressure_finiteDepth(constant["rho_seawater"], wave_amplitude, waveNumber_finite(circular_frequency, average_water_depth), circular_frequency, vertical_coordinate_z, average_water_depth, coordinate_x_y,time_t)
        dynamic_pressure_infiniteDepth = dynamic_Pressure_deepWater(constant["rho_seawater"], wave_amplitude, waveNumber_infinite(circular_frequency), circular_frequency, vertical_coordinate_z, coordinate_x_y,time_t)

        # -----------------------Deep / Infinite Water Calculations---------------------------------------------
        waveNumber_infinite_k = waveNumber_infinite(circular_frequency)
        wave_length_deep_water_lambda = wave_Length_infinite(waveNumber_infinite_k)
        velocity_Potential_phi_infiniteDepth = velocity_Potential_infiniteDepth(wave_amplitude, waveNumber_infinite_k, circular_frequency, vertical_coordinate_z, direction_of_Wave_Propagation, coordinate_x_y, time_t)
        wave_Profile_infinite_zeta = wave_Profile(wave_amplitude, waveNumber_infinite_k, waveNumber_finite(circular_frequency, average_water_depth), circular_frequency, coordinate_x_y, time_t)


        # ------------------------Shallow / Finite Depth Water Calculations---------------------------------------------
        waveNumber_finite_k = waveNumber_finite(circular_frequency, average_water_depth)
        wave_length_finite_depth_lambda = wave_Length_finiteDepth(waveNumber_finite_k)
        velocity_Potential_phi_finiteDepth = velocity_Potential_finiteDepth(wave_amplitude, waveNumber_finite_k, circular_frequency, vertical_coordinate_z, average_water_depth, direction_of_Wave_Propagation, coordinate_x_y, time_t)
        # wave_Profile = wave_Profile(wave_amplitude, waveNumber_infinite_k, waveNumber_finite_k, circular_frequency, coordinate_x_y, time_t)
        wave_Profile_finite_zeta, wave_Profile_infinite_zeta = wave_Profile(wave_amplitude, waveNumber_infinite_k, waveNumber_finite_k, circular_frequency, coordinate_x_y, time_t)

        # --------------------------------Display Results---------------------------------------------
        print("\nResults:---------------------------------------------------------------------------------")
        print("Wave Calculations for Deep Water and Finite Depth Water")
        print(check_wave_number_with_circular_frequency)

        print("-------------------------------------------------------------")
        print(f"Wave Period (T): {wave_period} seconds")
        print(f"Average Water Depth (h): {average_water_depth} meters")
        print(f"Circular Frequency (ω): {circular_frequency} rad/s")
        print(f"Wave Number (k) - Deep Water: {waveNumber_infinite_k}")
        print(f"Wave Length (λ) - Deep Water: {wave_length_deep_water_lambda} meters")
        print(f"Wave Number (k) - Finite Depth Water: {waveNumber_finite_k}")
        print(f"Wave Length (λ) - Finite Depth Water: {wave_length_finite_depth_lambda} meters")

        print("-------------------------------------------------------------")
        print("Velocity Potential and Wave Profile Calculations:")
        print(f"Velocity Potential (φ) - Deep / Infinite Water: {velocity_Potential_phi_infiniteDepth}")
        print(f"Velocity Potential (φ) - Finite Depth Water: {velocity_Potential_phi_finiteDepth}")
        # print(f"Wave Profile (ζ) - Finite Depth Water and Deep / Infinite Water : {wave_Profile}")
        print(f"Wave Profile (ζ) - Finite Depth Water: {wave_Profile_finite_zeta}")
        print(f"Wave Profile (ζ) - Deep / Infinite Water: {wave_Profile_infinite_zeta}")

        print("-------------------------------------------------------------")
        print("Dynamic Pressure Calculations:")
        print(f"Dynamic Pressure (p) - Deep / Infinite Water: {dynamic_pressure_infiniteDepth}")
        print(f"Dynamic Pressure (p) - Finite Depth Water: {dynamic_pressure_finiteDepth}")


        print("-------------------------------------------------------------")
        print("X Component of Velocity and Acceleration for Finite Depth Water:")
        x_velocity_finiteDepth = x_component_velocity_finiteDepth(circular_frequency, wave_amplitude, waveNumber_finite_k, average_water_depth, vertical_coordinate_z, direction_of_Wave_Propagation, coordinate_x_y, time_t)
        x_acceleration_finiteDepth = x_component_acceleration_finiteDepth(circular_frequency, wave_amplitude, waveNumber_finite_k, average_water_depth, vertical_coordinate_z, direction_of_Wave_Propagation, coordinate_x_y, time_t)
        print(f"X Component of Velocity (u) - Finite Depth Water: {x_velocity_finiteDepth}")
        print(f"X Component of Acceleration (a) - Finite Depth Water: {x_acceleration_finiteDepth}")
        x_velocity_infiniteDepth = x_component_velocity_infiniteDepth(circular_frequency, wave_amplitude, waveNumber_infinite_k, vertical_coordinate_z, direction_of_Wave_Propagation, coordinate_x_y, time_t)
        x_acceleration_infiniteDepth = x_component_acceleration_infiniteDepth(circular_frequency, wave_amplitude, waveNumber_infinite_k, vertical_coordinate_z, direction_of_Wave_Propagation, coordinate_x_y, time_t)
        print(f"X Component of Velocity (u) - Deep / Infinite Water: {x_velocity_infiniteDepth}")
        print(f"X Component of Acceleration (a) - Deep / Infinite Water: {x_acceleration_infiniteDepth}")


        print("-------------------------------------------------------------")
        print("Z Component of Velocity and Acceleration for Finite Depth Water:")
        z_velocity_finiteDepth = z_component_velocity_finiteDepth(circular_frequency, wave_amplitude, waveNumber_finite_k, average_water_depth, vertical_coordinate_z, direction_of_Wave_Propagation, coordinate_x_y, time_t)
        z_acceleration_finiteDepth = z_component_acceleration_finiteDepth(circular_frequency, wave_amplitude, waveNumber_finite_k, average_water_depth, vertical_coordinate_z, direction_of_Wave_Propagation, coordinate_x_y, time_t)
        print(f"Z Component of Velocity (w) - Finite Depth Water: {z_velocity_finiteDepth}")
        print(f"Z Component of Acceleration (a) - Finite Depth Water: {z_acceleration_finiteDepth}")
        z_velocity_infiniteDepth = z_component_velocity_infiniteDepth(circular_frequency, wave_amplitude, waveNumber_infinite_k, vertical_coordinate_z, direction_of_Wave_Propagation, coordinate_x_y, time_t)
        z_acceleration_infiniteDepth = z_component_acceleration_infiniteDepth(circular_frequency, wave_amplitude, waveNumber_infinite_k, vertical_coordinate_z, direction_of_Wave_Propagation, coordinate_x_y, time_t)
        print(f"Z Component of Velocity (w) - Deep / Infinite Water: {z_velocity_infiniteDepth}")
        print(f"Z Component of Acceleration (a) - Deep / Infinite Water: {z_acceleration_infiniteDepth}")


        # ============================================================
        # RESULT DICTIONARY
        # ============================================================

        result = {

            "wave_period": wave_period,
            "average_water_depth": average_water_depth,
            "circular_frequency": circular_frequency,
            "waveNumber_infinite_k" : waveNumber_infinite_k,
            "wave_length_deep_water_lambda": wave_length_deep_water_lambda,
            "waveNumber_finite_k": waveNumber_finite_k,
            "wave_length_finite_depth_lambda": wave_length_finite_depth_lambda,
            # ------------------------------------------------------------
          
            "velocity_Potential_phi_infiniteDepth": velocity_Potential_phi_infiniteDepth,
            "velocity_Potential_phi_finiteDepth": velocity_Potential_phi_finiteDepth,
            # "wave_Profile":wave_Profile,
            "wave_Profile_finite_zeta": wave_Profile_finite_zeta,
            "wave_Profile_infinite_zeta":wave_Profile_infinite_zeta,
            # ------------------------------------------------------------
            
            "dynamic_pressure_infiniteDepth": dynamic_pressure_infiniteDepth,
            "dynamic_pressure_finiteDepth": dynamic_pressure_finiteDepth,

            # ------------------------------------------------------------
            
            "x_velocity_finiteDepth": x_velocity_finiteDepth,
            "x_acceleration_finiteDepth": x_acceleration_finiteDepth,
            "x_velocity_infiniteDepth": x_velocity_infiniteDepth,
            "x_acceleration_infiniteDepth": x_acceleration_infiniteDepth,

            # ----------------------------------------------------------------
            
            "z_velocity_finiteDepth": z_velocity_finiteDepth,
            "z_acceleration_finiteDepth":z_acceleration_finiteDepth,
            "z_velocity_infiniteDepth":z_velocity_infiniteDepth,
            "z_acceleration_infiniteDepth":z_acceleration_infiniteDepth


        }

        print("\n======================================================")
        print("Thermoddynamics")
        print("======================================================")


        

        

        # # --------------------------------Plotting Section---------------------------------------------
        # # Generate a span of k values from 0 up to double the deep water wave number for comparison
        # k_values = [i * (2 * waveNumber_infinite_k / 200) for i in range(201)]

        # # Evaluate the right side function: f(k) = k * tanh(k * h)
        # finite_curve = [k * math.tanh(k * average_water_depth) for k in k_values]

        # # Evaluate the constants left side target: constants = ω² / g
        # target_value = (circular_frequency ** 2) / constant["g"]
        # constants_line = [target_value for _ in k_values]

        # # Initialize the plot layout
        # plt.figure(figsize=(9, 5))
        # plt.plot(k_values, finite_curve, label=r'$k \tanh(kh)$ (Finite Depth Function)', color='blue', linewidth=2)
        # plt.axhline(y=target_value, color='red', linestyle='--', label=r'$\omega^2 / g$ (Target Value)', linewidth=1.5)

        # # Highlight the exact solved value intersection point
        # plt.plot(waveNumber_finite_k, target_value, 'go', markersize=8, label=f'Solved Solution ($k$ = {waveNumber_finite_k:.4f})')

        # # Add explicit design labels, grid structure, and legends
        # plt.title(f'Transcendental Dispersion Relation Solution\n(T = {wave_period}s, h = {average_water_depth}m)', fontsize=12)
        # plt.xlabel('Wave Number ($k$)', fontsize=10)
        # plt.ylabel('Value', fontsize=10)
        # plt.grid(True, which='both', linestyle=':', alpha=0.6)
        # plt.legend(loc='lower right', fontsize=10)

        # # Display the window onto the desktop screen
        # plt.show()

        return result





    except Exception as e:

        print("Error Occured : ", e)

        return {
            "status":"FAILED",
            "message": str(e)
        }






