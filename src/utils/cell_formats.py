
# Base compartida para alineación y fuente
BASE_ESTILO = {
    'font_name': 'Calibri',
    'font_size': 11,
    'align': 'center',
    'valign': 'vcenter',
    'text_wrap' : True
}

# ==============================================================================
# DICCIONARIO DE COMBINACIONES DE BORDES (Negrita Gruesa vs Fino Gris)
# ==============================================================================
COMBINACIONES_BORDES_STR = {

    # --------------------------------------------------------------------------
    # 0 LADOS EN NEGRITA (Base: Todos grises finos)
    # --------------------------------------------------------------------------
    'borde_ninguno_negrita': BASE_ESTILO | {
        'top': 1, 'top_color': '#D9D9D9',
        'bottom': 1, 'bottom_color': '#D9D9D9',
        'left': 1, 'left_color': '#D9D9D9',
        'right': 1, 'right_color': '#D9D9D9'
    },

    # --------------------------------------------------------------------------
    # 1 LADO EN NEGRITA (4 combinaciones)
    # --------------------------------------------------------------------------
    'borde_negrita_top': BASE_ESTILO | {
        'top': 2, 'top_color': 'black',
        'bottom': 1, 'bottom_color': '#D9D9D9',
        'left': 1, 'left_color': '#D9D9D9',
        'right': 1, 'right_color': '#D9D9D9'
    },
    'borde_negrita_bottom': BASE_ESTILO | {
        'top': 1, 'top_color': '#D9D9D9',
        'bottom': 2, 'bottom_color': 'black',
        'left': 1, 'left_color': '#D9D9D9',
        'right': 1, 'right_color': '#D9D9D9'
    },
    'borde_negrita_left': BASE_ESTILO | {
        'top': 1, 'top_color': '#D9D9D9',
        'bottom': 1, 'bottom_color': '#D9D9D9',
        'left': 2, 'left_color': 'black',
        'right': 1, 'right_color': '#D9D9D9'
    },
    'borde_negrita_right': BASE_ESTILO | {
        'top': 1, 'top_color': '#D9D9D9',
        'bottom': 1, 'bottom_color': '#D9D9D9',
        'left': 1, 'left_color': '#D9D9D9',
        'right': 2, 'right_color': 'black'
    },

    # --------------------------------------------------------------------------
    # 2 LADOS EN NEGRITA (6 combinaciones)
    # --------------------------------------------------------------------------
    'borde_negrita_top_bottom': BASE_ESTILO | {
        'top': 2, 'top_color': 'black',
        'bottom': 2, 'bottom_color': 'black',
        'left': 1, 'left_color': '#D9D9D9',
        'right': 1, 'right_color': '#D9D9D9'
    },
    'borde_negrita_top_left': BASE_ESTILO | {
        'top': 2, 'top_color': 'black',
        'bottom': 1, 'bottom_color': '#D9D9D9',
        'left': 2, 'left_color': 'black',
        'right': 1, 'right_color': '#D9D9D9'
    },
    'borde_negrita_top_right': BASE_ESTILO | {
        'top': 2, 'top_color': 'black',
        'bottom': 1, 'bottom_color': '#D9D9D9',
        'left': 1, 'left_color': '#D9D9D9',
        'right': 2, 'right_color': 'black'
    },
    'borde_negrita_bottom_left': BASE_ESTILO | {
        'top': 1, 'top_color': '#D9D9D9',
        'bottom': 2, 'bottom_color': 'black',
        'left': 2, 'left_color': 'black',
        'right': 1, 'right_color': '#D9D9D9'
    },
    'borde_negrita_bottom_right': BASE_ESTILO | {
        'top': 1, 'top_color': '#D9D9D9',
        'bottom': 2, 'bottom_color': 'black',
        'left': 1, 'left_color': '#D9D9D9',
        'right': 2, 'right_color': 'black'
    },
    'borde_negrita_left_right': BASE_ESTILO | {
        'top': 1, 'top_color': '#D9D9D9',
        'bottom': 1, 'bottom_color': '#D9D9D9',
        'left': 2, 'left_color': 'black',
        'right': 2, 'right_color': 'black'
    },

    # --------------------------------------------------------------------------
    # 3 LADOS EN NEGRITA (4 combinaciones)
    # --------------------------------------------------------------------------
    'borde_negrita_top_bottom_left': BASE_ESTILO | {
        'top': 2, 'top_color': 'black',
        'bottom': 2, 'bottom_color': 'black',
        'left': 2, 'left_color': 'black',
        'right': 1, 'right_color': '#D9D9D9'
    },
    'borde_negrita_top_bottom_right': BASE_ESTILO | {
        'top': 2, 'top_color': 'black',
        'bottom': 2, 'bottom_color': 'black',
        'left': 1, 'left_color': '#D9D9D9',
        'right': 2, 'right_color': 'black'
    },
    'borde_negrita_top_left_right': BASE_ESTILO | {
        'top': 2, 'top_color': 'black',
        'bottom': 1, 'bottom_color': '#D9D9D9',
        'left': 2, 'left_color': 'black',
        'right': 2, 'right_color': 'black'
    },
    'borde_negrita_bottom_left_right': BASE_ESTILO | {
        'top': 1, 'top_color': '#D9D9D9',
        'bottom': 2, 'bottom_color': 'black',
        'left': 2, 'left_color': 'black',
        'right': 2, 'right_color': 'black'
    },

    # --------------------------------------------------------------------------
    # 4 LADOS EN NEGRITA (Todos en negro grueso)
    # --------------------------------------------------------------------------
    'borde_todos_negrita': BASE_ESTILO | {
        'top': 2, 'top_color': 'black',
        'bottom': 2, 'bottom_color': 'black',
        'left': 2, 'left_color': 'black',
        'right': 2, 'right_color': 'black'
    }
}

