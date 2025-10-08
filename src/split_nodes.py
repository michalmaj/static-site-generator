# src/split_nodes.py

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Dzieli węzły typu TEXT po podanym delimiterze i wstawia węzły o wskazanym text_type
    dla fragmentów "wewnątrz" delimiterów.

    Przykład:
        Input:  [TextNode("A **bold** B", TEXT)]
        Call:   split_nodes_delimiter([...], "**", TextType.BOLD)
        Output: [TextNode("A ", TEXT), TextNode("bold", BOLD), TextNode(" B", TEXT)]

    Zasady:
      - Tylko węzły TEXT są dzielone; inne przechodzą bez zmian.
      - Liczba delimiterów musi być parzysta (len(parts) nieparzyste). W przeciwnym razie ValueError.
      - Puste segmenty tekstowe są pomijane (nie tworzymy pustych TextNode(TEXT, "")).

    Parametry:
      old_nodes : list[TextNode]
      delimiter : str (np. "`", "**", "_")
      text_type : TextType (np. TextType.CODE, TextType.BOLD, TextType.ITALIC)

    Zwraca:
      list[TextNode]
    """
    if not isinstance(old_nodes, list):
        raise TypeError("old_nodes must be a list of TextNode")

    new_nodes = []
    for node in old_nodes:
        # Przechodzimy bez zmian wszystko, co nie jest czystym tekstem
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Dzielimy po delimiterze dosłownym (bez regexów)
        parts = node.text.split(delimiter)

        # Jeżeli delimiter nie występuje — nic nie zmieniamy
        if len(parts) == 1:
            new_nodes.append(node)
            continue

        # Liczba delimiterów musi być parzysta => liczba parts nieparzysta
        # Np.: "A **b** C" -> split("**") => ["A ", "b", " C"] (3 części)
        if len(parts) % 2 == 0:
            raise ValueError(f"Unmatched delimiter '{delimiter}' in text: {node.text!r}")

        # parts: [TEXT, IN, TEXT, IN, TEXT, ...] (naprzemiennie)
        # i = 0 -> TEXT, i = 1 -> IN (typ text_type), i = 2 -> TEXT, itd.
        for i, chunk in enumerate(parts):
            if chunk == "":
                # pomijamy puste segmenty — nie tworzymy pustych TextNode(TEXT, "")
                # (np. gdy tekst zaczyna/kończy się delimiterem)
                continue

            if i % 2 == 0:
                # Parzyste indeksy -> zwykły tekst
                new_nodes.append(TextNode(chunk, TextType.TEXT))
            else:
                # Nieparzyste -> fragment wewnątrz delimiterów
                new_nodes.append(TextNode(chunk, text_type))

    return new_nodes
