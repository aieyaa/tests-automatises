class Calculator:
    """
    Une classe simple de calculatrice fournissant les opérations arithmétiques de base.
    """

    def add(self, a, b):
        """
        Additionne deux nombres.

        Args:
            a: Premier nombre
            b: Deuxième nombre

        Returns:
            La somme de a et b
        """
        return a + b

    def subtract(self, a, b):
        """
        Soustrait b de a.

        Args:
            a: Premier nombre
            b: Deuxième nombre

        Returns:
            La différence entre a et b
        """
        return a - b

    def multiply(self, a, b):
        """
        Multiplie deux nombres.

        Args:
            a: Premier nombre
            b: Deuxième nombre

        Returns:
            Le produit de a et b
        """
        return a * b

    def divide(self, a, b):
        """
        Divise a par b.

        Args:
            a: Numérateur
            b: Dénominateur

        Returns:
            Le quotient de a divisé par b

        Raises:
            ZeroDivisionError: Si b est égal à zéro
        """
        if b == 0:
            raise ZeroDivisionError("Division par zéro impossible")
        return a / b

    def power(self, a, b):
        """Calcule a^b. Retourner 1 pour 0^0."""
        return a ** b 

    def sqrt(self, a):
        """Racine carrée. Lever ValueError si a < 0."""
        if a < 0:
            raise ValueError("La racine carrée d'un nombre négatif est indéfinie")
        return a ** 0.5

    def modulo(self, a, b):
        """Reste de division. Lever ZeroDivisionError si b = 0."""
