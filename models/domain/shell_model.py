from pydantic import BaseModel, Field
from typing import List, Optional

class VentaModel(BaseModel):
    id: str = Field(..., description="Identificador único del desarrollador UUID",) # uuid
    precio_total: float = Field(..., description="Precio total de la venta en Euros")
    fecha_venta: str = Field(..., description="Fecha de la venta en formato YYYY-MM-DD")
    codigo_descuento: Optional[str] = Field(None, description="Código de descuento aplicado a la venta, si existe")
