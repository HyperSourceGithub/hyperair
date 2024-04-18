# Lift simulation
    # Data sources: 
    #   https://www.grc.nasa.gov/www/k-12/VirtualAero/BottleRocket/airplane/lifteq.html
    #   https://www.grc.nasa.gov/www/k-12/VirtualAero/BottleRocket/airplane/area.html
    #   https://aerospaceweb.org/question/aerodynamics/q0252.shtml
    # lift = 0.5 * d * v^2 * A * Cl
    # Not a 100% accurate since it breaks things
    lift = 0.5 * 0.302 * speed * 0.08 * 0.02 * math.cos(math.radians(pitch)) * dt

    # Gravity
    plane_y += 98 * dt - lift
