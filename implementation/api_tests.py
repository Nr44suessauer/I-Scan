import unittest  # Standard-Bibliothek für Tests in Python
import tkinter as tk  # UI-Bibliothek für die GUI
from unittest.mock import MagicMock, patch  # Mock-Werkzeuge zum Simulieren von Objekten und Funktionen
from Api_Fenster import ApiClient, DeviceControl, OperationQueue, ControlApp, Logger  # Import der zu testenden Klassen

# -------------------------------------------------------------------------
# Behavior Tests (Funktionale Tests)
# Diese Tests prüfen das Verhalten der Komponenten aus Nutzersicht
# -------------------------------------------------------------------------

class BehaviorTests(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://test-url.com"
        # Root-Fenster für Tkinter-Variablen
        self.root = tk.Tk()
        self.root.withdraw()  # Verstecke das Fenster während Tests
    
    @patch('Api_Fenster.requests.get')
    def test_api_request_success(self, mock_get):
        # Test: API-Anfrage erfolgreich durchgeführt
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "success"}
        mock_get.return_value = mock_response
        
        result = ApiClient.make_request("testEndpoint", {"param": "value"}, self.base_url)
        
        # Prüfe ob die Anfrage korrekt gesendet wurde und die Antwort korrekt verarbeitet wurde
        mock_get.assert_called_once_with(f"{self.base_url}/testEndpoint", 
                                         params={"param": "value"}, 
                                         timeout=30)
        self.assertEqual(result, {"status": "success"})
    
    @patch('Api_Fenster.ApiClient.make_request')
    def test_set_servo_to_specific_angle(self, mock_make_request):
        # Test: Servo auf einen bestimmten Winkel setzen
        mock_make_request.return_value = "OK"
        
        result = ApiClient.set_servo_angle(45, self.base_url)
        
        # Prüfe ob der richtige API-Aufruf gemacht wurde
        mock_make_request.assert_called_once_with("setServo", {"angle": 45}, self.base_url)
        self.assertIn("Servo set to 45 degrees", result)
    
    @patch('Api_Fenster.ApiClient.make_request')
    def test_move_stepper_specific_distance(self, mock_make_request):
        # Test: Schrittmotor um eine bestimmte Distanz bewegen
        mock_make_request.return_value = "OK"
        
        result = ApiClient.move_stepper(100, 1, 80, self.base_url)
        
        # Prüfe ob der richtige API-Aufruf mit korrekten Parametern gemacht wurde
        mock_make_request.assert_called_once_with("setMotor", 
                                                 {"steps": 100, "direction": 1, "speed": 80}, 
                                                 self.base_url)
        self.assertIn("Stepper motor moves 100 steps up", result)
    
    @patch('Api_Fenster.ApiClient.make_request')
    def test_button_state_detection(self, mock_make_request):
        # Test: Button-Status erkennen
        mock_make_request.return_value = {"pressed": True}
        
        result = ApiClient.get_button_state(self.base_url)
        button_pressed = ApiClient.is_button_pressed(result)
        
        self.assertTrue(button_pressed)
        mock_make_request.assert_called_once_with("getButtonState", base_url=self.base_url)
    
    @patch('Api_Fenster.threading.Thread')
    def test_queue_execution_workflow(self, mock_thread):
        # Test: Workflow der Warteschlangen-Ausführung
        queue_list = MagicMock()
        logger = MagicMock()
        operation_queue = OperationQueue(logger, queue_list)
        
        # Operation hinzufügen und Queue ausführen
        operation_queue.add('servo', {'angle': 45}, "Servo: Set angle to 45°")
        operation_queue.execute_all(self.base_url, {}, MagicMock(), MagicMock(), MagicMock())
        
        # Prüfe ob der Ausführungs-Thread gestartet wurde
        logger.log.assert_called_with("Starting queue execution...")
        mock_thread.assert_called_once()
        mock_thread.return_value.start.assert_called_once()
    
    @patch('Api_Fenster.ApiClient.get_button_state')
    @patch('Api_Fenster.ApiClient.make_request')
    @patch('Api_Fenster.ApiClient.is_button_pressed')
    def test_home_function_complete_workflow(self, mock_is_pressed, mock_make_request, mock_get_button):
        # Test: Vollständiger Workflow der Home-Funktion
        base_url_var = tk.StringVar(value=self.base_url)
        position_var = tk.DoubleVar(value=10.0)  # Startposition nicht 0
        servo_angle_var = tk.IntVar(value=0)
        
        widgets = {
            'diameter_entry': MagicMock(),
            'stepper_speed': MagicMock(),
            'update_position_label': MagicMock()
        }
        
        widgets['diameter_entry'].get = MagicMock(return_value="28")
        widgets['stepper_speed'].get = MagicMock(return_value="80")
        
        logger = MagicMock()
        
        device_control = DeviceControl(
            logger, 
            base_url_var, 
            widgets, 
            position_var, 
            servo_angle_var
        )
        
        # Simuliere Button-Status: nicht gedrückt -> nicht gedrückt -> gedrückt
        mock_is_pressed.side_effect = [False, False, True]
        
        # Führe Home-Funktion ohne Verzögerungen aus
        with patch('Api_Fenster.time.sleep'):
            device_control.home_func()
        
        # Prüfe ob die Home-Funktion korrekt durchlaufen wurde
        self.assertEqual(mock_get_button.call_count, 3)
        self.assertEqual(mock_make_request.call_count, 3)
        self.assertEqual(position_var.get(), 0)  # Position sollte auf 0 zurückgesetzt sein

