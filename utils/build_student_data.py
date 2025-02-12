from datetime import datetime
from gui.handlers import build_section_code  # Asegúrate de que build_section_code esté implementado

def build_student_data(values):
    """Construye y devuelve un diccionario con los datos del estudiante."""
    student_data = {
        'nombre': values['-NOMBRE-'],
        'ci': values['-CI-'],
        'materia': values['-SUBJECT-'],
        'seccion': build_section_code(values),
        'universidad': "Universidad Alejandro de Humboldt",
        'carrera': "Ing. En Informática",
        'eval_num': values['-EVAL_NUM-'],
        'corte': values['-CORTE-'],
        'fecha': datetime.now().strftime("%d/%m/%Y"),
        'tema': values['-TOPIC-']
    }
    return student_data