import re

def obtener_categoria(titulo):
    #Clasificar el producto basado en palabras clave del título.
    titulo = str(titulo).lower()
    
    keywords = {
        'Suplementos': ['aceite', 'omega', 'probioticos', 'probiótico', 'polvo', 'gastro', 'aid', 'suplemento', 'vitaminas', 'calcio', 'condroitina', 'dogelthy', 'regenerador', 'articulaciones', 'salmon', 'salmón', 'antioxidante'],
        'Alimento': ['alimento', 'croqueta', 'comida', 'bulto', 'nutricion', 'diet', 'nupec', 'royal canin', 'pedigree', 'dog chow', 'pro plan', 'ganador', 'minino', 'whiskas', 'eukanuba', 'hills', 'virbac', 'diamond', 'kirkland', 'blue buffalo', 'taste of the wild', 'fulltrust', 'exceed', 'beneful', 'dow chow', 'purina', 'mainstay', 'champion', 'premios', 'galletas', 'carnaza', 'sobre', 'pouch', 'latas', 'húmedo'],
        'Accesorios': ['correa', 'collar', 'arnes', 'pechera', 'placa', 'identificacion', 'cama', 'colchon', 'tapete', 'casita', 'casa', 'jaula', 'transportadora', 'kennel', 'ropa', 'sueter', 'disfraz', 'abrigo', 'impermeable', 'zapato', 'bota', 'juguete', 'pelota', 'kong', 'mordedera', 'peluche', 'frisbee', 'bebedero', 'comedero', 'plato', 'dispensador', 'tazon', 'acero', 'puerta', 'reja', 'escalera'],
        'Salud/Higiene': ['pulga', 'garrapata', 'antipulgas', 'desparasitante', 'shampoo', 'jabon', 'acondicionador', 'perfume', 'toallitas', 'locion', 'bravecto', 'nexgard', 'simparica', 'seresto', 'frontline', 'advocate', 'credelio', 'pañal', 'entrenador', 'pipeta', 'cepillo', 'carda', 'cortaunas', 'limpiador', 'arena', 'sanitario', 'solutions']
    }
    
    for categoria, palabras in keywords.items():
        if any(palabra in titulo for palabra in palabras):
            return categoria
            
    if 'gato' in titulo:
        return 'Multimascota/Gatos'
        
    return 'Otros'


