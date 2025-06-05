#!/usr/bin/env python3
"""
Test-Skript zum Überprüfen des CSV-Imports im main.py-Format
"""

import csv
import json

def test_csv_import(csv_filename):
    """
    Testet den Import einer CSV-Datei im main.py-Format
    """
    print(f"=== Testing CSV Import: {csv_filename} ===")
    
    try:
        with open(csv_filename, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            operations = []
            row_count = 0
            
            for row in reader:
                row_count += 1
                op_type = row['type']
                
                # JSON-Parameter parsen
                try:
                    params = json.loads(row['params'])
                except json.JSONDecodeError as e:
                    print(f"  ❌ Zeile {row_count}: JSON-Fehler in params: {e}")
                    print(f"     Rohe params: {row['params']}")
                    continue
                
                description = row['description']
                
                # Operation hinzufügen
                operation = {
                    'type': op_type,
                    'params': params,
                    'description': description
                }
                operations.append(operation)
                
                # Details ausgeben
                print(f"  ✅ Zeile {row_count}: {op_type}")
                print(f"     Params: {params}")
                print(f"     Description: {description}")
                
                # Spezielle Validierung für Stepper-Operationen
                if op_type == 'stepper':
                    required_params = ['steps', 'direction', 'speed']
                    for param in required_params:
                        if param not in params:
                            print(f"     ⚠️  Warnung: Fehlender Parameter '{param}' in Stepper-Operation")
                        else:
                            print(f"     ✓ Parameter '{param}': {params[param]}")
                
                # Spezielle Validierung für Servo-Operationen
                elif op_type == 'servo':
                    if 'angle' not in params:
                        print(f"     ⚠️  Warnung: Fehlender Parameter 'angle' in Servo-Operation")
                    else:
                        print(f"     ✓ Parameter 'angle': {params['angle']}")
                
                print()  # Leerzeile für bessere Lesbarkeit
                
            print(f"=== Import-Test abgeschlossen ===")
            print(f"Gesamte Operationen erfolgreich gelesen: {len(operations)}")
            print(f"Zeilen verarbeitet: {row_count}")
            
            # Zusammenfassung der Operation-Typen
            type_counts = {}
            for op in operations:
                op_type = op['type']
                type_counts[op_type] = type_counts.get(op_type, 0) + 1
            
            print(f"\nOperations-Zusammenfassung:")
            for op_type, count in type_counts.items():
                print(f"  - {op_type}: {count} Operationen")
                
            return True
            
    except FileNotFoundError:
        print(f"❌ Datei nicht gefunden: {csv_filename}")
        return False
    except Exception as e:
        print(f"❌ Fehler beim Import: {e}")
        return False

if __name__ == "__main__":
    # Teste die erstellte CSV-Datei
    csv_files = [
        "calculator/winkeltabelle_40x0_3punkte_approximiert.csv",
        "test_import.csv"
    ]
    
    for csv_file in csv_files:
        try:
            success = test_csv_import(csv_file)
            if success:
                print(f"✅ {csv_file}: Import-Test erfolgreich!\n")
            else:
                print(f"❌ {csv_file}: Import-Test fehlgeschlagen!\n")
        except Exception as e:
            print(f"❌ {csv_file}: Unerwarteter Fehler: {e}\n")
