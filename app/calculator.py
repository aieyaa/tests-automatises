import re 

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

def calculate(self, expression: str) -> float:
            # 1. Nettoyage et validation de base
            expression = expression.replace(" ", "")
            if not re.match(r'^[0-9+\-*/.]+$', expression):
                raise ValueError("Syntaxe invalide : caractères interdits")

            tokens = re.findall(r'\d*\.?\d+|[+\-*/]', expression)
            
            i = 0
            while i < len(tokens):
                if tokens[i] in ('*', '/'):
                    try:
                        a = float(tokens[i-1])
                        op = tokens[i]
                        b = float(tokens[i+1])
                    except (IndexError, ValueError):
                        # Si on ne peut pas récupérer a ou b, l'expression est mal formée
                        raise ValueError("Expression mal formée")
                    
                    if op == '/' and b == 0:
                        raise ValueError("Division par zéro impossible")
                    
                    res = a * b if op == '*' else a / b
                    tokens[i-1:i+2] = [res]
                    i -= 1 
                i += 1

            try:
                if not tokens: raise ValueError()
                
                result = float(tokens[0])
                for i in range(1, len(tokens), 2):
                    op = tokens[i]
                    val = float(tokens[i+1])
                    if op == '+':
                        result += val
                    elif op == '-':
                        result -= val
                return result
            except (IndexError, ValueError):
                raise ValueError("Expression mal formée")