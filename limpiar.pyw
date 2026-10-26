import pandas as pd

def _monto(d): return float((d.Quantity * d.UnitPrice).sum())

def limpiar(df, devolver_bitacora=False):
    """Devuelve df limpio (conserva índice original). NO elimina filas sin CustomerID
    (se necesitan para la serie de ventas; la Parte 6 las quita aparte)."""
    d = df.copy(); bit = []
    def regla(nombre, mask):
        nonlocal d
        bit.append({'regla': nombre, 'filas': int(mask.sum()), 'monto_£': _monto(d[mask])})
        d = d[~mask]
    regla('1. duplicados exactos', d.duplicated(keep='first'))
    regla('2. factura con prefijo distinto de dígito/C (ej. A = ajuste deuda)',
          ~d.InvoiceNo.str.match(r'^[0-9C]'))
    regla('3. StockCode no producto (salvo créditos M con factura C)',
          ~d.StockCode.str.match(r'^(\d{5}|DCGS)')
          & ~((d.StockCode == 'M') & d.InvoiceNo.str.startswith('C')))
    regla('4. UnitPrice <= 0', d.UnitPrice <= 0)
    regla('5. Quantity < 0 en factura que no es cancelación',
          (d.Quantity < 0) & ~d.InvoiceNo.str.startswith('C'))
    return (d, pd.DataFrame(bit)) if devolver_bitacora else d
