from collections.abc import Callable
from typing import Any


class AnalyzerRunner:
    """
    Generieke runner voor registry-gebaseerde analyzers.

    De runner kent geen domeinlogica.

    Verantwoordelijkheden:

    - analyzers in deterministische volgorde uitvoeren
    - registry afhandelen
    - hetzelfde resultaatobject doorgeven
    - uiteindelijke resultaat retourneren

    Hierdoor kunnen meerdere engines dezelfde infrastructuur gebruiken,
    terwijl iedere engine verantwoordelijk blijft voor zijn eigen logica.
    """

    def run(
        self,
        registry: Any,
        result: Any,
        analyzer_executor: Callable[[Any, Any], Any],
    ) -> Any:
        """
        Voert alle geregistreerde analyzers uit.

        Parameters
        ----------
        registry:
            Registry met analyzers.

        result:
            Resultaatobject dat door alle analyzers wordt gedeeld.

        analyzer_executor:
            Callback die bepaalt hoe een analyzer wordt uitgevoerd.

        Returns
        -------
        Het bijgewerkte resultaatobject.
        """

        for analyzer_definition in registry.get_analyzers():
            result = analyzer_executor(
                analyzer_definition,
                result,
            )

        return result