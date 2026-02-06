from textblob import TextBlob

def analizar_sentimiento(texto):
    """
    Devuelve un valor entre -1 (muy negativo) y 1 (muy positivo).
    0 es neutral.
    """
    if not texto:
        return 0.0
    
    analysis = TextBlob(texto)
    # La polaridad mide el sentimiento
    return round(analysis.sentiment.polarity, 2)

def categorizar_tono(polaridad):
    if polaridad < -0.1:
        return "Hostil/Negativo"
    elif polaridad > 0.1:
        return "Positivo/Constructivo"
    else:
        return "Neutral/Informativo"
