
# ==============================================================================
# 1. BORDES PUROS DECLARADOS (Sin fuentes, alineaciones ni tipos de datos)
# ==============================================================================
BORDES_PUROS = {
    # 0 Lados Gruesos
    'borde_ninguno_negrita': {
        'top': 1, 'top_color': '#D9D9D9',
        'bottom': 1, 'bottom_color': '#D9D9D9',
        'left': 1, 'left_color': '#D9D9D9',
        'right': 1, 'right_color': '#D9D9D9'
    },

    # 1 Lado Grueso
    'borde_negrita_top': {
        'top': 2, 'top_color': 'black',
        'bottom': 1, 'bottom_color': '#D9D9D9',
        'left': 1, 'left_color': '#D9D9D9',
        'right': 1, 'right_color': '#D9D9D9'
    },
    'borde_negrita_bottom': {
        'top': 1, 'top_color': '#D9D9D9',
        'bottom': 2, 'bottom_color': 'black',
        'left': 1, 'left_color': '#D9D9D9',
        'right': 1, 'right_color': '#D9D9D9'
    },
    'borde_negrita_left': {
        'top': 1, 'top_color': '#D9D9D9',
        'bottom': 1, 'bottom_color': '#D9D9D9',
        'left': 2, 'left_color': 'black',
        'right': 1, 'right_color': '#D9D9D9'
    },
    'borde_negrita_right': {
        'top': 1, 'top_color': '#D9D9D9',
        'bottom': 1, 'bottom_color': '#D9D9D9',
        'left': 1, 'left_color': '#D9D9D9',
        'right': 2, 'right_color': 'black'
    },

    # 2 Lados Gruesos
    'borde_negrita_top_bottom': {
        'top': 2, 'top_color': 'black',
        'bottom': 2, 'bottom_color': 'black',
        'left': 1, 'left_color': '#D9D9D9',
        'right': 1, 'right_color': '#D9D9D9'
    },
    'borde_negrita_top_left': {
        'top': 2, 'top_color': 'black',
        'bottom': 1, 'bottom_color': '#D9D9D9',
        'left': 2, 'left_color': 'black',
        'right': 1, 'right_color': '#D9D9D9'
    },
    'borde_negrita_top_right': {
        'top': 2, 'top_color': 'black',
        'bottom': 1, 'bottom_color': '#D9D9D9',
        'left': 1, 'left_color': '#D9D9D9',
        'right': 2, 'right_color': 'black'
    },
    'borde_negrita_bottom_left': {
        'top': 1, 'top_color': '#D9D9D9',
        'bottom': 2, 'bottom_color': 'black',
        'left': 2, 'left_color': 'black',
        'right': 1, 'right_color': '#D9D9D9'
    },
    'borde_negrita_bottom_right': {
        'top': 1, 'top_color': '#D9D9D9',
        'bottom': 2, 'bottom_color': 'black',
        'left': 1, 'left_color': '#D9D9D9',
        'right': 2, 'right_color': 'black'
    },
    'borde_negrita_left_right': {
        'top': 1, 'top_color': '#D9D9D9',
        'bottom': 1, 'bottom_color': '#D9D9D9',
        'left': 2, 'left_color': 'black',
        'right': 2, 'right_color': 'black'
    },

    # 3 Lados Gruesos
    'borde_negrita_top_bottom_left': {
        'top': 2, 'top_color': 'black',
        'bottom': 2, 'bottom_color': 'black',
        'left': 2, 'left_color': 'black',
        'right': 1, 'right_color': '#D9D9D9'
    },
    'borde_negrita_top_bottom_right': {
        'top': 2, 'top_color': 'black',
        'bottom': 2, 'bottom_color': 'black',
        'left': 1, 'left_color': '#D9D9D9',
        'right': 2, 'right_color': 'black'
    },
    'borde_negrita_top_left_right': {
        'top': 2, 'top_color': 'black',
        'bottom': 1, 'bottom_color': '#D9D9D9',
        'left': 2, 'left_color': 'black',
        'right': 2, 'right_color': 'black'
    },
    'borde_negrita_bottom_left_right': {
        'top': 1, 'top_color': '#D9D9D9',
        'bottom': 2, 'bottom_color': 'black',
        'left': 2, 'left_color': 'black',
        'right': 2, 'right_color': 'black'
    },

    # 4 Lados Gruesos
    'borde_todos_negrita': {
        'top': 2, 'top_color': 'black',
        'bottom': 2, 'bottom_color': 'black',
        'left': 2, 'left_color': 'black',
        'right': 2, 'right_color': 'black'
    }
}


# ==============================================================================
# 2. DEFINIR BASES POR TIPO DE DATO
# ==============================================================================
BASE_COMUN = {
    'font_name': 'Calibri',
    'font_size': 11,
    'align': 'center',
    'valign': 'vcenter',
    'text_wrap': True
}

BASE_STR = BASE_COMUN
BASE_INT = BASE_COMUN | {'num_format': '0'}
BASE_FLOAT_2d = BASE_COMUN | {'num_format': '0.00'}
BASE_FLOAT_3d = BASE_COMUN | {'num_format': '0.000'}
BASE_DATETIME = BASE_COMUN | {'num_format': 'dd-mm-yyyy hh:mm'}


# ==============================================================================
# 3. CREAR DICCIONARIOS FINALES FUSIONANDO (BASE + BORDE PURO)
# ==============================================================================
COMBINACIONES_BORDES_STR = {k: BASE_STR | v for k, v in BORDES_PUROS.items()}
COMBINACIONES_BORDES_INT = {k: BASE_INT | v for k, v in BORDES_PUROS.items()}
COMBINACIONES_BORDES_FLOAT_2D = {k: BASE_FLOAT_2d | v for k, v in BORDES_PUROS.items()}
COMBINACIONES_BORDES_FLOAT_3D = {k: BASE_FLOAT_3d | v for k, v in BORDES_PUROS.items()}
COMBINACIONES_BORDES_DATE = {k: BASE_DATETIME | v for k, v in BORDES_PUROS.items()}