# -------------------------------------------------------------------------
# Structural Tests (Strukturelle Tests)
# Diese Tests prüfen die interne Struktur und Implementierung der Komponenten
# -------------------------------------------------------------------------

class ApiClientStructuralTests(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://test-url.com"
    
    def test_make_request_structure(self):
        # Test: Struktur und Parameter der make_request Methode
        self.assertTrue(hasattr(ApiClient, 'make_request'))
        self.assertEqual(ApiClient.make_request.__defaults__[-1], 30)  # Prüfe Default-Timeout
    
    def test_set_servo_angle_validation(self):
        # Test: Validierung der Winkel-Grenzen
        result_too_low = ApiClient.set_servo_angle(-10, self.base_url)
        result_too_high = ApiClient.set_servo_angle(100, self.base_url)
        
        self.assertIn("Error", result_too_low)
        self.assertIn("Error", result_too_high)
    
    def test_move_stepper_validation(self):
        # Test: Validierung der Schrittmotor-Parameter
        result_negative_steps = ApiClient.move_stepper(-100, 1, 80, self.base_url)
        result_invalid_direction = ApiClient.move_stepper(100, 2, 80, self.base_url)
        
        self.assertIn("Error", result_negative_steps)
        self.assertIn("Error", result_invalid_direction)
    
    def test_led_brightness_validation(self):
        # Test: Validierung der LED-Helligkeitsgrenzen
        result_too_low = ApiClient.set_led_brightness(-10, self.base_url)
        result_too_high = ApiClient.set_led_brightness(110, self.base_url)
        
        self.assertIn("Error", result_too_low)
        self.assertIn("Error", result_too_high)


class DeviceControlStructuralTests(unittest.TestCase):
    def setUp(self):
        root = tk.Tk()
        self.base_url_var = tk.StringVar(value="http://test-url.com")
        self.position_var = tk.DoubleVar(value=0.0)
        self.servo_angle_var = tk.IntVar(value=0)
        
        self.widgets = {
            'diameter_entry': MagicMock(),
            'servo_angle': MagicMock(),
            'stepper_length_cm': MagicMock(),
            'stepper_dir': MagicMock(),
            'stepper_speed': MagicMock(),
            'led_color': MagicMock(),
            'led_bright': MagicMock(),
            'update_position_label': MagicMock()
        }
        
        self.logger = MagicMock()
        
        self.device_control = DeviceControl(
            self.logger, 
            self.base_url_var, 
            self.widgets, 
            self.position_var, 
            self.servo_angle_var
        )
    
    def test_device_control_initialization(self):
        # Test: Korrekte Initialisierung der DeviceControl-Klasse
        self.assertEqual(self.device_control.logger, self.logger)
        self.assertEqual(self.device_control.base_url_var, self.base_url_var)
        self.assertEqual(self.device_control.widgets, self.widgets)
        self.assertEqual(self.device_control.position, self.position_var)
        self.assertEqual(self.device_control.servo_angle_var, self.servo_angle_var)
    
    @patch('Api_Fenster.ApiClient.set_servo_angle')
    def test_servo_cmd_error_handling(self, mock_set_servo):
        # Test: Fehlerbehandlung in servo_cmd
        self.widgets['servo_angle'].get.side_effect = ValueError("Ungültiger Wert")
        
        self.device_control.servo_cmd()
        
        # Prüfe ob Fehler geloggt wurde
        self.logger.log.assert_called_once()
        log_arg = self.logger.log.call_args[0][0]
        self.assertIn("Error", log_arg)
    
    @patch('Api_Fenster.ApiClient.move_stepper')
    def test_stepper_cmd_error_handling(self, mock_move_stepper):
        # Test: Fehlerbehandlung in stepper_cmd
        self.widgets['diameter_entry'].get.side_effect = ValueError("Ungültiger Wert")
        
        self.device_control.stepper_cmd()
        
        # Prüfe ob Fehler geloggt wurde
        self.logger.log.assert_called_once()
        log_arg = self.logger.log.call_args[0][0]
        self.assertIn("Error", log_arg)


class OperationQueueStructuralTests(unittest.TestCase):
    def setUp(self):
        self.queue_list = MagicMock()
        self.logger = MagicMock()
        self.operation_queue = OperationQueue(self.logger, self.queue_list)
    
    def test_operations_list_structure(self):
        # Test: Struktur der Operations-Liste
        self.assertIsInstance(self.operation_queue.operations, list)
        self.assertEqual(len(self.operation_queue.operations), 0)
    
    def test_add_operation_structure(self):
        # Test: Struktur der hinzugefügten Operation
        self.operation_queue.add('servo', {'angle': 45}, "Servo: Set angle to 45°")
        
        operation = self.operation_queue.operations[0]
        self.assertIn('type', operation)
        self.assertIn('params', operation)
        self.assertIn('description', operation)
        self.assertEqual(operation['type'], 'servo')
    
    def test_update_display_structure(self):
        # Test: Struktur der Display-Aktualisierung
        # Mock reset_mock für queue_list, um vorherige Aufrufe zu löschen
        self.queue_list.reset_mock()
        
        # Operation hinzufügen
        self.operation_queue.add('servo', {'angle': 45}, "Servo: Set angle to 45°")
        
        # Mock erneut zurücksetzen, um nur den update_display Aufruf zu testen
        self.queue_list.reset_mock()
        
        # Display aktualisieren
        self.operation_queue.update_display()
        
        # Prüfe ob Listbox korrekt aktualisiert wurde
        self.queue_list.delete.assert_called_with(0, tk.END)
        self.queue_list.insert.assert_called_once()


class LoggerStructuralTests(unittest.TestCase):
    def setUp(self):
        self.output = MagicMock()
        self.position_var = tk.DoubleVar(value=0.0)
        self.servo_angle_var = tk.IntVar(value=0)
        self.update_callback = MagicMock()
        
        self.logger = Logger(
            self.output, 
            self.position_var, 
            self.servo_angle_var, 
            self.update_callback
        )
    
    def test_log_message_color_selection(self):
        # Test: Farbauswahl basierend auf Nachrichteninhalt
        
        # Motor-Nachricht sollte blaue Farbe haben
        self.logger.log("Motor bewegt sich um 100 Steps")
        color_motor = self.output.insert.call_args[0][2][0]
        self.output.tag_config.assert_called_with(color_motor, foreground=color_motor)
        
        # Servo-Nachricht sollte grüne Farbe haben
        self.output.reset_mock()
        self.logger.log("Servo auf 45 Grad gesetzt")
        color_servo = self.output.insert.call_args[0][2][0]
        self.output.tag_config.assert_called_with(color_servo, foreground=color_servo)
    
    def test_update_from_log_position_parsing(self):
        # Test: Position wird aus Log-Nachricht extrahiert
        self.logger.log("Motor: 100 Steps, 3.50 cm, Direction up, Position: 8.75 cm")
        
        # Prüfe ob Position korrekt extrahiert wurde
        self.assertEqual(self.position_var.get(), 8.75)
    
    def test_update_from_log_servo_angle_parsing(self):
        # Test: Servo-Winkel wird aus Log-Nachricht extrahiert
        self.logger.log("Servo set to 45 degrees. Response: OK")
        
        # Prüfe ob Servo-Winkel korrekt extrahiert wurde
        self.assertEqual(self.servo_angle_var.get(), 45)


if __name__ == '__main__':
    unittest.main()  # Startet die Tests, wenn das Skript direkt ausgeführt wird