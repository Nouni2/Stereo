# --------------------------------------------------------------
# Algorithme de Simplification de Courbe - Douglas-Peucker
# --------------------------------------------------------------
# L'algorithme de Douglas-Peucker est une méthode de simplification des courbes. Il fonctionne en identifiant les
# points importants d'une courbe pour réduire le nombre total de points tout en préservant l'apparence générale de la courbe.

# La méthode utilise un seuil de simplification appelé epsilon. Plus epsilon est petit, plus la simplification est importante.
# L'algorithme procède comme suit :

# 1. Si la liste de points contient deux points ou moins, elle est renvoyée telle quelle car elle ne peut pas être simplifiée davantage.
# 2. La fonction `perpendicular_distance` est utilisée pour calculer la distance perpendiculaire d'un point à une ligne définie
#    par les deux extrémités de la liste de points.
# 3. Le point avec la plus grande distance perpendiculaire est identifié.
# 4. Si cette distance est supérieure à epsilon, la liste est divisée en deux segments au point identifié, et le processus est
#    répété de manière récursive sur les deux segments.
# 5. Si la distance maximale est inférieure ou égale à epsilon, la liste originale est simplifiée en conservant seulement le premier
#    et le dernier point.

def douglas_peucker(point_list, epsilon):
    """
    Simplifie une liste de points en utilisant l'algorithme de Douglas-Peucker.

    Parameters:
    - point_list (list): Liste de points (chaque point étant un tuple (x, y)).
    - epsilon (float): Seuil de simplification.

    Returns:
    - list: Liste de points simplifiée.
    """
    if len(point_list) <= 2:
        return point_list

    # Fonction de calcul de la distance perpendiculaire d'un point à une ligne
    def perpendicular_distance(point, line_start, line_end):
        x, y = point
        x1, y1 = line_start
        x2, y2 = line_end

        num = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1)
        den = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
        if den == 0:
            den = 1

        return num / den

    max_distance = 0
    index = 0

    # Trouver le point avec la plus grande distance
    for i in range(1, len(point_list) - 1):
        distance = perpendicular_distance(point_list[i], point_list[0], point_list[-1])
        if distance > max_distance:
            index = i
            max_distance = distance

    # Vérifier si la distance maximale est supérieure à epsilon
    if max_distance > epsilon:
        # Récursivement simplifier les deux segments résultants
        segment1 = douglas_peucker(point_list[:index + 1], epsilon)
        segment2 = douglas_peucker(point_list[index:], epsilon)
        return segment1[:-1] + segment2  # Éviter la duplication du point à l'index

    else:
        return [point_list[0], point_list[-1]]
