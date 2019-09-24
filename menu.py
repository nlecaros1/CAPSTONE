from tools import *
cajeros = carga()
decision = 1
opciones = ['1', '2', '3']
dias = ['1', '2', '3', '4', '5', '6', '7']
horarios = ['1', '2', '3']
while decision:
    print("")        
    decision = input(f''' ¿Qué quiere hacer?
1) Ver el mapa
2) Ver la disponibilidad
3) Recargar y observar.
4) Salir
>> ''')
    while decision not in opciones:
        print("No existe esa opcion.")
        decision = input(f''' ¿Qué quiere hacer?
1) Ver el mapa
2) Ver la disponibilidad
3) Salir
>> ''')
    if decision == '1':
        draw(cajeros)
    elif decision == '2':
        dia = input(f''' Seleccione el dia que quiere:
1) Lunes
2) Martes
3) Miercoles
4) Jueves
5) Viernes
6) Sabado
7) Domingo
>> ''')
        while dia not in dias:
            print("No existe esa opcion.")
            dia = input(f''' Seleccione el dia que quiere:
1) Lunes
2) Martes
3) Miercoles
4) Jueves
5) Viernes
6) Sabado
7) Domingo
>> ''')
        dia = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo'][int(dia) - 1]
        horario = input(f'''Seleccione el horario:
1) Manana
2) Tarde
3) Noche
>> ''')
        while horario not in horarios:
            print("No existe esa opcion.")
            horario = input(f'''Seleccione el horario:
1) Manana
2) Tarde
3) Noche
>> ''')
        horario = ['Manana', 'Tarde', 'Noche'][int(horario) - 1]
        disponibilidad(cajeros, 0, dia, horario)
    elif decision == '3':
        monto = input('Escriba el monto a recargar en MM$: ')
        calculador(cajeros, int(monto))
    else:
        break


print('='*50)
print('Termino')