# Base compartida para enteros (agrega el formato numérico)
BASE_ESTILO_INT = BASE_ESTILO | {
    'num_format': '0'  # Cambia a '#,##0' si quieres separador de miles
}

# ==============================================================================
# DICCIONARIO DE COMBINACIONES DE BORDES PARA ENTEROS
# ==============================================================================
COMBINACIONES_BORDES_INT = {

    # --------------------------------------------------------------------------
    # 0 LADOS EN NEGRITA (Base: Todos grises finos)
    # --------------------------------------------------------------------------
    'borde_ninguno_negrita': BASE_ESTILO_INT | {
        'top': 1, 'top_color': '#D9D9D9',
        'bottom': 1, 'bottom_color': '#D9D9D9',
        'left': 1, 'left_color': '#D9D9D9',
        'right': 1, 'right_color': '#D9D9D9'
    },

    # --------------------------------------------------------------------------
    # 1 LADO EN NEGRITA (4 combinaciones)
    # --------------------------------------------------------------------------
    'borde_negrita_top': BASE_ESTILO_INT | {
        'top': 2, 'top_color': 'black',
        'bottom': 1, 'bottom_color': '#D9D9D9',
        'left': 1, 'left_color': '#D9D9D9',
        'right': 1, 'right_color': '#D9D9D9'
    },
    'borde_negrita_bottom': BASE_ESTILO_INT | {
        'top': 1, 'top_color': '#D9D9D9',
        'bottom': 2, 'bottom_color': 'black',
        'left': 1, 'left_color': '#D9D9D9',
        'right': 1, 'right_color': '#D9D9D9'
    },
    'borde_negrita_left': BASE_ESTILO_INT | {
        'top': 1, 'top_color': '#D9D9D9',
        'bottom': 1, 'bottom_color': '#D9D9D9',
        'left': 2, 'left_color': 'black',
        'right': 1, 'right_color': '#D9D9D9'
    },
    'borde_negrita_right': BASE_ESTILO_INT | {
        'top': 1, 'top_color': '#D9D9D9',
        'bottom': 1, 'bottom_color': '#D9D9D9',
        'left': 1, 'left_color': '#D9D9D9',
        'right': 2, 'right_color': 'black'
    },

    # --------------------------------------------------------------------------
    # 2 LADOS EN NEGRITA (6 combinaciones)
    # --------------------------------------------------------------------------
    'borde_negrita_top_bottom': BASE_ESTILO_INT | {
        'top': 2, 'top_color': 'black',
        'bottom': 2, 'bottom_color': 'black',
        'left': 1, 'left_color': '#D9D9D9',
        'right': 1, 'right_color': '#D9D9D9'
    },
    'borde_negrita_top_left': BASE_ESTILO_INT | {
        'top': 2, 'top_color': 'black',
        'bottom': 1, 'bottom_color': '#D9D9D9',
        'left': 2, 'left_color': 'black',
        'right': 1, 'right_color': '#D9D9D9'
    },
    'borde_negrita_top_right': BASE_ESTILO_INT | {
        'top': 2, 'top_color': 'black',
        'bottom': 1, 'bottom_color': '#D9D9D9',
        'left': 1, 'left_color': '#D9D9D9',
        'right': 2, 'right_color': 'black'
    },
    'borde_negrita_bottom_left': BASE_ESTILO_INT | {
        'top': 1, 'top_color': '#D9D9D9',
        'bottom': 2, 'bottom_color': 'black',
        'left': 2, 'left_color': 'black',
        'right': 1, 'right_color': '#D9D9D9'
    },
    'borde_negrita_bottom_right': BASE_ESTILO_INT | {
        'top': 1, 'top_color': '#D9D9D9',
        'bottom': 2, 'bottom_color': 'black',
        'left': 1, 'left_color': '#D9D9D9',
        'right': 2, 'right_color': 'black'
    },
    'borde_negrita_left_right': BASE_ESTILO_INT | {
        'top': 1, 'top_color': '#D9D9D9',
        'bottom': 1, 'bottom_color': '#D9D9D9',
        'left': 2, 'left_color': 'black',
        'right': 2, 'right_color': 'black'
    },

    # --------------------------------------------------------------------------
    # 3 LADOS EN NEGRITA (4 combinaciones)
    # --------------------------------------------------------------------------
    'borde_negrita_top_bottom_left': BASE_ESTILO_INT | {
        'top': 2, 'top_color': 'black',
        'bottom': 2, 'bottom_color': 'black',
        'left': 2, 'left_color': 'black',
        'right': 1, 'right_color': '#D9D9D9'
    },
    'borde_negrita_top_bottom_right': BASE_ESTILO_INT | {
        'top': 2, 'top_color': 'black',
        'bottom': 2, 'bottom_color': 'black',
        'left': 1, 'left_color': '#D9D9D9',
        'right': 2, 'right_color': 'black'
    },
    'borde_negrita_top_left_right': BASE_ESTILO_INT | {
        'top': 2, 'top_color': 'black',
        'bottom': 1, 'bottom_color': '#D9D9D9',
        'left': 2, 'left_color': 'black',
        'right': 2, 'right_color': 'black'
    },
    'borde_negrita_bottom_left_right': BASE_ESTILO_INT | {
        'top': 1, 'top_color': '#D9D9D9',
        'bottom': 2, 'bottom_color': 'black',
        'left': 2, 'left_color': 'black',
        'right': 2, 'right_color': 'black'
    },

    # --------------------------------------------------------------------------
    # 4 LADOS EN NEGRITA (Todos en negro grueso)
    # --------------------------------------------------------------------------
    'borde_todos_negrita': BASE_ESTILO_INT | {
        'top': 2, 'top_color': 'black',
        'bottom': 2, 'bottom_color': 'black',
        'left': 2, 'left_color': 'black',
        'right': 2, 'right_color': 'black'
    }
}