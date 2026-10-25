from datetime import datetime
from pathlib import Path

import pandas as pd


class DatasetSummarizer:
    """Genera un resumen en texto de un DataFrame y lo guarda en un archivo .txt."""

    def __init__(self, df: pd.DataFrame, nombre: str = "Dataset"):
        if not isinstance(df, pd.DataFrame):
            raise TypeError("DatasetSummarizer espera un DataFrame de pandas.")
        self.df = df
        self.nombre = nombre

    def build_summary(self) -> str:
        df = self.df
        filas, columnas = df.shape
        nulos = df.isnull().sum()

        lineas = [
            f"RESUMEN DEL DATASET: {self.nombre}",
            f"Generado: {datetime.now():%Y-%m-%d %H:%M}",
            "=" * 60,
            "",
            "1. DIMENSIONES",
            f"Filas: {filas}",
            f"Columnas: {columnas}",
            "",
            "2. COLUMNAS Y TIPOS DE DATOS",
            df.dtypes.to_string(),
            "",
            "3. VALORES NULOS POR COLUMNA",
            nulos.to_string(),
            f"Total de valores nulos: {int(nulos.sum())}",
            "",
            "4. ESTADÍSTICAS DESCRIPTIVAS (columnas numéricas)",
            self._estadisticas_numericas(),
            "",
            "5. COLUMNAS CATEGÓRICAS (valores más frecuentes)",
            self._resumen_categoricas(),
        ]
        return "\n".join(lineas)

    def _estadisticas_numericas(self) -> str:
        numericas = self.df.select_dtypes(include="number")
        if numericas.empty:
            return "No hay columnas numéricas."
        return numericas.describe().round(2).to_string()

    def _resumen_categoricas(self) -> str:
        categoricas = self.df.select_dtypes(include=["object", "category", "string"])
        if categoricas.empty:
            return "No hay columnas categóricas."
        bloques = []
        for col in categoricas.columns:
            conteo = categoricas[col].value_counts().head(5)
            bloques.append(f"[{col}] - {categoricas[col].nunique()} valores únicos")
            bloques.append(conteo.to_string())
            bloques.append("")
        return "\n".join(bloques).rstrip()

    def save(self, path: str) -> str:
        ruta = Path(path)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(self.build_summary(), encoding="utf-8")
        return str(ruta)