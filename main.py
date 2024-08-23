class Auto:
    def __init__(self, placa, marca, modelo, descripcion, precio_unitario):
        self.placa = placa
        self.marca = marca
        self.modelo = modelo
        self.descripcion = descripcion
        self.precio_unitario = precio_unitario

class Cliente:
    def __init__(self, nombre, correo, nit):
        self.nombre = nombre
        self.correo = correo
        self.nit = nit

class Compra:
    id_counter = 1

    def __init__(self, cliente):
        self.id = Compra.id_counter
        Compra.id_counter += 1
        self.cliente = cliente
        self.lista_productos = []
        self.costo_total = 0.0

    def agregar_auto(self, auto):
        self.lista_productos.append(auto)
        self.costo_total += auto.precio_unitario

    def generar_factura(self, agregar_seguro):
        if agregar_seguro:
            self.costo_total += sum(auto.precio_unitario * 0.15 for auto in self.lista_productos)
        return self.costo_total

autos = []
clientes = []
compras = []

def registrar_auto():
    placa = input("Ingrese la placa del auto: ")
    if any(auto.placa == placa for auto in autos):
        print("La placa ya está registrada. Intente con una placa diferente.")
        return
    marca = input("Ingrese la marca del auto: ")
    modelo = input("Ingrese el modelo del auto: ")
    descripcion = input("Ingrese la descripción del auto: ")
    precio_unitario = float(input("Ingrese el precio unitario del auto: "))
    auto = Auto(placa, marca, modelo, descripcion, precio_unitario)
    autos.append(auto)
    print("Auto registrado exitosamente.")

def registrar_cliente():
    nombre = input("Ingrese el nombre del cliente: ")
    correo = input("Ingrese el correo electrónico del cliente: ")
    nit = input("Ingrese el NIT del cliente: ")
    if any(cliente.nit == nit for cliente in clientes):
        print("El NIT ya está registrado. Intente con un NIT diferente.")
        return
    cliente = Cliente(nombre, correo, nit)
    clientes.append(cliente)
    print("Cliente registrado exitosamente.")

def realizar_compra():
    nit = input("Ingrese el NIT del cliente: ")
    cliente = next((c for c in clientes if c.nit == nit), None)
    if not cliente:
        print("Cliente no encontrado.")
        return

    compra = Compra(cliente)
    while True:
        print("------------- Menú Compra -------------")
        print("1. Agregar Auto")
        print("2. Terminar Compra y Facturar")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            placa = input("Ingrese la placa del auto: ")
            auto = next((a for a in autos if a.placa == placa), None)
            if auto:
                compra.agregar_auto(auto)
                print("Auto agregado a la compra.")
            else:
                print("Auto no encontrado.")
        elif opcion == "2":
            agregar_seguro = input("¿Desea agregar seguro al auto? (SI/NO): ").strip().upper() == "SI"
            total = compra.generar_factura(agregar_seguro)
            compras.append(compra)
            print(f"Compra finalizada. Total: Q{total:.2f}")
            break

def reporte_compras():
    print("------------- REPORTE DE COMPRAS -------------")
    total_general = 0.0
    for compra in compras:
        print("==============================================")
        print(f"CLIENTE:\nNombre: {compra.cliente.nombre}\nCorreo electrónico: {compra.cliente.correo}\nNit: {compra.cliente.nit}")
        print("AUTO(S) ADQUIRIDO(S)")
        for auto in compra.lista_productos:
            print(f"{auto.placa}, {auto.marca}, {auto.modelo}, Q{auto.precio_unitario:.2f}, {auto.descripcion}")
        print(f"TOTAL: Q{compra.costo_total:.2f}")
        total_general += compra.costo_total
    print("==============================================")
    print(f"Total General: Q{total_general:.2f}")
    print("---------------------------------------------")

def datos_estudiante():
    print("Nombre: Javier Andrés Velásquez Bonilla")
    print("Carnet: 202307775")

def menu_principal():
    while True:
        print("------------- Menú Principal -------------")
        print("1. Registrar Auto")
        print("2. Registrar Cliente")
        print("3. Realizar Compra")
        print("4. Reporte de Compras")
        print("5. Datos del Estudiante")
        print("6. Salir")
        print("------------------------------------------")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_auto()
        elif opcion == "2":
            registrar_cliente()
        elif opcion == "3":
            realizar_compra()
        elif opcion == "4":
            reporte_compras()
        elif opcion == "5":
            datos_estudiante()
        elif opcion == "6":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    menu_principal()