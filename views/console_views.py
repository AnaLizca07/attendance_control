import json

class ConsoleView:
    @staticmethod
    def display_user_info(user_id, user_info):
        print("\n" + "="*60)
        print(f"Usuario ID: {user_id}")
        print(f"Nombre: {user_info.get('name', 'No registrado')}")
        print(f"Privilegio: {user_info.get('privilege', 'No registrado')}")
        print(f"Grupo ID: {user_info.get('group_id', 'No registrado')}")
        print("="*60)

    @staticmethod
    def display_attendance(date, times):
        times.sort()
        entrada = times[0] if times else "Sin registro"
        salida = times[-1] if len(times) > 1 else "Sin registro"
        
        print(f"Fecha: {date}")
        print(f"  Entrada: {entrada}")
        print(f"  Salida:  {salida}")
        print(f"  Total registros del día: {len(times)}")
        print("-" * 30)

    @staticmethod
    def display_device_info(device_info):
        print("\n" + "="*60)
        print(f"Nombre del dispositivo: {device_info.get('device_name', 'Desconocido')}")
        print(f"  Descripción: {device_info.get('description', {})}")
        print("="*60)

    @staticmethod
    def save_json_output(data, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"\nDatos guardados en: {filename}")