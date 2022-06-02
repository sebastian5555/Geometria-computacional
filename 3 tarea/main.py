from autonfleet import AutonFleet


def main():
    ship = AutonFleet(Fleet)
    # ((puntox,puntoy), vecinos)
    ship.nearest_ships((0.6772819, 0.3003644), 5)
    # (Index localizacion buque, radio)
    ship.avoiding_collisions(3, 0.3)
    ship.partner_lookup()
    ship.operation_radius()


# Flota
fichero = open('fleet10.dat',)
Fleet = []

for lineas in fichero.readlines():
    list = lineas.split()
    list = [float(list[0]), float(list[1]), float(list[2]), float(list[3])]
    Fleet.append(list)

fichero.close()
main()
